import os
import shutil

def main():
    print("==================================================")
    print("   Bluestock Capstone Project Packager Tool")
    print("==================================================")
    
    # Get user name
    user_name = input("Enter your name (e.g. Ajay): ").strip()
    if not user_name:
        user_name = "Intern"
        
    submission_folder_name = f"{user_name}_Submission"
    package_dir = os.path.join(os.getcwd(), "Submission_Package")
    dest_path = os.path.join(package_dir, submission_folder_name)
    
    # Remove previous packager build if exists
    if os.path.exists(package_dir):
        try:
            shutil.rmtree(package_dir)
        except Exception as e:
            print(f"Note: Could not clear old directory: {e}")
        
    print(f"\nCreating submission folder structure at:\n--> {dest_path}")
    
    # Create the 5 required sub-folders
    folders = ["Source Code", "Datasets", "Documentation", "PPT_Slides", "Demo Video"]
    for f in folders:
        os.makedirs(os.path.join(dest_path, f), exist_ok=True)
        
    print("\n[1/3] Copying Source Code...")
    # Copy day folders into Source Code
    for day in range(1, 8):
        day_dir = f"Day {day}"
        if os.path.exists(day_dir):
            try:
                shutil.copytree(day_dir, os.path.join(dest_path, "Source Code", day_dir))
            except Exception as e:
                print(f"  Warning: Error copying {day_dir}: {e}")
    
    # Copy requirements.txt and package script as helper
    if os.path.exists("requirements.txt"):
        shutil.copy("requirements.txt", os.path.join(dest_path, "Source Code"))
        
    print("[2/3] Copying Datasets...")
    # Copy data folder
    if os.path.exists("data"):
        try:
            shutil.copytree("data", os.path.join(dest_path, "Datasets", "data"))
        except Exception as e:
            print(f"  Warning: Error copying data folder: {e}")
        
    print("[3/3] Copying Documentation...")
    # Copy README, E2E explanation, final report, data dictionary
    docs_to_copy = [
        ("README.md", "README.md"),
        ("E2E_Process_Explained.md", "E2E_Process_Explained.md"),
        ("Day 7/Final_Report_Template.md", "Final_Report.md"),
        ("Day 2/data_dictionary.md", "Data_Dictionary.md")
    ]
    for src, dest_name in docs_to_copy:
        if os.path.exists(src):
            try:
                shutil.copy(src, os.path.join(dest_path, "Documentation", dest_name))
            except Exception as e:
                print(f"  Warning: Error copying {src}: {e}")
            
    # Create placeholder note in PPT/Slides and Demo Video
    with open(os.path.join(dest_path, "PPT_Slides", "PLACE_SLIDES_HERE.txt"), "w") as f:
        f.write("Please place your final PowerPoint (PPT/Slides) file in this folder.")
        
    with open(os.path.join(dest_path, "Demo Video", "PLACE_DEMO_VIDEO_HERE.txt"), "w") as f:
        f.write("Please place your 2-minute project Walkthrough/Demo Video file in this folder.")
        
    print("\n" + "="*50)
    print("🎉 Submission Folder Packaged Successfully!")
    print("="*50)
    print(f"Location: {dest_path}")
    print("\nNext Steps to Submit:")
    print("1. Open the folder: Submission_Package\\" + submission_folder_name)
    print("2. Copy your presentation PPT/slides file into the 'PPT_Slides' folder.")
    print("3. Copy your project demo video file into the 'Demo Video' folder.")
    print("4. Upload the entire '" + submission_folder_name + "' folder to Google Drive.")
    print("5. Share the folder on Google Drive as 'Anyone with the link -> Viewer'.")
    print("6. Copy the Google Drive folder link and paste it into the Bluestock portal!")
    print("="*50)

if __name__ == "__main__":
    main()
