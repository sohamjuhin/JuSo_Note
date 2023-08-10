import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from reportlab.pdfgen import canvas

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")

        self.text = ScrolledText(root, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True)

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text.edit_redo)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.font_menu = tk.Menu(self.format_menu, tearoff=0)
        self.format_menu.add_cascade(label="Font", menu=self.font_menu)
        self.fonts = ["Arial", "Times New Roman", "Courier New"]
        for font in self.fonts:
            self.font_menu.add_command(label=font, command=lambda f=font: self.change_font(f))

        self.pdf_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="PDF", menu=self.pdf_menu)
        self.pdf_menu.add_command(label="Convert to PDF", command=self.convert_to_pdf)

        self.current_file = None

    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, file.read())
                self.current_file = file_path

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text.get(1.0, tk.END))
            self.current_file = file_path

    def change_font(self, font):
        self.text.configure(font=(font, 12))

    def convert_to_pdf(self):
        text_content = self.text.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if file_path:
            c = canvas.Canvas(file_path)
            c.drawString(100, 750, "Notepad Text to PDF Conversion")
            c.drawString(100, 700, "-" * 50)
            c.drawString(100, 650, text_content)
            c.save()

            messagebox.showinfo("PDF Conversion", "Text converted to PDF successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
