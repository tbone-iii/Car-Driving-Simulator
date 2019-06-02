import pygame
import config

pygame.init()


class Text:
    """ Text class handles all text displays on a game window,
        which is passed by the game handle. Each instance of Text
        is its own type of text (e.g. velocity output, position output),
        allowing for easy enabling and disabling of text display.
    """
    white = config.WHITE
    black = config.BLACK
    possible_positions = ('topleft', 'topright', 'bottomright', 'bottomleft',
                          'center')

    def __init__(self, game_window, font_size=config.default_font_size):
        """ Class constructor initializing with the
            pygame game_window/screen handle.
        """
        self.game_window = game_window
        self.text_surfaces = []
        self.text_rects = []
        self.text_positions = []
        self.font_size = int(font_size)
        self.normal_font = pygame.font.Font(config.font, self.font_size)

    def text_objects(self, text: str, font, color: tuple):
        """ Takes text and pygame font and returns a text surface and rect.
        """
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def message_display(self, text, x: int, y: int,
                        position: str = 'topleft',
                        color: tuple = white):
        """ Takes text and places it at (x, y) coordinates.
            The position argument is a string representating the
            rectangle origin location.

            For example, position can be 'bottomright'
            or 'center'.
        """
        text_surface, text_rect = self.text_objects(
            text=text, font=self.normal_font, color=color)

        # Set the coordinates of the rectangle depending on position
        if position not in Text.possible_positions:
            print("WARNING: {position} does not exist!"
                  "Defaulting to 'topleft'.")
            position = "topleft"
        setattr(text_rect, position, (x, y))

        # Fills previous text with black rectangle.
        self.game_window.fill(Text.black, text_rect)
        # Blit the new text onto the surface.
        self.game_window.blit(text_surface, text_rect)

        # Append list of text surfaces, rectancles, and positions
        self.text_surfaces.append(text_surface)
        self.text_rects.append(text_rect)
        self.text_positions.append(position)

        pygame.display.update()
        return text_surface

    def change_text(self, index: int, new_text: str) -> None:
        """ Updates the text in the list with a new text at the index.
            Automatically finds the coordinates of the previous text.
        """
        # Establish the previous text rect
        prev_rect = self.text_rects[index]

        # Set up the new message text and font
        color = Text.white
        text_surface, text_rect = self.text_objects(
            text=new_text, font=self.normal_font, color=color)
        # Set the proper coordinates for the new text rect (old coordinates)
        position = self.text_positions[index]   # e.g. 'topleft', 'center'
        prev_rect_position = getattr(prev_rect, position)
        setattr(text_rect, position, prev_rect_position)

        # Fill old text with black using the previous rect
        self.game_window.fill(Text.black, prev_rect)

        # Blit the new text surface
        self.game_window.blit(text_surface, text_rect)
        pygame.display.update([text_rect, prev_rect])

        # Update the list of text_rects and text_surfaces
        self.text_surfaces[index] = text_surface
        self.text_rects[index] = text_rect
