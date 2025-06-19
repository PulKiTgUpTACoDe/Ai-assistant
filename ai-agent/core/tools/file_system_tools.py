import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Union
from datetime import datetime
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class FileSystemTools:
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.observer = Observer()
        self.observer.start()
        self.watched_paths = set()
        self.watch_paths = set()
        
    def set_base_path(self, new_path: str) -> bool:
        try:
            path = Path(new_path)
            if not path.exists():
                return False
            if not path.is_dir():
                return False
            self.base_path = path
            return True
        except Exception:
            return False

    def _get_full_path(self, path: str) -> Path:
        return self.base_path / path

    def _validate_path(self, path: Union[str, Path]) -> Path:

        path = Path(path)
        if not path.is_absolute():
            path = self.base_path / path
        try:
            path = path.resolve()
            if not str(path).startswith(str(self.base_path)):
                raise ValueError(f"Path {path} is outside the base directory {self.base_path}")
            return path
        except Exception as e:
            raise ValueError(f"Invalid path: {e}")

    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """Read the contents of a file."""
        try:
            path = self._validate_path(file_path)
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

    def write_file(self, file_path: str, content: str, encoding: str = 'utf-8') -> None:
        """Write content to a file, creating it if it doesn't exist."""
        try:
            path = self._validate_path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            raise

    def delete_file(self, file_path: str) -> None:
        """Delete a file at the given path."""
        try:
            path = self._validate_path(file_path)
            if path.is_file():
                path.unlink()
            else:
                raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            raise

    def list_directory(self, dir_path: str = '.', pattern: str = '*') -> List[Dict]:
        """List files and directories in the given directory, optionally filtered by pattern."""
        try:
            path = self._validate_path(dir_path)
            if not path.is_dir():
                raise NotADirectoryError(f"Not a directory: {dir_path}")
                
            results = []
            for item in path.glob(pattern):
                try:
                    stat = item.stat()
                    results.append({
                        'name': item.name,
                        'path': str(item.relative_to(self.base_path)),
                        'type': 'directory' if item.is_dir() else 'file',
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Error getting info for {item}: {e}")
            return results
        except Exception as e:
            logger.error(f"Error listing directory {dir_path}: {e}")
            raise

    def create_directory(self, dir_path: str) -> None:
        """Create a new directory at the given path."""
        try:
            path = self._validate_path(dir_path)
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating directory {dir_path}: {e}")
            raise

    def move_file(self, source: str, destination: str) -> None:
        """Move a file or directory from source to destination."""
        try:
            src = self._validate_path(source)
            dst = self._validate_path(destination)
            shutil.move(str(src), str(dst))
        except Exception as e:
            logger.error(f"Error moving {source} to {destination}: {e}")
            raise

    def copy_file(self, source: str, destination: str) -> None:
        """Copy a file or directory from source to destination."""
        try:
            src = self._validate_path(source)
            dst = self._validate_path(destination)
            if src.is_dir():
                shutil.copytree(str(src), str(dst))
            else:
                shutil.copy2(str(src), str(dst))
        except Exception as e:
            logger.error(f"Error copying {source} to {destination}: {e}")
            raise

    def get_file_hash(self, file_path: str, algorithm: str = 'sha256') -> str:
        """Get the hash of a file using the specified algorithm (default: sha256)."""
        try:
            path = self._validate_path(file_path)
            if not path.is_file():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            hash_obj = hashlib.new(algorithm)
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            raise

    def start_watching(self, dir_path: str, callback) -> None:
        
        try:
            path = self._validate_path(dir_path)
            if not path.is_dir():
                raise NotADirectoryError(f"Not a directory: {dir_path}")
                
            if self.observer is None:
                self.observer = Observer()
                self.observer.start()
                
            class Handler(FileSystemEventHandler):
                def on_any_event(self, event):
                    callback(event)
                    
            self.observer.schedule(Handler(), str(path), recursive=True)
            self.watch_paths.add(str(path))
        except Exception as e:
            logger.error(f"Error starting watch for {dir_path}: {e}")
            raise

    def stop_watching(self, dir_path: str) -> None:
       
        try:
            path = str(self._validate_path(dir_path))
            if path in self.watch_paths:
                # Stop all watches for this path
                self.observer.unschedule_all()
                self.watch_paths.remove(path)
        except Exception as e:
            logger.error(f"Error stopping watch for {dir_path}: {e}")
            raise

    def cleanup(self) -> None:
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.watch_paths.clear() 

# Create an instance
file_tools_instance = FileSystemTools()

# Define standalone functions with docstrings for LangGraph
@tool
def list_directory(dir_path: str = '.', pattern: str = '*'):
    """List files and directories in the given directory, optionally filtered by pattern."""
    return file_tools_instance.list_directory(dir_path, pattern)

@tool
def read_file(file_path: str, encoding: str = 'utf-8'):
    """Read the contents of a file."""
    return file_tools_instance.read_file(file_path, encoding)

@tool
def write_file(file_path: str, content: str, encoding: str = 'utf-8'):
    """Write content to a file, creating it if it doesn't exist."""
    return file_tools_instance.write_file(file_path, content, encoding)

@tool
def delete_file(file_path: str):
    """Delete a file at the given path."""
    return file_tools_instance.delete_file(file_path)

@tool
def create_directory(dir_path: str):
    """Create a new directory at the given path."""
    return file_tools_instance.create_directory(dir_path)

@tool
def move_file(source: str, destination: str):
    """Move a file or directory from source to destination."""
    return file_tools_instance.move_file(source, destination)

@tool
def copy_file(source: str, destination: str):
    """Copy a file or directory from source to destination."""
    return file_tools_instance.copy_file(source, destination)

@tool
def get_file_hash(file_path: str, algorithm: str = 'sha256'):
    """Get the hash of a file using the specified algorithm (default: sha256)."""
    return file_tools_instance.get_file_hash(file_path, algorithm)


llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.7
)

file_tools = [list_directory, read_file, write_file, delete_file, create_directory, move_file, copy_file, get_file_hash]

file_langgraph_agent = create_react_agent(llm, file_tools)