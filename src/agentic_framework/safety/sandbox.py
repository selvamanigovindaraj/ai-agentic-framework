"""Secure Code Execution Sandbox using Docker"""
import docker
from typing import Dict, Any, Optional
import tempfile
import os

class DockerSandbox:
    """Executes code in an isolated Docker container"""
    
    def __init__(self, image: str = "python:3.9-slim", timeout: int = 30):
        self.image = image
        self.timeout = timeout
        try:
            self.client = docker.from_env()
        except Exception:
            self.client = None
            print("⚠️ Docker client not available. Sandbox will fail.")

    def run_code(self, code: str) -> Dict[str, Any]:
        """Run Python code in the container"""
        if not self.client:
            return {"success": False, "error": "Docker not available"}
            
        try:
            # Pull image if needed
            try:
                self.client.images.get(self.image)
            except docker.errors.ImageNotFound:
                print(f"Pulling image {self.image}...")
                self.client.images.pull(self.image)

            # Create container
            container = self.client.containers.run(
                self.image,
                command=["python", "-c", code],
                detach=True,
                mem_limit="128m",
                network_disabled=True, # No internet access by default
                cpu_quota=50000, # 50% CPU
            )
            
            # Wait for result
            exit_code = container.wait(timeout=self.timeout)
            logs = container.logs().decode("utf-8")
            container.remove()
            
            if exit_code["StatusCode"] == 0:
                return {"success": True, "output": logs}
            else:
                return {"success": False, "error": logs}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
