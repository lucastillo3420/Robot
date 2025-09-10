#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import time

class RobotTesterNode(Node):
    def __init__(self):
        super().__init__('robot_tester_node')
        
        # Solo publicamos goals, NO cmd_vel
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)
        
        # Parameters
        self.declare_parameter('goal_x', 1.0)
        self.declare_parameter('goal_y', 0.0)
        
        self.get_logger().info("🚗 Robot Tester Node iniciado")
        self.get_logger().info("🎯 Enviará un solo goal y se detendrá")
        
        # Enviar goal después de 2 segundos
        self.timer = self.create_timer(2.0, self.send_test_goal)
        self.goal_sent = False

    def send_test_goal(self):
        if self.goal_sent:
            return
            
        # Get parameters
        goal_x = self.get_parameter('goal_x').value
        goal_y = self.get_parameter('goal_y').value
        
        self.get_logger().info(f"🎯 Enviando goal a: ({goal_x}, {goal_y})")
        
        # Enviar el goal
        goal_msg = PoseStamped()
        goal_msg.header.stamp = self.get_clock().now().to_msg()
        goal_msg.header.frame_id = 'odom'
        goal_msg.pose.position.x = goal_x
        goal_msg.pose.position.y = goal_y
        goal_msg.pose.orientation.w = 1.0
        
        self.goal_pub.publish(goal_msg)
        
        self.goal_sent = True
        self.timer.cancel()  # Detener el timer
        
        # Esperar un poco y luego shutdown limpio
        self.shutdown_timer = self.create_timer(1.0, self.clean_shutdown)

    def clean_shutdown(self):
        self.get_logger().info("✅ Goal enviado. Apagando nodo...")
        self.shutdown_timer.cancel()
        raise KeyboardInterrupt  # Shutdown limpio

def main(args=None):
    rclpy.init(args=args)
    node = RobotTesterNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("⏹️  Apagado limpio")
    except Exception as e:
        node.get_logger().error(f"❌ Error: {e}")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
