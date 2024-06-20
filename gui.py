import tkinter as tk
from tkinter import filedialog, messagebox
from config import save_config, load_config, on_closing
from image_processing import preview_image, resize_image
from editor import image_editor
from PIL import Image, ImageOps, ImageTk, ImageGrab
import os
from globals import *

# Select image for processing
def select_input_image():
    input_path = filedialog.askopenfilename(title="Select an Image File", filetypes=[("Image files", "*.jpg;*jpeg;*.png;*bmp;*.gif")])
    if input_path:
        input_path_var.set(input_path)
        preview_image(input_path)
        tipLabel = tk.Label(root, text="Click image to edit", fg="black")
        tipLabel.grid(row=3, column=8)


# Select whole folder for processing
def select_input_folder():
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    if input_folder:
        input_path_var.set(input_folder)

def select_output_folder():
    outputFolder = filedialog.askdirectory(title="Select Output Destination:")
    if outputFolder:
        output_path_var.set(outputFolder)

def create_main_window():
    root.title("Dohna Dohna Image Character Creator")
    create_character_profile(root)
    
    label1 = tk.Label(root, text="Select image to go with character profile")
    label1.grid(row=0, column=8)

    inputLabel = tk.Label(root, text="Input Path:")
    inputLabel.grid(row=1, column=7, padx=0, pady=0, sticky="e")
    inputEntry = tk.Entry(root, textvariable=input_path_var, width=85)
    inputEntry.grid(row=1, column=8, padx=0, pady=0)
    inputButton = tk.Button(root, text="Browse...", command=select_input_image)
    inputButton.grid(row=1, column=9, padx=0, pady=0, sticky="w")

    outputLabel = tk.Label(root, text="Output Path:")
    outputLabel.grid(row=2, column=7, padx=0, pady=0, sticky="e")
    outputEntry = tk.Entry(root, textvariable=output_path_var, width=85)
    outputEntry.grid(row=2, column=8, padx=0, pady=0)
    outputButton = tk.Button(root, text="Browse Folder...", command=select_output_folder)
    outputButton.grid(row=2, column=9, padx=0, pady=0, sticky="w")

    # processButton = tk.Button(root, text="Process Image", command=process_image)
    # processButton.grid(row=3, column=8, padx=0, pady=0)

    #statusLabel = tk.Label(root, text="", fg="black", width=65)
    #statusLabel.grid(row=4, column=8)
    
    image_preview_label.grid(row=3, column=7, columnspan=20, rowspan=23)

    image_preview_label.bind("<Button-1>", lambda event: image_editor())

    root.protocol("WM_DELETE_WINDOW", on_closing)

    load_config()

    root.mainloop()

def on_validate(P, length):
        # P is the value in the entry widget right after this edit
        if len(P) <= length:
            return True
        else:
            return False
        
def create_character_profile(root):
    nameLabel = tk.Label(root, text="Name:")
    nameLabel.grid(row=0, column=0, sticky="e")

    validate_cmd_name = root.register(lambda P: on_validate(P, 10))

    nameEntry = tk.Entry(root, validate="key", validatecommand=(validate_cmd_name, '%P'), width=25)
    nameEntry.grid(row=0, column=1, columnspan=2, sticky="w")
    

    tipLabel = tk.Label(root, text= "(Max 10 characters)")
    tipLabel.grid(row=0, column=2, sticky="w")
    characterType = tk.Label(root, text="TYPE:")
    characterType.grid(row=1, column=0, sticky="e")

    types = [("Talent", "Talent"), ("Client", "Client")]
    type_var = tk.StringVar(value="Talent")

    for i, (text, value) in enumerate(types):
        radio = tk.Radiobutton(root, text=text, variable=type_var, value=value)
        radio.grid(row=i+1, column=1, sticky="w")

    ranks = [
        ("S+ God-tier", "S+"),
        ("S  Legendary", "S"),
        ("A+ World class", "A+"),
        ("A  National class", "A"),
        ("B+ Highly impressive", "B+"),
        ("B  Impressive", "B"),
        ("C+ Somewhat impressive", "C+"),
        ("C  Ordinary", "C"),
        ("D+ Below average", "D+"),
        ("D  Miserable", "D"),
        ("Assign a random value", "Random")
    ]

    # Looks ----------------------------------
    looksLabel = tk.Label(root, text="Looks Rank:")
    looksLabel.grid(row=3, column=1, sticky="w")

    looks_var = tk.StringVar(value="Random")  # Default value

    for i, (text, value) in enumerate(ranks):
        radio = tk.Radiobutton(root, text=text, variable=looks_var, value=value)
        radio.grid(row=4 + i, column=1, sticky="w")

    # Technique -----------------------------
    techLabel = tk.Label(root, text="Technique Rank:")
    techLabel.grid(row=3, column=2, sticky="w")

    tech_var = tk.StringVar(value="Random")  # Default value

    for i, (text, value) in enumerate(ranks):
        radio = tk.Radiobutton(root, text=text, variable=tech_var, value=value)
        radio.grid(row=4 + i, column=2, sticky="w")

    # Mentality -----------------------------
    menLabel = tk.Label(root, text="Mentality Rank:")
    menLabel.grid(row=3, column=3, sticky="w")

    men_var = tk.StringVar(value="Random")  # Default value

    for i, (text, value) in enumerate(ranks):
        radio = tk.Radiobutton(root, text=text, variable=men_var, value=value)
        radio.grid(row=4 + i, column=3, sticky="w")

    # Traits ----------------------------------
    traits = [
        ("Big Tits", "巨乳"), ("Tiny Tits", "貧乳"), ("Wide Hips", "安産型"), ("Beautiful Legs", "脚線美"), 
        ("Smooth Skin", "玉の肌"), ("Muscular", "筋肉質"), ("Skinny", "着やせ"), ("Famous", "名器"), 
        ("Injured", "外傷"), ("Broken", "骨折"), ("Wheelchair", "車椅子"), ("Low Blood Pressure", "低血圧"), 
        ("Sickly", "病弱"), ("Blind", "失明"), ("Tattoo", "タトゥ"), ("Piercing", "ピアス"), 
        ("Sensitive", "敏感"), ("Smelly", "体臭"), ("Daughter", "令嬢"), ("Celebrity", "有名人"), 
        ("Chairwoman", "委員長"), ("Honor Student", "優等生"), ("Sporty", "運動部"), ("Corrected", "補導歴"), 
        ("Struggled in life", "生活難"), ("Has Boyfriend", "彼氏有"), ("Has Girlfriend", "彼女有"), 
        ("Married", "既婚"), ("Has Children", "経産婦"), ("Popular", "人気者"), ("Prince charming", "王子様"), 
        ("Attractive", "愛嬌"), ("Cool", "クール"), ("Silent", "無口"), ("Strong-willed", "強情"), 
        ("Positive", "前向き"), ("Single-minded", "一途"), ("Shy", "照れ屋"), ("Timid", "臆病"), 
        ("Submissive", "従順"), ("Righteous", "正義感"), ("Serious", "真面目"), ("Seductive", "小悪魔"), 
        ("High spirited", "高飛車"), ("Fastidious", "潔癖"), ("Innocent", "無垢"), ("Naughty", "えっち"), 
        ("Perverted", "変態"), ("Healing", "癒し系"), ("Loose", "ゆるい"), ("Mysterious", "不思議"), 
        ("Evil", "心の闇"), ("Self-deprecating", "自虐的"), ("Psycho", "サイコ"), ("Classy", "上品"), 
        ("Homely", "家庭的"), ("Demonic", "魔性")
    ]

    selected_traits = []

    def update_traits(var, index):
        if var.get():
            if len(selected_traits) < 3:
                selected_traits.append(traits[index])
            else:
                var.set(0)  # Prevent additional selection
        else:
            selected_traits.remove(traits[index])

        # Enable/disable checkbuttons based on the current selection count
        for i, chk in enumerate(trait_checks):
            if not trait_vars[i].get() and len(selected_traits) >= 3:
                chk.config(state=tk.DISABLED)
            else:
                chk.config(state=tk.NORMAL)

    trait_vars = []
    trait_checks = []
    traitLabel = tk.Label(root, text="Traits (Select up to 3):")
    traitLabel.grid(row=5 + len(ranks), column=0, sticky="e")

    for i, (english_name, japanese_text) in enumerate(traits):
        var = tk.IntVar()
        chk = tk.Checkbutton(root, text=english_name, variable=var, command=lambda v=var, idx=i: update_traits(v, idx))
        row = 6 + len(ranks) + (i // 6)
        col = (i % 6) + 1
        chk.grid(row=row, column=col, sticky="w")
        trait_vars.append(var)
        trait_checks.append(chk)

    # Virginity Status -----------------------
    virginLabel = tk.Label(root, text="Virginity Status:")
    virginLabel.grid(row=6 + len(ranks) + 10, column=0, sticky="e")

    virgin = [("Virgin", "1"), ("Non-virgin", "0")]
    virgin_var = tk.StringVar(value="1")

    for i, (text, value) in enumerate(virgin):
        radio = tk.Radiobutton(root, text=text, variable=virgin_var, value=value)
        radio.grid(row=i + 6 + len(ranks) + 11, column=1, sticky="w")

    # Voice Types -----------------------------
    voices_older_woman = [
        ("Older Woman", "Serious", "女子汎用／大／真面目"), 
        ("Older Woman", "Cheerful", "女子汎用／大／陽気"), 
        ("Older Woman", "Confident", "女子汎用／大／強気")
    ]
    voices_young_woman = [
        ("Young Woman", "Serious", "女子汎用／高／真面目"), 
        ("Young Woman", "Lively", "女子汎用／高／活発"), 
        ("Young Woman", "Cheerful", "女子汎用／高／陽気"), 
        ("Young Woman", "Humble", "女子汎用／高／控え目"), 
        ("Young Woman", "Innocent", "女子汎用／高／無邪気")
    ]
    voices_teenager = [
        ("Teenager", "Serious", "女子汎用／中／真面目"), 
        ("Teenager", "Lively", "女子汎用／中／活発"), 
        ("Teenager", "Humble", "女子汎用／中／控え目")
    ]
    voices_young_girl = [
        ("Young Girl", "Innocent", "女子汎用／小／無邪気"), 
        ("Young Girl", "Tenacious", "女子汎用／小／勝ち気"), 
        ("Young Girl", "Humble", "女子汎用／小／勝ち気")
    ]
    voice_categories = [voices_older_woman, voices_young_woman, voices_teenager, voices_young_girl]
    category_titles = ["Older Woman", "Young Woman", "Teenager", "Young Girl"]

    voiceLabel = tk.Label(root, text="Voice Type:")
    voiceLabel.grid(row=8 + len(ranks) + 11, column=0, sticky="e")

    voice_var = tk.StringVar(value=voices_older_woman[0])  # Default value
    current_row = 9 + len(ranks) + 11

    for col, (category, title) in enumerate(zip(voice_categories, category_titles)):
        title_label = tk.Label(root, text=title)
        title_label.grid(row=current_row, column=col + 1, sticky="w")

        for i, (category_text, voice_text, japanese_text) in enumerate(category):
            radio = tk.Radiobutton(root, text=voice_text, variable=voice_var, value=japanese_text)
            radio.grid(row=current_row + 1 + i, column=col + 1, sticky="w")

    bioLabel = tk.Label(root, text="Enter Bio:")
    bioLabel.grid(row=37,column=0, sticky="e")

    # limit characters to 50 
    validate_cmd_bio = root.register(lambda P: on_validate(P, 50))

    bioEntry = tk.Entry(root, validate="key", validatecommand=(validate_cmd_bio, '%P'), width=55)
    bioEntry.grid(row=37, column=1, columnspan=5, sticky="w")

    # Function to collect data and write to file
    def submit_profile():
        name = nameEntry.get()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        
        if os.path.exists("temp_editor_image.png"):
            input_image_path = "temp_editor_image.png"  # Use the temp image if available
        else:
            input_image_path = input_path_var.get()
        output_folder = output_path_var.get()
        if output_folder:
            output_image_path = os.path.join(output_folder, f"{name}.png")
            output_file_path = os.path.join(output_folder, f"{name}.txt")
        else:
            profiles_folder = os.path.join(os.getcwd(), "profiles")
            if not os.path.exists(profiles_folder):
                os.makedirs(profiles_folder)
            output_image_path = os.path.join(profiles_folder, f"{name}.png")
            output_file_path = os.path.join(profiles_folder, f"{name}.txt")
        
        try:
            resize_image(input_image_path, output_image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

        character_type = type_var.get()
        looks_rank = looks_var.get()
        technique_rank = tech_var.get()
        mentality_rank = men_var.get()
        trait_lines = "\n".join([f"TRAIT={trait[1]}" for trait in selected_traits])
        virginity_status = virgin_var.get()
        voice_type = voice_var.get()
        


        # Check if looks_rank, technique_rank, or mentality_rank is "Random" and omit them from profile data if true
        profile_data = (
            f"NAME={name}\n"
            f"IMAGE={name}.png\n"
            f"TYPE={character_type}\n"
            f"VIRGIN={virginity_status}\n"
            f"VOICE={voice_type}\n"
            f"{trait_lines}\n"
        )

        if looks_rank != "Random":
            profile_data += f"LKS={looks_rank}\n"

        if technique_rank != "Random":
            profile_data += f"TEC={technique_rank}\n"

        if mentality_rank != "Random":
            profile_data += f"MEN={mentality_rank}\n"

        # Write the profile data to a file
        with open(output_file_path, "w") as file:
            file.write(profile_data)
        messagebox.showinfo("Success", "Profile saved successfully!")

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=submit_profile)
    submit_button.grid(row=38, column=0, columnspan=10)