#pragma once
#include "Motion.hh"
#include <sstream>
namespace campus {
inline std::vector<Vec> parseRoute(const std::string& text) {
  std::istringstream input(text); std::vector<Vec> points; Vec v;
  while(input >> v.x) {
    if(!(input >> v.y >> v.z)) throw std::invalid_argument("waypoint needs x y z");
    points.push_back(v);
  }
  if(!input.eof() || points.empty()) throw std::invalid_argument("invalid route text");
  return points;
}
}
