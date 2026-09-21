// Test the actual QML color functions with synthetic data, without Gazebo motion.
#include <QGuiApplication>
#include <QFile>
#include <QQmlEngine>
#include <QQmlComponent>
#include <QQmlContext>
#include <QVariant>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <iostream>
#include <stdexcept>
class MockSample: public QObject {
  Q_OBJECT
  Q_PROPERTY(QString state READ State NOTIFY StateChanged)
 public:
  QString value="{}";
  QString State() const {return value;}
 signals:
  void StateChanged();
};
int main(int argc,char**argv) {
  QGuiApplication app(argc,argv); QQmlEngine engine;
  auto require=[](bool ok){if(!ok)throw std::runtime_error("HUD check failed");};
  require(argc==2);
  MockSample sample;
  engine.rootContext()->setContextProperty("ClearancePanel",&sample);
  QFile file(argv[1]);require(file.open(QIODevice::ReadOnly));
  QQmlComponent component(&engine);
  component.setData(file.readAll(),QUrl("qrc:/panel-test.qml"));
  std::unique_ptr<QObject> panel(component.create());
  if(!panel){std::cerr<<component.errorString().toStdString();return 1;}
  int cases=0;
  for(int wave:{1,2})for(int index=0;index<(wave==1?1:3);++index) {
    auto call=[&](const char*method){QVariant out;
      require(QMetaObject::invokeMethod(panel.get(),method,Q_RETURN_ARG(QVariant,out),Q_ARG(QVariant,index)));
      return out.toString();};
    for(double margin:{-.01,0.,.79,.81}) {
      QJsonArray distances{7.2,8.,8.};distances[index]=(index==0?3.2:4.2)+margin;
      QJsonObject data{{"wave",wave},{"distances",distances},{"paused",true},
        {"sim_time",12.},{"phases",QJsonArray{"TRAVEL","YIELD"}}};
      sample.value=QString::fromUtf8(QJsonDocument(data).toJson());
      emit sample.StateChanged();
      app.processEvents();
      require(call("label")== (margin<0?"VIOLATION":margin<.8?"NEAR LIMIT":"CLEAR"));
      require(call("shade")== (margin<0?"#ff646b":margin<.8?"#ffbe59":"#62e5ac"));
      require(panel->property("height").toInt()==(wave==2?334:176));++cases;
    }
    panel->setProperty("fresh",false);
    require(call("label")=="NO LIVE DATA" && call("shade")=="#9ba9b2");++cases;
  }
  std::cout<<"{\"status\":\"PASS\",\"cases\":"<<cases
    <<",\"scope\":\"real QML; synthetic data only; no unsafe simulation\"}\n";
}

#include "panel_check.moc"
