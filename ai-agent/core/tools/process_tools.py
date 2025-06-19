import os
import psutil
import platform
import subprocess
from typing import Dict, List, Optional, Union
import logging
from datetime import datetime
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

load_dotenv()

class ProcessTools:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def list_processes(self, name_filter: Optional[str] = None) -> List[Dict]:
        """Get comprehensive information about all running processes, including detailed metrics like CPU usage, memory usage, etc. Optionally filter by process name."""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
            try:
                if name_filter and name_filter.lower() not in proc.info['name'].lower():
                    continue

                process = psutil.Process(proc.info['pid'])
                cpu = process.cpu_percent(interval=0.1)

                process_info = {
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'cpu_percent': cpu,
                    'memory_percent': proc.info['memory_percent'],
                    'status': process.status(),
                }
                processes.append(process_info)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return processes

    def kill_process(self, pid: int) -> bool:
        """Terminate a process by its PID."""
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=3)
            return True
        except psutil.NoSuchProcess:
            return False
        except psutil.TimeoutExpired:
            process.kill()
            return True

    def get_system_info(self) -> Dict:
        """Get system-wide resource usage statistics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            try:
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
            except Exception:
                disk_percent = None
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent
            }
        except Exception as e:
            return {'error': str(e)}

    def start_process(self, command: str, shell: bool = True) -> Optional[int]:
        """Start a new process with the given command."""
        try:
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return process.pid
        except Exception:
            return None

# Create an instance
process_tools_instance = ProcessTools()

# Define standalone functions with docstrings for LangGraph
@tool
def list_processes(name_filter=None):
    """Get comprehensive information about all running processes, including detailed metrics like CPU usage, memory usage, etc. Optionally filter by process name."""
    return process_tools_instance.list_processes(name_filter)

@tool
def get_system_info():
    """Get system-wide resource usage statistics."""
    return process_tools_instance.get_system_info()

@tool
def kill_process(pid: int):
    """Terminate a process by its PID."""
    return process_tools_instance.kill_process(pid)

@tool
def start_process(command: str, shell: bool = True):
    """Start a new process with the given command."""
    return process_tools_instance.start_process(command, shell)

llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.7
)

process_tools = [list_processes, get_system_info, kill_process, start_process]
process_langgraph_agent = create_react_agent(llm, process_tools) 