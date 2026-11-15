from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from file_manager import list_files, create_files, create_folders, read_files, delete

app = FastAPI(
    title= "Apis for file management",
    summary="/files, /files/folders, GET POST DELETE",
    version= "0.1.0",
    openapi_url= "/openapi.json"
)
@app.get("/")
def home():
    return{
        "message": "AI OS local-companion is running",
        "status" : "Online"
    }
@app.get("/files")
def get_files(folder: str = "Downloads"):
    return list_files(folder)

class createFileRequest(BaseModel):
    file: str
class createFolderRequest(BaseModel):
    folder: str


@app.post("/folder")
def post_folder(request: createFolderRequest):
    return create_folders(request.folder)

@app.post("/file")
def post_files(request: createFileRequest):
    return create_files(request.file)

@app.get("/file/read")
def read_file(file: str):
    return read_files(file)

class DeleteRequest(BaseModel):
    path: str
    confirm : bool = False
@app.delete("/delete")
def delete_file(request: DeleteRequest ):
    if not request.confirm:
        return {"message": "Deletion not confirmed. Set confirm to true."}
    return delete(request.path)

