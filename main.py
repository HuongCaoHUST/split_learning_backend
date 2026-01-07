from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from database import create_table, register_node, get_all_nodes, delete_node, delete_all_nodes

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

@app.get("/nodes")
async def get_nodes():
    nodes = get_all_nodes()
    return {"nodes": [dict(row) for row in nodes]}

@app.delete("/nodes/{client_id}")
async def delete_single_node(client_id: uuid.UUID):
    delete_node(client_id)
    return {"message": f"Node {client_id} deleted successfully"}

@app.delete("/nodes")
async def delete_all_nodes_endpoint():
    delete_all_nodes()
    return {"message": "All nodes deleted successfully"}

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
