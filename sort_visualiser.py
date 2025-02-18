from bar import Bar
import tkinter as tk
import random
from ttkthemes import themed_tk as theme
from tkinter import ttk as ttk
from tkinter import messagebox
from solver import Solver


class SortVisualiser:

    def __init__(self):
        self.algorithms = ['Selection Sort', 'Insertion Sort', 'Bubble Sort', 'Merge Sort', 'Quick Sort']
        self.graph_width, self.graph_height = 1430, 810
        self.root = theme.ThemedTk()
        self.menu_frame = ttk.Frame(self.root, width=self.graph_width / 2)
        self.canvas = tk.Canvas(self.root, height=self.graph_height, width=self.graph_width, bg='#333333')
        self.n_bars = 100
        self.bars = []
        self.bar_width = 0
        self.y_scale = 0
        self.solve_mode = 0
        self.colours = ['#FF5733', '#DAF7A6', '#581845', '#900C3F', '#FFC300', '#FF33FF']  # Changed colors
        self.colour = random.sample(self.colours, k=1)

        self.is_solving = False
        self.is_rendering = False

        self.config_root()
        self.config_menu()
        self.config_canvas()

        self.root.mainloop()

    def config_root(self):
        self.root.title('Sorting Algorithm Visualisation')
        self.root.resizable(False, False)
        self.root.set_theme('radiance')

    def config_menu(self):
        self.menu_frame.grid(row=0, column=0, sticky='new')

        ttk.Button(self.menu_frame, text='Visualise', command=self.validate_setup)
        ttk.Button(self.menu_frame, text='Regenerate', command=self.clean_canvas)

        current_algo = tk.StringVar()
        current_algo.set(self.algorithms[self.solve_mode])

        algorithms_menu = ttk.OptionMenu(self.menu_frame, current_algo, self.algorithms[0], *self.algorithms, command=self.algorithm_change)
        algorithms_menu.config(width=15)

        ttk.Label(self.menu_frame, text='Array Size', anchor='e')
        callback = self.menu_frame.register(self.only_numeric_input)
        ttk.Entry(self.menu_frame, validate="key", validatecommand=(callback, "%P")).insert(0, str(self.n_bars))

        for c, child in enumerate(self.menu_frame.winfo_children()):
            pad = 0 if isinstance(child, tk.Button) else 5
            child.grid_configure(row=0, column=c, sticky='ew', padx=pad, pady=pad)

    def config_canvas(self):
        self.canvas.bind('<Configure>', self.config_bars)
        self.canvas.grid(row=1, column=0)

    def config_bars(self, event=None):
        if self.is_solving or self.n_bars < 2:
            self.is_rendering = False
            return

        self.bars = []
        self.bar_width = self.graph_width / self.n_bars
        values = random.sample(range(0, self.n_bars), self.n_bars)

        self.y_scale = self.graph_height / max(values)

        for i, value in enumerate(values):
            bar = Bar(self.bar_width, i, value * self.y_scale, self)
            self.bars.append(bar)
            self.render_bar(bar)

        self.is_rendering = False

    def clean_canvas(self):
        if self.is_rendering or self.is_solving:
            return
        self.is_rendering = True

        for bar in self.bars:
            self.canvas.delete(bar.shape)

        self.colour = random.sample(self.colours, k=1)

        self.config_bars()

    def change_array_size(self, value):
        if self.is_rendering or self.is_solving:
            return

        self.n_bars = int(float(value))
        self.clean_canvas()

    def algorithm_change(self, *args):
        self.solve_mode = self.algorithms.index(args[0])

    def validate_setup(self):
        if self.bars is None or self.is_solving or self.is_rendering:
            return

        self.is_solving = True

        Solver(self.bars, self.n_bars, self.solve_mode, self)

        self.is_solving = False

    def render_bar(self, bar):
        bar.shape = self.canvas.create_rectangle(bar.x1, 0, bar.x2, bar.value, fill=self.colour)
        self.root.update()

    def update_bar(self, bar, fill):
        self.canvas.coords(bar.shape, bar.x1, 0, bar.x2, bar.value)
        self.canvas.itemconfig(bar.shape, fill=fill)
        self.root.update()
        self.canvas.itemconfig(bar.shape, fill=self.colour)

    def only_numeric_input(self, i):
        try:
            if i == '':
                self.n_bars = 100
            else:
                self.n_bars = int(i)
            return True
        except Exception as e:
            tk.messagebox.showerror('Array Size Error', 'Please enter a positive integer for the array size or leave blank 100')
            print(e)
            return False


if __name__ == '__main__':
    visualiser = SortVisualiser()
