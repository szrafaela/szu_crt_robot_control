import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import String


class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')
        self.subscription = self.create_subscription(
            Range, '/distance', self.distance_callback, 10
        )
        self.publisher = self.create_publisher(String, '/robot_status', 10)

    def distance_callback(self, msg):
        status = String()

        if msg.range < 0.5:
            status.data = 'STOP'
        elif msg.range <= 1.0:
            status.data = 'SLOW DOWN'
        else:
            status.data = 'FORWARD'

        self.publisher.publish(status)
        self.get_logger().info(
            f'Tavolsag: {msg.range:.2f} m -> Allapot: {status.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
