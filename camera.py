from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

DC = {"VERTICAL": 90, "HORIZONTAL": 0, "ISOMETRIC": -45, "FREE": 60}

class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 0, 3.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0
        self.pitch_constraint = 60
        self.move_disabled = False


    def camera_mode(self, mode):
        if mode == "TOPVIEW":
            self.jaw = 90
            self.pitch_constraint = DC["VERTICAL"]
            self.pitch = -90
            self.camera_pos = Vector3([0, 10, 0])
            self.move_disabled = True
            self.update_camera_vectors()

        if mode == "FRONTVIEW":
            self.pitch_constraint = DC["HORIZONTAL"]
            self.camera_pos = Vector3([0.0, 0, -10])
            self.camera_front = Vector3([0.0, 0.0, -1.0])
            self.camera_up = Vector3([0.0, 1.0, 0.0])
            self.camera_right = Vector3([1.0, 0.0, 0.0])
            self.jaw = 90
            self.pitch = 0
            self.move_disabled = True
            self.update_camera_vectors()

        if mode == "ISOMETRICVIEW":
            self.pitch_constraint = DC["ISOMETRIC"]
            self.camera_pos = Vector3([15, 15, -15])
            self.camera_front = Vector3([0.0, 0.0, -1.0])
            self.camera_up = Vector3([0.0, 1.0, 0.0])
            self.camera_right = Vector3([1.0, 0.0, 0.0])
            self.jaw = -45
            self.pitch = -45
            self.move_disabled = True
            self.update_camera_vectors()

        if mode == "FREECAM":
            self.pitch_constraint = DC["FREE"]
            self.camera_pos = Vector3([0.0, 0, 3.0])
            self.camera_front = Vector3([0.0, 0.0, -1.0])
            self.camera_up = Vector3([0.0, 1.0, 0.0])
            self.camera_right = Vector3([1.0, 0.0, 0.0])
            self.jaw = -90
            self.pitch = 0
            self.pitch_constraint = 60
            self.move_disabled = False
            self.update_camera_vectors()


    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        if self.move_disabled:
            return
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > self.pitch_constraint:
                self.pitch = self.pitch_constraint
            if self.pitch < -self.pitch_constraint:
                self.pitch = -self.pitch_constraint

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        # self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))
        self.camera_up = vector.normalise(self.camera_up)


    # Camera method for the WASD movement
    def process_keyboard(self, direction, velocity):
        if self.move_disabled:
            return
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity
        if direction == "UP":
            self.camera_pos += self.camera_up * velocity
        if direction == "DOWN":
            self.camera_pos -= self.camera_up * velocity


