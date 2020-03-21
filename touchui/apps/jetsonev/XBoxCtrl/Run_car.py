from JetsonEV import JetsonEV
import time
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser(description='Activate the JetsonEV for use with an XBox 360 Controller.')
    parser.add_argument('--enable-imu', action='store_true', help='enable the IMU')
    parser.add_argument('--enable-lidar', action='store_true', help='enable the Lidar Sensor')
    parser.add_argument('--enable-camera', action='store_true', help='enable the Camera')
    args, unknown = parser.parse_known_args()

    imu = args.enable_imu
    camera = args.enable_camera
    lidar = args.enable_lidar

    car = JetsonEV(mode='xbox', initialize_camera=camera, initialize_lidar=lidar, max_speed_limit=0.30)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Exited')
    quit()
