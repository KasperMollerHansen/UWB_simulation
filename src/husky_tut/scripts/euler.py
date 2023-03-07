import rospy
from math import atan2, sqrt, pi
from nav_msgs.msg import Odometry
from husky_tut.msg import Euler 

def callback(data):
#    rospy.loginfo("position [x, y, z] = %s", data.pose.pose.position)
    q_w = data.pose.pose.orientation.w
    q_x = data.pose.pose.orientation.x
    q_y = data.pose.pose.orientation.y
    q_z = data.pose.pose.orientation.z

    #roll (x-axis rotation)
    sinr_cosp = 2*(q_w*q_x+q_y*q_z)
    cosr_cosp = 1- 2*(q_x*q_x+q_y*q_y)
    eul.roll = atan2(sinr_cosp,cosr_cosp)

    #pitch (y-axis rotation)
    sinp = sqrt(1+2*(q_w*q_y-q_x*q_z))
    cosp = sqrt(1+2*(q_w*q_y-q_x*q_z))
    eul.pitch = 2*atan2(sinp,cosp)- pi/2

    #yaw (z-axis rotation)
    siny_cosp = 2*(q_w*q_z+q_x*q_y)
    cosy_cosp = 1-2*(q_y*q_y+q_z*q_z)
    eul.yaw = atan2(siny_cosp,cosy_cosp)

    pub.publish(eul)
    
    
def listener():
    rospy.init_node('listener', anonymous=True)

    sub = rospy.Subscriber('odometry/filtered', Odometry, callback)
    global pub
    global eul
    eul = Euler()
    pub = rospy.Publisher('/husky_euler', Euler, queue_size=1)
    rate = rospy.Rate(2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
