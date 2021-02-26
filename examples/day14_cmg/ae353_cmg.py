import numpy as np
import pybullet as p
import time
import os
import matplotlib.pyplot as plt

class RobotSimulator:
    def __init__(self, damping=0., dt=0.001, display=True):
        # Choose the time step
        self.dt = dt

        # Connect to and configure pybullet
        self.display = display
        if self.display:
            p.connect(p.GUI)
            p.resetDebugVisualizerCamera(3.5, 50, -35, (0., 0., 0.))
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        else:
            p.connect(p.DIRECT)
        p.setGravity(0, 0, -9.81)
        p.setPhysicsEngineParameter(fixedTimeStep=self.dt, numSubSteps=1)

        # Load plane
        p.loadURDF(os.path.join('.', 'urdf', 'plane.urdf'),
                   baseOrientation=p.getQuaternionFromEuler([0., 0., 0.]))

        # Load robot (with mass and inertia coming from the URDF rather than
        # being recomputed by pybullet)
        self.robot_id = p.loadURDF(os.path.join('.', 'urdf', 'cmg.urdf'),
                                   basePosition=np.array([0., 0., 1.1]),
                                   baseOrientation=p.getQuaternionFromEuler([1.57, 0., 0.]),
                                   flags=(p.URDF_USE_IMPLICIT_CYLINDER  |
                                          p.URDF_USE_INERTIA_FROM_FILE  ))

        # Eliminate linear and angular damping (i.e., a poor model of drag that
        # is applied by default to every link)
        for joint_id in range(p.getNumJoints(self.robot_id)):
            p.changeDynamics(self.robot_id, joint_id, linearDamping=0., angularDamping=0.)

        # Specify maximum applied torque
        self.tau_max = 5.

        # Create a dictionary that maps joint names to joint indices
        self.joint_map = {}
        for joint_index in range(p.getNumJoints(self.robot_id)):
            joint_name = p.getJointInfo(self.robot_id, joint_index)[1].decode('UTF-8')
            self.joint_map[joint_name] = joint_index

        # Create a 1D numpy array with the index (according to bullet) of each joint we care about
        self.joint_names = [
            'world_to_outer',
            'outer_to_inner',
            'inner_to_wheel',
        ]
        self.num_joints = len(self.joint_names)
        self.joint_ids = np.array([self.joint_map[joint_name] for joint_name in self.joint_names])

        # Set damping of joints (i.e., coefficient of viscous friction)
        for id in self.joint_ids:
            p.changeDynamics(self.robot_id, id, jointDamping=damping)

        # Disable velocity control on joints so we can use torque control
        p.setJointMotorControlArray(self.robot_id, self.joint_ids,
                                    p.VELOCITY_CONTROL, forces=np.zeros(self.num_joints))

    def get_sensor_measurements(self):
        q, v = self.get_state()
        return q[0], v[0], q[1], v[1], q[2], v[2]

    def set_actuator_commands(self, tau_gimbal_desired, tau_rotor_desired):
        tau_gimbal = np.clip(tau_gimbal_desired, -self.tau_max, self.tau_max)
        tau_rotor = np.clip(tau_rotor_desired, -self.tau_max, self.tau_max)
        self.set_joint_torque(np.array([0., tau_gimbal, tau_rotor]))
        return tau_gimbal, tau_rotor

    def reset(self, rotor_rpm=100.):
        q = np.zeros(self.num_joints)
        v = np.zeros(self.num_joints)
        v[2] = rotor_rpm * 2 * np.pi / 60
        self.set_state(q, v)

    def get_state(self):
        """
        returns two 1D numpy arrays: joint positions and joint velocities
        """
        joint_states = p.getJointStates(self.robot_id, self.joint_ids)
        q = np.zeros([self.num_joints])
        v = np.zeros_like(q)
        for i in range(self.num_joints):
            q[i] = joint_states[i][0]
            v[i] = joint_states[i][1]
        return q, v

    def set_state(self, q, v=None):
        """
        sets the state to the joint positions and joint velocities that are
        specified by 1D numpy arrays q and (optionally) v, respectively
        """
        if v is None:
            v = np.zeros_like(q)
        for i, joint_id in enumerate(self.joint_ids):
            p.resetJointState(self.robot_id, joint_id, q[i], v[i])
        if self.display:
            p.resetDebugVisualizerCamera(3.5, 50, -35, (0., 0., 0.))

    def set_joint_torque(self, tau):
        """
        sets joint torques (or forces) to the values specified by the 1D numpy
        array tau
        """
        assert(tau.shape[0] == self.num_joints)
        zero_gains = tau.shape[0] * (0.,)
        p.setJointMotorControlArray(self.robot_id, self.joint_ids,
                                    p.TORQUE_CONTROL, forces=tau,
                                    positionGains=zero_gains, velocityGains=zero_gains)

    def step(self, t=None):
        """
        does one step in the simulation
        """
        if self.display:
            if t is None:
                time.sleep(self.dt)
            else:
                time_to_wait = t - time.time()
                while time_to_wait > 0:
                    time.sleep(0.9 * time_to_wait)
                    time_to_wait = t - time.time()
        p.stepSimulation()

    def snapshot(self, filename, width=640, height=480):
        """
        saves image to filename (only works with GUI enabled, i.e., with display=True)
        """
        im = p.getCameraImage(width, height, shadow=True, renderer=p.ER_BULLET_HARDWARE_OPENGL)
        plt.imsave(filename, im[2])
