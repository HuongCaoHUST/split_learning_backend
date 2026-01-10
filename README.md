# Split Learning Backend

This project provides a simple backend for a split learning system, allowing nodes to register themselves and update their hardware specifications and data information.

## Prerequisites

- Docker
- Docker Compose

## Running the Application

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd split_learning_backend
    ```

2.  **Start the application using Docker Compose:**
    ```bash
    docker-compose up -d
    ```
    The application will be running at `http://localhost:8000`.

## API Endpoints

### Test Endpoint

-   **URL:** `/`
-   **Method:** `GET`
-   **Description:** A simple endpoint to check if the API is running.
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** `{"message": "API is running"}`

### Register Node

-   **URL:** `/register`
-   **Method:** `POST`
-   **Description:** Registers a new node in the system. 

-   **Request Body:**
    ```json
    {
      "action": "REGISTER",
      "client_id": "your-uuid-v4",
      "run_id": "your-run-id"
    }
    ```
    -   `action` (string, required): Must be "REGISTER".
    -   `client_id` (string, required): A unique identifier for the node (UUID v4 format).
    -   `run_id` (string, required): A unique identifier for the run.
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** `{"message": "Node registered successfully"}`
-   **Error Response:**
    -   **Code:** 400 Bad Request
    -   **Content:** `{"detail": "Invalid action"}`

### Get All Nodes

-   **URL:** `/nodes`
-   **Method:** `GET`
-   **Description:** Retrieves a list of all registered nodes with their details.
-   **Success Response:**
    -   **Code:** 200
    -   **Content:**
        ```json
        [
          {
            "client_id": "2b846577-befe-4bef-837b-f1654de6abbf",
            "registered_at": "2026-01-07T10:00:00",
            "number_images": 1000,
            "ram": "8GB",
            "cpu": "Intel Core i7"
          }
        ]
        ```

### Get Single Node

-   **URL:** `/nodes/{client_id}/{run_id}`
-   **Method:** `GET`
-   **Description:** Retrieves details of a specific node by its client ID and run ID.
-   **URL Parameters:**
    -   `client_id` (string, required): The UUID of the node.
    -   `run_id` (string, required): The ID of the run.
-   **Success Response:**
    -   **Code:** 200
    -   **Content:**
        ```json
        {
          "client_id": "2b846577-befe-4bef-837b-f1654de6abbf",
          "run_id": "your-run-id",
          "registered_at": "2026-01-07T10:00:00",
          "number_images": 1000,
          "ram": "8GB",
          "cpu": "Intel Core i7"
        }
        ```
-   **Error Response:**
    -   **Code:** 404 Not Found
    -   **Content:** `{"detail": "Node not found"}`

### Update Node Details

-   **URL:** `/nodes/{client_id}/{run_id}`
-   **Method:** `PATCH`
-   **Description:** Updates specific details of an existing node. You can update `number_images`, `ram`, or `cpu`. Only provide the fields you wish to change.
-   **URL Parameters:**
    -   `client_id` (string, required): The UUID of the node to update.
    -   `run_id` (string, required): The ID of the run.
-   **Request Body (example):**
    ```json
    {
      "number_images": 1500,
      "ram": "16GB"
    }
    ```
    -   `number_images` (integer, optional): The number of images on the node.
    -   `ram` (string, optional): RAM specifications (e.g., "8GB", "16GB").
    -   `cpu` (string, optional): CPU specifications (e.g., "Intel Core i7", "AMD Ryzen 5").
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** The updated node object.
        ```json
        {
          "client_id": "2b846577-befe-4bef-837b-f1654de6abbf",
          "run_id": "your-run-id",
          "registered_at": "2026-01-07T10:00:00",
          "number_images": 1500,
          "ram": "16GB",
          "cpu": "Intel Core i7"
        }
        ```
-   **Error Response:**
    -   **Code:** 404 Not Found
    -   **Content:** `{"detail": "Node not found"}`
    -   **Code:** 500 Internal Server Error
    -   **Content:** `{"detail": "Failed to update node"}`

### Delete Nodes by Run ID

-   **URL:** `/nodes/{run_id}`
-   **Method:** `DELETE`
-   **Description:** Deletes all nodes associated with a specific run ID.
-   **URL Parameters:**
    -   `run_id` (string, required): The ID of the run.
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** `{"message": "Nodes with run_id {run_id} deleted successfully"}`

### Delete a Node

-   **URL:** `/nodes/{client_id}/{run_id}`
-   **Method:** `DELETE`
-   **Description:** Deletes a specific node by its client ID and run ID.
-   **URL Parameters:**
    -   `client_id` (string, required): The UUID of the node to delete.
    -   `run_id` (string, required): The ID of the run.
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** `{"message": "Node {client_id} with run_id {run_id} deleted successfully"}`

### Delete All Nodes

-   **URL:** `/nodes`
-   **Method:** `DELETE`
-   **Description:** Deletes all registered nodes.
-   **Success Response:**
    -   **Code:** 200
    -   **Content:** `{"message": "All nodes deleted successfully"}`

### Example using cURL

**Register a node:**
```bash
curl -X POST "http://localhost:8000/register" -H "Content-Type: application/json" -d '{"action": "REGISTER", "client_id": "2b846577-befe-4bef-837b-f1654de6abbf", "run_id": "your-run-id"}'
```

**Get all nodes:**
```bash
curl -X GET "http://localhost:8000/nodes"
```

**Get a single node:**
```bash
curl -X GET "http://localhost:8000/nodes/2b846577-befe-4bef-837b-f1654de6abbf/your-run-id"
```

**Update a node's details:**
```bash
curl -X PATCH "http://localhost:8000/nodes/2b846577-befe-4bef-837b-f1654de6abbf/your-run-id" -H "Content-Type: application/json" -d '{"number_images": 1200, "ram": "16GB"}'
```

**Delete nodes by run_id:**
```bash
curl -X DELETE "http://localhost:8000/nodes/your-run-id"
```

**Delete a specific node:**
```bash
curl -X DELETE "http://localhost:8000/nodes/2b846577-befe-4bef-837b-f1654de6abbf/your-run-id"
```

**Delete all nodes:**
```bash
curl -X DELETE "http://localhost:8000/nodes"
```