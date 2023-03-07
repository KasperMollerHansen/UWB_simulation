from math import atan2, sqrt, pi
from numpy import cos, sin, dot, array

def quat2eul(q_w,q_x,q_y,q_z):
    #roll (x-axis rotation)
    sinr_cosp = 2*(q_w*q_x+q_y*q_z)
    cosr_cosp = 1 - 2*(q_x*q_x+q_y*q_y)
    roll = atan2(sinr_cosp,cosr_cosp)

    #pitch (y-axis rotation)
    sinp = sqrt(1+2*(q_w*q_y-q_x*q_z))
    cosp = sqrt(1+2*(q_w*q_y-q_x*q_z))
    pitch = 2*atan2(sinp,cosp)- pi/2

    #yaw (z-axis rotation)
    siny_cosp = 2*(q_w*q_z+q_x*q_y)
    cosy_cosp = 1-2*(q_y*q_y+q_z*q_z)
    yaw = atan2(siny_cosp,cosy_cosp)
    return roll, pitch, yaw

def tf_eul(roll, pitch, yaw):
    #Transformation matrix 
    #(around x-axis)
    trans_x = array([[1, 0, 0],[0, cos(roll), sin(roll)],[0, -sin(roll), cos(roll)]])
    #(around y-axis)
    trans_y = array([[cos(pitch), 0, -sin(pitch)],[0, 1, 0],[sin(roll), 0, cos(roll)]])
    #(around z-axis)
    trans_z = array([[cos(yaw), sin(yaw),0],[-sin(yaw), cos(yaw), 0],[0, 0, 1]])
    #creating position transformation matrix for all three axis
    tf_matrix = dot(dot(trans_x, trans_y),trans_z)

    return tf_matrix

def coord_trans_eul(frame_pos,frame_ori,point_pos,point_ori):
    #calculating orientation of point w.r.t new frame
    pose_ori = point_ori- frame_ori
    #new orientation
    ori = [[pose_ori[0]],[pose_ori[1]],[pose_ori[2]]]
    #transformation matrix
    tf_matrix = tf_eul(frame_ori[0], frame_ori[1], frame_ori[2])
    #calculating position of point in body frame
    pose_pos = dot(tf_matrix,(point_pos-frame_pos))
    #new position
    pos = [[pose_pos[0]],[pose_pos[1]],pose_pos[2]]
    
    #transforming orientation to quaternion
    cr = cos(pose_ori[0] * 0.5)
    sr = sin(pose_ori[0] * 0.5)
    cp = cos(pose_ori[1] * 0.5)
    sp = sin(pose_ori[1] * 0.5)
    cy = cos(pose_ori[2] * 0.5)
    sy = sin(pose_ori[2] * 0.5)
    #new quaternion
    q_w = cr * cp * cy + sr * sp * sy
    q_x = sr * cp * cy - cr * sp * sy
    q_y = cr * sp * cy + sr * cp * sy
    q_z = cr * cp * sy - sr * sp * cy
    quat = [[q_w],[q_x],[q_y],[q_z]]

    return pos, ori, quat
    