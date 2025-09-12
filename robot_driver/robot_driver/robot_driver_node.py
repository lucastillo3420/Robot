#Este es el nodo principal que integra todos los módulos

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
import math
from robot_driver.kinematics import Kinematics
from robot_driver.roboclaw_interface import RoboClawInterface
from robot_driver.odometry import RobotOdometry
import tf2_ros
from tf_transformations import quaternion_from_euler


class RobotDriverNode(Node):
    def __init__(self):
        super().__init__('robot_driver_node')
        self.kinematics=Kinematics(wheel_radius=0.06, wheel_base=0.34, axle_distance=0.24)
        self.roboclaw=RoboClawInterface( port_delantero="/dev/ttyACM0", port_trasero="/dev/ttyACM1", buadrate=115200)
        self.odometry=RobotOdometry()
        self.odom_frame='odom'
        self.base_frame ='base_link'
        self.PPR=537.7   # Pulsos por revolución del encoder
        #self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        self.target_v = 0.0
        self.target_omega = 0.0
        self.last_cmd_vel_time = self.get_clock().now()

        #Nos suscribiomos al cmd_vel y publicamos odometria 
        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        self.timer_period = 0.05
        self.timer = self.create_timer(self.timer_period, self.update_loop)
        self.odom_pub = self.create_publisher(Odometry, '/odom/wheel', 10)
        #Comprobamos Bateria de roboclaw
        voltage_real, battery_porcentage=self.roboclaw.ReadVoltage()
        self.get_logger().info(f"Voltaje de la batería principal: {voltage_real} V")
        self.get_logger().info(f"Voltaje de la batería principal: {battery_porcentage} %")
        #Reiniciamos Encoders 
        self.roboclaw.reset_encoders()

        self.last_odom_time = self.get_clock().now()
    
    def cmd_vel_callback(self, msg):
        """Callback para comandos de velocidad."""
        self.target_v = msg.linear.x
        self.target_omega = msg.angular.z
        self.last_cmd_vel_time = self.get_clock().now()

    def update_loop(self):
        # Medida de seguridad: si no recibimos cmd_vel en un tiempo, paramos el robot.
        current_time = self.get_clock().now()
        if (current_time - self.last_cmd_vel_time).nanoseconds / 1e9 > 0.5: # 0.5 segundos de timeout
            self.target_v = 0.0
            self.target_omega = 0.0

        # Mover el robot con la velocidad guardada
        self.move_robot(self.target_v, self.target_omega)
        
        #self.roboclaw.check_status()

        # Actualizar y publicar la odometría de forma constante
        self.update_and_publish_odometry(current_time)

    def rads_to_pps(self, rads):
        """Convierte radianes por segundo (rad/s) a pulsos por segundo (PPS)."""
        return int((rads * self.PPR) / (2 * math.pi))
    
    def pps_to_rads(self, pps):
        """Convierte pulsos por segundo (PPS) a radianes por segundo (rad/s)."""
        return (pps * 2 * math.pi) / self.PPR


    def move_robot(self, v, omega):
        """Mueve el robot usando cinemática inversa y RoboClaw."""
        omega1, omega2, omega3, omega4 = self.kinematics.inverse_kinematics(v, omega)

        # Convertir velocidades de ruedas de rad/s a PPS
        front_left_pps = self.rads_to_pps(omega1)
        front_right_pps = self.rads_to_pps(omega2)
        rear_left_pps = self.rads_to_pps(omega3)
        rear_right_pps = self.rads_to_pps(omega4)
        # Enviar velocidades a las controladoras RoboClaw
        self.roboclaw.set_wheel_speed(front_left_pps, front_right_pps, rear_left_pps, rear_right_pps)
    def update_and_publish_odometry(self, current_time):
        #leer encoders
        encoder_D1, encoder_D2, encoder_T1, encoder_T2= self.roboclaw.read_encoders_speed()
        #Convertir velocidades de ruedas de rad/s a PPS
        omega1_real = self.pps_to_rads(encoder_D1)
        omega2_real = self.pps_to_rads(encoder_D2)
        omega3_real = self.pps_to_rads(encoder_T1)
        omega4_real = self.pps_to_rads(encoder_T2)
        # Cinemática directa: calcular v_real y omega_real
        v_real_calculada, omega_real_calculada = self.kinematics.direct_kinematics(omega1_real, omega2_real, omega3_real, omega4_real)
        
    
        #Calcular dt (tiempo transcurrido)
        dt=(current_time-self.last_odom_time).nanoseconds/1e9
        self.last_odom_time=current_time
        if dt <= 0: # Evitar división por cero o dt negativo si hay saltos de tiempo
                self.get_logger().warn("dt <= 0, saltando actualización de odometría")
                return
        


        self.odometry.update(v_real_calculada, omega_real_calculada, dt)
        #crear y pblicar Transformaciones TF(odom->base_link)
        
       # t=TransformStamped()
       # t.header.stamp=current_time.to_msg()
       # t.header.frame_id=self.odom_frame
        #t.child_frame_id=self.base_frame

        #Posicion
       # t.transform.translation.x=self.odometry.x
      # t.transform.translation.y=self.odometry.y
        #t.transform.translation.z=0.0#robot plano

        #orientacion
        q=quaternion_from_euler(0,0,self.odometry.theta)
        #t.transform.rotation.x=q[0]
       # t.transform.rotation.y=q[1]
       # t.transform.rotation.z=q[2]
       # t.transform.rotation.w=q[3]
        #enviar transformacion
       # self.tf_broadcaster.sendTransform(t)
        
        # Publicar odometría
        odom_msg = Odometry()
        odom_msg.header.stamp=current_time.to_msg()
        odom_msg.header.frame_id=self.odom_frame
        odom_msg.child_frame_id=self.base_frame
        #posicion y orientacion
        odom_msg.pose.pose.position.x = self.odometry.x
        odom_msg.pose.pose.position.y = self.odometry.y
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]

        odom_msg.twist.twist.linear.x = v_real_calculada
        odom_msg.twist.twist.linear.y = 0.0 # No movimiento lateral
        odom_msg.twist.twist.angular.z = omega_real_calculada

        self.odom_pub.publish(odom_msg)
    
def main(args=None):
    rclpy.init(args=args)
    node = RobotDriverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


        
