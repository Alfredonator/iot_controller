#! /usr/bin/env python

import sys
import rospy
import moveit_commander
import geometry_msgs.msg
import std_msgs
from std_msgs.msg import Bool, String

class iot_controller:
    arm_group = None
    
    def __init__(self):
        self.robot = moveit_commander.RobotCommander()
        self.arm_group = moveit_commander.MoveGroupCommander("edo")
        rospy.logwarn("before sub")
	self.robot_operation_consumer = rospy.Subscriber("/robot_operation", String, self.edo_operations, queue_size=10)
	rospy.logwarn("after sub")

    def edo_operations(self, action):
        if action.data == "stop":
            rospy.loginfo("stoping the robot operation")
	    self.arm_group.stop()
        elif action.data == "start":
	    rospy.loginfo("removing stop, allowing eDO to move again")	
        elif action.data == "home":
            self.home_position()
            rospy.loginfo("sending eDO to candle position")
	else: 
	    rospy.logwarn("undefined message")

    def home_position(self):
        self.arm_group.set_named_target("candle")
        self.arm_group.go()
    

def main(args):
    moveit_commander.roscpp_initialize(sys.argv)
    iot_controller()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    rospy.init_node('ball_grasper', anonymous=True)
    rospy.logwarn("Starting iot controller node")
    main(sys.argv)
rospy.sleep(5)
moveit_commander.roscpp_shutdown()
