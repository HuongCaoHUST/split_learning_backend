from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from database import create_table, register_node

app = FastAPI()

class RegisterRequest(BaseModel):
    action: str
    client_id: uuid.UUID


@app.get("/")
async def root():
    return {"message": "API is running"}

@app.on_event("startup")
async def startup_event():
    create_table()

@app.post("/register")
async def register(request: RegisterRequest):
    if request.action == "REGISTER":
        register_node(request.client_id)
        return {"message": "Node registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
