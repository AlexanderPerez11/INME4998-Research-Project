from pyquaternion import Quaternion
from numpy import *

from math import pi, sin, cos, tan
set_printoptions(suppress=True)
q = Quaternion(axis=[1, 0, 0], angle=pi)

sample_rate = 100
samples = 1000
dt = pi
w_x = 0.5
w_z = 0.5
w_y = 0.5

w_norm = sqrt(w_x**2 + w_y**2 + w_z**2)

alpha = dt*w_norm/2
q0 = cos(alpha)
q1 = sin(alpha)*w_x/w_norm
q2 = sin(alpha)*w_y/w_norm
q3 = sin(alpha)*w_z/w_norm

rot = Quaternion(q0, q1, q2, q3)
v = array([1, 0, 0])
v_prime = rot.rotate(v)
print(v_prime)

def quaternion_rotation(sample_rate, w_x, w_y, w_z, v_x, v_y, v_z, n):
    w_norm = np.sqrt(w_x[n] ** 2 + w_y[n] ** 2 + w_z[n] ** 2)
    alpha = w_norm / (sample_rate * 2)
    q0 = np.cos(alpha)
    q1 = np.sin(alpha) * w_x[n] / w_norm
    q2 = np.sin(alpha) * w_y[n] / w_norm
    q3 = np.sin(alpha) * w_z[n] / w_norm

    v = np.array([v_x[n], v_y[n], v_z[n]])
    q = Quaternion(q0, q1, q2, q3)
    v_prime = q.rotate(v)

    return v_prime

# testingData = sum(q0 + q1)