"""
Autonomous AI Company — 16-Department Agent Orchestration Layer.

Step 2:
- Department #1: CEO & Chief of Staff (`CEOExecutiveAgent`)
- Department #15: HR & Agent Operations Director (`HRAgentDirector`)
"""

from __future__ import annotations

from .ceo_hr_orchestrator import CEOExecutiveAgent, HRAgentDirector

__all__ = [
    "CEOExecutiveAgent",
    "HRAgentDirector",
]
