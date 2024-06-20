import os
import tkinter as tk
from tkinter import filedialog, messagebox
from config import save_config, load_config, on_closing, CONFIG_FILE
import globals
from editor import image_editor
from image_processing import *
from gui import create_main_window


def main():
    create_main_window()

if __name__ == "__main__":
    main()
