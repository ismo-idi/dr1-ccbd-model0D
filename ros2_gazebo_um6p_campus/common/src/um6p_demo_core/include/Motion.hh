#pragma once
// First-party deterministic kinematics. No optimizer or rigid-body dynamics.
#include <algorithm>
#include <array>
#include <cmath>
#include <stdexcept>
#include <string>
#include <vector>

namespace campus {
struct Vec {
  double x{}, y{}, z{};
  Vec operator+(Vec b) const {return {x+b.x,y+b.y,z+b.z};}
  Vec operator-(Vec b) const {return {x-b.x,y-b.y,z-b.z};}
  Vec operator*(double s) const {return {x*s,y*s,z*s};}
  double dot(Vec b) const {return x*b.x+y*b.y+z*b.z;}
  double norm() const {return std::sqrt(dot(*this));}
};
inline double segmentDistance(Vec a, Vec b) {
  const Vec d=b-a;
  const double t=d.dot(d)>0 ? std::clamp(-a.dot(d)/d.dot(d),0.0,1.0):0;
  return (a+d*t).norm();
}
inline Vec toward(Vec p, Vec target, double step) {
  Vec d=target-p; double n=d.norm();
  return n<=step ? target : p+d*(step/n);
}
constexpr double radius=1.2, pairGap=.8, obstacleGap=.6;
constexpr double pairRequired=2*radius+pairGap;
constexpr double ballRadius=2.4, ballRequired=ballRadius+radius+obstacleGap;
const Vec bodyOffset{0,0,.36}, ball{0,-22,2.4};
const std::array<Vec,2> starts{{{-3.6,-8.2,.12},{3.6,-8.2,.12}}};

struct Motion {
  int wave;
  std::array<Vec,2> p=starts;
  std::array<std::vector<Vec>,2> route;
  std::array<size_t,2> next{{0,0}};
  double elapsed=0, minPair=1e9, minBall=1e9;
  size_t yieldTicks=0, rejectedTicks=0;
  bool failed=false, yielding=false;
  std::string reason;
  explicit Motion(int w, std::array<std::vector<Vec>,2> routes):wave(w),route(std::move(routes)) {
    if (w!=1 && w!=2) throw std::invalid_argument("wave must be 1 or 2");
    for(const auto& points:route) {
      if(points.empty()) throw std::invalid_argument("empty route");
      for(auto v:points) if(!std::isfinite(v.norm())) throw std::invalid_argument("invalid waypoint");
    }
  }
  bool done() const {return next[0]==route[0].size() && next[1]==route[1].size();}
  std::string phase(int i) const {
    if(failed) return "FAILED";
    if(done() || next[i]==route[i].size()) return "LANDED";
    if(elapsed<3) return "READY";
    if(next[i]==0) return "TAKEOFF";
    if(i==1 && yielding && next[i]>0) return "YIELD";
    if(next[i]+1==route[i].size()) return "LANDING";
    return wave==2 ? "BYPASS" : "TRAVEL";
  }
  bool admissible(const std::array<Vec,2>& q) const {
    if(segmentDistance(p[0]-p[1],q[0]-q[1])<pairRequired+1e-6) return false;
    for(int i=0;i<2;++i) {
      // Convex reserved corridor; endpoints imply the full segment stays inside.
      // Ground contact is checked by mesh z bounds, not the inflated sphere.
      for(Vec v:{p[i],q[i]})
        if(!std::isfinite(v.norm()) || v.x < -7 || v.x > 7 ||
            v.y < -41 || v.y > -7 || v.z < .12-1e-9 || v.z > 2.8+1e-9) return false;
      if(wave==2 && segmentDistance(p[i]+bodyOffset-ball,q[i]+bodyOffset-ball)<ballRequired+1e-6) return false;
    }
    return true;
  }
  bool remainingLegsClear() const {
    // Predict constant-speed travel to each current waypoint, then hold there.
    // Arrival times split the prediction into synchronized linear intervals.
    std::array<Vec,2> goal=p;
    std::array<double,3> times{{0,0,0}};
    for(int i=0;i<2;++i) if(next[i]<route[i].size()) {
      goal[i]=route[i][next[i]];
      times[i+1]=(goal[i]-p[i]).norm()/.85;
    }
    std::sort(times.begin(),times.end());
    auto relative=[&](double t){
      return toward(p[0],goal[0],.85*t)-toward(p[1],goal[1],.85*t);};
    for(int k=1;k<3;++k)
      if(segmentDistance(relative(times[k-1]),relative(times[k]))<pairRequired+.32)
        return false;
    return true;
  }
  void advance(double dt) {
    if(!(dt>0 && dt<=.0200001)) throw std::invalid_argument("invalid time step");
    if(failed || done()) return;
    elapsed+=dt;
    if(elapsed<3) return;
    auto q=p;
    std::array<Vec,2> forecast=p;
    for(int i=0;i<2;++i) if(next[i]<route[i].size())
      forecast[i]=toward(p[i],route[i][next[i]],.85*1.0);
    if(yielding) yielding=!remainingLegsClear();
    else yielding=next[1]>0 && next[1]<route[1].size() &&
      segmentDistance(p[0]-p[1],forecast[0]-forecast[1])<pairRequired+.3;

    for(int i=0;i<2;++i) {
      if(next[i]==route[i].size()) continue;
      if(phase(i)=="YIELD") {++yieldTicks; continue;}
      q[i]=toward(p[i],route[i][next[i]],.85*dt);
    }
    if(!admissible(q)) {q=p; ++rejectedTicks;}
    minPair=std::min(minPair,segmentDistance(p[0]-p[1],q[0]-q[1]));
    if(wave==2) for(int i=0;i<2;++i)
      minBall=std::min(minBall,segmentDistance(p[i]+bodyOffset-ball,q[i]+bodyOffset-ball));
    p=q;
    for(int i=0;i<2;++i)
      if(next[i]<route[i].size() && (p[i]-route[i][next[i]]).norm()<1e-9) ++next[i];
    if(elapsed>120 && !done()) {failed=true;reason="mission timeout / blocked path";}
  }
};
}
