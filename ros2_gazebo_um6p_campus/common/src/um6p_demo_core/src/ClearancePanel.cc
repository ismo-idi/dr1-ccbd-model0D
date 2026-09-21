#include "ClearancePanel.hh"
#include <gz/plugin/Register.hh>
#include <QQuickItem>
#include <QQuickWindow>
#include <QImage>
#include <QJsonDocument>
#include <QJsonObject>

void ClearancePanel::LoadConfig(const tinyxml2::XMLElement*) {
  node.Subscribe("/campus/demo/state",&ClearancePanel::Receive,this);
  node.Advertise("/campus/demo/hud_capture",&ClearancePanel::Capture,this);
}
void ClearancePanel::Receive(const gz::msgs::StringMsg& msg) {
  const QString next=QString::fromStdString(msg.data());
  // Transport callback runs off the GUI thread; all QML state changes are queued.
  QMetaObject::invokeMethod(this,[this,next]{
    state=next;
    auto data=QJsonDocument::fromJson(next.toUtf8()).object();
    if(auto card=CardItem()) {
      card->setProperty("height",data["wave"].toInt()==2?334:176);
      if(auto parent=card->parentItem())
        card->setX(qMax(16.0,parent->width()-376.0));
    }
    emit StateChanged();
  },Qt::QueuedConnection);
}
bool ClearancePanel::Capture(const gz::msgs::StringMsg& request,gz::msgs::Boolean& reply) {
  bool saved=false;
  const QString path=QString::fromStdString(request.data());
  QMetaObject::invokeMethod(this,[this,path,&saved]{
    auto item=PluginItem();
    if(item && item->window())saved=item->window()->grabWindow().save(path,"PNG");
  },Qt::BlockingQueuedConnection);
  reply.set_data(saved);return saved;
}
GZ_ADD_PLUGIN(ClearancePanel,gz::gui::Plugin)
