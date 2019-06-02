import pygame
import config
import car
import debug_output


# TODO:
# ! 1) Permit active changing of car variables while the game is running.
# * 2) Show a HITBOX and IMAGE OUTLINE of the car, which shows stuff like:
# * ----- a) The centerpoint of the car
# ! ----- b) The PIVOT point of the car (back tires, centralized)
#   ----- c) etc.
# * 3) Change the mechanism behind the rotation of the car.
# * ----- a) Have the car pivot about the back tires
# * ----- b) Calculate the angular speed the car can move with respect to
# * ........  the turning radius (and proportional the car velocity and length)
# * ----- c) Doing ^ THIS ^ may require determining the relative positions of
# * ........  the car tires (the center of these positions, that is)
# * 4) Change the steering mechanism
# * ----- a) Gradually change the steering angle up to the maximum while
# * ........  the left and right keys are pressed.
# ! 5) Refactor the text display for the debug output usage. Suboptimal method
# ? 6) In the future, potentially figure out another way for rear-pivoting.
# * 7) Limit turning angle at high speeds (maximum centripetal acc. prop)
# ? 7) Change screen wrapping to include two images for smoother wrapping.

# Initialize pygame modules
pygame.init()


# Main game loop
def main_loop():
    # Create the main window and clock
    screen = pygame.display.set_mode(config.RESOLUTION)
    clock = pygame.time.Clock()

    # Create the player's car
    player_car = car.Car(
        screen=screen,
        position=(config.DISPLAY_WIDTH/2, config.DISPLAY_HEIGHT/2),
        image_path=config.image_player_car)

    # Establish the main loop
    screen.fill(config.BLACK)

    # Create debugging options
    DEBUGGING = True
    if DEBUGGING:
        player_car_info = debug_output.Player_Car_Info(player_car, screen)

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                break

            # If a key is pushed down
            if event.type == pygame.KEYDOWN:
                # Quits the game on ESCAPE
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                # If the UP KEY is pressed, cause the car to accelerate
                if event.key == pygame.K_UP:
                    player_car.accelerate()
                # Toggles the display of the car text information
                if event.key == pygame.K_d:
                    # Clear the text of the debugging info
                    player_car_info.clear_debug_text()
                    # Invert the debugging option
                    DEBUGGING = not DEBUGGING
                # If the F1 key is pressed, show variable change options
                if event.key == pygame.K_F1:
                    # TODO: Show command options to change certain car vars.
                    # TODO: And allow input
                    player_car_info.toggle_console()

            # If a key is released
            if event.type == pygame.KEYUP:
                # If the UP KEY is released, reduce velocity by fric (neg acc)
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_car.decelerate_frictionally()
        # Find which keys are being pressed
        keys_pressed = pygame.key.get_pressed()

        # Determine left and right turns
        if keys_pressed[pygame.K_LEFT]:
            player_car.turn_left()
        if keys_pressed[pygame.K_RIGHT]:
            player_car.turn_right()
        # If left and right keys not pressed, allow steering
        # angle to return to 0
        if not (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
            player_car.turn_none()
        # Determine braking
        if keys_pressed[pygame.K_DOWN]:
            player_car.brake()

        # Update and draw player car on the screen
        player_car.update()

        # If debug mode is on, update the debug text
        if DEBUGGING:
            player_car_info.update()
        # If the console is on, update the console text
        if player_car_info.IS_OPEN:
            player_car_info.open_console()

        # Update the screen
        pygame.display.flip()

        # Move one frame
        clock.tick(config.FPS)


if __name__ == '__main__':
    main_loop()
