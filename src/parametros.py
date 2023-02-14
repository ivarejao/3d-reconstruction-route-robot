import json

import numpy as np


# Function to read the intrinsic and extrinsic parameters of each camera
def camera_parameters(file):
    camera_data = json.load(open(file))
    K = np.array(camera_data['intrinsic']['doubles']).reshape(3, 3)
    res = [camera_data['resolution']['width'],
           camera_data['resolution']['height']]
    tf = np.array(camera_data['extrinsic']['tf']['doubles']).reshape(4,
                                                                     4)  # converte referencial da camera para o mundo
    R = tf[:3, :3]
    T = tf[:3, 3].reshape(3, 1)
    dis = np.array(camera_data['distortion']['doubles'])
    return K, R, T, res, dis, np.linalg.inv(tf)  # np.linalg.inv(tf) converte referencial do mundo para a camera


# Load cameras parameters
K0, R0, T0, res0, dis0, tf0 = camera_parameters('../data/calib/0.json')
K1, R1, T1, res1, dis1, tf1 = camera_parameters('../data/calib/1.json')
K2, R2, T2, res2, dis2, tf2 = camera_parameters('../data/calib/2.json')
K3, R3, T3, res3, dis3, tf3 = camera_parameters('../data/calib/3.json')

pi = np.eye(3, 4)

P0 = np.dot(K0, np.dot(pi, tf0))
P1 = np.dot(K1, np.dot(pi, tf1))
P2 = np.dot(K2, np.dot(pi, tf2))
P3 = np.dot(K3, np.dot(pi, tf3))
