from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List, Any, Callable, Dict

class APIServer:
    def __init__(self, process_fn: Callable[[List[Any]], Dict[Any, Any]], get_etfs_fn: Callable, get_etf_history_fn: Callable[[str], str], allowed_origins: List[str] = None):
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
        self._setup_static()

    def _register_routes(self):
        # nu mai e necesar sa deschizi index.html, fisierul e servit de api
        @self.app.get("/", response_class=HTMLResponse)
        async def serve_index():
            html_path = Path("../page/index.html")
            return html_path.read_text(encoding="utf-8")

        @self.app.post("/process", response_model=Dict[Any, Any])
        async def process(payload: List[Any] = Body(...)):
            print("process")
            result = self.process_fn(payload)
            if not isinstance(result, dict):
                raise ValueError("process_fn must return a dictionary")
            return result
        
        # asta trebuie pus aici, ca altfel e singurul care poate fi accesat. (post-ul nu merge)
        @self.app.get("/get_etfs", response_model=List[Any])
        async def get_etfs():
            result = self.get_etfs_fn()
            if not isinstance(result, list):
                raise ValueError("get_etfs_fn must return a list")
            return result
        
        @self.app.get("/get_etf_history", response_model=str)
        async def get_etf_history(etf: str = Query()):
            result = self.get_etf_history_fn(etf)
            if not isinstance(result, str):
                raise ValueError("get_etf_history_fn must return a JSON string")
            return result

    # dam mount la fisierele statice (js, css), complet independente fata de aplicatia python
    def _setup_static(self):
        self.app.mount("/static", StaticFiles(directory="../page"), name="static")

    def get_app(self):
        return self.app
