#!/usr/bin/env python3
"""Bounded installed-workspace check; never requests control, step or unpause."""
import argparse, json, math, os, re, signal, subprocess, time
from pathlib import Path
import rclpy
from std_msgs.msg import String
from gz.transport13 import Node
from gz.msgs10.empty_pb2 import Empty
from gz.msgs10.scene_pb2 import Scene
from gz.msgs10.world_stats_pb2 import WorldStatistics
from gz.msgs10.stringmsg_pb2 import StringMsg

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser(); p.add_argument('--gui',action='store_true')
p.add_argument('--view',default='courtyard',choices=['courtyard','overview'])
p.add_argument('--output',default='evidence/runtime'); args=p.parse_args()
out=ROOT/args.output; out.mkdir(parents=True,exist_ok=True)
os.environ['GZ_PARTITION']='campus_verify_'+str(os.getpid())
os.environ['ROS_DOMAIN_ID']='84'
os.environ['ROS_AUTOMATIC_DISCOVERY_RANGE']='LOCALHOST'
os.environ['ROS_LOG_DIR']=str(ROOT/'log/verification')
result={'status':'FAIL','mode':'gui' if args.gui else 'headless','runs':[]}
stats=[]; gz=Node()
gz.subscribe(WorldStatistics,'/world/um6p_campus/stats',lambda m: stats.append({
 'paused':m.paused,'iterations':m.iterations,'sim_sec':m.sim_time.sec,
 'sim_nsec':m.sim_time.nsec,'stepping':m.stepping}))
rclpy.init(); node=rclpy.create_node('campus_verifier'); messages=[]
node.create_subscription(String,'/campus/evidence',lambda m:messages.append(m.data),10)
pub=gz.advertise('/campus/evidence',StringMsg)
try:
 for run in range(2):
  stats.clear(); messages.clear()
  log=open(out/f'launch-{run+1}.log','w')
  proc=subprocess.Popen([str(ROOT/'scripts/launch_paused.sh'),'gui' if args.gui else 'headless',args.view],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  record={'pid':proc.pid}; result['runs'].append(record)
  try:
   deadline=time.monotonic()+35; scene=None
   while time.monotonic()<deadline:
    assert proc.poll() is None, 'launch exited before scene response'
    ok, reply=gz.request('/world/um6p_campus/scene/info',Empty(),Empty,Scene,1000)
    if ok and len(reply.model)==7: scene=reply;break
    time.sleep(.2)
   assert scene is not None, 'scene service did not return seven models'
   (out/f'scene-{run+1}.txt').write_text(str(scene))
   names=sorted(m.name for m in scene.model)
   assert names==sorted(['courtyard','pergola','campus_buildings','um6p_landmark','landscaping','uav_1','uav_2']), names
   poses={}
   for m in scene.model:
    if m.name.startswith('uav_'):
     expected=(-3.6,-8.2,.12) if m.name=='uav_1' else (3.6,-8.2,.12)
     actual=(m.pose.position.x,m.pose.position.y,m.pose.position.z)
     assert all(abs(a-b)<1e-8 for a,b in zip(actual,expected)),actual
     yaw=.3 if m.name=='uav_1' else -.3
     assert abs(m.pose.orientation.z-math.sin(yaw/2))<1e-8
     assert abs(m.pose.orientation.w-math.cos(yaw/2))<1e-8
     poses[m.name]=list(actual)+[0,0,yaw]
   token=f'campus-paused-check-{run+1}'
   deadline=time.monotonic()+12
   while token not in messages and time.monotonic()<deadline:
    pub.publish(StringMsg(data=token));rclpy.spin_once(node,timeout_sec=.2)
   assert token in messages, 'No Gazebo-to-ROS text message exchange'
   # Wall time, independent of simulation time. No /clock assumption.
   deadline=time.monotonic()+(12 if args.gui else 4)
   while time.monotonic()<deadline:rclpy.spin_once(node,timeout_sec=.1)
   assert len(stats)>=3,'No sufficient world statistics samples'
   assert all(s['paused'] and s['iterations']==0 and s['sim_sec']==0 and s['sim_nsec']==0 and not s['stepping'] for s in stats),stats[-3:]
   discovered=sorted(node.get_node_names())
   assert discovered==['campus_evidence_bridge','campus_verifier'],discovered
   record.update(names=names,uav_poses=poses,ros_nodes=discovered,bridge_received=token,stats_samples=len(stats),stats_first=stats[0],stats_last=stats[-1])
   if args.gui and run==0:
    services=subprocess.run(['gz','service','-l'],capture_output=True,text=True,timeout=5)
    (out/'gui-services.txt').write_text(services.stdout)
    # Screenshot service is an inspection-only GUI operation.
    assert '/gui/screenshot' in services.stdout, 'Screenshot service unavailable'
    if '/gui/screenshot' in services.stdout:
     from gz.msgs10.boolean_pb2 import Boolean
     from gz.msgs10.gui_camera_pb2 import GUICamera
     from ament_index_python.packages import get_package_share_directory
     cfg=Path(get_package_share_directory('um6p_campus_bringup'))/'config'/('overview.config' if args.view=='overview' else 'gui.config')
     xyzrpy=list(map(float,re.search(r'<camera_pose>(.*?)</camera_pose>',cfg.read_text()).group(1).split()))
     camera=GUICamera();camera.pose.position.x,camera.pose.position.y,camera.pose.position.z=xyzrpy[:3]
     pitch,yaw=xyzrpy[4:]
     camera.pose.orientation.x=-math.sin(yaw/2)*math.sin(pitch/2)
     camera.pose.orientation.y=math.cos(yaw/2)*math.sin(pitch/2)
     camera.pose.orientation.z=math.sin(yaw/2)*math.cos(pitch/2)
     camera.pose.orientation.w=math.cos(yaw/2)*math.cos(pitch/2)
     command=['gz','service','-s','/gui/move_to/pose','--reqtype','gz.msgs.GUICamera','--reptype','gz.msgs.Boolean','--timeout','5000','--req',str(camera)]
     moved=subprocess.run(command,capture_output=True,text=True,timeout=8)
     record['camera_reset_response']=moved.stdout
     assert moved.returncode==0 and 'data: true' in moved.stdout, 'Saved camera reset failed: '+moved.stdout+moved.stderr
     time.sleep(2)
     record['screenshot_camera_xyzrpy']=xyzrpy
     before=set(out.glob('*.png'))
     shot=subprocess.run(['gz','service','-s','/gui/screenshot','--reqtype','gz.msgs.StringMsg','--reptype','gz.msgs.Boolean','--timeout','5000','--req',str(StringMsg(data=str(out.resolve())))],capture_output=True,text=True,timeout=8)
     record['screenshot_service']={'exit_code':shot.returncode,'reply':shot.stdout}
     assert shot.returncode==0 and 'data: true' in shot.stdout, 'Screenshot request failed: '+shot.stdout+shot.stderr
     deadline=time.monotonic()+5
     while not (set(out.glob('*.png'))-before) and time.monotonic()<deadline:time.sleep(.1)
     assert set(out.glob('*.png'))-before, 'No actual screenshot file saved'
     record['screenshot_files']=[p.name for p in set(out.glob('*.png'))-before]
     assert all(s['paused'] and s['iterations']==0 and s['sim_sec']==0 and s['sim_nsec']==0 for s in stats), 'Time advanced during camera inspection'
   record['status']='PASS'
  finally:
   if proc.poll() is None:proc.send_signal(signal.SIGINT)
   try:proc.wait(timeout=15)
   except subprocess.TimeoutExpired:
    os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
    record['forced_shutdown']=True
   log.close();record['exit_code']=proc.returncode
   text=(out/f'launch-{run+1}.log').read_text()
   assert 'process has died' not in text, 'Gazebo or bridge child failed; inspect launch log'
   assert 'Missing material' not in text and 'Unable to find uri' not in text, 'Resource warnings'
   assert '[Err]' not in text, 'Gazebo error in launch log'
   assert proc.returncode==0, f'unclean launch exit {proc.returncode}'
   time.sleep(1)
 result['status']='PASS'
except Exception as exc:
 result['error']=str(exc); raise
finally:
 result['stats_tail']=stats[-5:]
 (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
 node.destroy_node();rclpy.shutdown()
 print(json.dumps(result,indent=2))
