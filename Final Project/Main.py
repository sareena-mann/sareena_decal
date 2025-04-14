import tkinter as tk

# Creates new Window
root = tk.Tk()
root.geometry("900x1200")
root.title("Near Earth Comet Simulator")

label = tk.Label(root, text="Welcome to the Near Earth Comet Simulator!", font = ('Arial', 20))
label.pack(padx=10, pady=10)

# Basic information about why I am doing this, aim, background on near Earth objects


#Something the user can type into
txtbox = tk.Entry(root, width = 20)
txtbox.pack(padx=10)

button = tk.Button(root, text= "Animate!", font = ('Arial', 20))
# Make stickY??
button.pack(padx=10, pady=10)


#List of all options to choose from

#Maybe another window that has the table

root.mainloop()

