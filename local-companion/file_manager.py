from pathlib import Path

WORKSPACE = Path(__file__).parent / "workspace"

def list_files(folder):
    folder_path = WORKSPACE/folder
    
    for item in folder_path.iterdir():
        print(item.name)
def create_folders(folder):
    folder_path = WORKSPACE/folder
    folder_path.mkdir(parents = True,  exist_ok = True)
    print(f"Folder path is create at {folder_path}")


list_files("Downloads")
create_folders("Projects/NewProject")
