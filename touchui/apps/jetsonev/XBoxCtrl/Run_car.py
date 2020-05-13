from JetsonEV import JetsonEV
from DataSocket import SendSocket
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
    car = JetsonEV(mode=JetsonEV.xbox_direct_mode,
                   initialize_imu=imu,
                   initialize_camera=camera,
                   initialize_lidar=lidar,
                   max_speed_limit=1,
                   max_duty_cycle=0.15,
                   rc_communication=1,
                   rc_control=JetsonEV.ARDUINO_CONTROL)

    speed_socket = SendSocket(tcp_port=4021)
    speed_old_fwd_func = car.motor_encoder.forwarding_function

    def speed_forwarding_function(values):
        speed_old_fwd_func(values)
        speed_socket.send_data(car.speed)

    car.motor_encoder.forwarding_function = speed_forwarding_function
    car._output_sockets.append(speed_socket)
    speed_socket.thread.start()

    # add sockets for touch app for requested car features
    if imu:
        imu_socket = SendSocket(tcp_port=9009)

        def imu_new_forwarding_function(values):
            imu_socket.send_data({'accel': values[0], 'gyro': values[1]})
        car.imu.forwarding_function = imu_new_forwarding_function
        car._output_sockets.append(imu_socket)
        imu_socket.thread.start()

    if camera:
        print('making camera socket')
        camera_socket = SendSocket(tcp_port=9011)
        cam_old_fwd_func = car.camera.forwarding_function

        def cam_new_forwarding_function(values):
            cam_old_fwd_func(values)
            camera_socket.send_data(values)
        car.camera.forwarding_function = cam_new_forwarding_function
        car._output_sockets.append(camera_socket)
        camera_socket.thread.start()

    if lidar:
        lidar_socket = SendSocket(tcp_port=9010)
        lidar_old_fwd_func = car.lidar.forwarding_function

        def lidar_new_forwarding_function(values):
            lidar_old_fwd_func(values)
            lidar_socket.send_data(values)

        car.lidar.forwarding_function = lidar_new_forwarding_function
        car._output_sockets.append(lidar_socket)
        lidar_socket.thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Exited')
    quit()
