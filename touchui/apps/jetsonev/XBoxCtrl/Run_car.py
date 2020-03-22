from JetsonEV import JetsonEV, NumpySocket
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

    # initialize car
    car = JetsonEV(mode='xbox', initialize_camera=camera, initialize_lidar=lidar, max_speed_limit=0.30)

    # add sockets for touch app for requested car features
    if imu:
        imu_socket = NumpySocket(tcp_port=9009)

        def new_forwarding_function(values):
            imu_socket.send_data(values)
        car.imu.forwarding_function = new_forwarding_function
        car._output_sockets.append(imu_socket)
        imu_socket.thread.start()

    if camera:
        print('making camera socket')
        camera_socket = NumpySocket(tcp_port=9011)
        old_fwd_func = car.camera.forwarding_function

        def new_forwarding_function(values):
            old_fwd_func(values)
            camera_socket.send_data(values)
        car.camera.forwarding_function = new_forwarding_function
        car._output_sockets.append(camera_socket)
        camera_socket.thread.start()

    if lidar:
        lidar_socket = NumpySocket(tcp_port=9010)
        old_fwd_func = car.lidar.forwarding_function

        def new_forwarding_function(values):
            old_fwd_func(values)
            lidar_socket.send_data(values)

        car.lidar.forwarding_function = new_forwarding_function
        car._output_sockets.append(lidar_socket)
        lidar_socket.thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Exited')
    quit()
