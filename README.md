# Split Learning Backend

This project provides a simple backend for a split learning system, allowing nodes to register themselves.

## Prerequisites

- Docker
- Docker Compose

## Running the Application

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd split_learning_backend
   ```

2. **Start the application using Docker Compose:**
   ```bash
   docker-compose up -d
   ```
   The application will be running at `http://localhost:8000`.

## API Endpoints

### Test Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Description:** A simple endpoint to check if the API is running.
- **Success Response:**
  - **Code:** 200
  - **Content:** `{"message": "API is running"}`

### Register Node

- **URL:** `/register`
- **Method:** `POST`
- **Description:** Registers a new node in the system.
- **Request Body:**
  ```json
  {
    "action": "REGISTER",
    "client_id": "your-uuid-v4"
  }
  ```
  - `action` (string, required): Must be "REGISTER".
  - `client_id` (string, required): A unique identifier for the node (UUID v4 format).
- **Success Response:**
  - **Code:** 200
  - **Content:** `{"message": "Node registered successfully"}`
- **Error Response:**
  - **Code:** 400 Bad Request
  - **Content:** `{"detail": "Invalid action"}`

### Get All Nodes

- **URL:** `/nodes`
- **Method:** `GET`
- **Description:** Retrieves a list of all registered nodes.
- **Success Response:**
  - **Code:** 200
  - **Content:** 
    ```json
    {
      "nodes": [
        {
          "client_id": "2b846577-befe-4bef-837b-f1654de6abbf",
          "registered_at": "2026-01-07 10:00:00"
        }
      ]
    }
    ```

### Delete a Node

- **URL:** `/nodes/{client_id}`
- **Method:** `DELETE`
- **Description:** Deletes a specific node by its client ID.
- **URL Parameters:**
  - `client_id` (string, required): The UUID of the node to delete.
- **Success Response:**
  - **Code:** 200
  - **Content:** `{"message": "Node {client_id} deleted successfully"}`

### Delete All Nodes

- **URL:** `/nodes`
- **Method:** `DELETE`
- **Description:** Deletes all registered nodes.
- **Success Response:**
  - **Code:** 200
  - **Content:** `{"message": "All nodes deleted successfully"}`

### Example using cURL

**Register a node:**
```bash
curl -X POST "http://localhost:8000/register" -H "Content-Type: application/json" -d '{"action": "REGISTER", "client_id": "2b846577-befe-4bef-837b-f1654de6abbf"}'
```

**Get all nodes:**
```bash
curl -X GET "http://localhost:8000/nodes"
```

**Delete a specific node:**
```bash
curl -X DELETE "http://localhost:8000/nodes/2b846577-befe-4bef-837b-f1654de6abbf"
```

**Delete all nodes:**
```bash
curl -X DELETE "http://localhost:8000/nodes"
```
