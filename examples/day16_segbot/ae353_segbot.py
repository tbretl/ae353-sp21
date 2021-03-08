import numpy as np
import pybullet as p
import time
import os
import matplotlib.pyplot as plt

class RobotSimulator:
    def __init__(self, damping=0., dt=0.01, display=True):
        # Choose the time step
        self.dt = dt

        # Define parameters
        self.track_radius = 10.
        self.wheel_radius = 0.325
        self.wheel_base = 0.7
        self.turn_left = False
        self.camera_chase_yaw = None

        # Connect to and configure pybullet
        self.display = display
        if self.display:
            p.connect(p.GUI)
            self.camera_sideview()
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        else:
            p.connect(p.DIRECT)
        p.setGravity(0, 0, -9.81)
        p.setPhysicsEngineParameter(fixedTimeStep=self.dt,
                                    numSubSteps=1,
                                    restitutionVelocityThreshold=0.05)

        # Load robot (with mass and inertia coming from the URDF rather than
        # being recomputed by pybullet)
        self.robot_id = p.loadURDF(os.path.join('.', 'urdf', 'segbot.urdf'),
                                   basePosition=np.array([0., -self.track_radius if self.turn_left else self.track_radius, 0.325 + 0.3]),
                                   baseOrientation=p.getQuaternionFromEuler([0., 0., 0.]),
                                   flags=(p.URDF_USE_IMPLICIT_CYLINDER  |
                                          p.URDF_USE_INERTIA_FROM_FILE  ))

        # Load plane and track
        self.plane_id = p.loadURDF(os.path.join('.', 'urdf', 'plane.urdf'),
                                        basePosition=np.array([0., 0., -5.]),
                                        baseOrientation=p.getQuaternionFromEuler([0., 0., 0.]),
                                        useFixedBase=1)
        self.track_id = p.loadURDF(os.path.join('.', 'urdf', 'track.urdf'),
                                        basePosition=np.array([0., 0., -2.5]),
                                        baseOrientation=p.getQuaternionFromEuler([0., 0., 0. if self.turn_left else np.pi]),
                                        useFixedBase=1)

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
            'chassis_to_left_wheel',
            'chassis_to_right_wheel',
        ]
        self.num_joints = len(self.joint_names)
        self.joint_ids = np.array([self.joint_map[joint_name] for joint_name in self.joint_names])

        # Set damping of joints (i.e., coefficient of viscous friction)
        for id in self.joint_ids:
            p.changeDynamics(self.robot_id, id, jointDamping=damping)

        # Set contact parameters
        for object_id in [self.robot_id, self.track_id, self.plane_id]:
            for joint_id in range(-1, p.getNumJoints(object_id)):
                p.changeDynamics(object_id, joint_id,
                    lateralFriction=1.0,
                    spinningFriction=0.0,
                    rollingFriction=0.0,
                    restitution=0.5,
                    contactDamping=-1,
                    contactStiffness=-1)

        # Disable velocity control on joints so we can use torque control
        p.setJointMotorControlArray(self.robot_id, self.joint_ids,
                                    p.VELOCITY_CONTROL, forces=np.zeros(self.num_joints))


    def get_sensor_measurements(self):
        """
        The measurements are:

            lateral error
            heading error
            forward speed
            turning rate
            pitch angle
            pitch rate

        They are computed assuming that both wheels are rolling without
        slipping and that the ground pitch is zero.
        """

        # Position of each wheel
        link_states = p.getLinkStates(self.robot_id, self.joint_ids)
        pl = np.array(link_states[0][0])
        pr = np.array(link_states[1][0])
        pc = 0.5 * (pr + pl)

        # Velocity of each wheel
        joint_states = p.getJointStates(self.robot_id, self.joint_ids)
        q = np.zeros([self.num_joints])
        v = np.zeros_like(q)
        for i in range(self.num_joints):
            q[i] = joint_states[i][0]
            v[i] = joint_states[i][1]
        vl = v[0] * self.wheel_radius
        vr = v[1] * self.wheel_radius

        # Lateral error
        lateral_error = np.sqrt(pc[0]**2 + pc[1]**2) - self.track_radius
        if self.turn_left:
            lateral_error *= -1.

        # Heading error
        a = np.array([pc[0], pc[1]])
        a /= np.linalg.norm(a)
        ap = np.array([-a[1], a[0]])
        b = (pr - pl)[0:2]
        if not self.turn_left:
            a *= -1.
            ap *= -1.
        heading_error = np.arctan2(np.dot(ap, b), np.dot(a, b))

        # Forward speed and turning rate
        forward_speed = (vr + vl) / 2.0
        turning_rate = (vr - vl) / np.linalg.norm(pr - pl)

        # Position, orientation, and angular velocity of chassis
        pos, ori = p.getBasePositionAndOrientation(self.robot_id)
        vel = p.getBaseVelocity(self.robot_id)
        R_body_in_world = np.reshape(np.array(p.getMatrixFromQuaternion(ori)), (3, 3))
        w_in_world = np.reshape(np.array(vel[1]), (3, 1))
        w_in_body = R_body_in_world.T @ w_in_world

        # Pitch angle and pitch rate
        pitch_angle = p.getEulerFromQuaternion(ori)[1]
        pitch_rate = w_in_body[1, 0]

        return lateral_error, heading_error, forward_speed, turning_rate, pitch_angle, pitch_rate

    def camera_topview(self):
        p.resetDebugVisualizerCamera(17., -90, -85, [0., 0., 0.])
        self.camera_chase_yaw = None

    def camera_sideview(self):
        p.resetDebugVisualizerCamera(17., -60, -35, [0., 0., -5.])
        self.camera_chase_yaw = None

    def camera_chaseview(self, yaw=270.):
        """
        view from right side: yaw=0
        view from front: yaw=90
        view from left side: yaw=180
        view from back: yaw=270
        """
        self.camera_chase_yaw = yaw
        pos, ori = p.getBasePositionAndOrientation(self.robot_id)
        eul = p.getEulerFromQuaternion(ori)
        p.resetDebugVisualizerCamera(3., (eul[2] * 180 / np.pi) + yaw, -15, pos)

    def set_actuator_commands(self, tau_left_desired, tau_right_desired):
        tau_left = np.clip(tau_left_desired, -self.tau_max, self.tau_max)
        tau_right = np.clip(tau_right_desired, -self.tau_max, self.tau_max)
        self.set_joint_torque(np.array([tau_left, tau_right]))
        return tau_left, tau_right

    def reset(self,
              turn_left=True,
              ground_pitch=0.,
              initial_speed=0.,
              initial_lateral_error=0.,
              initial_heading_error=0.,
              initial_pitch=0.):

        if np.abs(ground_pitch) >= (np.pi / 2):
            raise ValueError(f'ground_pitch ({ground_pitch}) must be have magnitude less than pi / 2')

        self.turn_left = turn_left
        if not self.turn_left:
            ground_pitch *= -1

        # Place the track
        pos = np.array([0., 0., - 2.5 / np.cos(ground_pitch)])
        ori = p.getQuaternionFromEuler([0., ground_pitch, 0. if self.turn_left else np.pi])
        p.resetBasePositionAndOrientation(self.track_id, pos, ori)

        # Place the robot
        pos = np.array([self.wheel_radius * np.sin(ground_pitch), initial_lateral_error + (-self.track_radius if self.turn_left else self.track_radius), 0.325 + 0.3])
        ori = p.getQuaternionFromEuler([0., initial_pitch, initial_heading_error])
        p.resetBasePositionAndOrientation(self.robot_id, pos, ori)
        vel = np.array([initial_speed * np.cos(initial_heading_error), initial_speed * np.sin(initial_heading_error), 0.])
        p.resetBaseVelocity(self.robot_id, linearVelocity=vel)
        angvel_wheels = initial_speed / self.wheel_radius
        for i, joint_id in enumerate(self.joint_ids):
            p.resetJointState(self.robot_id, joint_id, 0., angvel_wheels)

    def set_joint_torque(self, tau):
        """
        sets joint torques to the values specified by the 1D numpy array tau
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
        if self.display and (self.camera_chase_yaw is not None):
            self.camera_chaseview(yaw=self.camera_chase_yaw)

    def snapshot(self, filename, width=640, height=480):
        """
        saves image to filename (only works with GUI enabled, i.e., with display=True)
        """
        im = p.getCameraImage(width, height, shadow=True, renderer=p.ER_BULLET_HARDWARE_OPENGL)
        plt.imsave(filename, im[2])
