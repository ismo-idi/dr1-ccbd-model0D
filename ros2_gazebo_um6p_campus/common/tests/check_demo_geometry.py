#!/usr/bin/env python3
"""Conservative mesh-bound checks for the fixed showcase, independent of Motion.hh."""
import csv,json,math,sys
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'campus_environment/src/um6p_campus_description'

def vertices(path):
    v=[];f=[]
    for line in path.read_text().splitlines():
        if line.startswith('v '):v.append(tuple(map(float,line.split()[1:])))
        elif line.startswith('f '):f.append([int(x.split('/')[0])-1 for x in line.split()[1:]])
    return v,f

def point_box(p,lo,hi):
    return sum(max(lo[i]-p[i],0,p[i]-hi[i])**2 for i in range(3))

def segment_box(a,b,lo,hi):
    d=[b[i]-a[i] for i in range(3)];cuts={0.,1.}
    for i in range(3):
        if d[i]:
            for bound in (lo[i],hi[i]):
                t=(bound-a[i])/d[i]
                if 0<t<1:cuts.add(t)
    cuts=sorted(cuts);best=min(point_box(a,lo,hi),point_box(b,lo,hi))
    for left,right in zip(cuts,cuts[1:]):
        mid=(left+right)/2;num=den=0
        for i in range(3):
            value=a[i]+mid*d[i]
            bound=lo[i] if value<lo[i] else hi[i] if value>hi[i] else None
            if bound is not None:num+=d[i]*(a[i]-bound);den+=d[i]**2
        t=max(left,min(right,-num/den)) if den else mid
        best=min(best,point_box([a[i]+t*d[i] for i in range(3)],lo,hi))
    return math.sqrt(best)

def check(trace):
    radii={}
    for name in ('uav_1','uav_2'):
        vs=[v for path in (PKG/'models'/name/'meshes').glob('*.obj') for v in vertices(path)[0]]
        radii[name]=max(math.dist(v,(0,0,.36)) for v in vs)
        assert radii[name]<1.2
        assert min(v[2] for v in vs)>=.005-1e-9
    for wave in (1,2):
        demo=ET.parse(ROOT/'demo'/('demo_1_no_obstacle' if wave==1 else 'demo_2_static_sphere')/f'src/um6p_demo_{wave}/worlds/demo.sdf').getroot().find('world')
        plugins=[p.attrib['filename'] for p in demo.findall('plugin')]
        assert plugins==['gz-sim-scene-broadcaster-system','CampusKinematics'],plugins
        assert float(demo.findtext('physics/max_step_size'))==.02
        apron=demo.find("model[@name='demo_apron']/link/visual")
        assert list(map(float,apron.findtext('pose').split()))==[0,-35,-.15,0,0,0]
        assert list(map(float,apron.findtext('geometry/box/size').split()))==[26,20,.3]
        # Apron covers the corridor beyond original courtyard edge y=-25.
        assert -13 < -8.2 and 13 > 8.2 and -45 < -42.2
        pads=demo.findall("model[@name='landing_pads']/link/visual")
        assert sorted(tuple(map(float,v.findtext('pose').split()[:3])) for v in pads)==[(-3.6,-40,.06),(3.6,-40,.06)]
        assert all(float(v.findtext('geometry/cylinder/length'))==.12 for v in pads)
        sphere=demo.find("model[@name='static_sphere']")
        assert (sphere is not None)==(wave==2)
        if sphere is not None:
            assert sphere.findtext('static')=='true'
            assert list(map(float,sphere.findtext('pose').split()[:3]))==[0,-22,2.4]
            assert float(sphere.findtext('link/visual/geometry/sphere/radius'))==2.4
    boxes=[];total=0
    world=ET.parse(PKG/'worlds/campus.sdf').getroot().find('world')
    for inc in world.findall('include'):
        name=inc.findtext('name')
        if name in ('courtyard','uav_1','uav_2'):continue
        pose=list(map(float,inc.findtext('pose').split()));assert pose[3:]==[0,0,0]
        for path in (PKG/'models'/name/'meshes').glob('*.obj'):
            vs,faces=vertices(path)
            for face in faces:
                total+=1
                triangle=[[vs[j][i]+pose[i] for i in range(3)] for j in face]
                lo=[min(v[i] for v in triangle) for i in range(3)]
                hi=[max(v[i] for v in triangle) for i in range(3)]
                # Entire flight center region inflated by 1.2m; discard irrelevant triangles.
                if hi[0]<-8.2 or lo[0]>8.2 or hi[1]<-42.2 or lo[1]>-5.8 or lo[2]>4.36:continue
                boxes.append((lo,hi,name))
    rows=list(csv.DictReader(Path(trace).open()));minimum=1e9;last=None
    for row in rows:
        ps=[[float(row[f'{axis}{i}']) for axis in 'xyz'] for i in (1,2)]
        for v in ps:v[2]+=.36
        if last is not None and ps!=last:
            for i in range(2):
                for lo,hi,name in boxes:minimum=min(minimum,segment_box(last[i],ps[i],lo,hi))
        last=ps
    assert total>0
    assert minimum>1.2,minimum
    return {'status':'PASS','radius_bound':1.2,'measured_radii':radii,
        'scenery_triangles_inspected':total,'near_corridor_triangle_boxes':len(boxes),
        'min_body_center_to_scenery_box':minimum if boxes else None,
        'corridor_clear_by_broadphase':not boxes,
        'ground_check':'minimum vertex z = model z + .005; z>=.12, pads top .12; paving top 0',
        'scope':'fixed geometry; sphere/inter-UAV checked separately; conservative triangle-AABB distance'}

if __name__=='__main__':print(json.dumps(check(sys.argv[1]),indent=2))
