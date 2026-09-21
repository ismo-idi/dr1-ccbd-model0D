#include "Routes.hh"
#include <gz/sim/System.hh>
#include <gz/sim/EntityComponentManager.hh>
#include <gz/sim/components/Model.hh>
#include <gz/sim/components/Name.hh>
#include <gz/sim/components/Pose.hh>
#include <gz/plugin/Register.hh>
#include <gz/transport/Node.hh>
#include <gz/msgs/stringmsg.pb.h>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <memory>
#include <sstream>

namespace campus {
class Kinematics: public gz::sim::System, public gz::sim::ISystemConfigure,
    public gz::sim::ISystemPreUpdate, public gz::sim::ISystemPostUpdate {
  std::unique_ptr<Motion> motion;
  std::array<gz::sim::Entity,2> entities{};
  gz::transport::Node node;
  gz::transport::Node::Publisher publisher;
  std::ofstream csv;
  uint64_t tick=0;
  bool bound=false;
 public:
  void Configure(const gz::sim::Entity&,const std::shared_ptr<const sdf::Element>& sdf,
      gz::sim::EntityComponentManager&,gz::sim::EventManager&) override {
    motion=std::make_unique<Motion>(sdf->Get<int>("wave"),
        std::array<std::vector<Vec>,2>{{parseRoute(sdf->Get<std::string>("route_1")),
          parseRoute(sdf->Get<std::string>("route_2"))}});
    publisher=node.Advertise<gz::msgs::StringMsg>("/campus/demo/state");
    const char* path=std::getenv("CAMPUS_TRACE");
    if(path) {csv.open(path); if(!csv) throw std::runtime_error("Cannot open CAMPUS_TRACE");
      csv<<"tick,sim_time,paused,x1,y1,z1,x2,y2,z2,phase1,phase2,status\n"<<std::setprecision(17);}
  }
  void PreUpdate(const gz::sim::UpdateInfo& info,gz::sim::EntityComponentManager& ecm) override {
    if(!bound) {
      for(int i=0;i<2;++i)entities[i]=ecm.EntityByComponents(
          gz::sim::components::Model(),gz::sim::components::Name("uav_"+std::to_string(i+1)));
      bound=entities[0] && entities[1];
    }
    if(!bound || info.paused) return;
    double dt=std::chrono::duration<double>(info.dt).count();
    if(dt<=0) return;
    if(std::abs(dt-.02)>1e-8) {motion->failed=true;motion->reason="step must equal 0.02s";return;}
    // Reject external pose changes instead of silently overwriting them.
    for(int i=0;i<2;++i) {
      auto pose=ecm.Component<gz::sim::components::Pose>(entities[i])->Data();
      Vec actual{pose.Pos().X(),pose.Pos().Y(),pose.Pos().Z()};
      if((actual-motion->p[i]).norm()>1e-8) {
        motion->failed=true;motion->reason="unexpected pose modification";return;
      }
    }
    motion->advance(dt);++tick;
    for(int i=0;i<2;++i) {
      Vec p=motion->p[i];
      ecm.SetComponentData<gz::sim::components::Pose>(entities[i],
          gz::math::Pose3d(p.x,p.y,p.z,0,0,i==0?.3:-.3));
      ecm.SetChanged(entities[i],gz::sim::components::Pose::typeId,
          gz::sim::ComponentState::PeriodicChange);
    }
  }
  void PostUpdate(const gz::sim::UpdateInfo& info,const gz::sim::EntityComponentManager& ecm) override {
    if(!bound) return;
    const double time=std::chrono::duration<double>(info.simTime).count();
    const std::string status=motion->failed?"FAILED":motion->done()?"COMPLETE":"RUNNING";
    std::ostringstream s;s<<std::setprecision(17);
    s<<"{\"tick\":"<<tick<<",\"sim_time\":"<<time<<",\"paused\":"<<(info.paused?"true":"false")
     <<",\"wave\":"<<motion->wave<<",\"status\":\""<<status<<"\",\"poses\":[";
    if(csv)csv<<tick<<","<<time<<","<<info.paused;
    for(int i=0;i<2;++i) {
      auto p=ecm.Component<gz::sim::components::Pose>(entities[i])->Data().Pos();
      if(i)s<<",";s<<"["<<p.X()<<","<<p.Y()<<","<<p.Z()<<"]";
      if(csv)csv<<","<<p.X()<<","<<p.Y()<<","<<p.Z();
    }
    s<<"],\"distances\":["<<(motion->p[0]-motion->p[1]).norm()<<","<<
      (motion->p[0]+bodyOffset-ball).norm()<<","<<(motion->p[1]+bodyOffset-ball).norm();
    s<<"],\"phases\":[\""<<motion->phase(0)<<"\",\""<<motion->phase(1)
     <<"\"],\"yield_ticks\":"<<motion->yieldTicks<<",\"rejected_ticks\":"<<motion->rejectedTicks
     <<",\"reason\":\""<<motion->reason<<"\"}";
    if(csv) {csv<<","<<motion->phase(0)<<","<<motion->phase(1)<<","<<status<<"\n";
      if(motion->done() || motion->failed)csv.flush();}
    // Publisher is telemetry only. The simulator's update thread owns both UAV poses.
    if(tick%5==0 || info.paused || motion->done() || motion->failed) {
      gz::msgs::StringMsg msg;msg.set_data(s.str());publisher.Publish(msg);
    }
  }
};
}
GZ_ADD_PLUGIN(campus::Kinematics,gz::sim::System,campus::Kinematics::ISystemConfigure,
    campus::Kinematics::ISystemPreUpdate,campus::Kinematics::ISystemPostUpdate)
