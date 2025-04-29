import tkinter as tk
import tkinter.messagebox as mbox
import random
import string


WORDS_TO_FIND = ["CROATIA", "ITALY", "BRAZIL", "FRANCE", "SWITZERLAND", "EGYPT"]
GRID_SIZE = 15

class WordSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search Game")
        self.grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.labels = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.selected_labels = []
        self.found_words = set()
        self.mouse_down = False

        self.place_words()
        self.fill_random_letters()
        self.create_grid()
        self.create_ui()
        self.bind_mouse_events()

    def place_words(self):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for word in WORDS_TO_FIND:
            placed = False
            while not placed:
                dir_x, dir_y = random.choice(directions)
                start_x = random.randint(0, GRID_SIZE - 1)
                start_y = random.randint(0, GRID_SIZE - 1)
                end_x = start_x + dir_x * (len(word) - 1)
                end_y = start_y + dir_y * (len(word) - 1)
                if 0 <= end_x < GRID_SIZE and 0 <= end_y < GRID_SIZE:
                    can_place = True
                    for i in range(len(word)):
                        x = start_x + dir_x * i
                        y = start_y + dir_y * i
                        if self.grid[x][y] not in ('', word[i]):
                            can_place = False
                            break
                    if can_place:
                        for i in range(len(word)):
                            x = start_x + dir_x * i
                            y = start_y + dir_y * i
                            self.grid[x][y] = word[i]
                        placed = True

    def fill_random_letters(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == '':
                    self.grid[i][j] = random.choice(string.ascii_uppercase)

    def create_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                lbl = tk.Label(self.root, text=self.grid[i][j], font=('Consolas', 16), width=2, height=1,
                               borderwidth=0, relief="sunken", bg="white",)
                lbl.grid(row=i, column=j)
                lbl.row, lbl.col = i, j
                self.labels[i][j] = lbl

    def create_ui(self):
        self.word_label = tk.Label(self.root, text="Find these words:\n" + ", ".join(WORDS_TO_FIND), font=('Arial', 12))
        self.word_label.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, pady=10)

        self.found_label = tk.Label(self.root, text="Found: ", font=('Arial', 12, 'italic'))
        self.found_label.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE)

    def bind_mouse_events(self):
        self.root.bind("<Button-1>", self.on_mouse_down)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_up)

    def on_mouse_down(self, event):
        self.mouse_down = True
        self.clear_selection()
        self.select_label_under_mouse(event)

    def on_mouse_drag(self, event):
        if self.mouse_down:
            self.select_label_under_mouse(event)
        
    def on_mouse_up(self, event):
        self.mouse_down = False
        word = ''.join(lbl.cget("text") for lbl in self.selected_labels)
        reversed_word = word[::-1]
        if word in WORDS_TO_FIND and word not in self.found_words:
            self.mark_found(word)
        elif reversed_word in WORDS_TO_FIND and reversed_word not in self.found_words:
            self.mark_found(reversed_word)
        elif word in WORDS_TO_FIND and word in self.found_words:
            self.mark_found(word)
        else:
            self.clear_selection()

    def select_label_under_mouse(self, event):
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        
        if isinstance(widget, tk.Label) and widget not in self.selected_labels:
            if not self.selected_labels or self.is_adjacent(widget, self.selected_labels[-1]):
                widget.config(bg="lightblue")
                self.selected_labels.append(widget)
        

    def is_adjacent(self, lbl1, lbl2):
        return abs(lbl1.row - lbl2.row) <= 1 and abs(lbl1.col - lbl2.col) <= 1
    
    def clear_selection(self):
        for lbl in self.selected_labels:
            lbl.config(bg="white")
        self.selected_labels.clear()

    def mark_found(self, word):
        for lbl in self.selected_labels:
            lbl.config(bg="lightgreen")
        self.found_words.add(word)
        self.update_found_label()
        self.selected_labels.clear()
        if len(self.found_words) == len(WORDS_TO_FIND):
            mbox.showinfo("Good job, You found all the word!")

    def update_found_label(self):
        self.found_label.config(text="Found: " + ", ".join(sorted(self.found_words)))

if __name__ == "__main__":
    root = tk.Tk()
    app = WordSearch(root)
    root.mainloop()


