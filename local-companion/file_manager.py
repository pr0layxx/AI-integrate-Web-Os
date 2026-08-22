from pathlib import Path
import os

WORKSPACE = Path(__file__).parent / "workspace"

def list_files(folder):
    folder_path = WORKSPACE/folder
    
    for item in folder_path.iterdir():
        print(item.name)
def create_folders(folder):
    folder_path = WORKSPACE/folder
    folder_path.mkdir(parents = True,  exist_ok = True)
    print(f"Folder path is create at {folder_path}")

def create_files(file):
    path = WORKSPACE/file
    path.parent.mkdir(parents = True,  exist_ok = True)
    path.touch(exist_ok = True)
    print(f"File path is create at {path}")

def read_files(file):
    path =  WORKSPACE/file
        
    with path.open("r", encoding = "utf-8") as file:
        content = file.read()
    print(content)
    
def open_files(file):
    path = WORKSPACE/file

    if not path.exists():
        print("File or folder does not exist.")
        return
    try:
        os.startfile(path)
        print(f"opened: {path}" )
        
    except OSError as error:
        print(f"File can't be opned{error}")
        
def delete(path_to_delete):
    path=  WORKSPACE/path_to_delete
    
    if not path.exists():
        print("file or folder does not exist.")
        return
    if path.is_file():
        path.unlink()
        print(f"file deleted:{path}")

    elif path.is_dir():
        path.rmdir()
        print(f"folder deleted: {path}")

# list_files("Downloads")
# create_folders("Projects/NewProject/delete_me")
# create_files("Projects/NewProject/delete_me.txt")
# read_files("Projects/NewProject/Hello.txt")
# open_files("Projects/NewProject/Hello.txt")
delete("Projects/NewProject/delete_me")
