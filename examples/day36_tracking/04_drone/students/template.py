import numpy as np

class RobotController:
    def __init__(self, limiter=None):
        self.dt = 0.01
        self.limiter = limiter

    def get_color(self):
        return [1., 0., 0.]

    def reset(self, pos):
        self.xhat = np.zeros(12)

    def run(self, pos, rpy, pos_ring, is_last_ring, pos_others):
        tau_x = 0.
        tau_y = 0.
        tau_z = 0.
        f_z = 0.

        if self.limiter is not None:
            tau_x, tau_y, tau_z, f_z = self.limiter(tau_x, tau_y, tau_z, f_z)

        return tau_x, tau_y, tau_z, f_z
