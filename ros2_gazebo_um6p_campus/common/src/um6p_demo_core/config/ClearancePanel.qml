import QtQuick 2.12
import QtQuick.Layouts 1.12

Rectangle {
  id: panel
  width: 360
  height: obstacle ? 334 : 176
  color: "#ed13232e"
  radius: 14
  property var sample: ({})
  property bool obstacle: sample.wave === 2
  property double updated: 0
  property bool fresh: false
  function accept() {
    try { sample = JSON.parse(ClearancePanel.state); updated = Date.now(); fresh = true; }
    catch (error) { fresh = false; }
  }
  Connections { target: ClearancePanel; onStateChanged: panel.accept() }
  Timer { interval: 250; running: true; repeat: true
    onTriggered: panel.fresh = Date.now() - panel.updated < 1500 }
  function distance(index) { return sample.distances ? sample.distances[index] : 0; }
  function minimum(index) { return index === 0 ? 3.2 : 4.2; }
  function shade(index) {
    if (!fresh || !sample.distances) return "#9ba9b2";
    var margin = distance(index) - minimum(index);
    return margin < 0 ? "#ff646b" : margin < 0.8 ? "#ffbe59" : "#62e5ac";
  }
  function label(index) {
    if (!fresh || !sample.distances) return "NO LIVE DATA";
    var margin = distance(index) - minimum(index);
    return margin < 0 ? "VIOLATION" : margin < 0.8 ? "NEAR LIMIT" : "CLEAR";
  }
  Column {
    anchors.fill: parent; anchors.margins: 16; spacing: 9
    Row {
      spacing: 10
      Text { text: "LIVE CLEARANCE"; color: "#ffffff"; font.pixelSize: 17; font.bold: true }
      Text { text: panel.sample.paused ? "PAUSED" : panel.sample.status === "COMPLETE" ? "LANDED" : "LIVE"
        color: "#a9bac7"; font.pixelSize: 12; anchors.baseline: parent.children[0].baseline }
    }
    Text { text: "Wave " + (panel.sample.wave || "\u2013") + "  \u00b7  " +
        (panel.sample.sim_time || 0).toFixed(1) + " s  \u00b7  " +
        (panel.sample.phases ? panel.sample.phases.join(" / ") : "Waiting for scene")
      color: "#c5d3dc"; font.pixelSize: 12 }
    Repeater {
      model: panel.obstacle ? 3 : 1
      delegate: Rectangle {
        width: 328; height: 70; radius: 8; color: "#293c49"
        Rectangle { width: 4; height: 46; radius: 2; x: 10; y: 12; color: panel.shade(index) }
        Text { x: 24; y: 8; text: index === 0 ? "UAV 1  \u2194  UAV 2" : "UAV " + index + "  \u2194  SPHERE"
          color: "#e5edf3"; font.pixelSize: 13; font.bold: true }
        Text { x: 24; y: 28; text: panel.fresh && panel.sample.distances ? panel.distance(index).toFixed(2) + " m" : "\u2014"
          color: panel.shade(index); font.pixelSize: 27; font.bold: true }
        Text { x: 196; y: 12; text: panel.label(index); color: panel.shade(index); font.pixelSize: 12; font.bold: true }
        Text { x: 196; y: 33; text: "min " + panel.minimum(index).toFixed(2) + " m"
          color: "#c5d3dc"; font.pixelSize: 12 }
        Text { x: 196; y: 49; text: "margin " + (panel.distance(index)-panel.minimum(index)).toFixed(2) + " m"
          color: "#c5d3dc"; font.pixelSize: 11 }
      }
    }
  }
}
