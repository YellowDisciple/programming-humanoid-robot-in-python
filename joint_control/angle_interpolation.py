'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello
from keyframes import wipe_forehead
from scipy import interpolate
import numpy as np


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.start_time = 0
        self.moving = False

    def run_keyframe(self, keyframe, start_time):
        self.keyframes = keyframe
        self.start_time = start_time
        self.moving = True

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        j = 0
        time = perception.time - self.start_time
        #print(time)
        while j < len(keyframes[0]) :
            name = keyframes[0][j]
            i = 0
            time_axis = np.zeros(len(keyframes[1][j]) + 1)
            angle_axis = np.zeros(len(keyframes[1][j]) + 1)
            time_axis[0] = 0
            angle_axis[0] = perception.joint[name]
            while i < len(keyframes[1][j]):
                time_axis[i+1] = keyframes[1][j][i]
                angle_axis[i+1] = keyframes[2][j][i][0]
                i += 1
            #print(time_axis)
            #print(angle_axis)
            target_time = time
            if time > time_axis[len(time_axis)-1]:
                target_time = time_axis[len(time_axis)-1]
                self.moving = False
            target_joints[name] = interpolate.splev(target_time, interpolate.splrep(time_axis, angle_axis, k = 3))
            j += 1
            #print(interpolate.splev(time, interpolate.splrep(time_axis, angle_axis, k = 3)))
            #x_points = [ 0, 1, 2, 3, 4, 5]
            #y_points = [12,14,22,39,58,77]
            #tck = interpolate.splrep(x_points, y_points)
            #print(interpolate.splev(1.25, tck))
        #print(target_joints)
        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    #agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run_keyframe(wipe_forehead(), agent.perception.time)
    agent.run()
