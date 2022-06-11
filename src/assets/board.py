import pygame
from pygame.math import Vector2

from assets.arrow import Arrow
from assets.grid_squares.arrow_grid_square import ArrowGridSquare
from assets.grid_squares.number_grid_square import NumberGridSquare
from assets.number import Number
from control import colors
from control.grid_position import GridPosition
from control.screen import Screen
from control.settings import Settings
from utils.core import Core


class Board:
    """Class for game board that holds arrows and numbers"""

    def __init__(self):
        # frame that surrounds grid squares that hold numbers
        self.frame_size = tuple(Settings.grid_count * Settings.grid_size)
        self.frame_rect = pygame.Rect(
            tuple(GridPosition((0, 0)).get_coords()),
            self.frame_size
        )
        self.frame_color = colors.board_frame
        self.frame_width = 5

        # generate random values matrix and arrows dictionary
        Core.gen_numbers()
        arrows = Core.arrows
        numbers = Core.numbers

        # wrong numbers list for highlighting at the end of the game
        self.wrong_numbers = []

        # create grid squares group that hold numbers
        self.numbers = []
        for col, numbers_col in enumerate(numbers):
            for row, number in enumerate(numbers_col):
                self.numbers.append(NumberGridSquare(
                    Number(number).image,
                    col, row, number
                ))

        # create empty grid squares that hold arrows
        self.arrows = []
        for arrows_set_direction, arrows_set in arrows.items():
            for arrow_num, arrow in enumerate(arrows_set):
                self.arrows.append(ArrowGridSquare(
                    None, arrows_set_direction, arrow_num
                ))

        # current selection indicator for managing selections
        self.currently_selected: ArrowGridSquare | NumberGridSquare | None = None

    def clear_arrows(self) -> None:
        """Sets all arrow square images to None and their direction"""
        for arrow in self.arrows:
            arrow.image = None
            arrow.direction = None

    def update_arrows(self) -> None:
        """Updates all arrows to those stored in Core class"""

        self.arrows = []
        for arrows_set_direction, arrows_set in Core.arrows.items():
            for arrow_num, arrow in enumerate(arrows_set):
                self.arrows.append(ArrowGridSquare(
                    Arrow(arrow).image, arrows_set_direction, arrow_num, arrow
                ))

    def update_selection(self) -> None:
        """
        Deselect and select object for correct arrow adding and deletion
        """
        selected_arrow = self.get_selected_arrow()
        if selected_arrow:
            self.handle_arrow_selection(selected_arrow.position.get_coords_center())
            self.handle_arrow_selection(selected_arrow.position.get_coords_center())

    def deselect_all(self) -> None:
        """
        Deselect any selection
        """
        if isinstance(self.currently_selected, ArrowGridSquare):
            self.handle_arrow_selection(self.currently_selected.position.get_coords_center())
        if isinstance(self.currently_selected, NumberGridSquare):
            self.handle_number_selection(self.currently_selected.position.get_coords_center())

    def get_selected_arrow(self) -> ArrowGridSquare:
        """
        Return selected arrow object if any were selected

        :return: Arrow object that is selected if any
        """
        for arrow in self.arrows:
            if arrow.selected:
                return arrow

    def dehighlight_errors(self) -> None:
        """
        Get rid of highlighting on numbers that don't match
        """
        for number in self.numbers:
            if tuple(number.position.grid_square_pos) in self.wrong_numbers:
                number.dehighlight_error()

    def highlight_errors(self) -> None:
        """
        Highlight numbers that don't match
        """
        for number in self.numbers:
            if tuple(number.position.grid_square_pos) in self.wrong_numbers:
                number.highlight_error()

    def check_correctness(self) -> None:
        """
        Load current arrows and numbers to core class and evaluate correctness
        """
        for arrow in self.arrows:
            Core.arrows[arrow.arrow_set][arrow.arrow_num] = arrow.direction
        for number in self.numbers:
            Core.numbers[number.col][number.row] = number.value
        self.wrong_numbers = Core.evaluate_correctness()

    def get_arrow(self, pos: tuple[int, int]) -> ArrowGridSquare:
        """
        Get arrow by pixel position

        :return: arrow that is under given position
        :param pos: position to get arrow by
        """
        for arrow in self.arrows:
            if arrow.rect.collidepoint(pos):
                return arrow

    def set_arrow_image(self, image: pygame.Surface | None, direction: tuple[int, int] | None,
                        highlight_color: tuple[int]) -> None:
        """
        Set arrow image for selected arrow square if any

        :return: None
        :param image: New image to set
        :param direction: direcion of arrow on image to set direction attribute
        :param highlight_color: color that object was highlighted to restore it
        """
        for arrow in self.arrows:
            if arrow.selected:
                arrow.set_image(image, direction)
                arrow.select(highlight_color)

    def handle_auto_solve(self):
        """
        Use initially generated arrows for number generation as solution
        """
        for arrow, core_arrow in zip(self.arrows, Core.arrows):
            arrow.set_image(Arrow(core_arrow).image, core_arrow)

    def check_arrow_selection(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Check if arrow was selected

        :return: True if arrow under current mouse position is selected
        :param mouse_pos: Mouse position in pixel coordinates
        """
        for arrow in self.arrows:
            if arrow.rect.collidepoint(mouse_pos):
                return True
        return False

    def check_number_selection(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Check if number was selected

        :return: True if number under current mouse position is selected
        :param mouse_pos: Mouse position in pixel coordinates
        """
        for number in self.numbers:
            if number.rect.collidepoint(mouse_pos):
                return True
        return False

    def handle_arrow_selection(self, mouse_pos: tuple[int, int]) -> None:
        """
        Select arrow and numbers it points to

        :return: None
        :param mouse_pos: Current mouse position
        """
        # deselect previously selected numbers and its arrows
        if isinstance(self.currently_selected, NumberGridSquare):
            pointing_arrows = Core.get_pointings(Vector2(self.currently_selected.col, self.currently_selected.row))
            for arrow in self.arrows:
                if (arrow.arrow_set, arrow.arrow_num) in pointing_arrows:
                    arrow.deselect(colors.highlighted_yellow)
            self.currently_selected.deselect(colors.highlighted_blue)
            self.currently_selected = None

        # deselect previous arrow and its spanned numbers
        if isinstance(self.currently_selected, ArrowGridSquare):
            for number in self.numbers:
                if number.selected:
                    number.deselect(colors.highlighted_yellow)
            self.currently_selected.deselect(colors.highlighted_blue)

        # get currently selected arrows
        curr_arrow = None
        for arrow in self.arrows:
            if arrow.rect.collidepoint(mouse_pos):
                curr_arrow = arrow
                break

        # select current arrow and spanned numbers
        if curr_arrow != self.currently_selected:
            pointed_numbers = Core.get_span(curr_arrow.position.grid_square_pos, curr_arrow.direction)
            for number in self.numbers:
                if (number.col, number.row) in pointed_numbers:
                    number.select(colors.highlighted_yellow)
            curr_arrow.select(colors.highlighted_blue)
            self.currently_selected = curr_arrow
        else:
            self.currently_selected = None

    def handle_number_selection(self, mouse_pos: tuple[int, int]):
        """
        Select number and arrows that point to it

        :return: None
        :param mouse_pos: Current mouse position
        """
        # deselect previously selected arrow and numbers that it points to
        if isinstance(self.currently_selected, ArrowGridSquare):
            pointing_numbers = Core.get_span(self.currently_selected.position.grid_square_pos,
                                             self.currently_selected.direction)
            for number in self.numbers:
                if (number.col, number.row) in pointing_numbers:
                    number.deselect(colors.highlighted_yellow)
            self.currently_selected.deselect(colors.highlighted_blue)
            self.currently_selected = None

        # deselect previous number and all selected arrows if there is
        if isinstance(self.currently_selected, NumberGridSquare):
            for arrow in self.arrows:
                if arrow.selected:
                    arrow.deselect(colors.highlighted_yellow)
            self.currently_selected.deselect(colors.highlighted_blue)

        # get previously selected and currently selected numbers
        curr_num = None
        for number in self.numbers:
            if number.rect.collidepoint(mouse_pos):
                curr_num = number
                break

        # select current number and arrows if there is
        for arrow in self.arrows:
            Core.arrows[arrow.arrow_set][arrow.arrow_num] = arrow.direction
        if curr_num != self.currently_selected:
            pointed_arrows = Core.get_pointings(Vector2(curr_num.col, curr_num.row))
            for arrow in self.arrows:
                if (arrow.arrow_set, arrow.arrow_num) in pointed_arrows:
                    arrow.select(colors.highlighted_yellow)
            curr_num.select(colors.highlighted_blue)
            self.currently_selected = curr_num
        else:
            self.currently_selected = None

    def draw(self) -> None:
        """
        Draw object to given surface
        """
        # draw numbers grid squares
        for number in self.numbers:
            number.draw()

        # draw arrows grid squares
        for arrow in self.arrows:
            arrow.draw()

        # draw frame
        pygame.draw.rect(Screen.surface, self.frame_color, self.frame_rect, self.frame_width)
