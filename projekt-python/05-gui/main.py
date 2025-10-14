import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.colorchooser as cc
import random

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Demo GUI")
        self.root.geometry("800x600")

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        m_tasks = tk.Menu(menubar, tearoff=False)
        m_tasks.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="System", menu=m_tasks)

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        m_colors = tk.Menu(menubar, tearoff=False)
        m_colors.add_command(label="Red", command=lambda: self.set_bg("red"))
        m_colors.add_command(label="Green", command=lambda: self.set_bg("green"))
        m_colors.add_command(label="Blue", command=lambda: self.set_bg("blue"))
        menubar.add_cascade(label="Colors", menu=m_colors)

        m_graphics = tk.Menu(menubar, tearoff=False)
        m_graphics.add_command(label="Magické čáry", command=lambda: self.magic_barcode(5, 20))
        m_graphics.add_command(label="Šachovnice", command=lambda: self.chessboard_dialog())
        m_graphics.add_command(label="Terč", command=lambda: self.set_bg("blue"))
        menubar.add_cascade(label="Graphics", menu=m_graphics)

    def _canvas_size(self) -> tuple:
        w = self.canvas.winfo_width() or self.root.winfo_width() or 640
        h = self.canvas.winfo_height() or self.root.winfo_height() or 640
        return w, h

    def magic_barcode(self, min: int, max: int) -> None:
        self.clear()
        self.canvas.config(bg="white")

        width, height = self._canvas_size()

        x = 0
        while x < width:
            w = random.randrange(min, max, 2)
            self.canvas.create_line(x + w/2, 0, x + w/2, height, fill="#"+("%06x"%random.randint(0,16777215)), width=w)
            x += w

    def chessboard(self, size: int, light: str = "white", dark: str = "black") -> None:
        self.clear()
        self.canvas.config(bg=light)

        width, height = self._canvas_size()

        tile_width = width / size
        tile_height = height / size

        for y in range(size):
            for x in range(size):
                if (x + y) % 2 == 0:
                    self.canvas.create_rectangle(x * tile_width, y * tile_height, (x + 1) * tile_width, (y + 1) * tile_height, fill=dark, outline="")

    def chessboard_dialog(self) -> None:
        size = sd.askinteger(title="Šachovnice", prompt="Zadej počet polí", minvalue=2, maxvalue=20, initialvalue=8, parent=self.root)
        light = cc.askcolor(title="Vyber pozadí")[1]
        dark = cc.askcolor(title="Vyber barvu")[1]
        self.chessboard(size=size, light=light, dark=dark)

    def set_bg(self, color: str) -> None:
        self.canvas.config(bg=color)

    def clear(self) -> None:
        self.canvas.delete("all")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()
