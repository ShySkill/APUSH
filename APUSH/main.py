import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import os
import json

class PosterAnalysisTool:
    def __init__(self, root):
        self.root = root
        self.root.title("APUSH Karis Poster Analysis Tool")
        
        self.base_dir = Path(__file__).parent.absolute()
        self.images_dir = self.base_dir / "images"
        self.posters_dir = self.base_dir / "posters"
        self.data_dir = self.base_dir / "data"
        
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.bind('<Escape>', lambda e: self.create_welcome_screen())

        self.root.geometry(f"{width}x{height}")
        self.root.state('zoomed')
        
        icon_path = self.images_dir / "sovietunion.PNG"
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.wm_iconphoto(True, icon_photo)
            self.icon_photo = icon_photo
        except Exception as e:
            print(f"Error loading window icon: {e}")
        
        self.left_decoration_image = None
        self.right_decoration_image = None
        self.load_decoration_images()
        self.posters = []
        self.load_posters_from_json(self.data_dir / 'posters.json')
        self.create_welcome_screen()
        
        self.current_poster = None
        self.image_references = {}
    
    def bind_navigation_keys(self):
        self.root.bind('<Left>', lambda e: self.show_previous_poster())
        self.root.bind('<Right>', lambda e: self.show_next_poster())

    def unbind_navigation_keys(self):
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')

    def show_next_poster(self):
        if self.current_poster:
            try:
                current_index = next(i for i, p in enumerate(self.posters) if p['id'] == self.current_poster['id'])
                if current_index < len(self.posters) - 1:
                    self.show_poster_detail(self.posters[current_index + 1])
            except StopIteration:
                pass 

    def show_previous_poster(self):
        if self.current_poster:
            try:
                current_index = next(i for i, p in enumerate(self.posters) if p['id'] == self.current_poster['id'])
                if current_index > 0:
                    self.show_poster_detail(self.posters[current_index - 1])
            except StopIteration:
                pass

    def load_decoration_images(self):
        try:
            left_img_path = self.images_dir / "sovietunion.PNG"
            left_img = Image.open(left_img_path) if left_img_path.exists() else None
            
            right_img_path = self.images_dir / "Flag_of_the_United_States.png"
            right_img = Image.open(right_img_path) if right_img_path.exists() else None
            
            if left_img is None:
                left_img = Image.new('RGB', (400, 400), color='#f0f0f0')
                draw = Image.Draw(left_img)
                draw.text((50, 300), "Left Decoration", fill="black")
            
            if right_img is None:
                right_img = Image.new('RGB', (400, 400), color='#f0f0f0')
                draw = Image.Draw(right_img)
                draw.text((50, 300), "Right Decoration", fill="black")
            
            
            left_img = left_img.resize((400, 400), Image.LANCZOS)
            right_img = right_img.resize((400, 400), Image.LANCZOS)
            
            self.left_decoration_image = ImageTk.PhotoImage(left_img)
            self.right_decoration_image = ImageTk.PhotoImage(right_img)
            
        except Exception as e:
            print(f"Error loading decoration images: {e}")
            left_img = Image.new('RGB', (200, 600), color='#f0f0f0')
            right_img = Image.new('RGB', (200, 600), color='#f0f0f0')
            self.left_decoration_image = ImageTk.PhotoImage(left_img)
            self.right_decoration_image = ImageTk.PhotoImage(right_img)
    
    def load_posters_from_json(self, json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                self.posters = json.load(file)
            print(f"Successfully loaded {len(self.posters)} posters from {json_file}")
        except FileNotFoundError:
            print(f"Error: JSON file '{json_file}' not found. Using empty poster list.")
            self.posters = []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{json_file}'. Using empty poster list.")
            self.posters = []
    
    def load_and_resize_image(self, image_path, max_width, max_height):
        try:
            original_image = Image.open(image_path)
            
            original_width, original_height = original_image.size
            ratio = min(max_width/original_width, max_height/original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
            
            photo_image = ImageTk.PhotoImage(resized_image)
            
            return photo_image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            placeholder = Image.new('RGB', (max_width, max_height), color='gray')
            return ImageTk.PhotoImage(placeholder)
    
    def create_welcome_screen(self):
        self.clear_screen()
        
        welcome_frame = tk.Frame(self.root, bg="#85321A")
        welcome_frame.pack(expand=True, fill="both")
        
        context_button = tk.Button(
            welcome_frame,
            text="Historical Context",
            command=self.show_written_response,
            font=("Arial", 14),
            bg="#F2D19F",
            fg="#85321A",
            padx=15,
            pady=5,
            relief="raised"
        )
        context_button.place(relx=0.02, rely=0.02, anchor="nw")
        
        if self.left_decoration_image:
            left_img_label = tk.Label(welcome_frame, image=self.left_decoration_image, bg="#85321A")
            left_img_label.pack(side="left", padx=20)
        
        if self.right_decoration_image:
            right_img_label = tk.Label(welcome_frame, image=self.right_decoration_image, bg="#85321A")
            right_img_label.pack(side="right", padx=20)
        
        main_content_frame = tk.Frame(welcome_frame, bg="#85321A")
        main_content_frame.pack(expand=True, fill="both")
        
        center_frame = tk.Frame(main_content_frame, bg="#85321A")
        center_frame.pack(expand=True, fill="both")
        
        title_frame = tk.Frame(center_frame, bg="#85321A")
        title_frame.pack(pady=20)
        
        title_line1 = tk.Label(
            title_frame,
            text="Cold War Poster",
            font=("Helvetica", 100, "bold"),
            bg="#85321A",
            fg="#F2D19F"
        )
        title_line1.pack()
        
        title_line2 = tk.Label(
            title_frame,
            text="Analysis Tool",
            font=("Helvetica", 60, "bold"),
            bg="#85321A",
            fg="#F2D19F"
        )
        title_line2.pack()
        
        try:
            poster_path = self.posters_dir / "poster.jpg"
            poster_img = Image.open(poster_path)
            
            max_width = 600 
            max_height = 400 
            poster_img.thumbnail((max_width, max_height), Image.LANCZOS)
            
            poster_photo = ImageTk.PhotoImage(poster_img)
            
            self.image_references["welcome_poster"] = poster_photo
            
            poster_label = tk.Label(
                center_frame,
                image=poster_photo,
                bg="#85321A"
            )
            poster_label.pack(pady=20) 
        except Exception as e:
            print(f"Error loading poster image: {e}")
            poster_label = tk.Label(
                center_frame,
                text="[Featured Poster]",
                font=("Arial", 12),
                bg="#85321A",
                fg="#F2D19F"
            )
            poster_label.pack(pady=20)
        
        instruction_label = tk.Label(
            center_frame,
            text="Press Enter to view the poster gallery",
            font=("Arial", 30),
            bg="#85321A",
            fg="#F2D19F"
        )
        instruction_label.pack(pady=20)
        
        bottom_frame = tk.Frame(main_content_frame, bg="#85321A")
        bottom_frame.pack(side="bottom", fill="x", pady=40)
        
        extra_details = tk.Label(
            bottom_frame,
            text="Includes an in-depth historical analysis, propaganda techniques, and results of propaganda",
            font=("Arial", 20),
            bg="#85321A",
            fg="#F2D19F",
            wraplength=800
        )
        extra_details.pack()
        
        self.create_menu_button()
        
        self.root.bind('<Return>', lambda e: self.show_poster_gallery())
    
    def show_written_response(self):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        text_frame = tk.Frame(main_frame, width=600, bd=2, relief="ridge")
        text_frame.pack(side="left", fill="both", expand=True)
        text_frame.pack_propagate(False)
        
        title_label = tk.Label(
            text_frame,
            text="Historical Context of Cold War Propaganda",
            font=("Arial", 24, "bold"),
            pady=20
        )
        title_label.pack()
        
        text_content = tk.Text(
            text_frame,
            wrap="word",
            font=("Arial", 14),
            padx=20,
            pady=10
        )
        
        historical_text = """The Cold War (1947-1991) was a period of great tension between the Soviet Union and the US and their respective allies. Propaganda posters played a crucial role in shaping public opinion on both sides.

Key Themes in Cold War Propaganda:

1. Ideological Conflict: Posters emphasized the superiority of capitalism/democracy or communism, portraying the opposing system as oppressive or immoral.

2. Nuclear Threat: Many posters addressed the fear of nuclear war, either by promoting disarmament or by portraying the enemy as an aggressor.

3. Economic Competition: Posters often contrasted the prosperity of one system with the supposed failures of the other.

4. Patriotism and Defense: Many posters encouraged military service or civil defense preparedness.

5. Use of stereotypes: Posters would use popular figures that were fictional or real, such as Uncle Sam. 

The posters reveal how each side wanted to define itself in opposition to the other, using powerful imagery and easy to understand messages to appeal to emotions rather than rational argument."""

        results_text = """

    RESULTS OF PROPAGANDA:

    1. Changed Public Opinion: Propaganda deepened the divide between capitalist and communist ideologies, making compromise more difficult.
    2. Increased Military Spending: posters contributed to the arms race and increased defense budgets in both side.
    3. Cultural Stereotypes: Propaganda created lasting stereotypes about both sides that are still present even today.
    4. Political Mobilization: Posters were effective at getting citizens to get behind government policies and military actions.
    5. Distrust in Media: The extremist propaganda led many to become skeptical of all government messaging, a legacy that continues in modern politics.
    6. Artistic Legacy: While serving political purposes, these posters also represent significant works of graphic design and political art.
    
    According to http://large.stanford.edu/courses/2017/ph241/le2/, Exploring the Impact of Propaganda during the Cold War by Professor Adrien Ivan,
    sentiment towards the other side became much more prominent, as American were becoming increasingly radical towards soviet ideas, and vice versa.
    Propaganda also puposely justified the arms race.
    """

        text_content.insert("1.0", historical_text + results_text)
        
        text_content.tag_add("bold", "1.0", "end")
        text_content.tag_config("bold", font=("Arial", 14))
        
        start_index = text_content.search("RESULTS OF PROPAGANDA:", "1.0", stopindex="end")
        if start_index:
            end_index = f"{start_index}+{len('RESULTS OF PROPAGANDA:')}c"
            text_content.tag_add("bold_title", start_index, end_index)
            text_content.tag_config("bold_title", font=("Arial", 14, "bold"))
        
        text_content.config(state="disabled")
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_content.yview)
        text_content.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_content.pack(side="left", fill="both", expand=True)
        
        image_frame = tk.Frame(main_frame, width=400, bd=2, relief="ridge", bg="white")
        image_frame.pack(side="right", fill="both", expand=False)   
        image_frame.pack_propagate(False)
        
        try:
            img1_path = self.posters_dir / "poster1.jpg"
            if img1_path.exists():
                img1 = self.load_and_resize_image(img1_path, 350, 250)
                self.image_references["response_img1"] = img1
                img1_label = tk.Label(image_frame, image=img1, bg="white")
                img1_label.pack(pady=10)
                caption1 = tk.Label(
                    image_frame,
                    text="Example of Soviet propaganda poster",
                    font=("Arial", 10),
                    bg="white"
                )
                caption1.pack()
            
            
            img2_path = self.posters_dir / "poster3.jpg"
            if img2_path.exists():
                img2 = self.load_and_resize_image(img2_path, 350, 250)
                self.image_references["response_img2"] = img2
                img2_label = tk.Label(image_frame, image=img2, bg="white")
                img2_label.pack(pady=10)
            else:
                print("Failed to load poster 2")
            

            caption2 = tk.Label(
                image_frame,
                text="Example of American propaganda poster",
                font=("Arial", 10),
                bg="white"
            )
            caption2.pack()
            
        except Exception as e:
            print(f"error loading response images: {e}")
        
        back_button = tk.Button(
            image_frame,
            text="Back to Main Menu",
            command=self.create_welcome_screen,
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        back_button.pack(pady=20)
    
    def create_menu_button(self):
        self.menu_button = tk.Button(
            self.root,
            text="Main Menu",
            command=self.create_welcome_screen,
            font=("Arial", 12),
            bg="#f0f0f0",
            relief="flat"
        )
        self.menu_button.place(relx=0.95, rely=0.02, anchor="ne")
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            if widget not in [self.menu_button]:
                widget.destroy()
        self.image_references = {}
    
    def show_poster_gallery(self):
        self.clear_screen()
        self.root.unbind('<Return>')
        self.unbind_navigation_keys() 
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(side="left", fill="both", expand=True)
        
        rows, cols = 4, 6
        for i in range(rows):
            grid_frame.rowconfigure(i, weight=1)
        for j in range(cols):
            grid_frame.columnconfigure(j, weight=1)
        
        #calculate which posters to show (in case we have less than 24)
        posters_to_show = min(24, len(self.posters))
        
        for idx in range(posters_to_show):
            poster = self.posters[idx]
            row = idx // cols
            col = idx % cols
            
            poster_frame = tk.Frame(
                grid_frame,
                bd=2,
                relief="ridge",
                bg="white",
                padx=5,
                pady=5
            )
            poster_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            poster_frame.bind("<Button-1>", lambda e, p=poster: self.show_poster_detail(p))
            
            title_label = tk.Label(
                poster_frame,
                text=poster['title'],
                font=("Arial", 10, "bold"),
                bg="white"
            )
            title_label.pack(pady=5)
            
            #aaaaaaaaaaa
            info_label = tk.Label(
                poster_frame,
                text=f"{poster.get('designer', 'Unknown')}, {poster.get('year', 'N/A')}",
                font=("Arial", 8),
                bg="white"
            )
            info_label.pack()
            
            if 'image_path' in poster and poster['image_path']:
                image_path = Path(poster['image_path']) if not isinstance(poster['image_path'], Path) else poster['image_path']
                
                thumb_image = self.load_and_resize_image(image_path, 150, 100)
                self.image_references[f"thumb_{poster['id']}"] = thumb_image
                
                image_label = tk.Label(
                    poster_frame,
                    image=thumb_image,
                    bg="white"
                )
                image_label.pack(pady=5)
            else:
                placeholder = tk.Label(
                    poster_frame,
                    text="No Image",
                    width=15,
                    height=8,
                    bg="#e0e0e0",
                    relief="sunken"
                )
                placeholder.pack(pady=5)
            
            for child in poster_frame.winfo_children():
                child.bind("<Button-1>", lambda e, p=poster: self.show_poster_detail(p))
    
    def show_poster_detail(self, poster):
        self.clear_screen()
        self.current_poster = poster
        self.bind_navigation_keys() 
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        explanation_frame = tk.Frame(main_frame, width=400, bd=2, relief="ridge")
        explanation_frame.pack(side="left", fill="both", expand=False)
        explanation_frame.pack_propagate(False)
        
        explanation_title = tk.Label(
            explanation_frame,
            text="Analysis",
            font=("Arial", 16, "bold"),
            pady=10
        )
        explanation_title.pack()
        
        meta_frame = tk.Frame(explanation_frame)
        meta_frame.pack(pady=5)
        
        designer_label = tk.Label(
            meta_frame,
            text=f"Designer: {poster.get('designer', 'Unknown')}",
            font=("Arial", 12),
            anchor="w"
        )
        designer_label.pack(fill="x")
        
        year_label = tk.Label(
            meta_frame,
            text=f"Year: {poster.get('year', 'N/A')}",
            font=("Arial", 12),
            anchor="w"
        )
        year_label.pack(fill="x")
        
        explanation_text = tk.Text(
            explanation_frame,
            wrap="word",
            font=("Helvetica", 25),
            padx=10,
            pady=10
        )
        explanation_text.insert("1.0", poster['explanation'])
        explanation_text.config(state="disabled")
        
        scrollbar = ttk.Scrollbar(explanation_frame, orient="vertical", command=explanation_text.yview)
        explanation_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        explanation_text.pack(side="left", fill="both", expand=True)
        
        poster_frame = tk.Frame(main_frame, bd=2, relief="ridge", bg="white")
        poster_frame.pack(side="right", fill="both", expand=True)
        
        poster_title = tk.Label(
            poster_frame,
            text=poster['title'],
            font=("Arial", 30, "bold"),
            bg="white",
            pady=20
        )
        poster_title.pack()
        
        if 'image_path' in poster and poster['image_path']:
            image_path = Path(poster['image_path']) if not isinstance(poster['image_path'], Path) else poster['image_path']
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            full_image = self.load_and_resize_image(
                image_path,
                int(screen_width * 0.6),
                int(screen_height * 0.6)
            )
            self.image_references[f"full_{poster['id']}"] = full_image
            
            image_label = tk.Label(
                poster_frame,
                image=full_image,
                bg="white"
            )
            image_label.pack(pady=20)
        else:
            placeholder = tk.Label(
                poster_frame,
                text="No Image Available",
                font=("Arial", 30),
                bg="#e0e0e0",
                width=40,
                height=25,
                relief="sunken"
            )
            placeholder.pack(pady=20)
        
        nav_frame = tk.Frame(poster_frame, bg="white")
        nav_frame.pack(pady=10)
        
        prev_button = tk.Button(
            nav_frame,
            text="← Previous",
            command=self.show_previous_poster,
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        prev_button.pack(side="left", padx=10)
        
        back_button = tk.Button(
            nav_frame,
            text="Back to Gallery",
            command=self.show_poster_gallery,
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        back_button.pack(side="left", padx=10)
        
        next_button = tk.Button(
            nav_frame,
            text="Next →",
            command=self.show_next_poster,
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        next_button.pack(side="left", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PosterAnalysisTool(root)
    root.mainloop()
