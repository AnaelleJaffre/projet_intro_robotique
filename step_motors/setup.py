import pypot.dynamixel
import time

def motors_speed(dxl_io, speed):
    if isinstance(speed, list):
        dxl_io.set_moving_speed({1:speed[0]})
        dxl_io.set_moving_speed({2:speed[1]})   
    else: 
        dxl_io.set_moving_speed({1:speed})
        dxl_io.set_moving_speed({2:-speed})
    
def setup_motors():
    ports = pypot.dynamixel.get_available_ports()
    print(f"ports : {ports}")
    if not ports:
        exit('No port')
    dxl_io = pypot.dynamixel.DxlIO(ports[0])

    dxl_io.set_wheel_mode([1,2])
    #dxl_io.goto_postion(0,2)
    dxl_io.enable_torque([1,2])
    dxl_io.set_moving_speed({1:0})
    dxl_io.set_moving_speed({2:0})
    s = dxl_io.get_moving_speed([1, 2])
    print(s)
    return dxl_io

if __name__ == '__main__':
    setup_motors()