"""
    This file produces the player controlled car class for the main game.
"""

import pygame
import config
from math import cos, sin, pi, hypot


# Create the car class
class Car(pygame.sprite.Sprite):
    """ The car class holds each instance of car sprites that drive around.
    """
    def __init__(self,
                 screen,
                 position: tuple,
                 image_path: str = config.image_enemy_car,
                 max_v: float = 100.0,
                 max_a: float = 10.0,
                 turning_speed_deg: float = 2  # degrees per frame
                 ) -> None:
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert()
        self.screen = screen
        (im_x, im_y) = self.image.get_size()

        # Global position
        (self.px_global, self.py_global) = position
        # Global velocity
        (self.vx_global, self.vy_global) = (0, 0)
        # Global acceleration
        (self.ax_global, self.ay_global) = (0, 0)
        # Global angle relative to horizontal +X axis [deg]
        self.theta_deg = turning_speed_deg
        # Max absolute velocity/speed, pixels/sec
        self.max_v = max_v
        self.max_a = max_a

        # Acceleration parameters
        self.a_friction = -2  # frictional deceleration [pixels/sec^2]
        self.a_brake = -30    # frictional acceleration [pixels/sec^2]

        # Establish width and height as a percentage of the display width
        self.width = int(0.10 * config.DISPLAY_WIDTH)
        self.height = int(im_y/im_x * self.width)

        # Resize the image
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        self.original_image = self.image

        # Create a local frame of reference for the car (useful for drifting)
        self.px = 0
        self.py = 0
        self.vx = 0  # velocity of car in its "x-dir"
        self.vy = 0  # <-- unused right now, perhaps used for drifting later
        self.ax = 0
        self.ay = 0

        # Theta delta, time delta
        self.theta_delta_deg = 2
        self.time_delta = config.time_delta

        # Previous rectangle and image used to fill in black behind image
        self.prev_image = self.image
        self.rect = self.image.get_rect(topleft=position)

    def accelerate(self):
        """ Sets the car acceleration to the maximum
        """
        self.ax = self.max_a

    def decelerate_frictionally(self):
        """ Sets the car acceleration to the frictional deceleration amount.
        """
        self.ax = self.a_friction

    def brake(self):
        """ Sets the acceleration of the car to the braking deceleration
            amount.
        """
        if self.vx > 0:
            self.ax = self.a_brake
        else:
            self.ax = 0
            self.vx = 0

    def calculate_global_speed_magnitude(self):
        return hypot(self.vx_global, self.vy_global)

    def check_stop_acceleration(self):
        """ Sets the car acceleration and velocity
            to 0 if it is frictionally decelerating
            and the velocity of the car is close to 0
        """
        if (self.ax == self.a_friction
                and self.calculate_global_speed_magnitude() <= 0.25):
            self.ax = 0.0
            self.vx = 0.0

    def calculate_velocity(self):
        """ Using the "local" values, calculate the global vel.
        """
        # Establish local variables
        vx = self.vx
        ax = self.ax
        time_delta = self.time_delta
        max_v = self.max_v
        # Unit conversion
        theta_rad = self.theta_deg * pi/180

        # If the velocity can still increase beneath maximum velocity, do it
        if vx + ax * time_delta <= max_v:
            self.vx += ax * time_delta
        # If the velocity is close to the maximum velocity, set it to the max v
        elif abs(max_v - vx) <= ax * time_delta:
            self.vx = max_v

        # Compute the new velocities in the global frame
        self.vx_global = self.vx * cos(theta_rad)
        self.vy_global = -self.vx * sin(theta_rad)

    def calculate_position(self):
        """ Using the global values of velocity, find the new global pos.
        """
        time_delta = self.time_delta
        self.px_global += self.vx_global * time_delta
        self.py_global += self.vy_global * time_delta

    def turn(self):
        """ Performs the image rotation with background correction.
        """
        # Erase previous image before rotation
        self.screen.fill(config.BLACK, rect=self.rect)

        # Rotate the original image according to the global angle
        self.image = pygame.transform.rotate(
            self.original_image, self.theta_deg)

        # Set the image rect center to be the same as the sprite rect center
        self.rect = self.image.get_rect(topleft=self.rect.center)

    def turn_left(self):
        """ Increase the theta angle by some functional amount.
        """
        # Increment the angle
        self.theta_deg += self.theta_delta_deg
        # Correct the angle if outside 360 degree limit
        if (self.theta_deg >= 360):
            self.theta_deg -= 360

        # Perform the image rotation
        self.turn()

    def turn_right(self):
        """ Decrease the theta angle by some functional amount.
        """
        # Decrement the angle
        self.theta_deg -= self.theta_delta_deg
        # Correct the angle if it's outside of the 0 degree limit
        if (self.theta_deg <= 0):
            self.theta_deg += 360

        # Perform the image rotation
        self.turn()

    def update(self):
        """ Update the sprite conditions (pos and vel) on screen.
        """
        # Check to see if the car should stop accelerating
        self.check_stop_acceleration()

        # Calculates the velocity, then position of the car
        self.calculate_velocity()
        self.calculate_position()
        position = (self.px_global, self.py_global)

        # Erase the old rect with a black fill (optimization reasons)
        self.screen.fill(config.BLACK, rect=self.rect)

        # Determine the new center coordinates for the sprite
        self.rect.center = position

        # Show the sprite on the screen
        self.screen.blit(self.image, self.rect)

        # Update prev image
        self.prev_image = self.image
