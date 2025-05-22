from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Any, Callable
import uvicorn

class APIServer:
    """
    A simple API server that processes lists using a user-provided function.

    :param process_fn: Callable[[List[Any]], List[Any]] - Function to process incoming lists.
    :param allowed_origins: List[str] - CORS origins to allow.
    """
    def __init__(self, process_fn: Callable[[List[Any]], List[Any]], get_etfs_fn: Callable, allowed_origins: List[str] = None):
        if not callable(process_fn):
            raise ValueError("process_fn must be a callable that accepts and returns a List[Any]")
        self.process_fn = process_fn
        self.get_etfs_fn = get_etfs_fn
        self.app = FastAPI()
        # Configure CORS
        origins = allowed_origins or ["*"]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._register_routes()

    def _register_routes(self):
        @self.app.post("/process", response_model=List[Any])
        async def process(payload: List[Any] = Body(..., example=[1, 2, 3])):
            """Endpoint to process a list of values using the provided function."""
            result = self.process_fn(payload)
            if not isinstance(result, list):
                raise ValueError("process_fn must return a list")
            return result
    
    def _register_routes(self):
        @self.app.get("/get_etfs", response_model=List[Any])
        async def get_etfs():
            result = self.get_etfs_fn()
            if not isinstance(result, list):
                raise ValueError("get_etfs_fn must return a list")
            return result

    def run(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Start the API server.

        :param host: str - hostname to listen on
        :param port: int - port number
        """
        uvicorn.run(self.app, host=host, port=port)

# Example usage in your main file:
#
# from api import APIServer
#
# def my_processing_function(data: List[Any]) -> List[Any]:
#     # e.g., double each element if numeric
#     return [x * 2 if isinstance(x, (int, float)) else x for x in data]
#
# if __name__ == "__main__":
#     # Pass specific origins if needed, e.g. ["http://localhost:5500"]
#     server = APIServer(process_fn=my_processing_function, allowed_origins=["http://127.0.0.1:5500"])
#     server.run(host="0.0.0.0", port=8000)
