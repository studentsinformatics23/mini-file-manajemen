import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, filedialog
from file_system import MiniFileSystem
import io
import sys

class MiniFileSystemGUI:
    def _init_(self, root):
        self.fs = MiniFileSystem()
        self.root = root
        self.root.title("Mini File System Emulator")
        self.dark_mode = False
        self.set_colors()

        # Judul
        self.title = tk.Label(root, text="Mini File System Emulator", font=("Helvetica", 16, "bold"))
        self.title.pack(pady=10)

        # Frame tombol
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=5)

        # Tombol fungsi
        buttons = [
            ("Create File", self.create_file),
            ("Write File", self.write_file),
            ("Read File", self.read_file),
            ("Delete File", self.delete_file),
            ("Truncate File", self.truncate_file),
            ("List Files/Dirs", self.list_dir),
            ("Show Disk", self.show_disk),
            ("Show Metadata", self.show_metadata),
            ("Make Directory", self.make_dir),
            ("Change Directory", self.change_dir),
            ("Save FS", self.save_fs),
            ("Load FS", self.load_fs),
            ("Exit", root.quit)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(self.btn_frame, text=text, command=cmd, width=15, font=("Helvetica", 10))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)

        # Dark mode toggle checkbox
        self.dark_var = tk.IntVar()
        self.dark_check = tk.Checkbutton(root, text="Dark Mode", variable=self.dark_var, command=self.toggle_dark_mode, font=("Helvetica", 10))
        self.dark_check.pack()

        # Output area
        self.output = scrolledtext.ScrolledText(root, width=70, height=15, font=("Courier", 10))
        self.output.pack(padx=10, pady=10)

        # Status bar dengan path dan jumlah file
        self.status = tk.Label(root, font=("Helvetica", 10, "italic"))
        self.status.pack(side=tk.BOTTOM, pady=5)

        self.apply_colors()
        self.update_status()

    def set_colors(self):
        # Light mode colors
        self.light_bg = "#e6f0f7"
        self.light_btn_bg = "#cce0ff"
        self.light_fg = "#003366"
        self.light_output_bg = "#f7fbff"
        self.light_status_bg = "#e6f0f7"

        # Dark mode colors
        self.dark_bg = "#2e2e2e"
        self.dark_btn_bg = "#4a90e2"
        self.dark_fg = "#ffffff"
        self.dark_output_bg = "#1e1e1e"
        self.dark_status_bg = "#2e2e2e"

    def apply_colors(self):
        if self.dark_mode:
            bg = self.dark_bg
            btn_bg = self.dark_btn_bg
            fg = self.dark_fg
            output_bg = self.dark_output_bg
            status_bg = self.dark_status_bg
        else:
            bg = self.light_bg
            btn_bg = self.light_btn_bg
            fg = self.light_fg
            output_bg = self.light_output_bg
            status_bg = self.light_status_bg

        self.root.configure(bg=bg)
        self.title.configure(bg=bg, fg=fg)
        self.btn_frame.configure(bg=bg)
        for widget in self.btn_frame.winfo_children():
            widget.configure(bg=btn_bg, fg=fg, activebackground=btn_bg)
        self.dark_check.configure(bg=bg, fg=fg, selectcolor=bg, activebackground=bg)
        self.output.configure(bg=output_bg, fg=fg, insertbackground=fg)
        self.status.configure(bg=status_bg, fg=fg)

    def toggle_dark_mode(self):
        self.dark_mode = bool(self.dark_var.get())
        self.apply_colors()

    def update_status(self):
        path = self.fs.get_current_path()
        files = self.fs.list_files_only()
        total_files = len(files.split(", ")) if files != "No files available." else 0
        self.status.config(text=f"Current Directory: {path}    |    Total Files: {total_files}")

    def display(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def create_file(self):
        fname = simpledialog.askstring("Create File", "File name:")
        if fname:
            res = self.fs.create(fname)
            self.display(res)
            self.update_status()

    def write_file(self):
        files = self.fs.list_files_only()
        messagebox.showinfo("Available Files", f"Files: {files}")
        fname = simpledialog.askstring("Write File", "File name:")
        if not fname:
            return
        data = simpledialog.askstring("Write File", "Data to write:")
        if data is None:
            return
        res = self.fs.write(fname, data)
        self.display(res)
        self.update_status()

    def read_file(self):
        files = self.fs.list_files_only()
        messagebox.showinfo("Available Files", f"Files: {files}")
        fname = simpledialog.askstring("Read File", "File name:")
        if fname:
            content = self.fs.read(fname)
            self.display(f"Content of '{fname}':\n{content}")
            self.update_status()

    def delete_file(self):
        files = self.fs.list_files_only()
        messagebox.showinfo("Available Files", f"Files: {files}")
        fname = simpledialog.askstring("Delete File", "File name:")
        if fname:
            res = self.fs.delete(fname)
            self.display(res)
            self.update_status()

    def truncate_file(self):
        files = self.fs.list_files_only()
        messagebox.showinfo("Available Files", f"Files: {files}")
        fname = simpledialog.askstring("Truncate File", "File name:")
        if fname:
            res = self.fs.truncate(fname)
            self.display(res)
            self.update_status()

    def list_dir(self):
        listing = self.fs.ls()
        self.display("Directory Listing:\n" + listing)
        self.update_status()

    def show_disk(self):
        buffer = io.StringIO()
        sys.stdout = buffer
        self.fs.show_disk()
        sys.stdout = sys._stdout_
        output = buffer.getvalue()
        self.display(output)
        self.update_status()

    def show_metadata(self):
        files = self.fs.list_files_only()
        messagebox.showinfo("Available Files", f"Files: {files}")
        fname = simpledialog.askstring("Show Metadata", "File name:")
        if fname:
            meta = self.fs.show_metadata(fname)
            self.display(meta)
            self.update_status()

    def make_dir(self):
        dname = simpledialog.askstring("Make Directory", "Directory name:")
        if dname:
            res = self.fs.mkdir(dname)
            self.display(res)
            self.update_status()

    def change_dir(self):
        dname = simpledialog.askstring("Change Directory", "Directory name (.. to go up):")
        if dname:
            res = self.fs.cd(dname)
            self.display(res)
            self.update_status()

    def save_fs(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", ".json"), ("All files", ".*")],
            initialdir="data",
            title="Save File System As"
        )
        if path:
            res = self.fs.save_to_file(path)
            self.display(res)

    def load_fs(self):
        path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", ".json"), ("All files", ".*")],
            initialdir="data",
            title="Open File System"
        )
        if path:
            res = self.fs.load_from_file(path)
            self.display(res)
            self.update_status()

if __name__ == "_main_":
    root = tk.Tk()
    app = MiniFileSystemGUI(root)
    root.mainloop()