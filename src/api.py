from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Any, Callable
import uvicorn

class APIServer:
    """
    :param process_fn: Callable[[List[Any]], List[Any]] - Function to process incoming lists.
    :param allowed_origins: List[str] - CORS origins to allow.
    """
    def __init__(self, process_fn: Callable[[List[Any]], List[Any]], get_etfs_fn: Callable, get_etf_history_fn: Callable[[str], str], allowed_origins: List[str] = None):
        if not callable(process_fn):
            raise ValueError("process_fn must be a callable that accepts and returns a List[Any]")
        self.process_fn = process_fn
        self.get_etfs_fn = get_etfs_fn
        self.get_etf_history_fn = get_etf_history_fn
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
            print("process")
            """Endpoint to process a list of values using the provided function."""
            result = self.process_fn(payload)
            if not isinstance(result, list):
                raise ValueError("process_fn must return a list")
            return result
        
        # asta trebuie pus aici, ca altfel e singurul care poate fi accesat. (post-ul nu merge)
        @self.app.get("/get_etfs", response_model=List[Any])
        async def get_etfs():
            print("get_etfs")
            result = self.get_etfs_fn()
            if not isinstance(result, list):
                raise ValueError("get_etfs_fn must return a list")
            return result
        
        @self.app.get("/get_etf_history", response_model=str)
        async def get_etf_history(etf: str = Query()):
            print("get_etf_history")
            result = self.get_etf_history_fn(etf)
            if not isinstance(result, str):
                raise ValueError("get_etf_history_fn must return a JSON string")
            return result

    
    # def _register_routes(self):
    #     @self.app.get("/get_etfs", response_model=List[Any])
    #     async def get_etfs():
    #         print("get_etfs")
    #         result = self.get_etfs_fn()
    #         if not isinstance(result, list):
    #             raise ValueError("get_etfs_fn must return a list")
    #         return result

    def run(self, host: str = "127.0.0.1", port: int = 8000):
        uvicorn.run(self.app, host=host, port=port)
