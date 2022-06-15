import os

import pygame

from assets.board import Board
from assets.buttons.add_arrow_button import AddArrowButton
from assets.buttons.auto_solve_button import AutoSolveButton
from assets.buttons.delete_arrow_button import DeleteArrowButton
from assets.buttons.end_session_button import EndSessionButton
from assets.buttons.gen_new_board_button import GenNewBoardButton
from assets.messages.correct_message import CorrectMessage
from assets.messages.start_message import StartMessage
from assets.messages.wrong_message import WrongMessage
from control import colors
from control.screen import Screen
from control.settings import Settings
from control.states import States
from control.time_control import clock
from utils.core import Core


class ArrowsGame:
    """Main app class"""

    def __init__(self):
        """
        Init game objects
        """
        pygame.init()

        # initialize game objects
        self.board: Board = Board()
        self.gen_new_board_button: GenNewBoardButton = GenNewBoardButton()
        self.add_arrows_buttons: list = []
        self.delete_arrow_button: DeleteArrowButton | None = None
        self.end_session_button: EndSessionButton | None = None
        self.auto_solve_button = AutoSolveButton()
        self.message: StartMessage | WrongMessage | CorrectMessage | None = StartMessage()

        Screen.set_caption('Arrows')

    def _handle_events(self) -> None:
        """
        Handle pygame events queue
        """
        for event in pygame.event.get():
            # handle quit event
            if event.type == pygame.QUIT:
                exit(0)

            # handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # active game events
                if States.current_state == States.GAME_ACTIVE:
                    # button click events
                    self._handle_gen_new_board_event(mouse_pos)
                    self._handle_add_arrow_event(mouse_pos)
                    self._handle_delete_arrow_event(mouse_pos)
                    self._handle_end_session_event(mouse_pos)
                    self._handle_auto_solve_event(mouse_pos)
                    # arrow and number selection event
                    self._handle_arrow_selection_event(mouse_pos)
                    self._handle_number_selection_event(mouse_pos)

                # non-active game events
                elif States.current_state == States.GAME_START:
                    self._handle_start_message_events(mouse_pos)
                elif States.current_state == States.GAME_END_WRONG:
                    self._handle_end_message_wrong_events(mouse_pos)
                elif States.current_state == States.GAME_END_CORRECT:
                    self._handle_end_message_correct_events(mouse_pos)

    def _handle_auto_solve_event(self, mouse_pos: tuple[int, int]) -> None:
        """
        Uses arrows generated for number generation as the solution

        :return: None
        :param mouse_pos: Mouse position
        """

        if self.auto_solve_button.is_clicked(mouse_pos):
            self.board.handle_auto_solve()
            self.board.update_arrows()
            self.board.deselect_all()
            self.end_session_button = EndSessionButton()

    def _handle_gen_new_board_event(self, mouse_pos: tuple[int, int]) -> None:
        """
        Generate new board if gen_new_board_button is clicked, clear add and delete arrow buttons

        :return: None
        :param mouse_pos: Mouse position
        """
        if self.gen_new_board_button.is_clicked(mouse_pos):
            self.board = Board()
            self.add_arrows_buttons.clear()
            self.delete_arrow_button = None

    def _handle_add_arrow_event(self, mouse_pos: tuple[int, int]) -> None:
        """
        Set arrow image and direction of select arrow grid square if add_arrow_button is clicked. Updates selection for
        correct highlighting of numbers that the arrow points to. Creates delete arrow button. Creates and end session
        button if every arrow grid square is filled and gets rid of error numbers highlighting.

        :return: None
        :param mouse_pos: Mouse position
        """
        for add_arrow_button in self.add_arrows_buttons:
            if add_arrow_button.is_clicked(mouse_pos):
                self.board.set_arrow_image(*add_arrow_button.handle_click())
                self.board.update_selection()
                self.delete_arrow_button = DeleteArrowButton(len(self.add_arrows_buttons))

                filled_arrow_squares = [arrow for arrow in self.board.arrows if arrow.direction]
                if len(filled_arrow_squares) == 2 * (Settings.grid_count.x + Settings.grid_count.y):
                    self.end_session_button = EndSessionButton()
                if self.board.wrong_numbers:
                    self.board.dehighlight_errors()
                    self.board.wrong_numbers.clear()

    def _handle_delete_arrow_event(self, mouse_pos: tuple[int, int]) -> None:
        """
        Sets selected image and direction to None. Updates selection for correct highlighting of numbers that the arrow
        points to. Deletes delete arrow button and end session button, gets rid of error numbers highlighting.

        :return: None
        :param mouse_pos: Mouse position
        """
        if not self.delete_arrow_button:
            return
        if self.delete_arrow_button.is_clicked(mouse_pos):
            self.board.set_arrow_image(None, None, colors.highlighted_blue)
            self.delete_arrow_button = None
            self.board.update_selection()
            self.end_session_button = None
            if self.board.wrong_numbers:
                self.board.dehighlight_errors()
                self.board.wrong_numbers = []

    def _handle_end_session_event(self, mouse_pos: tuple[int, int]) -> None:
        """
        Evaluates correctness of arrows and sets appropriate game state

        :return: None
        :param mouse_pos: Mouse position
        """
        if not self.end_session_button:
            return
        if self.end_session_button.is_clicked(mouse_pos):
            self.board.check_correctness()
            if self.board.wrong_numbers:
                States.current_state = States.GAME_END_WRONG
                self.message = WrongMessage()
            else:
                States.current_state = States.GAME_END_CORRECT
                self.message = CorrectMessage()

    def _handle_arrow_selection_event(self, mouse_pos: tuple[int, int]) -> None:
        """
        Highlights selected arrow and numbers that it points to. Adds button for adding arrows to selected square.

        :return: None
        :param mouse_pos: Mouse position
        """
        if self.board.check_arrow_selection(mouse_pos):
            self.board.handle_arrow_selection(mouse_pos)
            arrow = self.board.get_arrow(mouse_pos)
            self.add_arrows_buttons.clear()
            self.delete_arrow_button = None
            if arrow.selected:
                possible_directions = Core.get_possible_directions(arrow.arrow_set, arrow.arrow_num)
                for i, direction in enumerate(possible_directions):
                    self.add_arrows_buttons.append(AddArrowButton(direction, i))
                if arrow.direction:
                    self.delete_arrow_button = DeleteArrowButton(len(self.add_arrows_buttons))

    def _handle_number_selection_event(self, mouse_pos: tuple[int, int]) -> None:
        """
        Highlights selected number and arrows that point to it. Clears all arrow manipulation buttons

        :return: None
        :param mouse_pos: Mouse position
        """
        if self.board.check_number_selection(mouse_pos):
            self.board.handle_number_selection(mouse_pos)
            self.add_arrows_buttons.clear()
            self.delete_arrow_button = None

    def _handle_start_message_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Sets game state to active and deletes message.

        :return: None
        :param mouse_pos: Mouse position
        """
        if self.message.collide_rect.collidepoint(mouse_pos):
            States.current_state = States.GAME_ACTIVE
            self.message = None

    def _handle_end_message_correct_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles end message button click when game is over and all numbers on grid match with number of arrows that
        point to it.

        :return: None
        :param mouse_pos: Mouse position
        """
        if self.message.collide_rect_again.collidepoint(mouse_pos):
            States.current_state = States.GAME_ACTIVE
            self.board = Board()
            self.message = None
            self.add_arrows_buttons.clear()
            self.delete_arrow_button = None
            self.end_session_button = None
        elif self.message.collide_rect_quit.collidepoint(mouse_pos):
            exit(0)

    def _handle_end_message_wrong_events(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles end message button click when game is over and at least one number on grid don't with number of arrows
        that point to it.

        :return: None
        :param mouse_pos: Mouse position
        """
        if self.message.collide_rect_continue.collidepoint(mouse_pos):
            self.board.highlight_errors()
            States.current_state = States.GAME_ACTIVE
            self.message = None
            self.board.deselect_all()
            self.add_arrows_buttons.clear()
            self.delete_arrow_button = None
            self.end_session_button = None
        elif self.message.collide_rect_quit.collidepoint(mouse_pos):
            exit(0)

    def _update_screen(self):
        """
        Render updated objects on screen and update screen
        """
        # fill background
        Screen.surface.fill(Screen.bg_color)

        # redraw objects based on current state
        if States.current_state == States.GAME_ACTIVE:
            self.board.draw()
            self.gen_new_board_button.draw()
            self.auto_solve_button.draw()
            for add_replace_button in self.add_arrows_buttons:
                add_replace_button.draw()
            if self.delete_arrow_button:
                self.delete_arrow_button.draw()
            if self.end_session_button:
                self.end_session_button.draw()
        if States.current_state in [States.GAME_START, States.GAME_END_CORRECT, States.GAME_END_WRONG]:
            self.message.draw()

        # update screen to expose newly drawn objects
        pygame.display.update()

    def run(self):
        """
        Run main game loop
        """
        while True:
            self._handle_events()
            self._update_screen()
            clock.tick(Settings.fps)


if __name__ == '__main__':
    # set absolute path when launching from shortcuts
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # create and run game
    arrows_game = ArrowsGame()
    arrows_game.run()
