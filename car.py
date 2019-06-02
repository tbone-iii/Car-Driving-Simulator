"""
    This file produces the player controlled car class for the main game.
"""

import pygame
import config
import text_display

from math import cos, sin, pi, atan
from typing import List


# Create the car class
class Car(pygame.sprite.Sprite):
    """ The car class holds each instance of car sprites that drive around.
    """
    def __init__(self,
                 screen,
                 position: tuple,
                 image_path: str = config.image_enemy_car,
                 max_v_mph: float = 120.0,
                 zero_to_sixty_time_sec: float = 4.0,
                 turning_speed_deg: float = 2  # degrees per frame
                 ) -> None:
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert()
        self.screen = screen
        (im_x, im_y) = self.image.get_size()

        # Global position, velocity, and acceleration
        (self.px_global, self.py_global) = position
        (self.vx_global, self.vy_global) = (0, 0)
        (self.ax_global, self.ay_global) = (0, 0)
        # Global angle relative to horizontal +X axis [deg]
        self.theta_deg = 0
        # Max absolute velocity/speed, pixels/sec
        self.max_v_mph = max_v_mph

        # Establish width and height as a percentage of the display width
        self.width = int(0.10 * config.DISPLAY_WIDTH)
        self.height = int(im_y/im_x * self.width)

        # ? Car length parameter
        car_length_feet = 15
        self.feet_per_pixel = car_length_feet / self.width

        # ? Acceleration parameters based on car length and 0-60 time
        self.zero_to_sixty_time_sec = 4
        # frictional accelerations [in g: 32.2f/s^2, e.g. 2Gs of decel.]
        self.a_friction_in_g = -0.05    # negative due to deceleration
        self.a_brake_in_g = -0.96
        self.a_max_centripetal_in_g = 0.94

        # Establish wheelbase based on "width" of the car and tire angle
        self.wheelbase = self.width * 0.70
        self.tire_angle_deg = 0
        self.max_tire_angle_deg = 45

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
        self.theta_delta_deg = turning_speed_deg
        self.time_delta = config.time_delta

        # Previous rectangle and image used to fill in black behind image
        self.prev_image = self.image
        self.rect = self.image.get_rect(topleft=position)

        # Screen wrap TRUE or FALSE
        self.screen_wrap_on = True
        self.speedometer_exists = False

        # Properties list in string format for var change in debug output
        self.properties = (
            "zero_to_sixty_time_sec", "max_tire_angle_deg", "a_friction_in_g",
            "a_brake_in_g", "max_v_mph", "screen_wrap_on")

    @property
    def theta_rad(self):
        """ Converts from degrees to radians as a property value. """
        return self.theta_deg * pi/180

    @property
    def max_a(self):
        """ Converts from 0-60 mph time to max acceleration in pixels/s^2. """
        # feet per second^2, convert mph to feet per second
        max_a_fpss = 60 / self.zero_to_sixty_time_sec * 5280/3600
        return max_a_fpss/self.feet_per_pixel

    @property
    def max_v(self):
        """ Converts the maximum MPH velocity to pixels per second velocity.
        """
        return self.max_v_mph*(5280/3600) / self.feet_per_pixel

    @property
    def a_friction(self):
        """ Convert acceleration due to friction from G-force to pixel/s/s. """
        return self.a_friction_in_g * 32.2 / self.feet_per_pixel

    @property
    def a_brake(self):
        """ Convert acceleration due to braking from G-force to pixel/s/s. """
        return self.a_brake_in_g * 32.2 / self.feet_per_pixel

    @property
    def a_max_centripetal(self):
        """ Convert max centripetal acceleration to pixel/s/s. """
        return self.a_max_centripetal_in_g * 32.2 / self.feet_per_pixel

    @property
    def turning_radius(self):
        """ Calculates the turning radius in pixels. """
        theta_rad = self.tire_angle_deg * pi/180
        if sin(theta_rad) == 0:
            return 10**8
        else:
            return cos(theta_rad)/sin(theta_rad) * self.wheelbase

    @property
    def a_centripetal(self):
        """ Calculates the current centripetal acceleration in pixels/s/s. """
        return self.vx**2 / self.turning_radius

    @property
    def max_theoretical_tire_angle_rad(self):
        """ Calculates the maximum tire angle based on max centripetal
            acceleration. Formula is atan(w*ac/v^2) = delta
        """
        if self.vx == 0:
            return self.max_tire_angle_deg
        else:
            return atan(self.wheelbase * self.a_max_centripetal / self.vx**2)

    @property
    def speed_absolute_MPH(self):
        """ Calculates the magnitude of velocity in MPH. """
        return self.vx * self.feet_per_pixel * 3600/5280

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

    def check_stop_acceleration(self):
        """ Sets the car acceleration and velocity
            to 0 if it is frictionally decelerating
            and the velocity of the car is close to 0
        """
        if (self.ax == self.a_friction
                and abs(self.vx) <= 5):
            self.ax = 0.0
            self.vx = 0.0

    def calculate_velocity(self):
        """ Using the "local" values, calculate the global velocity. """
        # Establish local variables
        vx = self.vx
        ax = self.ax
        time_delta = self.time_delta
        max_v = self.max_v
        theta_rad = self.theta_rad

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
        """ Using the global values of velocity, find the new global position.
        """
        time_delta = self.time_delta
        self.px_global += self.vx_global * time_delta
        self.py_global += self.vy_global * time_delta
        if self.screen_wrap_on:
            # If too far right
            if self.rect.right > config.DISPLAY_WIDTH:
                self.px_global -= config.DISPLAY_WIDTH
            # If too far left
            if self.rect.left < 0:
                self.px_global += config.DISPLAY_WIDTH
            # If too far up
            if self.rect.top < 0:
                self.py_global += config.DISPLAY_HEIGHT
            # If too far down
            if self.rect.bottom > config.DISPLAY_HEIGHT:
                self.py_global -= config.DISPLAY_HEIGHT

    def calculate_acceleration(self):
        """ Using the local value of acceleration, calculate the global
            values of acceleration.
        """
        theta_rad = self.theta_rad
        self.ax_global = self.ax * cos(theta_rad)
        self.ay_global = -self.ax * sin(theta_rad)

    def calculate_theta_delta(self):
        """ Computes the change in car image angle based on the car
            velocity and wheelbase (length between front and back
            tires).
        """
        vx = self.vx
        phi = self.tire_angle_deg * pi/180
        wb = self.wheelbase
        time_delta = self.time_delta
        self.theta_delta_deg = (vx * sin(phi)/wb * time_delta) * 180/pi

    def turn(self):
        """ Performs the image rotation with background correction.
        """
        # Perform a check to limit the tire angle based on max centripetal
        # acceleration.
        max_theory_angle = 180/pi * self.max_theoretical_tire_angle_rad
        angle = self.tire_angle_deg
        if abs(angle) > max_theory_angle:
            # Ensure the max theory angle has the same sign as the tire angle
            self.tire_angle_deg = max_theory_angle * abs(angle)/angle

        # Calculate the change in car angle with respect to time
        self.calculate_theta_delta()

        # Increment the angle
        self.theta_deg += self.theta_delta_deg
        # Correct the angle if outside 360 degree limit
        if self.theta_delta_deg > 0:      # if positive
            if self.theta_deg > 360:      # if angle outside 360
                self.theta_deg -= 360     # correct it
        elif self.theta_delta_deg < 0:    # if negative
            if self.theta_deg <= 0:       # if angle below or equal to 0
                self.theta_deg += 360     # correct it

        # Erase previous image before rotation
        self.screen.fill(config.BLACK, rect=self.rect)

        # Rotate the original image according to the global angle
        self.image = pygame.transform.rotate(
            self.original_image, self.theta_deg)

        # Set the image rect center to be the same as the sprite rect center
        self.rect = self.image.get_rect(topleft=self.rect.center)

    def turn_left(self):
        """ Increase the tire angle.
        """
        phi = self.tire_angle_deg
        if phi + 1 <= self.max_tire_angle_deg:
            self.tire_angle_deg += 1

        # Perform the image rotation
        self.turn()

    def turn_right(self):
        """ Decrease the tire angle.
        """
        phi = self.tire_angle_deg
        if phi - 1 >= -self.max_tire_angle_deg:
            self.tire_angle_deg -= 1

        # Perform the image rotation
        self.turn()

    def turn_none(self):
        """ Return the steering angle back to 0 degrees with no input.
        """
        if self.tire_angle_deg:
            self.tire_angle_deg *= 0.80**(self.vx/self.max_v)
            self.turn()
        if abs(self.tire_angle_deg) <= 0.1:
            self.tire_angle_deg = 0

    def update_speedometer(self):
        """ Creates a speedometer if it does not exist and updates it
            on every frame.
        """
        if not self.speedometer_exists:
            self.speedometer_exists = True
            self.text_speedometer = text_display.Text(self.screen)
            self.text_speedometer.message_display(
                "0", x=config.DISPLAY_WIDTH, y=0, position='topright',
                color=config.SILVER)
        self.text_speedometer.change_text(
            0, f"Speed: {self.speed_absolute_MPH: >6.2f} MPH")

    def hitbox_display(self):
        """ Display the hitbox, centerpoint, and rectangle outline.
        """
        # ? Draw the outline rectangle of the rectangle.
        pygame.draw.rect(self.screen, config.RED, self.rect, 1)

        # Determine coordinates of rotated image corners and set to list
        H = self.height * 0.92      # slightly reduced to shrink the hitbox
        L = self.width * 0.95

        # Establish the points to rotate from original frame to another.
        px = self.px_global
        py = self.py_global
        top_left = (-L/2, -H/2)
        bottom_left = (-L/2, H/2)
        bottom_right = (L/2, H/2)
        top_right = (L/2, -H/2)
        pointlist = [top_left, bottom_left, bottom_right, top_right]
        # Perform the rotation
        pointlist = rotation_transformation(
            pointlist=pointlist, angle_deg=self.theta_deg,
            translation=(px, py))
        # ? Draw the hitbox
        pygame.draw.polygon(self.screen, config.GREEN, pointlist, 1)

        # ? Draw the centerpoint
        (px, py) = int(px), int(py)
        pygame.draw.circle(self.screen, config.GREEN, (px, py), 2, 0)

    def update(self):
        """ Update the sprite conditions (pos and vel) on screen.
        """
        # Check to see if the car should stop accelerating
        self.check_stop_acceleration()

        # Calculates the velocity, then position of the car
        self.calculate_velocity()
        self.calculate_position()
        self.calculate_acceleration()
        self.calculate_theta_delta()
        position = (self.px_global, self.py_global)

        # Update the speedometer
        self.update_speedometer()

        # Erase the old rect with a black fill (optimization reasons)
        self.screen.fill(config.BLACK, rect=self.rect)

        # Determine the new center coordinates for the sprite
        self.rect.center = position

        # Show the sprite on the screen
        self.screen.blit(self.image, self.rect)

        # Update prev image
        self.prev_image = self.image


def rotation_transformation(pointlist: List[tuple],
                            angle_deg: float,
                            translation: tuple) -> List[tuple]:
    """ Performs a linear transformation on a list of points as tuples.
        This linear transformation is a rotation and translation from
        the base frame {0} to another frame {1} (of reference).

        Returns the transformed pointlist.
    """
    th = angle_deg * pi/180     # convert to radians from degrees
    px = translation[0]
    py = translation[1]
    # Operation below is R matrix times vector, plus frame transformation.
    for index, point in enumerate(pointlist):
        xt = cos(th) * point[0] + sin(th) * point[1] + px
        yt = -sin(th) * point[0] + cos(th) * point[1] + py
        pointlist[index] = (xt, yt)
    return pointlist