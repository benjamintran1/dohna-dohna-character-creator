from globals import output_path_var, root
import os

CONFIG_FILE = "dohna_config.txt"

def save_config():
    output_folder = output_path_var.get()
    with open(CONFIG_FILE, 'w') as f:
        f.write(output_folder)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            output_folder = f.read().strip()
            output_path_var.set(output_folder)

def on_closing():
    # if temp file exists
    temp_filename = "temp_editor_image.png"
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    save_config()
    root.destroy()
