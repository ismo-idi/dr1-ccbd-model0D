#!/usr/bin/env python3
"""Check installed assets and rendering-only scope, without running Gazebo."""
import hashlib, json, math, os, subprocess
from pathlib import Path
import xml.etree.ElementTree as E
from ament_index_python.packages import get_package_share_directory

pkg=Path(get_package_share_directory('um6p_campus_description'))
models=pkg/'models'; world=pkg/'worlds/campus.sdf'
w=E.parse(world).getroot().find('world')
assert w is not None and w.attrib['name']=='um6p_campus'
assert [x.attrib['name'] for x in w.findall('plugin')]==['gz::sim::systems::SceneBroadcaster']
assert len(w.findall('include'))==7
names=[]; meshes=0; triangles=0
for inc in w.findall('include'):
 name=inc.findtext('name');names.append(name)
 assert inc.findtext('uri')=='model://'+name
 sdf=models/name/'model.sdf'; model=E.parse(sdf).getroot().find('model')
 assert model.findtext('static')=='true'
 assert not model.findall('.//plugin')+model.findall('.//sensor')+model.findall('.//joint')
 for uri in model.findall('.//uri'):
  assert uri.text.startswith('model://')
  path=models/uri.text.removeprefix('model://')
  assert path.is_file(),path
  vertices=0; faces=[]
  for line in path.read_text().splitlines():
   if line.startswith('mtllib '):
    assert (path.parent/line.split(maxsplit=1)[1]).is_file(), 'Missing MTL'
   if line.startswith('v '):
    values=list(map(float,line.split()[1:]));assert len(values)==3 and all(math.isfinite(x) for x in values);vertices+=1
   if line.startswith('f '):faces.append([int(x.split('/')[0]) for x in line.split()[1:]])
  assert vertices>0 and faces and all(len(f)==3 and all(1<=i<=vertices for i in f) for f in faces)
  meshes+=1;triangles+=len(faces)
 env=dict(os.environ,SDF_PATH=str(models))
 r=subprocess.run(['gz','sdf','-k',str(sdf)],env=env,capture_output=True,text=True,timeout=15)
 assert r.returncode==0 and 'Valid.' in r.stdout and 'Error' not in r.stderr,(sdf,r.stdout,r.stderr)
r=subprocess.run(['gz','sdf','-k',str(world)],env=env,capture_output=True,text=True,timeout=15)
assert r.returncode==0 and 'Valid.' in r.stdout and 'Error' not in r.stderr,(r.stdout,r.stderr)
assert sorted(n for n in names if n.startswith('uav_'))==['uav_1','uav_2']
print(json.dumps({'status':'PASS','models':names,'meshes':meshes,'triangles':triangles,'SDF_validation':'world plus all 7 models','resolved_from':'installed package'},indent=2))
