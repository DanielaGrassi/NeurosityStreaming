import tkinter as tk
from tkinter import messagebox
from streaming import start_streaming, stop_streaming

class NeurosityApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Neurosity Data Streaming")
        self.geometry("300x150")

        self.start_button = tk.Button(self, text="Start Streaming", command=self.start_streaming)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(self, text="Stop Streaming", command=self.stop_streaming)
        self.stop_button.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_streaming(self):
        try:
            start_streaming()
            messagebox.showinfo("Info", "Data streaming started.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start streaming: {e}")

    def stop_streaming(self):
        try:
            stop_streaming()
            messagebox.showinfo("Info", "Data streaming stopped.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop streaming: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            stop_streaming()
            self.destroy()
