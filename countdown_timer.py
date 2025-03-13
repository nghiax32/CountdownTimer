import tkinter as tk
from datetime import datetime, timedelta

DEFAULT_WORKING_TIME = ((8 * 60 + 1 * 60) + 48) * 60

class CountdownTimer:
    def __init__(self, root, working_time=DEFAULT_WORKING_TIME):
        # Set the root window
        self.root = root
        self.root.title("Countdown Timer")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="white")

        # This is the real time when you arrive at the office. Its only for showing
        self.arrive_time = datetime.now()
        
        # This is the time that company system set for you to check-in
        self.start_time = max(
            datetime.now(),
            datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
        )

        # This is the time that you should leave the office
        self.end_time = min(
            self.start_time + timedelta(seconds=working_time),
            datetime.now().replace(hour=18, minute=48, second=0, microsecond=0)
        )

        # This is the time you work overtime
        self.over_time = None

        self.is_update_start_time = False

        self.timer_label = tk.Label(root, text="", font=("Segoe UI", 20), bg="white")
        self.timer_label.pack()

        self.io_label = tk.Label(root, text="", font=("Segoe UI", 10), bg="white")
        self.io_label.pack()
        self.io_label.config(text=f"{self.arrive_time.strftime('%H:%M')}  {self.end_time.strftime('%H:%M')}")

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Update Check-in Time", command=self.update_start_time)
        self.context_menu.add_command(label="Quit", command=self.root.quit)

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)
        self.root.bind("<Button-3>", self.show_context_menu)

        self.update_timer()
        self.root.mainloop()

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_move(self, event):
        x = self.root.winfo_x() + (event.x - self.start_x)
        y = self.root.winfo_y() + (event.y - self.start_y)
        self.root.geometry(f"+{x}+{y}")

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def update_start_time(self):
        # self.start_time = callAPI()
        pass

    def update_timer(self):
        now = datetime.now()
        remaining_time = self.end_time - now
        
        if remaining_time.total_seconds() > 0:
            remaining_str = str(remaining_time).split(".")[0]
            remaining_str = ":".join(f"{int(x):02}" for x in remaining_str.split(":"))
            self.timer_label.config(text=remaining_str)
        else:
            if self.over_time is None:
                self.start_countup_time = now
                self.root.configure(bg="green")
                self.timer_label.config(fg="red", bg="green")
                self.io_label.config(bg="green")

            self.over_time = now - self.start_countup_time
            over_str = str(self.over_time).split(".")[0]
            over_str = ":".join(f"{int(x):02}" for x in over_str.split(":"))
            self.timer_label.config(text=over_str)

        self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root) 
