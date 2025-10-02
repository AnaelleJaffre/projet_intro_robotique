import pypot.dynamixel
import time

## DEBUG ##
DEBUG = 0 # 1 to enable debug_print 0 to deactivate
def debug_print(message):
    if DEBUG:
        print(message)


ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1,2])
dxl_io.enable_torque([1,2])
debug_print(dxl_io.get_present_position({1,2}))

dxl_io.set_moving_speed({1: 400}) 
dxl_io.set_moving_speed({2: -400})

time.sleep(2)

dxl_io.set_moving_speed({1: 0})
dxl_io.set_moving_speed({2: 0})

debug_print(dxl_io.get_present_position({1,2}))

dxl_io.close()