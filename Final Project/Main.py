import tkinter as tk
from tkinter import messagebox
import pandas as pd
from tkintertable import TableCanvas, TableModel
import Calculations  # Assuming this is the module with your animation code

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x1200")
        self.root.title("Near Earth Comet Simulator")
        self.root.configure(bg="#d8d7d3")

        # Welcome label
        label = tk.Label(
            self.root,
            bg="#a68b8f",
            text="Welcome to the Near Earth Comet Simulator! Are you excited to see some comets? Please enter your "
                 "desired comet in the textbox below.",
            font=('Arial', 25),
            wraplength=800,
        )
        label.pack(padx=10, pady=10)

        # Entry widget for comet name
        self.txtbox = tk.Entry(self.root, bg="#d8d7d3", width=20)
        self.txtbox.pack(padx=10)

        # Checkbox for random comet
        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(
            self.root,
            text="Generate Random Comet",
            font=('Arial', 12),
            variable=self.check_state
        )
        self.check.pack(padx=5, pady=5)

        # Animate button
        button = tk.Button(
            self.root,
            text="Animate!",
            font=('Arial', 18),
            command=self.show_animation
        )
        button.pack(padx=10, pady=10)

        # Comet info label
        CometInfo = tk.Label(
            self.root,
            bg="#a68b8f",
            text="Below are the trajectories of 160 near-Earth comets used. The data is from NASA’s Open Data Portal",
            font=('Arial', 18),
            wraplength=800,
        )
        CometInfo.pack(padx=10, pady=10)

        # Load DataFrame
        try:
            self.df = pd.read_csv("near-earth-comets.csv")
            # Handle NaN and convert to strings
            self.df = self.df.fillna('')  # Replace NaN with empty string
            self.df = self.df.astype(str)  # Convert all columns to strings
        except FileNotFoundError:
            # Fallback: Create DataFrame from provided data
            comet_data = [
                ["1P/Halley", "49400", "2446467.395", "0.9671429085", "162.2626906", "111.3324851", "58.42008098",
                 "0.5859781115", "35.08", "75.32", "0.063782", "0.00000000027", "0.000000000155", "", "", "J863/77",
                 "1P/Halley"],
                ["2P/Encke", "56870", "2456618.204", "0.8482682514", "11.77999525", "186.5403463", "334.5698056",
                 "0.3360923855", "4.09", "3.3", "0.173092", "0.000000000158", "-0.00000000000505", "", "", "74",
                 "2P/Encke"],
            ]
            columns = ["Object", "Epoch", "TP", "e", "i", "w", "Node", "q", "Q", "P", "MOID", "A1", "A2", "A3", "DT",
                       "ref", "Object_name"]
            self.df = pd.DataFrame(comet_data, columns=columns)

        # Reset DataFrame index to ensure proper row numbering
        self.df.reset_index(drop=True, inplace=True)

        # Debug: Print DataFrame to verify contents
        print("DataFrame contents before rendering:")
        print(self.df)
        print(f"Number of rows: {len(self.df)}")
        print(f"Columns: {list(self.df.columns)}")

        # Show pandas table
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
        try:
            table_model = TableModel()
            # Convert DataFrame to dict with integer indices
            table_dict = {i: row for i, row in self.df.to_dict(orient='index').items()}
            table_model.importDict(table_dict)
            print(f"Table model row count: {table_model.getRowCount()}")
            print(f"Table model column count: {table_model.getColumnCount()}")

            table = TableCanvas(
                table_frame,
                model=table_model,
                width=850,
                height=400,
                readonly=True
            )
            # Set background and text colors
            table.bg = '#808080'  # Hex code for grey
            table.cellbackgr = '#808080'
            table.background = '#808080'
            table.textcolor = 'white'
            table.show()
            table.redraw()  # Force redraw to apply styling
        except Exception as e:
            messagebox.showerror(
                title="Table Rendering Error",
                message=f"Failed to render table: {str(e)}"
            )
            print(f"Table rendering error: {str(e)}")

        # Update scroll region
        table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Bind Enter key to show_animation
        self.root.bind('<Return>', self.shortcut)

        self.root.mainloop()

    def show_animation(self):
        comet = self.txtbox.get().strip()
        if self.check_state.get() == 1:  # Random comet selected
            comet = self.df['Object'].sample().iloc[0]  # Pick a random comet
            self.txtbox.delete(0, tk.END)
            self.txtbox.insert(0, comet)  # Update textbox with random comet name
        if not comet:
            messagebox.showinfo(
                title="Invalid Input",
                message="Please enter a comet name or check the box for a random one."
            )
        else:
            # Check both Object and Object_name columns
            comet_row = self.df[
                (self.df['Object'].str.lower() == comet.lower()) |
                (self.df['Object_name'].str.lower() == comet.lower())
            ]
            if not comet_row.empty:
                Calculations.animate(comet)
            else:
                messagebox.showinfo(
                    title="Comet Not Found",
                    message=f"No comet named '{comet}' found in the dataset."
                )

    def shortcut(self, event):
        if event.keysym == "Return":
            self.show_animation()

# Main
MyGUI()