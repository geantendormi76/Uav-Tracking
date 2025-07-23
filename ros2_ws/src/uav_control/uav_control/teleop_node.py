# Uav-Tracking/ros2_ws/src/uav_control/uav_control/teleop_node.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TeleopNode(Node):
    """
    一个简单的遥控节点，用于发布无人机起飞指令。
    该节点完全解耦，不知道仿真环境的存在。
    """
    def __init__(self):
        super().__init__('teleop_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.timer_callback) # 每秒执行一次
        self.start_time = time.time()
        self.get_logger().info('Teleop node started. Publishing takeoff command for 5 seconds...')

    def timer_callback(self):
        elapsed_time = time.time() - self.start_time
        
        msg = Twist()
        
        if elapsed_time <= 5.0:
            # 在前5秒内，发布一个向上的速度指令 (0.5 m/s)
            msg.linear.z = 0.5
            self.publisher_.publish(msg)
            self.get_logger().info(f'Publishing: linear.z = {msg.linear.z}')
        else:
            # 5秒后，发布悬停指令并关闭节点
            msg.linear.z = 0.0
            self.publisher_.publish(msg)
            self.get_logger().info('5 seconds elapsed. Publishing hover command and shutting down.')
            self.destroy_timer(self.timer) # 停止定时器
            # 稍微延迟后关闭，确保最后一条消息发出
            self.create_timer(1.0, lambda: self.destroy_node())

def main(args=None):
    rclpy.init(args=args)
    teleop_node = TeleopNode()
    try:
        rclpy.spin(teleop_node)
    except KeyboardInterrupt:
        pass
    finally:
        # 确保在退出时销毁节点
        if rclpy.ok():
            teleop_node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()