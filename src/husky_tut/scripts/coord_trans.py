import rospy
import sys
sys.path.append('/Desktop/functions/robo_func')
from math import pi
from numpy import array
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from husky_tut.msg import Euler 
from husky_tut.robo_func import quat2eul, coord_trans_eul

def callback(data):
    #observed point location in world frame
    point_pos = array([[2],[3],[0]])
    point_ori= array([[0],[0],[pi/2]])
    
    #loading position and orientation of Husky
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    z = data.pose.pose.position.z
    pose_odom = array([[x],[y],[z]])
    q_w = data.pose.pose.orientation.w
    q_x = data.pose.pose.orientation.x
    q_y = data.pose.pose.orientation.y
    q_z = data.pose.pose.orientation.z

    #quaternion to euler
    roll, pitch, yaw = quat2eul(q_w,q_x,q_y,q_z)
    ori_odom = [[roll],[pitch],[yaw]]
    #calculating position and orientation of point in new frame
    pos_new, ori_new, quat_new = coord_trans_eul(pose_odom,ori_odom,point_pos,point_ori)

    #saving pose of point in new frame
    eul.roll = ori_new[0]
    eul.pitch = ori_new[1]
    eul.yaw = ori_new[2]
    pos.position.x = pos_new[0]
    pos.position.y = pos_new[1]
    pos.position.z = pos_new[2]
    pos.orientation.w = quat_new[0]
    pos.orientation.x = quat_new[1]
    pos.orientation.y = quat_new[2]
    pos.orientation.z = quat_new[3]
    
    #publish position
    pub_frame.publish(pos)
    pub_eul.publish(eul)
    
    
def listener():
    rospy.init_node('listener', anonymous=True)

    sub = rospy.Subscriber('odometry/filtered', Odometry, callback)
    global pub_frame
    global pub_eul
    global pos
    global eul
    pos = Pose()
    eul = Euler()
    pub_frame = rospy.Publisher('/husky_body_frame', Pose, queue_size=1)
    pub_eul = rospy.Publisher('/husky_body_eul', Euler, queue_size=1)
    rate = rospy.Rate(2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
