import numpy as np
import cv2 # OpenCV
import math
from matplotlib import pyplot as plt
from numpy.lib.function_base import disp

from ..utils.process_text_file import ProcessTextFile

class PerspectiveProjection:
    def __init__(self, camera_K_matrix, camera_D_matrix):
        self.camera_K_matrix_ = camera_K_matrix
        self.camera_D_matrix_ = camera_D_matrix
        self.grayscale_image_ = []

    def load_image(self, image_fname, display):
        color_image = cv2.imread(image_fname, 0)
        self.grayscale_image_ = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        if display:
            self.display_image()

        return

    def display_image(self):
        plt.imshow(self.grayscale_image_)
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.show()

        return

    def scatter(self, points):

        return

    def lines(self, points):

        return

    def project_W_to_C(self, camera_pose, point_in_W):
        rot_mat_W_to_C = self.angle_axis_2_rot_mat(camera_pose[:2])
        t_pos_in_W = np.reshape(camera_pose[3:], (3,1))
        point_in_W = np.reshape(point_in_W, (3,1))

        point_in_C = self.camera_K_matrix_ * np.concatenate((rot_mat_W_to_C, t_pos_in_W), axis=1) * np.concatenate((point_in_W, np.ones((1,1))), dim=0)

        return point_in_C[:1] / point_in_C[2], point_in_C[2] # [u, v], lambda

    @staticmethod
    def angle_axis_2_rot_mat(angle_axis):
        eye3 = np.eye(3)
        theta = np.linalg.norm(angle_axis)
        k = angle_axis / theta
        
        k_skew_symmetrix = np.zeros((3,3))
        k_skew_symmetrix[0, 1] = -k[2]
        k_skew_symmetrix[0, 2] = k[1]
        k_skew_symmetrix[1, 2] = -k[0]

        k_skew_symmetrix -= np.transpose(k_skew_symmetrix)

        return eye3 + math.sin(theta) * k_skew_symmetrix + (1 - math.cos(theta)) * k_skew_symmetrix * k_skew_symmetrix