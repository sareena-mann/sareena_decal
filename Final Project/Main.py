import tkinter as tk
from tkinter import messagebox
import pandas as pd
from tkintertable import TableCanvas, TableModel
import Calculations

dataFrame = pd.DataFrame()
class MyGUI:
    def __init__(self):
        self.root = tk.Tk()

        # Creates new Window
        self.root.geometry("900x1200")
        self.root.title("Near Earth Comet Simulator")
        self.root.configure(bg="#d8d7d3")

        label = tk.Label(self.root, bg="#a68b8f",
                         text="Welcome to the Near Earth Comet Simulator! Are you excited to see some comets? Please enter your "
                                                                "desired comet in the textbox below.",
                         font = ('Arial', 25),
                         wraplength=800,)
        label.pack(padx=10, pady=10)

        # Something the user can type into
        self.txtbox = tk.Entry(self.root, bg = "#d8d7d3",width=20)
        self.txtbox.pack(padx=10)

        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.root, text="Generate Random Comet", font=('Arial', 12), variable = self.check_state)
        self.check.pack(padx=5, pady=5)

        button = tk.Button(self. root, text="Animate!", font=('Arial', 18), command=self.show_animation)
        button.pack(padx=10, pady=10)

        CometInfo = tk.Label(self.root,
                             bg="#a68b8f",
                             text="Below are the trajectories of 160 "
                                  "near-Earth comets used. "
                                  "The data is from NASA’s Open Data Portal",
                             font=('Arial', 18),
                             wraplength=800,
                             )
        CometInfo.pack(padx=10, pady=10)

        #Generate Pandas Table
        try:
            df = pd.read_csv("near-earth-comets.csv")
        except FileNotFoundError:
            # Fallback: Create DataFrame from provided data
            comet_data = [
                ["1P/Halley", 49400, 2446467.395, 0.9671429085, 162.2626906, 111.3324851, 58.42008098, 0.5859781115,
                 35.08, 75.32, 0.063782, 0.00000000027, 0.000000000155, "", "", "J863/77", "1P/Halley"],
                ["2P/Encke", 56870, 2456618.204, 0.8482682514, 11.77999525, 186.5403463, 334.5698056, 0.3360923855,
                 4.09, 3.3, 0.173092, 0.000000000158, -0.00000000000505, "", "", "74", "2P/Encke"],
                # Add more rows as needed...
            ]
            columns = ["Object", "Epoch", "TP", "e", "i", "w", "Node", "q", "Q", "P", "MOID", "A1", "A2", "A3", "DT",
                       "ref", "Object_name"]
            df = pd.DataFrame(comet_data, columns=columns)

        #Show pandas Table
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        # Create scrollable canvas for table
        canvas = tk.Canvas(frame)
        scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        table_frame = tk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        # Create table using tkintertable
        table_model = TableModel()
        table_model.importDict(df.to_dict(orient='index'))
        table = TableCanvas(table_frame, model=table_model, width=850, height=400)
        table.show()

        # Update scroll region
        table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.root.mainloop()

    def show_animation(self):
        comet = self.txtbox.get().strip()
        if self.check_state.get() == 0:
            if comet == "":
                messagebox.showinfo(title="Invalid Input",
                                    message="Please enter a comet name or check the box for a random one.")
            else:
                Calculations.animate(comet, df)
        else:
            messagebox.showinfo()

    def shortcut(self, event):
        if event.state == 12 & event.keysym == "Return":
            self.show_message()

#Main
MyGUI()
