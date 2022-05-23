import tkinter as tk


class InvertMatrixApp:
    """Main app class"""

    def __init__(self):
        self.tk = tk.Tk()

        self._create_objects()

    def _create_objects(self):
        label = tk.Label('Hello world')

    def run(self):
        """Run main loop"""
        self.tk.mainloop()


if __name__ == '__main__':
    invert_matrix_app = InvertMatrixApp()
    invert_matrix_app.run()
