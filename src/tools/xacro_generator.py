#!/usr/bin/env python3

#Define joints, links, properties, etc for a ROS2 robot and output both a xacro & urdf

import os

def create_header(outfile, robot_name, properties):
    text = '''<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="{}">'''.format(robot_name)

    for prop in properties:
        text += '''\n<xacro:property name="{}" value="{}"/>'''.format(prop, properties[prop])
    text += '''\n\n<link name="world"/>
<joint name="world_joint" type="fixed">
  <parent link="world"/>
  <child link="torso_lower"/>
  <origin rpy="0 0 0" xyz="0 0 0"/>
</joint>


    '''
    outfile.write(text)
    return(text)



def create_link(outfile, link_name, color):
    text = '''<link name="{}">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry>
          <mesh filename="{}" scale="1 1 1"/>
        </geometry>
    '''.format(link_name, '${' + link_name + '_mesh' + '}')

    if color != 'None':
      text += '''
        <material name="{}"/>
        <color rgba="{}"/>
    '''.format(color, '${' + color + '}')
      
    text += '''      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry>
          <mesh filename="{}" scale="1 1 1"/>
        </geometry>
      </collision>
</link>'''.format('${' + link_name + '_mesh' + '}')
    
    outfile.write(text)
    return(text)

def create_joint(outfile, joint_name, parent, child, ox, oy, oz, ax, ay, az, limit_lower, limit_upper, joint_type, effort, velocity):
    text = '''<joint name="{}" type="{}">
      <parent link="{}"/>
      <child link = "{}"/>
      <origin xyz="{} {} {}" rpy="0 0 0"/>
      <axis xyz="{} {} {}"/>
      <limit lower="{}" upper="{}" effort="{}" velocity="{}"/>
</joint>'''.format(joint_name, joint_type, parent, child, ox, oy, oz, ax, ay, az, limit_lower, limit_upper, effort, velocity)
    outfile.write(text)
    return(text)


#START EDITING HERE
def run():
  mesh_type = 'OBJ' #OBJ or STL
  output_location = '/home/username/my_ws/src/my_robot/src/my_robot_desc' #xacro destination in description folder
  robot_name = 'my_robot'

  v = 1 #joint angular velocity
  effort = 1 #joint effort

  #{joint_name:[joint_name, parent, child, origin x, origin y, origin z, axis x, axis y, axis z, limit_lower, limit_upper, joint_type, effort, velocity]}
  joints = {'spine_x':['spine_x', 'torso_lower', 'torso_mid', 0, 0, 0, 1, 0, 0, 0, .22, 'revolute', effort, v],     #joint examples
          'spine_z':['spine_z', 'torso_mid', 'torso_upper', 0, 0, .1, 0, 0, 1, -.22, .22, 'revolute', effort, v]
          }

  #Define link names (and stl colors)
  if mesh_type == 'STL':                                                         
    links = {'torso_lower':'Black',
            'torso_mid':'Black',
            'torso_upper':'Black'
            }
  elif mesh_type == 'OBJ':
     links = {'torso_lower':'None',
            'torso_mid':'None',
            'torso_upper':'None'
            }    

  properties = {'torso_lower_mesh':'file://{}/{}/torso_lower.{}'.format(output_location, mesh_type, mesh_type.lower()),
                'torso_mid_mesh':'file://{}/{}/torso_mid.{}'.format(output_location, mesh_type, mesh_type.lower()),
                'torso_upper_mesh':'file://{}/{}/torso_upper.{}'.format(output_location, mesh_type, mesh_type.lower()),
                'Black':'0.0 0.0 0.0 1.0'}

  
  with open('{}/my_robot.urdf.xacro'.format(output_location), 'w') as outfile:
    header_text = create_header(outfile, robot_name, properties)
    outfile.write('\n\n')
    for link in links:
        link_text = create_link(outfile, link, links[link])
        outfile.write('\n')
    outfile.write('\n')
    for joint in joints:    
        joint_text = create_joint(outfile, *joints[joint]) # unpack value
        outfile.write('\n')
    outfile.write('\n</robot>')
    print('header_text:{}'.format(header_text))
    print('link_text:{}'.format(link_text))
    print('joint_text:{}'.format(joint_text))
  os.system('ros2 run xacro xacro {}/my_robot.urdf.xacro > {}/my_robot.urdf'.format(output_location, output_location)) #generate urdf from xacro

run()
