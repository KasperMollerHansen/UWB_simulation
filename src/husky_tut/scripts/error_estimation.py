import rospy
from numpy import array
from numpy.linalg import norm
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseStamped
from husky_tut.msg import Error

def callback_odom(data):
    global odom_pos
    odom_pos = array([data.pose.pose.position.x,data.pose.pose.position.y])  

def callback_kal(data):
    global kal_pos
    kal_pos = array([data.pose.position.x,data.pose.position.y])    

def callback_sqr(data):
    global sqr_pos
    sqr_pos = array([data.pose.position.x,data.pose.position.y])

def callback_gt(data):
    global gt_pos
    global error
    gt_pos = array([data.pose.pose.position.x, data.pose.pose.position.y])
    #print('odom = ',odom_pos)
    #print('kalman = ',kal_pos)
    #print('sqr = ',sqr_pos)
    try:
        error.odom = norm(gt_pos-odom_pos)
        error.kalman = norm(gt_pos-kal_pos)
        error.sqr = norm(gt_pos-sqr_pos)
    except NameError:
        pass
    pub.publish(error)
    
    

    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    global odom_pos
    global kal_pos
    global sqr_pos
    global gt_pos
    global error
    error = Error()
    sub_odom = rospy.Subscriber('odometry/filtered', Odometry, callback_odom)
    sub_kal = rospy.Subscriber('localization_data_topic', PoseStamped, callback_kal)
    sub_sqr = rospy.Subscriber('localization_data_topic_sqr', PoseStamped, callback_sqr)
    sub_gt = rospy.Subscriber('husky_ground_truth', Odometry, callback_gt)

    global pub
    pub = rospy.Publisher('/husky_error', Error, queue_size=5)
    rate = rospy.Rate(50)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()