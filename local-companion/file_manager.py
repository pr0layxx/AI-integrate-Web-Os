from pathlib import Path
import os

WORKSPACE = Path(__file__).parent / "workspace"

def list_files(folder):
    folder_path = WORKSPACE/folder
    return [item.name for item in folder_path.iterdir()]
def create_folders(folder):
    folder_path = WORKSPACE/folder
    folder_path.mkdir(parents = True,  exist_ok = True)
    return {
        "message" : "Folder created successfully",
        "path" : str(folder_path)
    }
def create_files(file):
    path = WORKSPACE/file
    path.parent.mkdir(parents = True,  exist_ok = True)
    path.touch(exist_ok = True)
    return {
        "message":"File created successfully",
        "file" : str(path)
    }    

def read_files(file):
    path =  WORKSPACE/file
    if not path.exists():
        return {"error": "File not found"}

    if not path.is_file():
        return {"error": "Path is not a file"}

    return {
        "file": path.name,
        "content": path.read_text(encoding="utf-8")
    }   
    # with path.open("r", encoding = "utf-8") as file:
    #     content = file.read()
    # print(content)
    
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
    path = WORKSPACE / path_to_delete

    if not path.exists():
        return {"error": "File or folder does not exist"}

    if path.is_file():
        path.unlink()
        return {"message": f"File deleted: {path.name}"}

    elif path.is_dir():
        try:
            path.rmdir()
            return {"message": f"Folder deleted: {path.name}"}
        except OSError:
            return {"error": "Folder is not empty"}

    return {"error": "Unsupported path"}

# list_files("Downloads")
# create_folders("Projects/NewProject/delete_me")
# create_files("Projects/NewProject/delete_me.txt")
# read_files("Projects/NewProject/Hello.txt")
# open_files("Projects/NewProject/Hello.txt")
delete("Projects/NewProject/delete_me")
