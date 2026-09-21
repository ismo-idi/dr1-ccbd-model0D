#include "Routes.hh"
#include <fstream>
#include <iostream>
#include <iomanip>
int main(int argc,char**argv) {
  using namespace campus;
  auto require=[](bool b){if(!b) throw std::runtime_error("core check failed");};
  require(segmentDistance({-2,0,0},{2,0,0})==0);
  require(segmentDistance({3,0,0},{3,0,0})==3);
  require(segmentDistance({3,0,0},{4,0,0})==3);
  require(argc==3);
  std::array<std::array<std::vector<Vec>,2>,2> routes;
  for(int w=0;w<2;++w) {
    std::ifstream file(argv[w+1]); require(bool(file));
    for(int i=0;i<2;++i) {std::string line; require(bool(std::getline(file,line))); routes[w][i]=parseRoute(line);}
  }
  Motion crossing(1,routes[0]);
  crossing.p={Vec{-3.6,-10,2.8},Vec{3.6,-10,2.8}};
  require(!crossing.admissible({crossing.p[1],crossing.p[0]}));
  Motion throughBall(2,routes[1]);
  throughBall.p={Vec{-5.6,-22,2.8},Vec{6,-7.5,2.8}};
  require(!throughBall.admissible({Vec{5.6,-22,2.8},throughBall.p[1]}));
  Motion blocked(1,routes[0]);
  blocked.route[0]={Vec{100,-8.2,2.8}};
  for(int k=0;k<6100 && !blocked.failed;++k)blocked.advance(.02);
  require(blocked.failed && !blocked.done());
  for(int wave:{1,2}) {
    Motion a(wave,routes[wave-1]),b(wave,routes[wave-1]);
    int episodes=0;bool wasYielding=false;
    for(int k=0;k<6100 && !a.done() && !a.failed;++k){
      a.advance(.02);b.advance(.02);
      if(a.yielding && !wasYielding)++episodes;
      wasYielding=a.yielding;
      require((a.p[0]-b.p[0]).norm()==0 && (a.p[1]-b.p[1]).norm()==0);
      if(a.next[0]==0 && a.next[1]==0)require(a.p[0].z==a.p[1].z);
    }
    require(episodes==1);
    require(a.done() && !a.failed && a.rejectedTicks==0);
    require((a.p[0]-b.p[0]).norm()==0 && a.elapsed==b.elapsed);
    require(a.minPair>=pairRequired && (wave==1 || a.minBall>=ballRequired));
    require(wave!=1 || a.yieldTicks>0);
    std::cout<<"wave="<<wave<<" complete t="<<a.elapsed<<" min_pair="<<a.minPair
             <<" min_ball="<<a.minBall<<" yield_ticks="<<a.yieldTicks<<"\n";
  }
}
