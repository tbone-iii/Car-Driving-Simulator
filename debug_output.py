import text_display
import pygame

from config import DISPLAY_HEIGHT, DISPLAY_WIDTH, default_font_size
from typing import Tuple


class Player_Car_Info:
    """ A class containing the information and text surfaces for the player
        car. Such information includes position, velocity, acceleration, angle,
        and any other important status information regarding the player
        car Sprite.
    """
    def __init__(self, player_car, screen) -> None:
        # Initializing class vars
        self.player_car = player_car

        # Create the text handles for debugging purposes
        self.text_position = text_display.Text(screen)
        self.text_velocity = text_display.Text(screen)
        self.text_acceleration = text_display.Text(screen)
        self.text_angle = text_display.Text(screen)
        self.text_tire_angle = text_display.Text(screen)

        self.text_list = [self.text_position, self.text_velocity,
                          self.text_acceleration, self.text_angle,
                          self.text_tire_angle]

        # Establish initial text for debugging purposes
        self.text_position.message_display(
            f"px: {0: 5}, py: {0: 5}", 0, 30)
        self.text_velocity.message_display(
            f"vx: {0: 5}, vy: {0: 5}", 0, 0)
        self.text_acceleration.message_display(
            f"ax: {0: 5}, ay: {0: 5}", 0, 60)
        self.text_angle.message_display(
            f"Car Angle: {0: 5}", 0, 90)
        self.text_tire_angle.message_display("", 0, 120)

        # Create console variable (is open, is not open)
        self.IS_OPEN: bool = False
        self.text_console = text_display.Text(
            screen, font_size=default_font_size/2)
        self.text_console.message_display("INFO", 0, DISPLAY_HEIGHT - 60)
        self.text_console.message_display("INPUT", 0, DISPLAY_HEIGHT - 30)

    def update(self):
        """ Updates the text according to the internal
            changes of the player car (speed, pos, etc.).
        """
        player_car = self.player_car

        # Craft new text strings
        (px, py) = (player_car.px_global, player_car.py_global)
        (vx, vy) = (player_car.vx_global, player_car.vy_global)
        (ax, ay) = (player_car.ax_global, player_car.ay_global)
        theta_deg = player_car.theta_deg
        tire_angle = player_car.tire_angle_deg

        vel_text = (f"vx: {round(vx, 2): >10.2f}, "
                    + f"vy: {round(vy, 2): >10.2f}"
                    + " " * 5)
        pos_text = (f"px: {round(px, 2): >10.2f}, "
                    + f"py: {round(py, 2): >10.2f}"
                    + " " * 5)
        acc_text = (f"ax: {round(ax, 2): >10.2f}, "
                    + f"ay: {round(ay, 2): >10.2f}"
                    + " " * 5)
        angle_text = (f"Car Angle: {round(theta_deg, 2): >10.2f}"
                      + " " * 5)
        tire_angle_text = (f"Tire Angle: {round(tire_angle, 2): >10.2f}"
                           + " " * 5)

        # Update the message according to Car global vals using text above
        self.text_position.change_text(0, pos_text)
        self.text_velocity.change_text(0, vel_text)
        self.text_acceleration.change_text(0, acc_text)
        self.text_angle.change_text(0, angle_text)
        self.text_tire_angle.change_text(0, tire_angle_text)

        # Display the rectangle around the car
        player_car.hitbox_display()

    def clear_debug_text(self):
        for text in self.text_list:
            text.change_text(0, "")

    def open_console(self):
        player_car = self.player_car
        properties = player_car.properties

        car_properties = get_car_properties(
            car=player_car, properties=properties)

        text_console = self.text_console

        # While loop pre-allocated variable
        console_input = ""
        # While the console is open, receive player key input
        while self.IS_OPEN:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # If the player hits enter, accept the input and attempt
                    # to set the attribute
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        # If property doesn't exist, throw message
                        if console_input == "center":
                                player_car.px_global = DISPLAY_WIDTH/2
                                player_car.py_global = DISPLAY_HEIGHT/2
                                console_input = ""
                        elif console_input:
                            try:
                                (prop, value) = console_input.split()
                            except ValueError:
                                print(f"'{console_input}' is "
                                      "not splittable.\n")
                                prop = ""
                                value = ""

                            # Convert the value string into a float.
                            try:
                                value = float(value)
                            except ValueError:
                                print(f"Value {value} "
                                      "cannot be converted to float.\n")
                                console_input = ""

                            if prop not in properties:
                                print(f"There is no such attribute "
                                      "as {prop}.\n")
                            # If value is not an integer or float
                            elif type(value) is int or type(value) is float:
                                setattr(player_car, prop, value)
                                console_input = ""

                    # If F1 is pressed, toggle the IS_OPEN console variable
                    elif (event.key == pygame.K_F1
                            or event.key == pygame.K_ESCAPE):
                        self.IS_OPEN = False
                        break

                    # Text delete with backspace
                    elif event.key == pygame.K_BACKSPACE:
                        console_input = console_input[:-1]
                    # If any other key is pressed
                    else:
                        # If the key description is alphnumeric or a
                        # permissible character
                        if (str(event.unicode).isalnum()
                                or event.unicode in "_ -."):
                            # Add the key to the console input string
                            console_input += event.unicode
                        else:
                            print("Please enter an alphanumeric key.")

            # Update the text
            car_properties = get_car_properties(
                car=player_car, properties=properties)
            text_console.change_text(0, str(car_properties))
            text_console.change_text(1, str(console_input))

        # Close console (by clearing text) after while loop exits
        text_console.change_text(0, "")
        text_console.change_text(1, "")

    def toggle_console(self):
        # Invert this bool var
        self.IS_OPEN = not self.IS_OPEN


def get_car_properties(car, properties: Tuple[str]) -> dict:
    attrs = [getattr(car, name) for name in properties]
    return dict(zip(car.properties, attrs))
