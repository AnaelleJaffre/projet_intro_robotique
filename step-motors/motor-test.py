import pypot.dynamixel
import time

ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1])

pos = dxl_io.get_present_position({1,2})
print(dxl_io.dxl_to_degrees(pos[1]), dxl_io.dxl_to_degrees(pos[2]))

dxl_io.set_moving_speed({1: 550}) 
dxl_io.set_moving_speed({2: 50})

time.sleep(1)

dxl_io.set_moving_speed({1: 0})
dxl_io.set_moving_speed({2: 0})

print(dxl_io.get_present_position({1,2}))

dxl_io.close()