import os
from PIL import Image, ImageOps, ImageTk, ImageGrab
import tkinter as tk
from tkinter import filedialog, messagebox
from globals import input_path_var, image_preview_label, root

def image_editor():
    input_image_path = input_path_var.get()
    if not input_image_path:
        messagebox.showwarning("Warning", "No image to show.")
        return
    
    editor = tk.Toplevel(root)
    editor.title("Image Editor")

    def close():
        nonlocal canvas
        # Hide overlay before capture
        canvas.itemconfig(canvas_overlay, state="hidden")

        # Capture canvas content
        temp_filename = "temp_editor_image.png"
        canvas.update()  # Ensure all events are processed and canvas is updated
        x0 = editor.winfo_rootx() + canvas.winfo_x()
        y0 = editor.winfo_rooty() + canvas.winfo_y()
        x1 = x0 + canvas.winfo_width() - 4
        y1 = y0 + canvas.winfo_height() - 4

        # Capture and save canvas content
        ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(temp_filename)

        # Update preview image in main window
        try:
            # Load the captured image
            temp_image = Image.open(temp_filename).convert("RGBA")
            temp_image.thumbnail((500, 500))

            # Load the overlay image
            overlay_path = os.path.join(os.path.dirname(__file__), 'GuideImage.png')
            overlay = Image.open(overlay_path).convert("RGBA")
            overlay.thumbnail((500, 500))  # Ensure overlay has the same size as temp_image

            # Composite the overlay on top of the temp_image
            composite_image = Image.alpha_composite(temp_image, overlay)

            # Convert composite_image to PhotoImage for display in tkinter
            photo = ImageTk.PhotoImage(composite_image)
            image_preview_label.config(image=photo)
            image_preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preview image: {e}")

        editor.destroy()


    done_button = tk.Button(editor, text="Done", command=close)
    done_button.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

    shrink_button = tk.Button(editor, text="Shrink", command=lambda e=None: resize_image(e, "shrink"))
    shrink_button.pack(side=tk.LEFT, anchor=tk.NW, padx=10,pady=10)
    
    expand_button = tk.Button(editor, text="Expand", command=lambda e=None: resize_image(e, "expand"))
    expand_button.pack(side=tk.LEFT, anchor=tk.NW, padx=10,pady=10)

    canvas = tk.Canvas(editor, width=1024, height=1024, bg="black")
    canvas.pack()

    # Load the original image
    original_image = Image.open(input_image_path)
    display_image = original_image.copy()
    display_image.thumbnail((1024, 1024), Image.LANCZOS)
    original_image = display_image.copy()
    tk_image = ImageTk.PhotoImage(display_image)
    canvas_image = canvas.create_image(512, 512, image=tk_image)
    
    # Load the overlay image (GuideImage.png)
    overlay_path = os.path.join(os.path.dirname(__file__), 'GuideImage.png')
    overlay_image = Image.open(overlay_path).convert("RGBA")
    overlay_tk_image = ImageTk.PhotoImage(overlay_image)
    canvas_overlay = canvas.create_image(512, 512, image=overlay_tk_image)
    
    # Initial position of the main image
    image_position = {'x': 512, 'y': 512}
    
    def on_click(event):
        canvas.scan_mark(event.x, event.y)
        image_position['start_x'] = event.x
        image_position['start_y'] = event.y
    
    def on_drag(event):
        dx = event.x - image_position['start_x']
        dy = event.y - image_position['start_y']
        image_position['x'] += dx
        image_position['y'] += dy
        canvas.coords(canvas_image, image_position['x'], image_position['y'])
        image_position['start_x'] = event.x
        image_position['start_y'] = event.y
    
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)

    scale_factor = 0

    def resize_image(event, factor):
        nonlocal tk_image, canvas_image, display_image, scale_factor
        if factor == "shrink":
            scale_factor -= 1
        elif factor == "expand":
            scale_factor += 1
        new_width = int(original_image.size[0] * (1 + (0.05 * scale_factor)))
        new_height = int(original_image.size[1] * (1 + (0.05 * scale_factor)))
        display_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(display_image)
        canvas.itemconfig(canvas_image, image=tk_image)
    
    editor.mainloop()