import pypot.dynamixel
import time

def setup_motors():
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('No port')
    dxl_io = pypot.dynamixel.DxlIO(ports[0])

    dxl_io.set_wheel_mode([1,2])
    dxl_io.goto_postion(0,2)
    dxl_io.enable_torque([1,2])
    return dxl_io
    
