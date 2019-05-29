import text_display


class Player_Car_Info:
    """ A class containing the information and text surfaces for the player
        car. Such information includes position, velocity, acceleration, angle,
        and any other important status information regarding the player
        car Sprite.
    """
    def __init__(self, player_car, screen):
        # Initializing class vars
        self.player_car = player_car

        # Create the text handles for debugging purposes
        self.text_position = text_display.Text(screen)
        self.text_velocity = text_display.Text(screen)
        self.text_acceleration = text_display.Text(screen)
        self.text_angle = text_display.Text(screen)

        self.text_list = [self.text_position, self.text_velocity,
                          self.text_acceleration, self.text_angle]

        # Establish initial text for debugging purposes
        self.text_position.message_display(
            f"px: {0: 5}, py: {0: 5}", 0, 30)
        self.text_velocity.message_display(
            f"vx: {0: 5}, vy: {0: 5}", 0, 0)
        self.text_acceleration.message_display(
            f"ax: {0: 5}, ay: {0: 5}", 0, 60)
        self.text_angle.message_display(
            f"Angle: {0: 5}", 0, 90)

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
        vel_text = (f"vx: {round(vx, 2): >10.2f}, "
                    + f"vy: {round(vy, 2): >5.2f}"
                    + " " * 5)
        pos_text = (f"px: {round(px, 2): >10.2f}, "
                    + f"py: {round(py, 2): >5.2f}"
                    + " " * 5)
        acc_text = (f"ax: {round(ax, 2): >10.2f}, "
                    + f"ay: {round(ay, 2): >5.2f}"
                    + " " * 5)
        angle_text = (f"Angle: {round(theta_deg, 2): >10.2f}"
                      + " " * 5)

        # Update the message according to Car global vals using text above
        self.text_position.change_text(0, pos_text)
        self.text_velocity.change_text(0, vel_text)
        self.text_acceleration.change_text(0, acc_text)
        self.text_angle.change_text(0, angle_text)

        # Display the rectangle around the car
        player_car.hitbox_display()

    def clear_text(self):
        for text in self.text_list:
            text.change_text(0, "")
