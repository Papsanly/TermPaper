import pygame
from screen import Screen
from settings import Settings
from time_control import clock


class ArrowsGame:
    """Main app class"""

    def __init__(self):
        """Init game objects"""
        pygame.init()

        # get screen surface to create window
        self.screen = Screen.surface
        Screen.set_caption('Arrows')

    def _handle_events(self):
        """Handle pygame events queue"""
        for event in pygame.event.get():
            # handle quit event
            if event.type == pygame.QUIT:
                exit(0)

    def _update_objects(self):
        """Update game object attributes"""
        pass

    def _update_screen(self):
        """Render updated objects on screen and update screen"""
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
