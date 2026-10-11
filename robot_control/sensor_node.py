import random

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range


class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.publisher = self.create_publisher(Range, '/distance', 10)
        self.timer = self.create_timer(1.0, self.publish_distance)

    def publish_distance(self):
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'robot_sensor'
        msg.radiation_type = Range.INFRARED
        msg.field_of_view = 0.5
        msg.min_range = 0.1
        msg.max_range = 3.0
        msg.range = round(random.uniform(0.1, 3.0), 2)

        self.publisher.publish(msg)
        self.get_logger().info(f'Tavolsag: {msg.range} m')


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
