import tkinter as tk

# window=tk.Tk()
# window.title("Word Search Grid")
# window.config(bg="white")

# frm_b=tk.Frame(window, width=100, height=100, bg="pink")
# frm_b.pack(padx=10, pady=10)

# label=tk.Label(frm_b, text="", width=100, height=50, bg="white", relief="raised")
# label.pack(padx=5, pady=5)


import random
import string

COUNTRIES = ["CROATIA", "ITALY", "BRAZIL", "FRANCE", "SWITZERLAND", "EGYPT"]
GRID_SIZE = 15

class WordSearchGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Country Word Search")
        self.grid = self.build_word_search()
        self.labels = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_cells = []
        self.found_words = set()
        self.create_widgets()
        self.bind_events()
        self.mouse_down = False
        self.last_label = None

    def create_empty_grid(self, size):
        return [['' for _ in range(size)] for _ in range(size)]

    def fill_empty_with_random_letters(self, grid):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '':
                    grid[row][col] = random.choice(string.ascii_uppercase)
        return grid

    def place_word_in_grid(self, grid, word):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        size = len(grid)
        placed = False

        while not placed:
            dir_x, dir_y = random.choice(directions)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)
            end_x = start_x + dir_x * (len(word) - 1)
            end_y = start_y + dir_y * (len(word) - 1)

            if 0 <= end_x < size and 0 <= end_y < size:
                can_place = True
                for i in range(len(word)):
                    x = start_x + dir_x * i
                    y = start_y + dir_y * i
                    if grid[x][y] not in ('', word[i]):
                        can_place = False
                        break
                if can_place:
                    for i in range(len(word)):
                        x = start_x + dir_x * i
                        y = start_y + dir_y * i
                        grid[x][y] = word[i]
                    placed = True

    def build_word_search(self):
        grid = self.create_empty_grid(GRID_SIZE)
        for word in COUNTRIES:
            self.place_word_in_grid(grid, word)
        return self.fill_empty_with_random_letters(grid)

    def create_widgets(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                label = tk.Label(self.master, text=self.grid[i][j], font=('Consolas', 14),
                                 width=2, height=1, borderwidth=1, relief="solid", bg="white")
                label.grid(row=i, column=j)
                label.row = i
                label.col = j
                self.labels[i][j] = label

        self.word_label = tk.Label(self.master, text="Find these countries:\n" + ", ".join(COUNTRIES),
                                   font=("Arial", 12, "bold"))
        self.word_label.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE, pady=10)

        self.found_label = tk.Label(self.master, text="Found: ", font=("Arial", 12, "italic"))
        self.found_label.grid(row=GRID_SIZE + 2, column=0, columnspan=GRID_SIZE, pady=5)

    def bind_events(self):
        self.master.bind("<Button-1>", self.start_selection)
        self.master.bind("<B1-Motion>", self.track_selection)
        self.master.bind("<ButtonRelease-1>", self.end_selection)
        self.master.bind("<Leave>", lambda e: setattr(self, 'mouse_down', False))

    def start_selection(self, event):
        self.mouse_down = True 
        self.clear_selection()
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Label):
            self.select_cell(widget)

    def track_selection(self, event):
        if not self.mouse_down:
            return 
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Label) and widget != self.last_label:
            self.select_cell(widget)
            self.last_label = widget

    def end_selection(self, event):
        self.mouse_down = False
        word = ''.join([self.grid[label.row][label.col] for label in self.selected_cells])
        reversed_word = word[::-1]

        if word in COUNTRIES and word not in self.found_words:
            self.mark_word_found(word)
        elif reversed_word in COUNTRIES and reversed_word not in self.found_words:
            self.mark_word_found(reversed_word)
        else:
            self.clear_selection()
        self.last_label = None 

    def select_cell(self, label):
        if label not in self.selected_cells:
            print(f"Selected cell: ({label.row}, {label.col}) -> {label.cget('text')}")
            label.config(bg="lightblue")
            self.selected_cells.append(label)

    def clear_selection(self):
        for label in self.selected_cells:
            key = f"{label.row},{label.col}" 
            if key not in self.found_words:
                label.config(bg="white")
        self.selected_cells = []

    def mark_word_found(self, word):
        for label in self.selected_cells:
            label.config(bg="lightgreen")
            self.found_words.add(f"{label.row},{label.col}")
        self.found_words.add(word)
        self.update_found_words()
        self.selected_cells = []

    def update_found_words(self):
        found_display = "Found: " + ", ".join(sorted(self.found_words.intersection(COUNTRIES)))
        self.found_label.config(text=found_display)

        self.master.bind("Leave", lambda e: setattr(self, 'mouse_down', False))

if __name__ == "__main__":
    root = tk.Tk()
    app = WordSearchGame(root)
    root.mainloop()































