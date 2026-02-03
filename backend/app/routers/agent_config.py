"""
Agent Configuration API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..agent_config import AgentConfig, get_agent_config, update_agent_config, reset_agent_config

router = APIRouter(prefix="/api/agent-config", tags=["agent-config"])


@router.get("/", response_model=AgentConfig)
def get_current_config():
    """
    Get current AI agent configuration.
    """
    return get_agent_config()


@router.put("/", response_model=AgentConfig)
def update_config(config: AgentConfig):
    """
    Update AI agent configuration.
    All parameters are optional - only provided values will be updated.
    """
    return update_agent_config(config)


@router.post("/reset", response_model=AgentConfig)
def reset_config():
    """
    Reset AI agent configuration to default values.
    """
    return reset_agent_config()


@router.get("/schema")
def get_config_schema() -> Dict[str, Any]:
    """
    Get the configuration schema with descriptions and constraints.
    """
    return {
        "properties": AgentConfig.model_json_schema()["properties"],
        "defaults": AgentConfig().model_dump(),
        "description": "AI Quote Agent Configuration Schema"
    }


# Made with Bob