import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Load the CSV file
csv_file = 'User_Study.csv'
df = pd.read_csv(csv_file)

responses = []

class ImagePromptWindow:
    def __init__(self, master, row, on_submit):
        self.master = master
        self.row = row
        self.on_submit = on_submit

        # Read image and create ImageTk.PhotoImage object
        image_path = f"Images/{row['ID']}.png" if os.path.exists(f"Images/{row['ID']}.png") else f"Images/{row['ID']}.jpg"
        image = Image.open(image_path)
        image.thumbnail((400, 400))
        self.img = ImageTk.PhotoImage(image)

        # Display image
        self.img_label = tk.Label(self.master, image=self.img)
        self.img_label.pack()

        # Display prompts
        self.prompt1_label = tk.Label(self.master, text=f"Prompt 1: {row['Prompt 1']}", font=("Arial", 14))
        self.prompt1_label.pack()
        self.prompt2_label = tk.Label(self.master, text=f"Prompt 2: {row['Prompt 2']}", font=("Arial", 14))
        self.prompt2_label.pack()

        # Entry fields for user input
        self.prompt1_var = tk.IntVar()
        self.prompt2_var = tk.IntVar()
        self.neither_var = tk.IntVar()
        self.image_identical_var = tk.IntVar()
        self.threeD_identical_var = tk.IntVar()
        self.video_identical_var = tk.IntVar()

        tk.Checkbutton(self.master, text="Is Prompt 1", variable=self.prompt1_var).pack()
        tk.Checkbutton(self.master, text="Is Prompt 2", variable=self.prompt2_var).pack()
        tk.Checkbutton(self.master, text="Neither / Wrong", variable=self.neither_var).pack()
        tk.Checkbutton(self.master, text="Prompts visually identical (image)", variable=self.image_identical_var).pack()
        

        # Submit button to save user input
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        self.submit_button.pack()

    
    def submit(self):
        # Save user input
        df.loc[df['ID'] == self.row['ID'], 'Is Prompt 1'] = self.prompt1_var.get()
        df.loc[df['ID'] == self.row['ID'], 'Is Prompt 2'] = self.prompt2_var.get()
        df.loc[df['ID'] == self.row['ID'], 'Neither / Wrong'] = self.neither_var.get()
        df.loc[df['ID'] == self.row['ID'], 'Prompts visually identical (image)'] = self.image_identical_var.get()
        
        # Save responses to the original CSV file
        df.to_csv(csv_file, index=False)

        self.on_submit()
        self.master.destroy()
        
    def submit_backup(self):
        # Save user input
        response = {
            'ID': self.row['ID'],
            'Is Prompt 1': self.prompt1_var.get(),
            'Is Prompt 2': self.prompt2_var.get(),
            'Neither / Wrong': self.neither_var.get(),
            'Prompts visually identical (image)': self.image_identical_var.get()
        }
        responses.append(response)

        # Save responses to CSV
        responses_df = pd.DataFrame(responses)
        responses_df.to_csv('responses.csv', index=False)

        self.on_submit()
        self.master.destroy()


def open_next_image(index):
    if index < len(df):
        row = df.loc[index]
        window = tk.Toplevel()
        window.title(f"ID: {row['ID']}")
        app = ImagePromptWindow(window, row, lambda: open_next_image(index + 1))


root = tk.Tk()
root.withdraw()  # Hide the root window

open_next_image(0)

root.mainloop()