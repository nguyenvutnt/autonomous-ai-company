"""
Autonomous AI Company — 16-Department Agent Orchestration Layer.

Step 2:
- Department #1: CEO & Chief of Staff (`CEOExecutiveAgent`)
- Department #15: HR & Agent Operations Director (`HRAgentDirector`)
"""

from __future__ import annotations

from .ceo_hr_orchestrator import CEOExecutiveAgent, HRAgentDirector
from .creative_video_division import (
    ContentCopywriterAgent,
    CreativeDirectorAgent,
    CreativeVideoStudioDivision,
    DesignStudioAgent,
    MediaLivestreamAgent,
    VideoEditorAgent,
)
from .finance_it_pipeline_division import (
    AccountantBookkeeperAgent,
    CFOFinancialStrategistAgent,
    FinanceITAndMasterPipelineDivision,
    ITDevOpsSecurityAgent,
)
from .seo_aio_sao_division import (
    AIOCitationAgent,
    SAOSocialAgenticAgent,
    SEOSpecialistAgent,
    SearchGrowthDivision,
)
from .social_ads_sale_division import (
    AdsViralSeedingAgent,
    SaleLeadCloserAgent,
    SocialAdsSaleDivision,
    SocialDistributionAgent,
)

__all__ = [
    "CEOExecutiveAgent",
    "HRAgentDirector",
    "SEOSpecialistAgent",
    "AIOCitationAgent",
    "SAOSocialAgenticAgent",
    "SearchGrowthDivision",
    "CreativeDirectorAgent",
    "ContentCopywriterAgent",
    "DesignStudioAgent",
    "MediaLivestreamAgent",
    "VideoEditorAgent",
    "CreativeVideoStudioDivision",
    "SocialDistributionAgent",
    "AdsViralSeedingAgent",
    "SaleLeadCloserAgent",
    "SocialAdsSaleDivision",
    "CFOFinancialStrategistAgent",
    "AccountantBookkeeperAgent",
    "ITDevOpsSecurityAgent",
    "FinanceITAndMasterPipelineDivision",
]
