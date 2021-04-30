import numpy as np

class RobotController:
    def __init__(self, limiter=None):
        self.dt = 0.01
        self.limiter = limiter

        self.r_old = 0.
        self.p_old = 0.
        self.y_old = 0.

    def get_color(self):
        return [0., 1., 0.]

    def reset(self, pos):
        self.xhat = np.zeros(12)

    def run(self, pos, rpy, pos_ring, is_last_ring, pos_others):
        r = rpy[0]
        p = rpy[1]
        y = rpy[2]

        rdot = (r - self.r_old) / self.dt
        pdot = (p - self.p_old) / self.dt
        ydot = (y - self.y_old) / self.dt

        self.r_old = r
        self.p_old = p
        self.y_old = y

        tau_x = - 1. * (r - 0) - 0.1 * (rdot - 0)
        tau_y = - 1. * (p - 0) - 0.1 * (pdot - 0)
        tau_z = - 1. * (y - 0) - 0.1 * (ydot - 0)


        f_z = 0.5 * 9.81

        if self.limiter is not None:
            tau_x, tau_y, tau_z, f_z = self.limiter(tau_x, tau_y, tau_z, f_z)

#         print(f'{tau_x}, {tau_y}, {tau_z}, {f_z}')
#         raise Exception('stop')

        return tau_x, tau_y, tau_z, f_z
