from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from database import create_table, register_node, get_all_nodes, delete_node, delete_all_nodes, get_node, update_node_details

app = FastAPI()

class RegisterRequest(BaseModel):
    action: str
    client_id: uuid.UUID

class Node(BaseModel):
    client_id: uuid.UUID
    registered_at: str
    number_images: Optional[int] = None
    ram: Optional[str] = None
    cpu: Optional[str] = None

class NodeUpdate(BaseModel):
    number_images: Optional[int] = None
    ram: Optional[str] = None
    cpu: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.on_event("startup")
async def startup_event():
    create_table()

@app.get("/nodes", response_model=list[Node])
async def get_nodes():
    nodes = get_all_nodes()
    return [Node(**dict(row)) for row in nodes]

@app.get("/nodes/{client_id}", response_model=Node)
async def get_single_node(client_id: uuid.UUID):
    node = get_node(client_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return Node(**dict(node))

@app.patch("/nodes/{client_id}", response_model=Node)
async def update_node(client_id: uuid.UUID, node_update: NodeUpdate):
    existing_node = get_node(client_id)
    if existing_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    
    updated = update_node_details(
        client_id=client_id,
        number_images=node_update.number_images,
        ram=node_update.ram,
        cpu=node_update.cpu
    )
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update node")
    
    # Fetch the updated node to return it
    updated_node = get_node(client_id)
    return Node(**dict(updated_node))

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
