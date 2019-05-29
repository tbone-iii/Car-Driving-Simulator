import pygame
import config


class Text:
    """ Text class handles all text displays on a game window,
        which is passed by the game handle. Each instance of Text
        is its own type of text (e.g. velocity output, position output),
        allowing for easy enabling and disabling of text display.
    """
    font_size = config.default_font_size  # default font size
    white = config.WHITE
    black = config.BLACK

    def __init__(self, game_window):
        """ Class constructor initializing with the
            pygame game_window/screen handle.
        """
        self.game_window = game_window
        self.text_surfaces = []
        self.text_rects = []

    def text_objects(self, text: str, font, color: tuple):
        """ Takes text and pygame font and returns a text surface and rect.
        """
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def message_display(self, text, x: int, y: int, position: str = 'topleft',
                        color: tuple = white, fontsize=font_size):
        """ Takes text and places it at (x, y) coordinates.
            The position argument is a string representating the
            rectangle origin location.

            For example, position can be 'bottomright'
            or 'center'.
        """
        normal_font = pygame.font.Font('Marvelous-Sans-Demo.otf', fontsize)
        text_surface, text_rect = self.text_objects(text, normal_font, color)

        # TODO: Use dictionary to simplify this chain of if-statements below.
        if position is 'bottomright':
            text_rect.bottomright = (x, y)
        elif position is 'bottomleft':
            text_rect.bottomleft = (x, y)
        elif position is 'center':
            text_rect.center = (x, y)
        elif position is 'topleft':
            text_rect.topleft = (x, y)
        elif position is 'topright':
            text_rect.topright = (x, y)

        # Fills previous text with black rectangle.
        self.game_window.fill(Text.black, text_rect)
        # Blit the new text onto the surface.
        self.game_window.blit(text_surface, text_rect)

        # Append list of text_surfaces
        self.text_surfaces.append(text_surface)
        self.text_rects.append(text_rect)

        pygame.display.update()
        return text_surface

    def change_text(self, index: int, new_text: str,
                    fontsize=font_size) -> None:
        """ Updates the text in the list with a new text at the index.
            Automatically finds the coordinates of the previous text.
        """
        # Establish the previous text rect
        prev_rect = self.text_rects[index]

        # Set up the new message text and font
        color = Text.white
        normal_font = pygame.font.Font('Marvelous-Sans-Demo.otf', fontsize)
        text_surface, text_rect = self.text_objects(new_text, normal_font,
                                                    color)
        # Set the proper coordinates for the new text rect (old coordinates)
        # TODO: Generalize topleft, center, etc. below
        text_rect.topleft = prev_rect.topleft

        # Fill old text with black using the previous rect
        self.game_window.fill(Text.black, prev_rect)

        # Blit the new text surface
        self.game_window.blit(text_surface, text_rect)
        pygame.display.update(text_rect)

        # Update the list of text_rects and text_surfaces
        self.text_surfaces[index] = text_surface
        self.text_rects[index] = text_rect