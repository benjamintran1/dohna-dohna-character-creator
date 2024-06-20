import os
from PIL import Image, ImageOps, ImageTk, ImageGrab
from tkinter import messagebox
from globals import statusLabel, image_preview_label, input_path_var, output_path_var

def preview_image(input_image_path, size=(1024, 1024), color=(255, 255, 255)):
    try:
        # Open the input image
        image = Image.open(input_image_path)

        # Resize the image while maintaining aspect ratio
        image.thumbnail(size, Image.LANCZOS)

        # Calculate padding to add
        delta_width = size[0] - image.size[0]
        delta_height = size[1] - image.size[1]
        padding = (delta_width // 2, delta_height // 2, delta_width - (delta_width // 2), delta_height - (delta_height // 2))

        # Add padding
        new_image = ImageOps.expand(image, padding, color)

        # Load the overlay image
        overlay_path = os.path.join(os.path.dirname(__file__), 'GuideImage.png')
        overlay = Image.open(overlay_path).convert("RGBA")

        # Composite the overlay on top of the new_image
        new_image = Image.alpha_composite(new_image.convert("RGBA"), overlay)

        new_image.thumbnail((500, 500))
        # Convert to ImageTk format for preview
        photo = ImageTk.PhotoImage(new_image)

        # Update the label with the new image
        image_preview_label.config(image=photo)
        image_preview_label.image = photo
    except Exception as e:
        messagebox.showerror("Error", f"Failed to preview image {input_image_path}: {e}")

def process_image():
    input_path = input_path_var.get()
    output_folder = output_path_var.get()

    if not input_path:
        messagebox.showwarning("Warning", "No input file or folder selected.")
        return

    if not output_folder:
        messagebox.showwarning("Warning", "No output folder selected.")
        return

    # Process a single image
    input_image_path = input_path
    filename = os.path.basename(input_image_path)

    # Check if the filename already exists in the output folder
    base_name, extension = os.path.splitext(filename)
    output_image_path = os.path.join(output_folder, filename)

    n = 0
    while os.path.exists(output_image_path):
        n += 1
        filename = f"{base_name}({n}){extension}"
        output_image_path = os.path.join(output_folder, filename)

    # if temp file exists, use temp file instead of the input image
    temp_filename = "temp_editor_image.png"
    if os.path.exists(temp_filename):
        input_image_path = temp_filename

    resize_image(input_image_path, output_image_path)
    statusLabel.config(text=f"Image saved to {output_image_path}", fg="green")

def resize_image(input_image_path, output_image_path, size=(1024, 1024), color=(255, 255, 255)):
    try:
        # Open the input image
        image = Image.open(input_image_path)

        # Resize the image while maintaining aspect ratio
        image.thumbnail(size, Image.LANCZOS)

        # Calculate padding to add
        delta_width = size[0] - image.size[0]
        delta_height = size[1] - image.size[1]
        padding = (delta_width // 2, delta_height // 2, delta_width - (delta_width // 2), delta_height - (delta_height // 2))

        # Add padding
        new_image = ImageOps.expand(image, padding, color)

        # Save the output image
        new_image.save(output_image_path)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process image {input_image_path}: {e}")