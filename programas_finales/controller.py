import rospy
from std_msgs.msg import Float32MultiArray
from mavros_msgs.msg import State
from geometry_msgs.msg import TwistStamped

class control_node:
    def __init__(self):
        rospy.init_node('controller_node',anonymous=False)
        rospy.Subscriber('/detector_node',Float32MultiArray,self.callback)
        rospy.Subscriber('/mavros/state',State,self.callback2)
        self.pub = rospy.Publisher('u_control',Float32MultiArray,queue_size=10)
        self.pub2 = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',TwistStamped,queue_size=10)

        self.pos_y = 0.0
        self.pos_z = 0.0
        self.u_z = 0.0
        self.u_y = 0.0
        self.vehicle_mode = "String"

    def callback(self,data):
        self.pos_y = data.data[0]
        self.pos_z = data.data[1]
    
    def callback2(self,data):
        self.vehicle_mode = data.mode


    def ros_publish(self):
        msg = Float32MultiArray()
        msg.data = [self.u_y, self.u_z]
        self.pub.publish(msg)

        msg2 = TwistStamped()
        msg2.twist.linear.y = self.u_y
        msg2.twist.linear.z = self.u_z
        self.pub2.publish(msg2)
#===========================================================
#   Controlador ON-OFF
#-----------------------------------------------------------
#   sp | Set point
#   vp | Variable del proceso
#
class on_off_controller:
    def __init__(self):
        self.sp = 640.0/2.0
        self.vp = 640.0/2.0
        self.u = 0.0
        

    def calcular(self):
        error = 320.0 - self.vp
        negative_error = error <= -50.0 
        positive_error = error >= 50.0 
        if negative_error : self.u = 0.1
        elif positive_error: self.u=-0.1
        else: self.u = 0.0

if __name__ == '__main__':
    nodo_control = control_node()
    y_control = on_off_controller()
    z_control = on_off_controller()

    try:
        while not rospy.is_shutdown():
            y_control.vp = nodo_control.pos_y
            z_control.vp = nodo_control.pos_z

            y_control.calcular()
            z_control.calcular()

            nodo_control.u_y = -y_control.u
            nodo_control.u_z = -z_control.u
            #if nodo_control.vehicle_mode == 'OFFBOARD':

            nodo_control.ros_publish()



    except rospy.ROSException as e:
        print(e)






