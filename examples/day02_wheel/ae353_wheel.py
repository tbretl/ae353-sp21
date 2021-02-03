import numpy as np
import pybullet as p
import time
import os

class RobotSimulator:
    def __init__(self, damping=0.):
        # Choose the time step
        self.dt = 0.01

        # Connect to and configure pybullet
        p.connect(p.GUI)
        p.setGravity(0, 0, -9.81)
        p.setPhysicsEngineParameter(fixedTimeStep=self.dt, numSubSteps=1)

        # Define the camera view
        p.resetDebugVisualizerCamera(2.0, 50, -35, (0., 0., 0.))

        # Disable the GUI controller
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

        # Load plane
        p.loadURDF(os.path.join('.', 'urdf', 'plane.urdf'))

        # Load robot (with mass and inertia coming from the URDF rather than
        # being recomputed by pybullet)
        self.robot_id = p.loadURDF(os.path.join('.', 'urdf', 'wheel.urdf'),
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
        for joint_id in range(p.getNumJoints(self.robot_id)):
            joint_name = p.getJointInfo(self.robot_id, joint_id)[1].decode('UTF-8')
            self.joint_map[joint_name] = joint_id

        # Create a 1D numpy array with the index (according to bullet) of each joint we care about
        self.joint_names = [
            'base_to_wheel',
        ]
        self.num_joints = len(self.joint_names)
        self.joint_ids = np.array([self.joint_map[joint_name] for joint_name in self.joint_names])

        # Set damping of these joints (i.e., coefficient of viscous friction) to given value
        for id in self.joint_ids:
            p.changeDynamics(self.robot_id, id, jointDamping=damping)

        # Disable velocity control on joints so we can use torque control
        p.setJointMotorControlArray(self.robot_id, self.joint_ids,
                                    p.VELOCITY_CONTROL, forces=np.zeros(self.num_joints))

    def get_sensor_measurements(self):
        """
        returns two numbers: joint angle and joint velocity
        """
        q, v = self.get_state()
        return q[0], v[0]

    def set_actuator_commands(self, tau_desired):
        """
        sets the applied torque to the number given by tau, clipped to bounds
        """
        tau = np.clip(tau_desired, -self.tau_max, self.tau_max)
        self.set_joint_torque(np.array([tau]))
        return tau

    def reset(self):
        """
        sets both the joint angle and joint velocity to zero
        """
        self.set_state(np.array([0.]), np.array([0.]))

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

    def step(self):
        """
        does one step in the simulation
        """
        time.sleep(self.dt)
        p.stepSimulation()
