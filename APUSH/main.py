import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import os
import json

class PosterAnalysisTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Poster Analysis Tool")
        
        # Set up paths using pathlib
        self.base_dir = Path(__file__).parent.absolute()
        self.images_dir = self.base_dir / "images"
        self.posters_dir = self.base_dir / "posters"
        self.data_dir = self.base_dir / "data"
        
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.bind('<Escape>', lambda e: self.create_welcome_screen())

        self.root.geometry(f"{width}x{height}")
        self.root.state('zoomed')
        
        # Window icon
        icon_path = self.images_dir / "sovietunion.PNG"
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.wm_iconphoto(True, icon_photo)
            self.icon_photo = icon_photo
        except Exception as e:
            print(f"Error loading window icon: {e}")
        
        # Load decorative images for welcome screen
        self.left_decoration_image = None
        self.right_decoration_image = None
        self.load_decoration_images()
        self.posters = []
        self.load_posters_from_json(self.data_dir / 'posters.json')
        self.create_welcome_screen()
        
        self.current_poster = None
        # Dictionary to keep references to PhotoImage objects
        self.image_references = {}
    
    def load_decoration_images(self):
        """Load decorative images for welcome screen"""
        try:
            # Left decoration image
            left_img_path = self.images_dir / "sovietunion.PNG"
            left_img = Image.open(left_img_path) if left_img_path.exists() else None
            
            # Right decoration image
            right_img_path = self.images_dir / "Flag_of_the_United_States.png"
            right_img = Image.open(right_img_path) if right_img_path.exists() else None
            
            # If images don't exist, create placeholder images
            if left_img is None:
                left_img = Image.new('RGB', (400, 400), color='#f0f0f0')
                draw = Image.Draw(left_img)
                draw.text((50, 300), "Left Decoration", fill="black")
            
            if right_img is None:
                right_img = Image.new('RGB', (400, 400), color='#f0f0f0')
                draw = Image.Draw(right_img)
                draw.text((50, 300), "Right Decoration", fill="black")
            
            # Resize images to fit screen
            left_img = left_img.resize((400, 400), Image.LANCZOS)
            right_img = right_img.resize((400, 400), Image.LANCZOS)
            
            self.left_decoration_image = ImageTk.PhotoImage(left_img)
            self.right_decoration_image = ImageTk.PhotoImage(right_img)
            
        except Exception as e:
            print(f"Error loading decoration images: {e}")
            # Create simple placeholder images if there's an error
            left_img = Image.new('RGB', (200, 600), color='#f0f0f0')
            right_img = Image.new('RGB', (200, 600), color='#f0f0f0')
            self.left_decoration_image = ImageTk.PhotoImage(left_img)
            self.right_decoration_image = ImageTk.PhotoImage(right_img)
    
    def load_posters_from_json(self, json_file):
        """Load posters data from a JSON file"""
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
        """Load an image and resize it maintaining aspect ratio"""
        try:
            # Open the image file
            original_image = Image.open(image_path)
            
            # Calculate the new size while maintaining aspect ratio
            original_width, original_height = original_image.size
            ratio = min(max_width/original_width, max_height/original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Resize the image
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage for Tkinter
            photo_image = ImageTk.PhotoImage(resized_image)
            
            return photo_image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            # Return a placeholder if image can't be loaded
            placeholder = Image.new('RGB', (max_width, max_height), color='gray')
            return ImageTk.PhotoImage(placeholder)
    
    def create_welcome_screen(self):
        """Create the initial welcome screen"""
        self.clear_screen()
        
        welcome_frame = tk.Frame(self.root, bg="#85321A")
        welcome_frame.pack(expand=True, fill="both")
        
        # Add historical context button in top left corner
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
        
        # Add decorative images on left and right
        if self.left_decoration_image:
            left_img_label = tk.Label(welcome_frame, image=self.left_decoration_image, bg="#85321A")
            left_img_label.pack(side="left", padx=20)
        
        if self.right_decoration_image:
            right_img_label = tk.Label(welcome_frame, image=self.right_decoration_image, bg="#85321A")
            right_img_label.pack(side="right", padx=20)
        
        # Create a container frame for the main content
        main_content_frame = tk.Frame(welcome_frame, bg="#85321A")
        main_content_frame.pack(expand=True, fill="both")
        
        # Center content (title, image, and instruction)
        center_frame = tk.Frame(main_content_frame, bg="#85321A")
        center_frame.pack(expand=True, fill="both")
        
        # Create a frame specifically for the two-line title
        title_frame = tk.Frame(center_frame, bg="#85321A")
        title_frame.pack(pady=20)
        
        # First line of title
        title_line1 = tk.Label(
            title_frame,
            text="Cold War Poster",
            font=("Helvetica", 100, "bold"),
            bg="#85321A",
            fg="#F2D19F"
        )
        title_line1.pack()
        
        # Second line of title
        title_line2 = tk.Label(
            title_frame,
            text="Analysis Tool",
            font=("Helvetica", 60, "bold"),
            bg="#85321A",
            fg="#F2D19F"
        )
        title_line2.pack()
        
        # Add poster image in center
        try:
            poster_path = self.posters_dir / "poster.jpg"
            poster_img = Image.open(poster_path)
            
            # Resize to appropriate dimensions (adjust as needed)
            max_width = 600  # Maximum width for the image
            max_height = 400  # Maximum height for the image
            poster_img.thumbnail((max_width, max_height), Image.LANCZOS)
            
            poster_photo = ImageTk.PhotoImage(poster_img)
            
            # Store reference to prevent garbage collection
            self.image_references["welcome_poster"] = poster_photo
            
            # Create image label
            poster_label = tk.Label(
                center_frame,
                image=poster_photo,
                bg="#85321A"
            )
            poster_label.pack(pady=20)  # Add padding above and below the image
        except Exception as e:
            print(f"Error loading poster image: {e}")
            # Placeholder if image fails to load
            poster_label = tk.Label(
                center_frame,
                text="[Featured Poster]",
                font=("Arial", 12),
                bg="#85321A",
                fg="#F2D19F"
            )
            poster_label.pack(pady=20)
        
        # Instruction label
        instruction_label = tk.Label(
            center_frame,
            text="Press Enter to view the poster gallery",
            font=("Arial", 30),
            bg="#85321A",
            fg="#F2D19F"
        )
        instruction_label.pack(pady=20)
        
        # Create a bottom frame for the extra details
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
        
        # Add a menu button that will be visible in all screens
        self.create_menu_button()
        
        self.root.bind('<Return>', lambda e: self.show_poster_gallery())
    
    def show_written_response(self):
        """Show the written response page with images"""
        self.clear_screen()
        
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Left panel for text content
        text_frame = tk.Frame(main_frame, width=600, bd=2, relief="ridge")
        text_frame.pack(side="left", fill="both", expand=True)
        text_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            text_frame,
            text="Historical Context of Cold War Propaganda",
            font=("Arial", 24, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Text content with scrollbar
        text_content = tk.Text(
            text_frame,
            wrap="word",
            font=("Arial", 14),
            padx=20,
            pady=10
        )
        
        # Sample historical context text - replace with your actual content
        historical_text = """The Cold War (1947-1991) was a period of great tension between the Soviet Union and the US and their respective allies. Propaganda posters played a crucial role in shaping public opinion on both sides.

Key Themes in Cold War Propaganda:

1. Ideological Conflict: Posters emphasized the superiority of capitalism/democracy or communism, portraying the opposing system as oppressive or immoral.

2. Nuclear Threat: Many posters addressed the fear of nuclear war, either by promoting disarmament or by portraying the enemy as an aggressor.

3. Economic Competition: Posters often contrasted the prosperity of one system with the supposed failures of the other.

4. Patriotism and Defense: Many posters encouraged military service or civil defense preparedness.

5. Use of stereotypes: Posters would use popular figures that were fictional or real, such as Uncle Sam. 

The posters reveal how each side wanted to define itself in opposition to the other, using powerful imagery and easy to understand messages to appeal to emotions rather than rational argument."""
        
        text_content.insert("1.0", historical_text)
        text_content.config(state="disabled")
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_content.yview)
        text_content.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_content.pack(side="left", fill="both", expand=True)
        
        # Right panel for images
        image_frame = tk.Frame(main_frame, width=400, bd=2, relief="ridge", bg="white")
        image_frame.pack(side="right", fill="both", expand=False)   
        image_frame.pack_propagate(False)
        
        # Load and display example images
        try:
            # Image 1
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
            
            
            # Image 2
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
            print(f"Error loading response images: {e}")
        
        # Back button
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
        """Create a menu button that appears in all screens"""
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
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            if widget not in [self.menu_button]:
                widget.destroy()
        # Clear image references when changing screens
        self.image_references = {}
    
    def show_poster_gallery(self):
        self.clear_screen()
        self.root.unbind('<Return>')
        
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Grid frame for posters
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(side="left", fill="both", expand=True)
        
        # Create 4x6 grid of posters
        rows, cols = 4, 6
        for i in range(rows):
            grid_frame.rowconfigure(i, weight=1)
        for j in range(cols):
            grid_frame.columnconfigure(j, weight=1)
        
        # Calculate which posters to show (in case we have less than 24)
        posters_to_show = min(24, len(self.posters))
        
        for idx in range(posters_to_show):
            poster = self.posters[idx]
            row = idx // cols
            col = idx % cols
            
            # Create a frame for each poster thumbnail
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
            
            # Poster title
            title_label = tk.Label(
                poster_frame,
                text=poster['title'],
                font=("Arial", 10, "bold"),
                bg="white"
            )
            title_label.pack(pady=5)
            
            # Additional info (designer and year)
            info_label = tk.Label(
                poster_frame,
                text=f"{poster.get('designer', 'Unknown')}, {poster.get('year', 'N/A')}",
                font=("Arial", 8),
                bg="white"
            )
            info_label.pack()
            
            # Load and display the thumbnail image
            if 'image_path' in poster and poster['image_path']:
                # Convert to Path object if it isn't already
                image_path = Path(poster['image_path']) if not isinstance(poster['image_path'], Path) else poster['image_path']
                
                # Load and resize the image (thumbnail size)
                thumb_image = self.load_and_resize_image(image_path, 150, 100)
                # Store reference to prevent garbage collection
                self.image_references[f"thumb_{poster['id']}"] = thumb_image
                
                # Create image label
                image_label = tk.Label(
                    poster_frame,
                    image=thumb_image,
                    bg="white"
                )
                image_label.pack(pady=5)
            else:
                # Placeholder if no image path
                placeholder = tk.Label(
                    poster_frame,
                    text="No Image",
                    width=15,
                    height=8,
                    bg="#e0e0e0",
                    relief="sunken"
                )
                placeholder.pack(pady=5)
            
            # Bind click to the entire frame
            for child in poster_frame.winfo_children():
                child.bind("<Button-1>", lambda e, p=poster: self.show_poster_detail(p))
    
    def show_poster_detail(self, poster):
        """Show the detailed view of a selected poster"""
        self.current_poster = poster
        
        self.clear_screen()
        
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Left panel for explanation
        explanation_frame = tk.Frame(main_frame, width=400, bd=2, relief="ridge")
        explanation_frame.pack(side="left", fill="both", expand=False)
        explanation_frame.pack_propagate(False)
        
        # Explanation title
        explanation_title = tk.Label(
            explanation_frame,
            text="Analysis",
            font=("Arial", 16, "bold"),
            pady=10
        )
        explanation_title.pack()
        
        # Add designer and year information
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
        
        # Explanation text with scrollbar
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
        
        # Right panel for poster
        poster_frame = tk.Frame(main_frame, bd=2, relief="ridge", bg="white")
        poster_frame.pack(side="right", fill="both", expand=True)
        
        # Poster title
        poster_title = tk.Label(
            poster_frame,
            text=poster['title'],
            font=("Arial", 30, "bold"),
            bg="white",
            pady=20
        )
        poster_title.pack()
        
        # Load and display the full-size image
        if 'image_path' in poster and poster['image_path']:
            # Convert to Path object if it isn't already
            image_path = Path(poster['image_path']) if not isinstance(poster['image_path'], Path) else poster['image_path']
            
            # Get screen dimensions for sizing
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Load and resize the image (using about 60% of screen height)
            full_image = self.load_and_resize_image(
                image_path,
                int(screen_width * 0.6),
                int(screen_height * 0.6)
            )
            # Store reference to prevent garbage collection
            self.image_references[f"full_{poster['id']}"] = full_image
            
            # Create image label
            image_label = tk.Label(
                poster_frame,
                image=full_image,
                bg="white"
            )
            image_label.pack(pady=20)
        else:
            # Placeholder if no image path
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
        
        # Back button
        back_button = tk.Button(
            poster_frame,
            text="Back to Gallery",
            command=self.show_poster_gallery,
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        back_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = PosterAnalysisTool(root)
    root.mainloop()