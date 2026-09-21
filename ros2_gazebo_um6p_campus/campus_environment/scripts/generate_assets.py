#!/usr/bin/env python3
"""Deterministic first-party campus meshes. Metres; no downloaded assets."""
from pathlib import Path
from math import sin, cos, pi, sqrt, atan2
import json
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'src/um6p_campus_description'
COLORS = {
 'ivory': (.86,.84,.75), 'roof': (.50,.58,.60),
 'stone': (.72,.62,.46), 'recess': (.28,.25,.20),
 'glass': (.10,.30,.39), 'red': (.65,.025,.025),
 'letter': (.98,.83,.48), 'paving': (.60,.55,.44),
 'joint': (.43,.39,.31), 'green': (.23,.34,.10),
 'leaf': (.36,.43,.14), 'trunk': (.31,.21,.12),
 'dark': (.055,.065,.08), 'blue': (.025,.35,.70),
 'orange': (.96,.26,.045), 'white': (.94,.94,.88),
}

def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):
 d=sqrt(sum(x*x for x in a)); return tuple(x/d for x in a)

class Mesh:
 def __init__(self): self.triangles=[]
 def tri(self,a,b,c): self.triangles.append((a,b,c))
 def box(self,c,s,yaw=0):
  pts=[]
  for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
   x,y,z=x*s[0]/2,y*s[1]/2,z*s[2]/2
   pts.append((c[0]+cos(yaw)*x-sin(yaw)*y,c[1]+sin(yaw)*x+cos(yaw)*y,c[2]+z))
  for a,b,c_,d in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
   self.tri(pts[a],pts[b],pts[c_]); self.tri(pts[a],pts[c_],pts[d])
 def beam(self,a,b,w,depth=None):
  axis=unit(sub(b,a)); ref=(0,0,1) if abs(axis[2])<.95 else (0,1,0)
  u=unit(cross(axis,ref)); v=cross(axis,u); depth=depth or w
  pts=[tuple(p[i]+sx*w/2*u[i]+sy*depth/2*v[i] for i in range(3)) for p in (a,b) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
  for a_,b_,c_,d_ in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
   self.tri(pts[a_],pts[b_],pts[c_]); self.tri(pts[a_],pts[c_],pts[d_])
 def cylinder(self,c,r,h,n=16):
  for j in range(n):
   a,b=2*pi*j/n,2*pi*(j+1)/n
   p=[(c[0]+r*cos(t),c[1]+r*sin(t),c[2]+z) for z in (-h/2,h/2) for t in (a,b)]
   self.tri(p[0],p[1],p[3]); self.tri(p[0],p[3],p[2])
   self.tri((c[0],c[1],c[2]-h/2),p[1],p[0]); self.tri((c[0],c[1],c[2]+h/2),p[2],p[3])
 def write(self,p):
  out=['# First-party deterministic geometry; units: metres.', f'mtllib {p.stem}.mtl', 'o geometry', 'usemtl surface']
  color=COLORS[p.stem]
  p.with_suffix('.mtl').write_text('newmtl surface\nKa '+' '.join(map(str,color))+'\nKd '+' '.join(map(str,color))+'\nKs 0.08 0.08 0.08\nNs 16\nd 1\n')
  for i,(a,b,c) in enumerate(self.triangles):
   normal=unit(cross(sub(b,a),sub(c,a)))
   out.extend('v '+' '.join(f'{v:.6f}' for v in t) for t in (a,b,c))
   out.append('vn '+' '.join(f'{v:.6f}' for v in normal))
   out.append('f '+' '.join(f'{3*i+j}//{i+1}' for j in (1,2,3)))
  p.write_text('\n'.join(out)+'\n')

class Model:
 def __init__(self,name,pose=(0,0,0,0,0,0)):
  self.name=name; self.pose=pose; self.mesh={}
 def m(self,color): return self.mesh.setdefault(color,Mesh())
 def save(self):
  folder=PKG/'models'/self.name; (folder/'meshes').mkdir(parents=True,exist_ok=True)
  sdf=E.Element('sdf',version='1.10'); model=E.SubElement(sdf,'model',name=self.name)
  E.SubElement(model,'static').text='true'; link=E.SubElement(model,'link',name='body')
  for color,mesh in sorted(self.mesh.items()):
   mesh.write(folder/'meshes'/f'{color}.obj')
   vis=E.SubElement(link,'visual',name=color); geo=E.SubElement(vis,'geometry')
   E.SubElement(E.SubElement(geo,'mesh'),'uri').text=f'model://{self.name}/meshes/{color}.obj'
   mat=E.SubElement(vis,'material'); rgba=' '.join(map(str,(*COLORS[color],1)))
   E.SubElement(mat,'ambient').text=rgba; E.SubElement(mat,'diffuse').text=rgba
   E.SubElement(mat,'specular').text='.08 .08 .08 1'
  if self.name.startswith('uav_'):
   c=E.SubElement(link,'collision',name='placeholder_body')
   E.SubElement(c,'pose').text='0 0 .36 0 0 0'
   E.SubElement(E.SubElement(E.SubElement(c,'geometry'),'box'),'size').text='.65 .45 .24'
  E.indent(sdf); E.ElementTree(sdf).write(folder/'model.sdf',encoding='unicode',xml_declaration=True)
  (folder/'model.config').write_text(f'<model><name>{self.name}</name><version>1.0</version><sdf version="1.10">model.sdf</sdf><author><name>CCBO campus preparation</name></author><description>Static scene geometry; no validated dynamics.</description></model>\n')

models=[]
def make(name,pose=(0,0,0,0,0,0)):
 m=Model(name,pose); models.append(m); return m

court=make('courtyard')
court.m('paving').box((0,5,-.15),(64,60,.3))
for x in range(-30,31,2): court.m('joint').box((x,5,.001),(.018,58,.002))
for y in range(-23,35,2): court.m('joint').box((0,y,.001),(62,.018,.002))
for x in (-3.6,3.6):
 court.m('dark').cylinder((x,-8.2,.06),1.2,.12,48)
 court.m('white').box((x,-8.2,.122),(.8,.1,.004))
 for dx in (-.35,.35): court.m('white').box((x+dx,-8.2,.122),(.10,.75,.004))

pergola=make('pergola')
def roof_z(x): return 8.6+1.35*cos(pi*x/28)
for x in range(-14,14):
 for y in range(0,18,2):
  pergola.m('roof').beam((x+.04,y+1,roof_z(x)+.17),(x+.96,y+1,roof_z(x+1)+.17),1.91,.09)
for x in range(-14,15,2): pergola.m('ivory').beam((x,0,roof_z(x)),(x,18,roof_z(x)),.12,.24)
for y in range(0,19,2):
 for x in range(-14,14): pergola.m('ivory').beam((x,y,roof_z(x)),(x+1,y,roof_z(x+1)),.15,.25)
for y in (0,18):
 for x in range(-14,14): pergola.m('white').beam((x,y,roof_z(x)+.16),(x+1,y,roof_z(x+1)+.16),.28,.38)
for x in (-10,0,10):
 for y in (3,15):
  pergola.m('white').beam((x,y,0),(x+.35,y,4.6),.30,.40)
  for dx,dy in [(-3,-2.5),(3,-2.5),(-3,2.5),(3,2.5)]:
   pergola.m('white').beam((x+.35,y,4.2),(x+dx,y+dy,roof_z(x+dx)-.15),.22,.28)
  pergola.m('ivory').box((x,y,.12),(1,1,.24))

building=make('campus_buildings',(0,12,0,0,0,0))
# Columns and floor bands leave real recesses ahead of the glass backing.
for cx,width in [(-16,16),(5,22)]:
 building.m('stone').box((cx,25,4.5),(width,8,9))
 for z in (.5,4.6,8.7): building.m('stone').box((cx,20.4,z),(width,1.2,.8))
 for x in range(int(cx-width/2)+1,int(cx+width/2),3):
  building.m('stone').box((x,20.4,4.6),(.7,1.2,7.4))
  for z in (2.5,6.6):
   building.m('recess').box((x+1.35,20.98,z),(1.9,.04,3.2))
   building.m('glass').box((x+1.35,20.94,z),(1.45,.035,2.9))
   building.m('ivory').box((x+1.35,20.90,z),(.05,.04,2.9))
 building.m('ivory').box((cx,24.8,9.12),(width+.5,8.6,.24))

landmark=make('um6p_landmark',(-7,0,0,0,0,0))
# Hand-drawn line letters on front (-Y) and right (+X) faces. No font/logo asset.
letters={
 'U': [[(-.38,.48),(-.38,-.30),(-.22,-.48),(.22,-.48),(.38,-.30),(.38,.48)]],
 'M': [[(-.40,-.48),(-.40,.48),(0,-.05),(.40,.48),(.40,-.48)]],
 '6': [[(.30,.48),(-.15,.30),(-.36,-.12),(-.30,-.43),(.22,-.48),(.38,-.24),(.25,.02),(-.31,.02)]],
 'P': [[(-.35,-.48),(-.35,.48),(.20,.48),(.38,.28),(.20,.05),(-.35,.05)]],
}
for i,ch in enumerate('P6MU'):
 starts={c:len(m.triangles) for c,m in landmark.mesh.items()}
 z=.18+.79+i*1.60
 landmark.m('red').box((0,0,z),(1.6,1.6,1.56),0)
 for face in ('front','right'):
  for line in letters[ch]:
   for a,b in zip(line,line[1:]):
    a=(a[0]*1.25,a[1]*1.25); b=(b[0]*1.25,b[1]*1.25)
    p=(a[0],-.81,z+a[1]) if face=='front' else (.81,a[0],z+a[1])
    q=(b[0],-.81,z+b[1]) if face=='front' else (.81,b[0],z+b[1])
    landmark.m('letter').beam(p,q,.17,.17)
 # Rotate each block and its lettering together; U/6 share +12 deg, M/P -12 deg.
 angle=(12 if ch in 'U6' else -12)*pi/180
 for color,mesh in landmark.mesh.items():
  start=starts.get(color,0)
  mesh.triangles[start:]=[tuple((cos(angle)*x-sin(angle)*y,sin(angle)*x+cos(angle)*y,z_) for x,y,z_ in tri) for tri in mesh.triangles[start:]]
landmark.m('stone').box((0,0,.09),(2,2,.18))

landscape=make('landscaping')
for j,(x,y) in enumerate([(-19,0),(18,1),(-19,11),(18,12),(-12,29),(15,29)]):
 h=7.0+(j%3)*.55
 landscape.m('stone').cylinder((x,y,.2),1.25,.4,24)
 landscape.m('green').cylinder((x,y,.41),1.10,.08,24)
 landscape.m('trunk').beam((x,y,.4),(x+.3,y,h),.30)
 for z in range(1,int(h*5)):
  landscape.m('trunk').cylinder((x+.3*z/(h*5),y,z*.2),.19,.08,10)
 for k in range(11):
  a=k*2*pi/11+j*.22
  p=(x+.3,y,h)
  for t in range(5):
   r1,r2=t*.55,(t+1)*.55
   q=(x+.3+r2*cos(a),y+r2*sin(a),h+.5*sin(pi*r2/2.75)-.45*r2)
   landscape.m('leaf' if k%2 else 'green').beam(p,q,.28*(1-t/6),.06); p=q
for x,y in [(-12,-7),(11,-7),(-15,14),(14,15)]:
 landscape.m('stone').box((x,y,.35),(3,1.2,.7))
 landscape.m('green').box((x,y,.75),(2.8,1,.35))
for x in (-12,11):
 landscape.m('trunk').box((x,-9,.55),(3,.55,.16))
 for dx in (-1,1): landscape.m('dark').box((x+dx,-9,.27),(.15,.4,.54))

for i,(x,color,yaw) in enumerate([(-3.6,'blue',.3),(3.6,'orange',-.3)],1):
 m=make(f'uav_{i}',(x,-8.2,.12,0,0,yaw))
 m.m(color).box((0,0,.38),(.65,.45,.24))
 m.m('white').box((.16,0,.51),(.18,.30,.04))
 m.m('dark').box((.35,0,.30),(.16,.22,.16))
 for sx in (-1,1):
  for sy in (-1,1):
   p=(sx*.58,sy*.58,.42)
   m.m('dark').beam((sx*.2,sy*.15,.38),p,.10)
   m.m(color).cylinder(p,.13,.14)
   m.m('dark').box((p[0],p[1],.51),(.62,.075,.025),sx*sy*.4)
 for y in (-.27,.27):
  m.m('dark').beam((-.36,y,.03),(.36,y,.03),.05)
  for x_ in (-.22,.22): m.m('dark').beam((x_,y,.03),(x_,y,.30),.045)

for m in models: m.save()
world=E.Element('sdf',version='1.10'); w=E.SubElement(world,'world',name='um6p_campus')
# Explicit rendering-only system list prevents automatic default Physics loading.
E.SubElement(w,'plugin',filename='gz-sim-scene-broadcaster-system',name='gz::sim::systems::SceneBroadcaster')
scene=E.SubElement(w,'scene'); E.SubElement(scene,'ambient').text='.65 .65 .65 1'
E.SubElement(scene,'background').text='.55 .72 .86 1'; E.SubElement(scene,'shadows').text='true'
light=E.SubElement(w,'light',name='warm_sun',type='directional')
for k,v in {'pose':'0 0 20 0 0 0','diffuse':'.95 .86 .72 1','specular':'.2 .2 .2 1','direction':'-.45 .5 -.85','cast_shadows':'true'}.items(): E.SubElement(light,k).text=v
for m in models:
 inc=E.SubElement(w,'include'); E.SubElement(inc,'uri').text=f'model://{m.name}'
 E.SubElement(inc,'name').text=m.name; E.SubElement(inc,'pose').text=' '.join(map(str,m.pose))
(PKG/'worlds').mkdir(exist_ok=True); E.indent(world)
E.ElementTree(world).write(PKG/'worlds/campus.sdf',encoding='unicode',xml_declaration=True)
(ROOT/'docs/scene-manifest.json').write_text(json.dumps({
 'units':'metres, radians','frame':'right-handed; X courtyard right, Y toward rear buildings, Z up; no georeference',
 'models':[{'name':m.name,'pose':m.pose,'static':True,'triangles':sum(len(x.triangles) for x in m.mesh.values())} for m in models],
 'pergola_dimensions':[28,18],'canopy_height_range':[8.6,9.95],
 'landmark_blocks':4,'landmark_top_to_bottom':'UM6P','uav_center_spacing':7.2,
 'landmark_block_yaw_degrees_top_to_bottom':[12,-12,12,-12],
 'building_translation_y':12,'pergola_to_front_facade_gap':13.8,
 'reserved_forecourt':{'x':[-9,9],'y':[-22,-4],'area_m2':324,'status':'unmarked clear staging reserve; not a certified flight envelope or capacity claim'},
 'physics_plugin':False,'assets':'first-party procedural OBJ; no external runtime assets'},indent=2)+'\n')
print('Generated',len(models),'static models; exactly uav_1 and uav_2.')
