from tkinter import Label, StringVar
import tkinter as tk

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
CONFIG_FILE = "dohna_config.txt"

root = tk.Tk()
input_path_var = StringVar() 
output_path_var = StringVar()  
image_preview_label = tk.Label(root) 
statusLabel = Label() 