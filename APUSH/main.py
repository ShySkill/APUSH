import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json

class PosterAnalysisTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Poster Analysis Tool")

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        self.root.geometry(f"{width}x{height}")
        self.root.state('zoomed')
        self.create_welcome_screen()
        
        self.posters = []
        self.load_posters_from_json('posters.json')
        
        self.current_poster = None
        # Dictionary to keep references to PhotoImage objects
        self.image_references = {}
    
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
        
        welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        welcome_frame.pack(expand=True, fill="both")
        
        title_label = tk.Label(
            welcome_frame,
            text="Cold War Poster Analysis Tool",
            font=("Helvetica", 32, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=50)
        
        instruction_label = tk.Label(
            welcome_frame,
            text="Press Enter to view the poster gallery",
            font=("Arial", 16),
            bg="#f0f0f0",
            fg="#555"
        )
        instruction_label.pack(pady=20)
        
        self.root.bind('<Return>', lambda e: self.show_poster_gallery())
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
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
                # Load and resize the image (thumbnail size)
                thumb_image = self.load_and_resize_image(poster['image_path'], 150, 100)
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
            font=("Arial", 12),
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
            font=("Arial", 20, "bold"),
            bg="white",
            pady=20
        )
        poster_title.pack()
        
        # Load and display the full-size image
        if 'image_path' in poster and poster['image_path']:
            # Get screen dimensions for sizing
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Load and resize the image (using about 60% of screen height)
            full_image = self.load_and_resize_image(
                poster['image_path'],
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
                font=("Arial", 16),
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