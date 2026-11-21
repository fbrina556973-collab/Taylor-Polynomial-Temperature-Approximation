import math
import tkinter as tk
from tkinter import ttk, messagebox

A = 0  # Expansion point


# True temperature function
def true_temp(t):
    return 30 + 5 * math.sin(t)


# Third-degree Taylor polynomial
def taylor_p3(t):
    return 30 + 5 * t - (5 * t ** 3) / 6


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Taylor Polynomial Temperature Approximation")

        # Window size and center position
        width = 750
        height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(600, 500)
        self.resizable(True, True)

        # Main container
        main = ttk.Frame(self, padding=20)
        main.pack(fill="both", expand=True)

        main.columnconfigure(0, weight=1)
        main.rowconfigure(3, weight=1)

        # Title
        ttk.Label(
            main,
            text="Taylor Polynomial Temperature Approximation",
            font=("Segoe UI", 15, "bold"),
            anchor="center"
        ).grid(
            row=0, column=0,
            sticky="ew", pady=(0, 8)
        )

        # Formula
        ttk.Label(
            main,
            text="f(t) = 30 + 5 sin(t)     P₃(t) = 30 + 5t − (5/6)t³     a = 0",
            font=("Segoe UI", 10),
            anchor="center"
        ).grid(
            row=1, column=0,
            sticky="ew", pady=(0, 15)
        )

        # Input section
        input_frame = ttk.Frame(main)
        input_frame.grid(
            row=2, column=0,
            pady=(0, 15)
        )

        ttk.Label(
            input_frame,
            text="Enter time t:"
        ).grid(row=0, column=0, padx=5)

        self.t_var = tk.StringVar()

        entry = ttk.Entry(
            input_frame,
            textvariable=self.t_var,
            width=15
        )
        entry.grid(row=0, column=1, padx=5)
        entry.focus()

        entry.bind("<Return>", lambda e: self.compute())

        ttk.Button(
            input_frame,
            text="Compute",
            command=self.compute
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            input_frame,
            text="Clear",
            command=self.clear
        ).grid(row=0, column=3, padx=5)

        # Responsive content area
        content = ttk.Frame(main)
        content.grid(
            row=3, column=0,
            sticky="nsew"
        )

        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        # Results section
        results = ttk.LabelFrame(
            content,
            text="Results",
            padding=12
        )
        results.grid(
            row=0, column=0,
            sticky="ew", pady=(0, 15)
        )

        results.columnconfigure(1, weight=1)

        self.true_lbl = self._row(
            results, "True Temperature:", 0
        )

        self.approx_lbl = self._row(
            results, "Taylor P₃ Approximation:", 1
        )

        self.err_lbl = self._row(
            results, "Absolute Error:", 2
        )

        self.pct_lbl = self._row(
            results, "Percent Error:", 3
        )

        self.note_lbl = ttk.Label(
            results,
            text="",
            font=("Segoe UI", 9, "italic")
        )
        self.note_lbl.grid(
            row=4, column=0,
            columnspan=2,
            sticky="w",
            pady=(8, 0)
        )

        # History section
        history = ttk.LabelFrame(
            content,
            text="History",
            padding=10
        )
        history.grid(
            row=1, column=0,
            sticky="nsew"
        )

        history.columnconfigure(0, weight=1)
        history.rowconfigure(0, weight=1)

        columns = ("t", "True", "P3", "Error")

        self.tree = ttk.Treeview(
            history,
            columns=columns,
            show="headings",
            height=6
        )

        headings = {
            "t": "Time (t)",
            "True": "True Temperature",
            "P3": "Taylor P₃",
            "Error": "Absolute Error"
        }

        for col in columns:
            self.tree.heading(
                col,
                text=headings[col]
            )
            self.tree.column(
                col,
                width=130,
                minwidth=90,
                anchor="center",
                stretch=True
            )

        self.tree.grid(
            row=0, column=0,
            sticky="nsew"
        )

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            history,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.grid(
            row=0, column=1,
            sticky="ns"
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        # Plot button
        ttk.Button(
            main,
            text="Plot True vs P₃",
            command=self.plot
        ).grid(
            row=4, column=0,
            pady=(15, 0)
        )

    # Create result row
    def _row(self, parent, text, row):
        ttk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10)
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=10,
            pady=3
        )

        label = ttk.Label(
            parent,
            text="-",
            font=("Consolas", 11, "bold")
        )
        label.grid(
            row=row,
            column=1,
            sticky="w",
            padx=10
        )

        return label

    # Validate input
    def get_t(self):
        try:
            t = float(self.t_var.get())

            if not math.isfinite(t):
                raise ValueError

            return t

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid finite number for t."
            )
            return None

    # Compute temperature and errors
    def compute(self):
        t = self.get_t()

        if t is None:
            return

        try:
            true_value = true_temp(t)
            approximation = taylor_p3(t)

            if not (
                math.isfinite(true_value)
                and math.isfinite(approximation)
            ):
                raise OverflowError

            absolute_error = abs(
                true_value - approximation
            )

            percent_error = (
                absolute_error / abs(true_value)
            ) * 100

            if not math.isfinite(percent_error):
                raise OverflowError

        except (OverflowError, ValueError):
            messagebox.showerror(
                "Calculation Error",
                "The input is too large to calculate."
            )
            return

        # Display results
        self.true_lbl.config(
            text=f"{true_value:.6f}"
        )

        self.approx_lbl.config(
            text=f"{approximation:.6f}"
        )

        self.err_lbl.config(
            text=f"{absolute_error:.6f}"
        )

        self.pct_lbl.config(
            text=f"{percent_error:.4f} %"
        )

        # Accuracy message
        if abs(t - A) <= 1:
            self.note_lbl.config(
                text="Close to the center: approximation is accurate."
            )
        else:
            self.note_lbl.config(
                text="Far from the center: approximation may be less accurate."
            )

        # Add to history
        self.tree.insert(
            "",
            0,
            values=(
                f"{t:g}",
                f"{true_value:.4f}",
                f"{approximation:.4f}",
                f"{absolute_error:.4f}"
            )
        )

    # Clear results and history
    def clear(self):
        self.t_var.set("")

        for label in (
            self.true_lbl,
            self.approx_lbl,
            self.err_lbl,
            self.pct_lbl
        ):
            label.config(text="-")

        self.note_lbl.config(text="")

        for item in self.tree.get_children():
            self.tree.delete(item)

    # Plot true function and Taylor approximation
    def plot(self):
        try:
            import matplotlib
            matplotlib.use("TkAgg")

            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import (
                FigureCanvasTkAgg
            )

        except ImportError:
            messagebox.showinfo(
                "Matplotlib Missing",
                "Install it with: py -3.14 -m pip install matplotlib"
            )
            return

        # Create graph window
        win = tk.Toplevel(self)
        win.title("True Temperature vs Taylor P₃")

        # Center graph window
        width = 800
        height = 550

        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        win.geometry(f"{width}x{height}+{x}+{y}")
        win.minsize(500, 350)

        # Graph container
        graph_frame = ttk.Frame(win, padding=10)
        graph_frame.pack(
            fill="both",
            expand=True
        )

        # Create figure
        fig = Figure(
            figsize=(7, 4.5),
            dpi=100
        )

        ax = fig.add_subplot(111)

        xs = [
            i * 0.05
            for i in range(-120, 121)
        ]

        true_values = [
            true_temp(x) for x in xs
        ]

        taylor_values = [
            taylor_p3(x) for x in xs
        ]

        # Plot true function
        ax.plot(
            xs,
            true_values,
            label="True: 30 + 5sin(t)",
            linewidth=2
        )

        # Plot Taylor approximation
        ax.plot(
            xs,
            taylor_values,
            "--",
            label="Taylor P₃",
            linewidth=2
        )

        # Expansion point
        ax.axvline(
            A,
            color="gray",
            linewidth=0.8,
            linestyle=":"
        )

        # Mark entered time
        try:
            t = float(self.t_var.get())

            if math.isfinite(t) and -6 <= t <= 6:
                ax.plot(
                    [t],
                    [true_temp(t)],
                    "o",
                    label=f"t = {t:g}"
                )

        except ValueError:
            pass

        ax.set_xlabel("Time (t)")
        ax.set_ylabel("Temperature")
        ax.set_title(
            "True Temperature vs Taylor Polynomial"
        )

        ax.legend()
        ax.grid(alpha=0.3)

        # Automatically adjust graph layout
        fig.tight_layout()

        # Display graph inside Tkinter
        canvas = FigureCanvasTkAgg(
            fig,
            master=graph_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


# Start application
if __name__ == "__main__":
    app = App()
    app.mainloop()