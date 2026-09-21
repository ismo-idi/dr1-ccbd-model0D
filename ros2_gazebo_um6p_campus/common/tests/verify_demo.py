#!/usr/bin/env python3
"""Bounded integration harness for the explicitly authorized moving showcase."""
import argparse, csv, json, math, os, signal, subprocess, time, uuid
from pathlib import Path
import rclpy
from std_msgs.msg import String
from rosgraph_msgs.msg import Clock
from gz.transport13 import Node
from gz.msgs10.empty_pb2 import Empty
from gz.msgs10.scene_pb2 import Scene
from gz.msgs10.pose_v_pb2 import Pose_V
from google.protobuf import text_format

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('wave',type=int,choices=[1,2])
p.add_argument('--gui',action='store_true');p.add_argument('--output',required=True)
a=p.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
namespace='campus_verify_'+uuid.uuid4().hex
os.environ.update(GZ_PARTITION=namespace, CAMPUS_VERIFY_NAMESPACE=namespace, ROS_DOMAIN_ID='85',
    ROS_AUTOMATIC_DISCOVERY_RANGE='LOCALHOST',CAMPUS_TRACE=str(out/'trace.csv'),
    ROS_LOG_DIR=str(ROOT/'log/demo-verification'))
rclpy.init();node=rclpy.create_node('demo_verifier',namespace='/'+namespace);states=[];clocks=[];gz=Node()
render_poses={}
def render_update(message):
    for pose in message.pose:
        render_poses[pose.id]=[pose.position.x,pose.position.y,pose.position.z]
gz.subscribe(Pose_V,'/world/um6p_demo/dynamic_pose/info',render_update)
node.create_subscription(String,'/'+namespace+'/state',lambda m:states.append(json.loads(m.data)),100)
node.create_subscription(Clock,'/'+namespace+'/clock',lambda m:clocks.append(m.clock.sec+m.clock.nanosec*1e-9),100)
result={'status':'FAIL','wave':a.wave,'gui':a.gui,'ros_namespace':namespace,'gz_partition':namespace}
result['isolation']='unique Gazebo partition and ROS topics/node namespace'

def wait_for(predicate,seconds=40):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        if proc.poll() is not None:raise RuntimeError('launch exited early')
        rclpy.spin_once(node,timeout_sec=.05)
        if states and states[-1]['status']=='FAILED':raise RuntimeError(states[-1]['reason'])
        if predicate():return
    raise TimeoutError('condition timed out')

def service(name,reqtype,request):
    r=subprocess.run(['gz','service','-s',name,'--reqtype',reqtype,
        '--reptype','gz.msgs.Boolean','--timeout','5000','--req',request],
        text=True,capture_output=True,timeout=8)
    assert r.returncode==0 and 'data: true' in r.stdout,(name,r.stdout,r.stderr)

def control(paused):
    service('/world/um6p_demo/control','gz.msgs.WorldControl','pause: '+str(paused).lower())

def pause_and_confirm():
    before=len(states)
    minimum_tick=states[-1]['tick']
    control(True)
    wait_for(lambda:len(states)>before and states[-1]['paused']
        and states[-1]['tick']>=minimum_tick)
    return states[-1]

def scene_info():
    # Use bounded CLI exchange: the Python Scene request intermittently failed in headless mode.
    end=time.monotonic()+20
    while time.monotonic()<end:
        reply=subprocess.run(['gz','service','-s','/world/um6p_demo/scene/info',
            '--reqtype','gz.msgs.Empty','--reptype','gz.msgs.Scene','--timeout','3000',
            '--req',''],capture_output=True,text=True,timeout=5)
        try:
            scene=text_format.Parse(reply.stdout,Scene())
            if len(scene.model)==(10 if a.wave==2 else 9):return scene
        except text_format.ParseError:pass
        rclpy.spin_once(node,timeout_sec=.1)
    raise TimeoutError('scene service did not become ready')

def screenshot(filename="hud.png"):
    # Camera-only reset, using the same installed configuration as the launch.
    import re
    from ament_index_python.packages import get_package_share_directory
    from gz.msgs10.gui_camera_pb2 import GUICamera
    from gz.msgs10.stringmsg_pb2 import StringMsg
    cfg=Path(get_package_share_directory('um6p_demo_core'))/'config/gui.config'
    x,y,z,roll,pitch,yaw=map(float,re.search(r'<camera_pose>(.*?)</camera_pose>',cfg.read_text())[1].split())
    c=GUICamera();c.pose.position.x=x;c.pose.position.y=y;c.pose.position.z=z
    c.pose.orientation.x=-math.sin(yaw/2)*math.sin(pitch/2)
    c.pose.orientation.y=math.cos(yaw/2)*math.sin(pitch/2)
    c.pose.orientation.z=math.sin(yaw/2)*math.cos(pitch/2)
    c.pose.orientation.w=math.cos(yaw/2)*math.cos(pitch/2)
    service('/gui/move_to/pose','gz.msgs.GUICamera',str(c));time.sleep(2)
    service('/campus/demo/hud_capture','gz.msgs.StringMsg',str(StringMsg(data=str(out/filename))))
    assert (out/filename).is_file()

log=(out/'launch.log').open('w')
proc=subprocess.Popen([str(ROOT/'scripts/launch_demo.sh'),str(a.wave),
    'gui' if a.gui else 'headless'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
try:
    wait_for(lambda: len(states)>=3)
    assert all(s['paused'] and s['sim_time']==0 and s['wave']==a.wave for s in states)
    scene=scene_info()
    names=sorted(m.name for m in scene.model)
    expected=['demo_apron','campus_buildings','courtyard','landing_pads','landscaping','pergola',
        'uav_1','uav_2','um6p_landmark']+(['static_sphere'] if a.wave==2 else [])
    assert names==sorted(expected)
    assert [n for n in names if n.startswith('uav_')]==['uav_1','uav_2']
    assert ('static_sphere' in names)==(a.wave==2)
    result['initial_entities']=names
    ids={m.name:m.id for m in scene.model}
    control(False)
    if a.wave==2:
        wait_for(lambda:min(states[-1]['distances'][1:])<4.5,50)
        pause_and_confirm()
        result['near_obstacle_state']=states[-1]
        if a.gui:screenshot('obstacle.png')
        control(False)
    wait_for(lambda:states[-1]['phases'][1]=='YIELD' and states[-1]['distances'][0]<4.0,80)
    pause_and_confirm()
    hold=states[-1];mark=len(states);end=time.monotonic()+1.2
    while time.monotonic()<end:rclpy.spin_once(node,timeout_sec=.05)
    assert len(states)>mark
    assert all(s['poses']==hold['poses'] and s['sim_time']==hold['sim_time'] for s in states[mark:])
    result['pause_check']='PASS';result['midflight_state']=hold
    if a.gui:screenshot()
    control(False);wait_for(lambda:states[-1]['status']=='COMPLETE',70)
    result['completed_state']=states[-1]
    assert states[-1]['poses']==[[3.6,-40,.12],[-3.6,-40,.12]]
    assert states[-1]['yield_ticks']>0 and states[-1]['rejected_ticks']==0
    for state in states:
        assert state['wave']==a.wave, 'Foreign scenario telemetry received'
        assert abs(math.dist(*state['poses'])-state['distances'][0])<1e-8
        if a.wave==2:
            for i,pose in enumerate(state['poses']):
                center=[pose[0],pose[1],pose[2]+.36]
                assert abs(math.dist(center,[0,-22,2.4])-state['distances'][i+1])<1e-8
    result['telemetry_distances']='PASS'

    assert clocks and max(clocks)>10,'No advancing ROS clock exchange'
    assert sorted(name for name,ns in node.get_node_names_and_namespaces()
        if ns=='/'+namespace)==['campus_demo_bridge','demo_verifier']
    scene=scene_info()
    # Scene/info describes the scene graph; use dynamic render poses for motion.
    wait_for(lambda:all(ids[f'uav_{i+1}'] in render_poses and
        math.dist(render_poses[ids[f'uav_{i+1}']],states[-1]['poses'][i])<1e-8
        for i in range(2)),5)
    actual={f'uav_{i+1}':render_poses[ids[f'uav_{i+1}']] for i in range(2)}
    result['final_render_poses']=actual
    for i in range(2):
        assert math.dist(actual[f'uav_{i+1}'],states[-1]['poses'][i])<1e-8
    (out/'final-scene.txt').write_text(str(scene))
    control(True)
    result['ros_clock_max']=max(clocks);result['ros_messages']=len(states)
finally:
    if proc.poll() is None:proc.send_signal(signal.SIGINT)
    try:proc.wait(timeout=15)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
    log.close();result['exit_code']=proc.returncode
    (out/'received-states.json').write_text(json.dumps(states)+'\n')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    node.destroy_node();rclpy.shutdown()

# Independent calculation from the per-update ECM trace, not planner margins.
def sub(a,b):return [x-y for x,y in zip(a,b)]
def norm(a):return math.sqrt(sum(x*x for x in a))
def closest(a,b):
    d=sub(b,a);den=sum(x*x for x in d)
    t=min(1,max(0,-sum(x*y for x,y in zip(a,d))/den)) if den else 0
    return norm([x+t*y for x,y in zip(a,d)])
rows=list(csv.DictReader((out/'trace.csv').open()));minimum_pair=1e9;minimum_ball=1e9
previous=None;unique=[]
for row in rows:
    q=[[float(row[f'{axis}{i}']) for axis in 'xyz'] for i in (1,2)]
    assert all(math.isfinite(v) for p in q for v in p)
    if previous is not None:
        minimum_pair=min(minimum_pair,closest(sub(previous[0],previous[1]),sub(q[0],q[1])))
        for i in range(2):
            assert math.dist(previous[i],q[i])<=.85*.02+1e-8
            if a.wave==2:
                center=[0,-22,2.04] # sphere relative to UAV model origin; body center +.36z
                minimum_ball=min(minimum_ball,closest(sub(previous[i],center),sub(q[i],center)))
    for v in q:assert -7<=v[0]<=7 and -41<=v[1]<=-7 and .12-1e-9<=v[2]<=2.8+1e-9
    previous=q
    if not unique or int(row['tick'])!=unique[-1][0]:unique.append((int(row['tick']),q))
takeoff=[next(t for t,q in unique if q[i][2]>.12+1e-9) for i in range(2)]
assert takeoff[0]==takeoff[1]
yield_rows=[row for row in rows if row['phase2']=='YIELD']
assert yield_rows
first_yield=int(yield_rows[0]['tick']);last_yield=int(yield_rows[-1]['tick'])
assert any(int(row['tick'])>last_yield and row['phase2'] in ('TRAVEL','BYPASS') for row in rows)
scenario=ROOT/'demo'/('demo_1_no_obstacle' if a.wave==1 else 'demo_2_static_sphere')
expected=json.loads((scenario/'tests/expected.json').read_text())
assert takeoff[0]==expected['takeoff_tick']
assert int(rows[-1]['tick'])>=expected['completion_tick']
assert result['completed_state']['yield_ticks']==expected['yield_ticks']
result['simultaneous_takeoff_tick']=takeoff[0]
result['yield_interval_ticks']=[first_yield,last_yield]
unique_rows={int(row['tick']):row for row in rows}
assert all(unique_rows[t]['phase2']=='YIELD' for t in range(first_yield,last_yield+1))
result['single_continuous_yield']='PASS'
assert minimum_pair>=3.2+1e-6
if a.wave==2:assert minimum_ball>=4.2+1e-6
assert rows[-1]['status']=='COMPLETE'
assert proc.returncode==0
text=(out/'launch.log').read_text()
assert not any(x in text for x in ['[Err]','process has died','Missing material','Unable to find uri'])
from check_demo_geometry import check
result['geometry_check']=check(out/'trace.csv')
result.update(status='PASS',trace_rows=len(rows),min_pair=minimum_pair,
    min_ball=minimum_ball if a.wave==2 else None)
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
