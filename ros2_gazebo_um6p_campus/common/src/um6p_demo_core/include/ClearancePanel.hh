#pragma once
#include <gz/gui/Plugin.hh>
#include <gz/transport/Node.hh>
#include <gz/msgs/stringmsg.pb.h>
#include <gz/msgs/boolean.pb.h>
#include <QString>

class ClearancePanel: public gz::gui::Plugin {
  Q_OBJECT
  Q_PROPERTY(QString state READ State NOTIFY StateChanged)
 public:
  QString State() const {return state;}
  void LoadConfig(const tinyxml2::XMLElement*) override;
 signals:
  void StateChanged();
 private:
  QString state="{}";
  gz::transport::Node node;
  void Receive(const gz::msgs::StringMsg&);
  bool Capture(const gz::msgs::StringMsg&,gz::msgs::Boolean&);
};
