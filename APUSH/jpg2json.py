import os
import json

def create_poster_json(image_folder, output_file):
    posters = []
    
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith('.jpg')]
    
    for i, img_file in enumerate(image_files, start=1):
        poster = {
            "id": i,
            "title": os.path.splitext(img_file)[0].replace("_", " ").title(),
            "image_path": os.path.join(image_folder, img_file),
            "explanation": f"Detailed analysis of {os.path.splitext(img_file)[0].replace('_', ' ')}",
            "designer": "Unknown",
            "year": 2023
        }
        posters.append(poster)
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(posters, f, indent=2)
    
    print(f"Created {output_file} with {len(posters)} posters")

create_poster_json("path/to/your/posters", "posters.json")