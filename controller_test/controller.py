import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class control_node:
    def __init__(self):
        rospy.init_node('controller_node',anonymous=False)
        rospy.Subscriber('/detector_node',Float32MultiArray,self.callback)
        self.pub = rospy.Publisher('u_control',Float32MultiArray,queue_size=10)

        self.pos_y = 0.0
        self.pos_z = 0.0
        self.u_z = 0.0
        self.u_y = 0.0

    def callback(self,data):
        self.pos_y = data.data[0]
        self.pos_z = data.data[1]

    def ros_publish(self):
        msg = Float32MultiArray()
        msg.data = [self.u_y, self.u_z]
        self.pub.publish(msg)
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

            nodo_control.ros_publish()



    except rospy.ROSException as e:
        print(e)






