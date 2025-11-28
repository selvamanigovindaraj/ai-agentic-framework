"""Audit Logging System"""
import logging
import json
from datetime import datetime
from typing import Any, Dict

class AuditLogger:
    """Secure Audit Logger"""
    
    def __init__(self, log_file: str = "audit.log"):
        self.logger = logging.getLogger("audit_logger")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_event(self, event_type: str, agent_id: str, details: Dict[str, Any]):
        """Log a security event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "agent_id": agent_id,
            "details": details
        }
        self.logger.info(json.dumps(entry))
