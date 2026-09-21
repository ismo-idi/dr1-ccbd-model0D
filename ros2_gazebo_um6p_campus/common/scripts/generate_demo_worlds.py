#!/usr/bin/env python3
"""Generate standalone demonstration worlds; never edit the paused world/assets."""
from pathlib import Path
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
for wave in (1,2):
    slug='demo_1_no_obstacle' if wave==1 else 'demo_2_static_sphere'
    pkg=root/f'demo/{slug}/src/um6p_demo_{wave}'
    routes=(pkg/'config/routes.txt').read_text().splitlines()
    assert len(routes)==2
    for line in routes: assert len(line.split())%3==0 and all(__import__('math').isfinite(float(x)) for x in line.split())
    tree=ET.parse(root/'campus_environment/src/um6p_campus_description/worlds/campus.sdf')
    world=tree.getroot().find('world'); world.set('name','um6p_demo')
    physics=ET.SubElement(world,'physics',name='kinematic_clock',type='ignored')
    ET.SubElement(physics,'max_step_size').text='0.02'
    ET.SubElement(physics,'real_time_factor').text='1'
    plugin=ET.SubElement(world,'plugin',filename='CampusKinematics',name='campus::Kinematics')
    ET.SubElement(plugin,'wave').text=str(wave)
    for i,line in enumerate(routes,1): ET.SubElement(plugin,f'route_{i}').text=line
    for inc in world.findall('include'):
        if inc.findtext('name').startswith('uav_'):
            ET.SubElement(inc,'static').text='false'
    pads=ET.SubElement(world,'model',name='landing_pads')
    ET.SubElement(pads,'static').text='true'; link=ET.SubElement(pads,'link',name='body')
    for i,x in enumerate((-3.6,3.6)):
        visual=ET.SubElement(link,'visual',name=f'pad_{i}')
        ET.SubElement(visual,'pose').text=f'{x} -40 .06 0 0 0'
        geom=ET.SubElement(visual,'geometry'); cyl=ET.SubElement(geom,'cylinder')
        ET.SubElement(cyl,'radius').text='1.2';ET.SubElement(cyl,'length').text='.12'
        mat=ET.SubElement(visual,'material')
        for tag in ('ambient','diffuse'): ET.SubElement(mat,tag).text='.13 .15 .17 1'
    apron=ET.SubElement(world,'model',name='demo_apron')
    ET.SubElement(apron,'static').text='true'
    link=ET.SubElement(apron,'link',name='body')
    visual=ET.SubElement(link,'visual',name='paving')
    ET.SubElement(visual,'pose').text='0 -35 -.15 0 0 0'
    ET.SubElement(ET.SubElement(ET.SubElement(visual,'geometry'),'box'),'size').text='26 20 .3'
    mat=ET.SubElement(visual,'material')
    for field in ('ambient','diffuse'):ET.SubElement(mat,field).text='.60 .55 .44 1'
    if wave==2:
        ball=ET.SubElement(world,'model',name='static_sphere')
        ET.SubElement(ball,'static').text='true'
        ET.SubElement(ball,'pose').text='0 -22 2.4 0 0 0'
        link=ET.SubElement(ball,'link',name='body')
        for tag in ('visual','collision'):
            element=ET.SubElement(link,tag,name='sphere')
            ET.SubElement(ET.SubElement(ET.SubElement(element,'geometry'),'sphere'),'radius').text='2.4'
            if tag=='visual':
                mat=ET.SubElement(element,'material')
                for field in ('ambient','diffuse'):ET.SubElement(mat,field).text='.65 .07 .06 1'
    ET.indent(tree);tree.write(pkg/'worlds/demo.sdf',encoding='utf-8',xml_declaration=True)
print('Generated wave1.sdf and wave2.sdf; original campus world unchanged.')
