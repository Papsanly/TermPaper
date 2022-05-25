import os

import pygame

from assets.board import Board
from assets.buttons.gen_new_board_button import GenNewBoardButton
from control.screen import Screen
from control.settings import Settings
from control.time_control import clock

# set absolute path when launching from shortcuts
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class ArrowsGame:
    """Main app class"""

    def __init__(self):
        """Init game objects"""
        pygame.init()

        # create game objects
        self.board = Board()
        self.gen_new_board_button = GenNewBoardButton()

        # get screen surface to create window
        self.screen = Screen.surface
        Screen.set_caption('Arrows')

    def _handle_events(self):
        """Handle pygame events queue"""
        for event in pygame.event.get():
            # handle quit event
            if event.type == pygame.QUIT:
                exit(0)

            # handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.gen_new_board_button.is_clicked(mouse_pos):
                    self.board = self.gen_new_board_button.click()

    def _update_objects(self):
        """Update game object attributes"""
        pass

    def _update_screen(self):
        """Render updated objects on screen and update screen"""
        # fill background
        Screen.surface.fill(Screen.bg_color)

        # redraw objects
        self.board.draw(Screen.surface)
        self.gen_new_board_button.draw(Screen.surface)

        # update screen to expose newly drawn objects
        pygame.display.update()

    def run(self):
        """Run main game loop"""
        while True:
            self._handle_events()
            self._update_objects()
            self._update_screen()
            clock.tick(Settings.fps)


if __name__ == '__main__':
    arrows_game = ArrowsGame()
    arrows_game.run()
