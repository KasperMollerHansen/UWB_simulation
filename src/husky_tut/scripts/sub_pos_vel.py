import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion

def callback(data):
    pub_pos.publish(data.pose.pose.position)
    pub_q.publish(data.pose.pose.orientation)
    
    
def listener():
    rospy.init_node('listener', anonymous=True)

    sub = rospy.Subscriber('odometry/filtered', Odometry, callback)
    global pub_pos
    global pub_q
    pub_pos = rospy.Publisher('/husky_position', Point, queue_size=1)
    pub_q = rospy.Publisher('/husky_q_pos', Quaternion, queue_size=1)
    rate = rospy.Rate(2)
    pos = Point()
    q_pos = Quaternion()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
