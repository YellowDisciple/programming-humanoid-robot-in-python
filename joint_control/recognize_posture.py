'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''


from angle_interpolation import AngleInterpolationAgent
from keyframes import hello
import pickle
import numpy as np


class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        with open('robot_pose.pkl', 'rb') as file:
            self.posture_classifier = pickle.load(file) # LOAD YOUR CLASSIFIER


    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        # YOUR CODE HERE
        #['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'AngleX', 'AngleY']
        sensor_array = np.array([perception.joint['LHipYawPitch'],perception.joint['LHipRoll'], perception.joint['LHipPitch'] ,perception.joint['LKneePitch'] ,perception.joint['RHipYawPitch'] ,perception.joint['RHipRoll'] ,perception.joint['RHipPitch'] ,perception.joint['RKneePitch'], perception.imu[0], perception.imu[1]]).reshape(1, -1)
        pose = self.posture_classifier.predict(sensor_array)[0]
        match pose:
            case 0:
                posture = 'Back'
            case 1:
                posture = 'Belly'
            case 2:
                posture = 'Crouch'
            case 3:
                posture = 'Frog'
            case 4:
                posture = 'HeadBack'
            case 5:
                posture = 'Knee'
            case 6:
                posture = 'Left'
            case 7:
                posture = 'Right'
            case 8:
                posture = 'Sit'
            case 9:
                posture = 'Stand'
            case 10:
                posture = 'StandInit'
            case _:
                psture = 'unknown'

        #print(posture)
        return posture

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.run_keyframe(hello() , agent.perception.time)  # CHANGE DIFFERENT KEYFRAMES
    agent.target_joints['RshoulderPitch'] = 1.5
    agent.target_joints['LshoulderPitch'] = 1.5
    agent.run()
