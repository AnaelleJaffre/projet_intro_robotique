import time

from image_processing.shape_rendering import shape_rendering
from step_motors import setup, odom

## DEBUG ##
DEBUG = 0 # 1 to enable debug_print 0 to deactivate
def debug_print(message):
    if DEBUG:
        print(message)


f_ech = 100
rob_poses = []
if __name__ == '__main__':
    #Setup
    dxl_io = setup.setup_motors()
    dxl_io.disable_torque({1:0, 2:0})
    t_start = time.time()
    while time.time() - t_start < 10:
        x, y, theta = odom.get_odom(f_ech, dxl_io)
        rob_poses.append((x, y, "r"))
        debug_print("{:.2f}, {:.2f}, {:.2f}".format(x, y, theta))
        time.sleep(1/f_ech)

    shape_rendering(rob_poses)

