#!/usr/bin/env python3
"""
Real-Time Interactive Virtual Office & Executive Command Center Server
for the 16-Department Autonomous AI Company (`/root/ecosystem/virtual-office/server.py`).

Features:
- Instant non-blocking task delegation (`POST /api/delegate-task`) with background thread execution
  and real-time step-by-step progress tracking (0% -> 25% -> 50% -> 80% -> 100%).
- Animated 2D Virtual Office state with active moving packets, progress bars, and live terminal logs.
- Human-in-the-Loop Approval Gate (`APPROVE` & `REJECT_KAIZEN` with automatic HR #15 System Prompt hot-patching).
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import threading
import time
import urllib.parse
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))
sys.path.insert(0, str(ECOSYSTEM_ROOT / "agents"))

from ceo_hr_orchestrator import CEOExecutiveAgent, HRAgentDirector
from creative_video_division import CreativeVideoStudioDivision
from engine import CorporateSecondBrain, CORPORATE_DEPARTMENTS
from finance_it_pipeline_division import CFOFinancialStrategistAgent, AccountantBookkeeperAgent, ITDevOpsSecurityAgent
from seo_aio_sao_division import SearchGrowthDivision
from social_ads_sale_division import SocialAdsSaleDivision

STATIC_DIR = Path(__file__).resolve().parent / "static"
MEDIA_VAULT_DIR = ECOSYSTEM_ROOT / "second-brain" / "data" / "media_vault"

# Global Live Event Ring Buffer & Active Simulation State for Real-Time UI Streaming
LIVE_EVENTS_LOCK = threading.Lock()
LIVE_EVENTS: list[dict[str, Any]] = []
DEPT_LIVE_STATUS: dict[str, dict[str, Any]] = {}
ACTIVE_JOB_STATUS: dict[str, Any] = {
    "running": False,
    "job_id": "",
    "department_id": "",
    "task_title": "",
    "progress_percent": 0,
    "current_step": "Hệ thống sẵn sàng nhận lệnh",
    "started_at": "",
    "finished_at": "",
}

OFFICE_LAYOUT: dict[str, dict[str, Any]] = {
    "01_ceo": {"zone": "Executive Suite", "x": 14, "y": 16, "icon": "👑", "color": "#F59E0B", "short": "CEO #1"},
    "15_hr": {"zone": "Executive Suite", "x": 28, "y": 16, "icon": "🎖️", "color": "#EC4899", "short": "HR #15"},
    "13_cfo": {"zone": "Finance & Audit", "x": 14, "y": 42, "icon": "💎", "color": "#10B981", "short": "CFO #13"},
    "14_accountant": {"zone": "Finance & Audit", "x": 28, "y": 42, "icon": "🧾", "color": "#14B8A6", "short": "Kế Toán #14"},
    "16_it": {"zone": "Server & Security", "x": 21, "y": 68, "icon": "🛡️", "color": "#6366F1", "short": "IT/DevOps #16"},
    "07_seo": {"zone": "Search & AI Lab", "x": 48, "y": 18, "icon": "🔍", "color": "#3B82F6", "short": "SEO #7"},
    "08_aio": {"zone": "Search & AI Lab", "x": 68, "y": 18, "icon": "🧠", "color": "#8B5CF6", "short": "AIO #8"},
    "09_sao": {"zone": "Search & AI Lab", "x": 88, "y": 18, "icon": "⚡", "color": "#06B6D4", "short": "SAO #9"},
    "02_creative_director": {"zone": "OpenMontage Studio", "x": 48, "y": 48, "icon": "🎬", "color": "#F97316", "short": "Creative #2"},
    "04_content": {"zone": "OpenMontage Studio", "x": 64, "y": 48, "icon": "✍️", "color": "#EAB308", "short": "Content #4"},
    "03_design": {"zone": "OpenMontage Studio", "x": 80, "y": 48, "icon": "🎨", "color": "#EC4899", "short": "Design #3"},
    "05_media_livestream": {"zone": "OpenMontage Studio", "x": 92, "y": 38, "icon": "🎙️", "color": "#A855F7", "short": "Media #5"},
    "06_video_editor": {"zone": "OpenMontage Studio", "x": 92, "y": 56, "icon": "🎞️", "color": "#EF4444", "short": "Video #6"},
    "10_social": {"zone": "Growth & Twenty CRM", "x": 48, "y": 82, "icon": "🌐", "color": "#0EA5E9", "short": "Social #10"},
    "11_ads": {"zone": "Growth & Twenty CRM", "x": 68, "y": 82, "icon": "🚀", "color": "#F43F5E", "short": "Ads #11"},
    "12_sale": {"zone": "Growth & Twenty CRM", "x": 88, "y": 82, "icon": "🤝", "color": "#22C55E", "short": "Sale #12"},
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def push_live_event(
    source_dept: str,
    target_dept: str,
    action_type: str,
    message: str,
    status: str = "WORKING",
    progress_percent: int | None = None,
) -> dict[str, Any]:
    evt = {
        "event_id": f"evt_{uuid.uuid4().hex[:8]}",
        "timestamp": _utc_now_iso(),
        "source_dept": source_dept,
        "target_dept": target_dept,
        "action_type": action_type,
        "message": message,
        "status": status,
        "progress_percent": progress_percent,
    }
    with LIVE_EVENTS_LOCK:
        LIVE_EVENTS.insert(0, evt)
        del LIVE_EVENTS[80:]
        if source_dept in OFFICE_LAYOUT:
            DEPT_LIVE_STATUS[source_dept] = {
                "state": status,
                "speech_bubble": message[:110],
                "target_dept": target_dept,
                "progress_percent": progress_percent if progress_percent is not None else (100 if status != "WORKING" else 50),
                "updated_at": evt["timestamp"],
            }
        if target_dept in OFFICE_LAYOUT and status == "WORKING":
            DEPT_LIVE_STATUS[target_dept] = {
                "state": "WORKING",
                "speech_bubble": f"Đang nhận bàn giao từ {OFFICE_LAYOUT.get(source_dept, {}).get('short', source_dept)}: {message[:80]}",
                "target_dept": source_dept,
                "progress_percent": progress_percent or 35,
                "updated_at": evt["timestamp"],
            }
    return evt


def update_active_job(
    running: bool,
    department_id: str,
    task_title: str,
    progress_percent: int,
    current_step: str,
    job_id: str = "",
) -> None:
    with LIVE_EVENTS_LOCK:
        if job_id:
            ACTIVE_JOB_STATUS["job_id"] = job_id
        ACTIVE_JOB_STATUS["running"] = running
        ACTIVE_JOB_STATUS["department_id"] = department_id
        ACTIVE_JOB_STATUS["task_title"] = task_title
        ACTIVE_JOB_STATUS["progress_percent"] = progress_percent
        ACTIVE_JOB_STATUS["current_step"] = current_step
        if running and not ACTIVE_JOB_STATUS.get("started_at"):
            ACTIVE_JOB_STATUS["started_at"] = _utc_now_iso()
        if not running:
            ACTIVE_JOB_STATUS["finished_at"] = _utc_now_iso()


def _seed_initial_live_events() -> None:
    if LIVE_EVENTS:
        return
    push_live_event("01_ceo", "15_hr", "DELEGATE", "Phát hành 16 Work Orders chiến dịch CAMP_MASSAGE_11 (Mục tiêu 267M VNĐ)", "COMPLETED", 100)
    push_live_event("07_seo", "08_aio", "HANDOFF", "Khóa Topic Cluster 5 URL (0 Cannibalization) & chuyển sang AIO nhúng Schema JSON-LD", "COMPLETED", 100)
    push_live_event("06_video_editor", "10_social", "OPENMONTAGE_QA", "OpenMontage 'clip-factory' QA: Score 0.0/5.0 (STRONG) -> Xuất MP4 9:16 31.5s", "WAITING_APPROVAL", 100)
    push_live_event("11_ads", "04_content", "KAIZEN_SIGNAL", "Tự động tắt AdSet CPL 60kđ & bắn luật Kaizen Hook B sang Phòng Content/Video", "COMPLETED", 100)
    push_live_event("12_sale", "14_accountant", "TWENTY_CRM_WON", "Bóc tách 4 SĐT ẩn & đồng bộ Twenty CRM (4 WON Deals = 3,560,000đ)", "WAITING_APPROVAL", 100)
    push_live_event("13_cfo", "01_ceo", "BUDGET_APPROVAL", "ROAS đạt 12.92x, Biên lãi ròng 53.18% -> Đề xuất APPROVE_SCALE_UP_30_PERCENT", "WAITING_APPROVAL", 100)


class VirtualCompanyController:
    """Connects the Web UI directly to the 16 Department Agents and SQLite 3-Tier Second Brain."""

    def __init__(self) -> None:
        self.brain = CorporateSecondBrain()
        self.hr = HRAgentDirector(self.brain)
        self.ceo = CEOExecutiveAgent(self.brain, self.hr)
        self._ensure_approval_columns()
        self._ensure_all_16_work_orders_exist("CAMP_MASSAGE_11")
        _seed_initial_live_events()

    def _ensure_approval_columns(self) -> None:
        with self.brain._connect() as conn:
            cols = [r["name"] for r in conn.execute("PRAGMA table_info(ceo_work_orders);").fetchall()]
            if "approval_status" not in cols:
                conn.execute("ALTER TABLE ceo_work_orders ADD COLUMN approval_status TEXT NOT NULL DEFAULT 'PENDING_APPROVAL';")
            if "director_feedback" not in cols:
                conn.execute("ALTER TABLE ceo_work_orders ADD COLUMN director_feedback TEXT NOT NULL DEFAULT '';")

    def _ensure_all_16_work_orders_exist(self, campaign_id: str = "CAMP_MASSAGE_11") -> None:
        """Guarantees all 16 departments have active Work Orders under `campaign_id` for immediate UI interaction."""
        self.hr.recruit_full_16_department_roster()
        now_iso = _utc_now_iso()
        with self.brain._connect() as conn:
            existing_depts = {
                r["department_id"]
                for r in conn.execute(
                    "SELECT department_id FROM ceo_work_orders WHERE campaign_id = ?;",
                    (campaign_id,),
                ).fetchall()
            }
            for idx, (dept_id, meta) in enumerate(CORPORATE_DEPARTMENTS.items(), start=1):
                if dept_id not in existing_depts:
                    order_id = f"WO_{campaign_id}_{dept_id.upper()}"
                    conn.execute(
                        """
                        INSERT INTO ceo_work_orders (
                            order_id, campaign_id, department_id, phase_number,
                            task_title, sop_instructions, kpi_target_json, assigned_weapons,
                            status, deliverable_summary, kpi_achieved_json,
                            approval_status, director_feedback, created_at_utc, updated_at_utc
                        )
                        VALUES (?, ?, ?, ?, ?, ?, '{"completion": 100}', ?, 'WAITING_APPROVAL', ?, '{}', 'PENDING_APPROVAL', '', ?, ?);
                        """,
                        (
                            order_id,
                            campaign_id,
                            dept_id,
                            min(6, (idx - 1) // 3 + 1),
                            f"Chiến dịch Máy Massage Cổ Vai Gáy AI Pro — {meta['name']}",
                            meta["role"],
                            meta["weapons"],
                            f"Đã hoàn thành bàn giao chuẩn SOP: {meta['role']}",
                            now_iso,
                            now_iso,
                        ),
                    )

    def get_full_company_state(self, campaign_id: str = "CAMP_MASSAGE_11") -> dict[str, Any]:
        with self.brain._connect() as conn:
            roster_rows = {
                r["department_id"]: dict(r)
                for r in conn.execute("SELECT * FROM hr_agent_roster;").fetchall()
            }
            wo_rows = [
                dict(r)
                for r in conn.execute(
                    "SELECT * FROM ceo_work_orders WHERE campaign_id = ? ORDER BY phase_number ASC, department_id ASC;",
                    (campaign_id,),
                ).fetchall()
            ]
            kaizen_rows = [
                {
                    "source_department": r["department"],
                    "target_departments": r["applied_to_departments"],
                    "learned_rule": r["extracted_rule"],
                    "confidence": 0.95 if r["outcome_status"] == "WIN" else 0.90,
                    "created_at_utc": r["created_at_utc"],
                }
                for r in conn.execute(
                    "SELECT * FROM kaizen_lessons ORDER BY created_at_utc DESC LIMIT 25;"
                ).fetchall()
            ]
            kg_nodes = [
                dict(r)
                for r in conn.execute("SELECT * FROM kg_entities LIMIT 40;").fetchall()
            ]
            node_name_map = {n["entity_id"]: n["name"] for n in kg_nodes}
            kg_edges = [
                {
                    "source_entity": node_name_map.get(r["source_id"], r["source_id"]),
                    "relation_type": r["relation_type"],
                    "target_entity": node_name_map.get(r["target_id"], r["target_id"]),
                    "weight": r["weight"],
                }
                for r in conn.execute("SELECT * FROM kg_relations LIMIT 60;").fetchall()
            ]

            # Twenty CRM tables
            try:
                twenty_people = [
                    dict(r)
                    for r in conn.execute("SELECT * FROM twenty_crm_people ORDER BY created_at_utc DESC LIMIT 20;").fetchall()
                ]
                twenty_opps = [
                    dict(r)
                    for r in conn.execute(
                        "SELECT * FROM twenty_crm_opportunities WHERE campaign_id = ? ORDER BY updated_at_utc DESC LIMIT 20;",
                        (campaign_id,),
                    ).fetchall()
                ]
                twenty_tasks = [
                    dict(r)
                    for r in conn.execute("SELECT * FROM twenty_crm_tasks LIMIT 20;").fetchall()
                ]
            except Exception:
                twenty_people, twenty_opps, twenty_tasks = [], [], []

            # SEO Published Articles
            try:
                seo_articles = [
                    {
                        "article_id": r["article_id"],
                        "slug": r["slug"],
                        "title": r["title"],
                        "primary_keyword": r["primary_keyword"],
                        "word_count": r["word_count"],
                        "aio_direct_answer": r["aio_direct_answer"],
                        "webmcp_enabled": bool(r["webmcp_enabled"]),
                        "created_at_utc": r["created_at_utc"],
                    }
                    for r in conn.execute("SELECT * FROM seo_published_articles ORDER BY created_at_utc DESC LIMIT 10;").fetchall()
                ]
            except Exception:
                seo_articles = []

        wo_by_dept = {w["department_id"]: w for w in wo_rows}

        departments_list: list[dict[str, Any]] = []
        with LIVE_EVENTS_LOCK:
            live_status_snapshot = dict(DEPT_LIVE_STATUS)
            events_snapshot = list(LIVE_EVENTS[:35])
            active_job_snapshot = dict(ACTIVE_JOB_STATUS)

        for dept_id, meta in CORPORATE_DEPARTMENTS.items():
            layout = OFFICE_LAYOUT.get(dept_id, {"zone": "HQ", "x": 50, "y": 50, "icon": "🤖", "color": "#38BDF8", "short": dept_id})
            roster = roster_rows.get(dept_id, {})
            wo = wo_by_dept.get(dept_id, {})
            live = live_status_snapshot.get(dept_id, {})

            weapons = [w.strip() for w in meta.get("weapons", "").split(",") if w.strip()]

            departments_list.append(
                {
                    "department_id": dept_id,
                    "name": meta["name"],
                    "role": meta["role"],
                    "focus": meta["role"],
                    "zone": layout["zone"],
                    "x": layout["x"],
                    "y": layout["y"],
                    "icon": layout["icon"],
                    "color": layout["color"],
                    "short_label": layout["short"],
                    "weapons": weapons,
                    "system_prompt": roster.get("system_prompt_excerpt", ""),
                    "kaizen_patches": roster.get("kaizen_prompt_patch", ""),
                    "work_order": wo,
                    "kpi": {"kpi_score": roster.get("kpi_score", 100.0)},
                    "live_state": live.get("state", wo.get("status", "READY")),
                    "progress_percent": live.get("progress_percent", 100),
                    "speech_bubble": live.get("speech_bubble") or wo.get("deliverable_summary") or wo.get("task_title", "Sẵn sàng nhận lệnh"),
                    "target_dept": live.get("target_dept", ""),
                }
            )

        # Scan Media Vault (append mtime query param so browser refreshes updated MP4/WebP immediately)
        media_files: list[dict[str, Any]] = []
        if MEDIA_VAULT_DIR.exists():
            for p in sorted(MEDIA_VAULT_DIR.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True):
                if p.is_file() and p.suffix.lower() in (".mp4", ".webp", ".png", ".mp3", ".srt"):
                    mtime_int = int(p.stat().st_mtime)
                    media_files.append(
                        {
                            "filename": p.name,
                            "url": f"/media/{urllib.parse.quote(p.name)}?v={mtime_int}",
                            "ext": p.suffix.lower(),
                            "size_bytes": p.stat().st_size,
                            "updated_at": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                        }
                    )

        cfo_fin = CFOFinancialStrategistAgent(self.brain).audit_campaign_pnl_and_reallocate_budget(campaign_id=campaign_id)

        return {
            "campaign_id": campaign_id,
            "timestamp": _utc_now_iso(),
            "company_name": "AUTONOMOUS AI COMPANY (16 PHÒNG BAN & BỘ NÃO 3 TẦNG)",
            "active_job": active_job_snapshot,
            "integrated_engines": [
                {"name": "Paperclip AI Governance", "stars": "111.3K⭐", "role": "Org Chart, Goal Alignment & Approval Gate"},
                {"name": "OpenMontage Video Engine", "stars": "77.0K⭐", "role": "13 Pipelines & 6-Dim Anti-Slideshow QA (#6)"},
                {"name": "Twenty CRM GraphQL/Kanban", "stars": "60.5K⭐", "role": "People, Opportunities Kanban & Tasks (#12)"},
                {"name": "Pixel-Agents / AgentOffice", "stars": "10.5K⭐", "role": "Real-Time 2D Virtual Office Floorplan"},
                {"name": "3-Tier Corporate Second Brain", "stars": "Core", "role": "SQLite FTS5 + Kaizen Rules + LightRAG Graph"},
            ],
            "departments": departments_list,
            "work_orders": wo_rows,
            "financials": cfo_fin,
            "twenty_crm": {
                "people": twenty_people,
                "opportunities": twenty_opps,
                "tasks": twenty_tasks,
            },
            "media_vault": media_files[:20],
            "seo_articles": seo_articles,
            "kaizen_rules": kaizen_rows,
            "knowledge_graph": {
                "nodes": kg_nodes,
                "edges": kg_edges,
            },
            "live_events": events_snapshot,
        }

    def delegate_and_execute_department_task(
        self,
        department_id: str,
        task_title: str,
        instructions: str,
        campaign_id: str = "CAMP_MASSAGE_11",
        product_name: str = "Máy Massage Cổ Vai Gáy AI Pro",
        price_vnd: float = 890000,
        async_mode: bool = False,
    ) -> dict[str, Any]:
        """
        Assigns a live Work Order from the visual UI to a specific department (or CEO for full company).
        When `async_mode=True` (used by the Web UI), immediately marks the department `WORKING` with
        step-by-step live progress updates (15% -> 40% -> 75% -> 100%) in a background thread so the
        UI responds in <50ms and animates the workflow live!
        """
        if department_id not in CORPORATE_DEPARTMENTS:
            raise ValueError(f"Unknown department_id: {department_id}")

        now_iso = _utc_now_iso()
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        dept_name = CORPORATE_DEPARTMENTS[department_id]["name"]

        update_active_job(
            running=True,
            department_id=department_id,
            task_title=task_title,
            progress_percent=15,
            current_step=f"🚀 [15%] CEO (#1) đang giao lệnh '{task_title}' cho {dept_name}...",
            job_id=job_id,
        )
        push_live_event(
            "01_ceo",
            department_id,
            "DIRECT_ASSIGNMENT",
            f"[15%] Giao việc trực tiếp: '{task_title}' — {instructions[:70]}",
            "WORKING",
            progress_percent=15,
        )

        # Store custom instruction into Tier-1 Second Brain memory for that department
        self.brain.save_memory(
            category="CampaignRule",
            key=f"direct_wo_{department_id}_{uuid.uuid4().hex[:6]}",
            content=f"[{task_title}] Chỉ đạo trực tiếp từ Ban Giám Đốc trên Giao Diện Điều Hành: {instructions}",
            importance=5,
            department=department_id,
            tags=f"direct_delegation,{campaign_id},{department_id}",
        )

        # Update or insert Work Order in ceo_work_orders
        with self.brain._connect() as conn:
            existing = conn.execute(
                "SELECT order_id FROM ceo_work_orders WHERE campaign_id = ? AND department_id = ?;",
                (campaign_id, department_id),
            ).fetchone()
            if existing:
                order_id = existing["order_id"]
                conn.execute(
                    """
                    UPDATE ceo_work_orders
                    SET task_title = ?, sop_instructions = ?, status = 'WORKING',
                        deliverable_summary = ?, approval_status = 'PENDING_APPROVAL',
                        director_feedback = ?, updated_at_utc = ?
                    WHERE order_id = ?;
                    """,
                    (
                        task_title,
                        instructions,
                        f"⏳ Đang thực thi lệnh: {task_title} ({instructions[:80]})...",
                        instructions,
                        now_iso,
                        order_id,
                    ),
                )
            else:
                order_id = f"WO_{campaign_id}_{department_id.upper()}_{uuid.uuid4().hex[:4]}"
                conn.execute(
                    """
                    INSERT INTO ceo_work_orders (
                        order_id, campaign_id, department_id, phase_number,
                        task_title, sop_instructions, kpi_target_json, assigned_weapons,
                        status, deliverable_summary, kpi_achieved_json,
                        approval_status, director_feedback, created_at_utc, updated_at_utc
                    )
                    VALUES (?, ?, ?, 1, ?, ?, '{"completion": 100}', ?, 'WORKING', ?, '{}', 'PENDING_APPROVAL', ?, ?, ?);
                    """,
                    (
                        order_id,
                        campaign_id,
                        department_id,
                        task_title,
                        instructions,
                        CORPORATE_DEPARTMENTS[department_id]["weapons"],
                        f"⏳ Đang thực thi lệnh: {task_title}...",
                        instructions,
                        now_iso,
                        now_iso,
                    ),
                )

        def _execute_worker() -> str:
            try:
                update_active_job(
                    running=True,
                    department_id=department_id,
                    task_title=task_title,
                    progress_percent=40,
                    current_step=f"🧠 [40%] {dept_name} đang truy xuất Bộ Não 3 Tầng (SQLite FTS5 + Luật Kaizen + Đồ thị LightRAG)...",
                )
                push_live_event(
                    department_id,
                    department_id,
                    "SECOND_BRAIN_SYNC",
                    f"[40%] Đã nạp ngữ cảnh Bộ Não 3 Tầng & bắt đầu chạy vũ khí chuyên dụng cho '{task_title}'",
                    "WORKING",
                    progress_percent=40,
                )

                execution_summary = ""
                if department_id in ("01_ceo", "15_hr"):
                    self.hr.recruit_full_16_department_roster()
                    update_active_job(
                        running=True,
                        department_id=department_id,
                        task_title=task_title,
                        progress_percent=75,
                        current_step="📊 [75%] CEO (#1) & HR (#15) đang tính toán Unit Economics & phát hành 16 Work Orders...",
                    )
                    with self.brain._connect() as conn:
                        conn.execute(
                            """
                            UPDATE ceo_work_orders
                            SET status = 'WAITING_APPROVAL',
                                approval_status = 'PENDING_APPROVAL',
                                director_feedback = ?,
                                updated_at_utc = ?
                            WHERE campaign_id = ?;
                            """,
                            (instructions, _utc_now_iso(), campaign_id),
                        )
                    execution_summary = f"Đã lập Master Plan '{task_title}' & đồng bộ chỉ đạo mới cho toàn bộ 16/16 Phòng Ban."
                    push_live_event(department_id, "07_seo", "WORK_ORDERS_ISSUED", execution_summary, "WAITING_APPROVAL", 100)

                elif department_id in ("07_seo", "08_aio", "09_sao"):
                    update_active_job(
                        running=True,
                        department_id=department_id,
                        task_title=task_title,
                        progress_percent=70,
                        current_step="🔍 [70%] Khối Tìm Kiếm (#7 SEO, #8 AIO, #9 SAO) đang khóa Topic Cluster & xuất bản bài E-E-A-T + WebMCP...",
                    )
                    div = SearchGrowthDivision(self.brain)
                    res = div.execute_step3_search_dominance(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        price_vnd=price_vnd,
                        primary_keyword="máy massage cổ vai gáy loại nào tốt nhất 2026",
                        satellite_keywords=[
                            "máy massage cổ vai gáy cho dân văn phòng",
                            "cách giảm đau mỏi cổ vai gáy khi ngồi máy tính",
                        ],
                        target_persona=instructions or "Dân văn phòng & IT ngồi máy tính 8h/ngày",
                    )
                    execution_summary = (
                        f"[{task_title}] Xuất bản Pillar '{res['pillar_article']['slug']}' ({res['pillar_article']['word_count']} từ) + "
                        f"Schema JSON-LD + WebMCP Ready."
                    )
                    push_live_event(department_id, "02_creative_director", "SEARCH_CLUSTER_PUBLISHED", execution_summary, "WAITING_APPROVAL", 100)

                elif department_id in ("02_creative_director", "03_design", "04_content", "05_media_livestream", "06_video_editor"):
                    update_active_job(
                        running=True,
                        department_id=department_id,
                        task_title=task_title,
                        progress_percent=65,
                        current_step="🎬 [65%] Xưởng Phim OpenMontage (#2..#6) đang thu âm AI edge-tts, vẽ ảnh WebP & dựng video MP4 9:16...",
                    )
                    push_live_event(
                        "02_creative_director",
                        "06_video_editor",
                        "OPENMONTAGE_PIPELINE",
                        f"[65%] Đang chạy pipeline 'clip-factory' (OpenMontage) + thu âm edge-tts & render FFmpeg 1080x1920 cho '{task_title}'...",
                        "WORKING",
                        progress_percent=65,
                    )
                    studio = CreativeVideoStudioDivision(self.brain)
                    bundle = studio.produce_full_campaign_creative_bundle(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        price_vnd=price_vnd,
                        usp_highlights=[
                            "Xung điện TENS kép tác động sâu",
                            "Chườm ấm hồng ngoại chuẩn 42°C",
                            instructions[:65] if instructions else "Bảo hành 1 đổi 1 12 tháng - Freeship",
                        ],
                        target_persona="Dân văn phòng & Lập trình viên",
                        spintax_count=200,
                    )
                    om_qa = bundle["openmontage_qa_report"]
                    execution_summary = (
                        f"[{task_title}] Xuất Banner WebP + Audio TTS + Video 9:16 MP4 ({bundle['short_video_mp4']['duration_sec']}s) | "
                        f"OpenMontage '{om_qa['selected_pipeline']}' QA Score: {om_qa['slideshow_risk_score']}/5.0 ({om_qa['slideshow_risk_verdict'].upper()})."
                    )
                    push_live_event(department_id, "10_social", "CREATIVE_BUNDLE_READY", execution_summary, "WAITING_APPROVAL", 100)

                elif department_id in ("10_social", "11_ads", "12_sale"):
                    update_active_job(
                        running=True,
                        department_id=department_id,
                        task_title=task_title,
                        progress_percent=75,
                        current_step="🤝 [75%] Khối Tăng Trưởng & Sale (#10..#12) đang quét SĐT ẩn, bắn Zalo.Net & tạo Deal WON trên Twenty CRM...",
                    )
                    div = SocialAdsSaleDivision(self.brain)
                    rep = div.sale.mine_leads_and_auto_close(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        price_vnd=price_vnd,
                        raw_comments=[
                            {
                                "channel": "UI Live Task",
                                "uid": f"ui_{uuid.uuid4().hex[:6]}",
                                "author_name": f"Khách VIP ({task_title[:22]})",
                                "comment": f"Chốt ngay 1 máy theo yêu cầu '{task_title}', giao nhanh SĐT 0988.777.666 nhé!",
                            }
                        ],
                    )
                    tw = rep["twenty_crm_sync"]
                    execution_summary = (
                        f"[{task_title}] Đã quét Lead & đồng bộ Twenty CRM ({tw['total_people_in_crm']} People, "
                        f"{tw['campaign_opportunities_won']} WON Deals) -> Thu thêm {rep['revenue_generated_vnd']:,.0f}đ."
                    )
                    push_live_event(department_id, "13_cfo", "TWENTY_CRM_SYNCED", execution_summary, "WAITING_APPROVAL", 100)

                else:
                    update_active_job(
                        running=True,
                        department_id=department_id,
                        task_title=task_title,
                        progress_percent=75,
                        current_step="💎 [75%] Khối Tài Chính CFO (#13), Kế Toán (#14) & IT (#16) đang đối soát sổ cái P&L và kiểm tra bảo mật...",
                    )
                    cfo = CFOFinancialStrategistAgent(self.brain).audit_campaign_pnl_and_reallocate_budget(campaign_id=campaign_id)
                    it_rep = ITDevOpsSecurityAgent(self.brain).run_infrastructure_health_audit()
                    execution_summary = (
                        f"[{task_title}] P&L Lãi ròng: {cfo['net_operating_profit_vnd']:,.0f}đ (ROAS {cfo['actual_roas']}x -> {cfo['cfo_directive']}) | "
                        f"Hạ tầng IT: {it_rep['overall_status']} ({it_rep['git_submodules_count']} submodules)."
                    )
                    push_live_event(department_id, "01_ceo", "FINANCE_IT_AUDITED", execution_summary, "WAITING_APPROVAL", 100)

                with self.brain._connect() as conn:
                    conn.execute(
                        """
                        UPDATE ceo_work_orders
                        SET status = 'WAITING_APPROVAL',
                            approval_status = 'PENDING_APPROVAL',
                            deliverable_summary = ?,
                            updated_at_utc = ?
                        WHERE order_id = ?;
                        """,
                        (execution_summary, _utc_now_iso(), order_id),
                    )

                update_active_job(
                    running=False,
                    department_id=department_id,
                    task_title=task_title,
                    progress_percent=100,
                    current_step=f"✅ [100% HOÀN TẤT] {execution_summary}",
                )
                return execution_summary
            except Exception as exc:
                err_msg = f"❌ Lỗi thực thi tại {dept_name}: {exc}"
                update_active_job(
                    running=False,
                    department_id=department_id,
                    task_title=task_title,
                    progress_percent=100,
                    current_step=err_msg,
                )
                push_live_event(department_id, "01_ceo", "ERROR", err_msg, "REVISION_REQUIRED", 100)
                return err_msg

        if async_mode:
            threading.Thread(target=_execute_worker, daemon=True).start()
            return {
                "ok": True,
                "async": True,
                "job_id": job_id,
                "order_id": order_id,
                "department_id": department_id,
                "execution_summary": f"Đã phát lệnh '{task_title}' tới {dept_name}. Đang thực thi trực tiếp trên sơ đồ văn phòng ảo...",
            }

        summary = _execute_worker()
        return {
            "ok": True,
            "async": False,
            "job_id": job_id,
            "order_id": order_id,
            "department_id": department_id,
            "execution_summary": summary,
        }

    def review_and_approve_work_order(
        self,
        order_id: str,
        decision: str,
        feedback_note: str = "",
    ) -> dict[str, Any]:
        """
        Human-in-the-Loop Approval Gate:
        - `APPROVE`: Marks the work order `APPROVED` & `COMPLETED`, broadcasting confirmation to downstream departments.
        - `REJECT_KAIZEN`: Records a new Tier-2 Kaizen Self-Learning Rule, hot-patches the department's System Prompt via HR (#15),
          and marks the work order for revision.
        """
        now_iso = _utc_now_iso()
        with self.brain._connect() as conn:
            row = conn.execute("SELECT * FROM ceo_work_orders WHERE order_id = ?;", (order_id,)).fetchone()
            if not row:
                raise ValueError(f"Work order '{order_id}' not found")
            wo = dict(row)

        dept_id = wo["department_id"]
        if decision == "APPROVE":
            with self.brain._connect() as conn:
                conn.execute(
                    """
                    UPDATE ceo_work_orders
                    SET status = 'COMPLETED',
                        approval_status = 'APPROVED_BY_DIRECTOR',
                        director_feedback = ?,
                        updated_at_utc = ?
                    WHERE order_id = ?;
                    """,
                    (feedback_note or "Đã nghiệm thu & phê duyệt xuất bản.", now_iso, order_id),
                )
            msg = f"✅ Giám Đốc đã PHÊ DUYỆT Work Order của {CORPORATE_DEPARTMENTS[dept_id]['name']}: {feedback_note or 'Đạt chuẩn 100%'}"
            push_live_event("01_ceo", dept_id, "APPROVED", msg, "COMPLETED", 100)
            update_active_job(False, dept_id, wo.get("task_title", ""), 100, msg)
            return {"ok": True, "order_id": order_id, "department_id": dept_id, "new_status": "APPROVED_BY_DIRECTOR", "message": msg}

        # REJECT_KAIZEN: Inject Tier-2 Kaizen Rule & Hot-Patch Prompt via HR (#15)
        rule_text = feedback_note.strip() or "Phải tối ưu lại Hook 3s và CTA rõ ràng hơn theo chuẩn chuyển đổi thực chiến."
        patch_res = self.hr.evaluate_department_kpi_and_kaizen(
            department_id=dept_id,
            campaign_id=wo.get("campaign_id", "CAMP_MASSAGE_11"),
            kpi_achieved={"director_approval": 65.0},
            kpi_target={"director_approval": 100.0},
            notes=f"[Chỉ Đạo Trực Tiếp Từ Giám Đốc]: {rule_text}",
        )
        with self.brain._connect() as conn:
            conn.execute(
                """
                UPDATE ceo_work_orders
                SET status = 'REVISION_REQUIRED',
                    approval_status = 'REJECTED_WITH_KAIZEN',
                    director_feedback = ?,
                    updated_at_utc = ?
                WHERE order_id = ?;
                """,
                (rule_text, now_iso, order_id),
            )
        msg = f"🔄 Giám Đốc yêu cầu {CORPORATE_DEPARTMENTS[dept_id]['name']} làm lại & HR (#15) đã tự động vá System Prompt bằng luật Kaizen: '{rule_text}'"
        push_live_event("15_hr", dept_id, "KAIZEN_HOT_PATCH", msg, "REVISION_REQUIRED", 100)
        update_active_job(False, dept_id, wo.get("task_title", ""), 100, msg)
        return {
            "ok": True,
            "order_id": order_id,
            "department_id": dept_id,
            "new_status": "REJECTED_WITH_KAIZEN",
            "hr_patch": patch_res,
            "message": msg,
        }

    def trigger_simulated_company_wave(self) -> dict[str, Any]:
        """Emits a sequence of realistic inter-department handoff events across all 16 departments."""
        wave_steps = [
            ("01_ceo", "15_hr", "CEO_BRIEFING", "CEO (#1) & HR (#15) họp giao ban, khóa KPI ROAS >= 6.67x & CPL <= 33,375đ", "WORKING", 10),
            ("07_seo", "08_aio", "SEO_CLUSTER", "SEO (#7) khóa 5 URL Topic Cluster -> Chuyển AIO (#8) đóng gói JSON-LD & 45-word Answer", "WORKING", 20),
            ("09_sao", "04_content", "SAO_WEBMCP", "SAO (#9) xuất bộ từ khóa giọng nói 3s đầu & WebMCP Schema cho Content (#4)", "WORKING", 30),
            ("02_creative_director", "03_design", "HOOK_APPROVED", "Creative Director (#2) duyệt Hook B (Cảnh dân IT mỏi cổ 11h đêm) -> Chuyển Design (#3)", "WORKING", 45),
            ("05_media_livestream", "06_video_editor", "VOICE_READY", "Media (#5) xuất file thu âm vi-VN-HoaiMyNeural (31.51s) -> Chuyển Dựng Phim (#6)", "WORKING", 60),
            ("06_video_editor", "10_social", "OPENMONTAGE_RENDER", "Dựng Phim (#6) chạy OpenMontage 'clip-factory' (Risk 0.0/5 STRONG) & xuất MP4 9:16", "WAITING_APPROVAL", 70),
            ("10_social", "11_ads", "CAMOUFOX_DISPATCH", "Social (#10) kích hoạt 10 Profile Camoufox rải 12 kênh + Livestream MediaMTX 24/7", "WORKING", 80),
            ("11_ads", "12_sale", "ROAS_SCALING", "Ads (#11) nhân đôi ngân sách nhóm Reels CPL 20.3kđ & đẩy bình luận sang Sale (#12)", "WORKING", 88),
            ("12_sale", "14_accountant", "TWENTY_CRM_DEAL", "Sale (#12) lọc SĐT ẩn, bắn Zalo.Net & tạo 4 WON Deals trên Twenty CRM Kanban", "WAITING_APPROVAL", 95),
            ("14_accountant", "13_cfo", "PACKING_REPLAY", "Kế Toán (#14) xuất 8 video đóng gói Simple Replay & chuyển CFO (#13) duyệt lãi ròng 53.18%", "COMPLETED", 100),
        ]

        def _bg_wave() -> None:
            for src, dst, act, text, st, pct in wave_steps:
                update_active_job(pct < 100, src, "Mô phỏng dây chuyền 16 phòng ban", pct, f"⚡ [{pct}%] {text}")
                push_live_event(src, dst, act, text, st, pct)
                time.sleep(0.75)

        threading.Thread(target=_bg_wave, daemon=True).start()
        return {"ok": True, "wave_steps_scheduled": len(wave_steps)}


CONTROLLER = VirtualCompanyController()


class VirtualOfficeHTTPHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, data: Any, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def _serve_file(self, file_path: Path) -> None:
        if not file_path.exists() or not file_path.is_file():
            self._send_json({"error": "File not found"}, status=404)
            return
        mime_type, _ = mimetypes.guess_type(str(file_path))
        mime_type = mime_type or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self._serve_file(STATIC_DIR / "index.html")
            return

        if path == "/api/company-state":
            qs = urllib.parse.parse_qs(parsed.query)
            camp_id = qs.get("campaign_id", ["CAMP_MASSAGE_11"])[0]
            self._send_json(CONTROLLER.get_full_company_state(campaign_id=camp_id))
            return

        if path.startswith("/media/"):
            fname = urllib.parse.unquote(path[len("/media/"):])
            safe_path = (MEDIA_VAULT_DIR / fname).resolve()
            if MEDIA_VAULT_DIR.resolve() in safe_path.parents:
                self._serve_file(safe_path)
                return
            self._send_json({"error": "Invalid media path"}, status=403)
            return

        self._send_json({"error": f"Unknown route {path}"}, status=404)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", "0"))
        body_raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body_raw) if body_raw else {}
        except Exception:
            payload = {}

        try:
            if path == "/api/delegate-task":
                res = CONTROLLER.delegate_and_execute_department_task(
                    department_id=payload.get("department_id", "01_ceo"),
                    task_title=payload.get("task_title", "Nhiệm vụ đột xuất"),
                    instructions=payload.get("instructions", ""),
                    campaign_id=payload.get("campaign_id", "CAMP_MASSAGE_11"),
                    product_name=payload.get("product_name", "Máy Massage Cổ Vai Gáy AI Pro"),
                    price_vnd=float(payload.get("price_vnd", 890000)),
                    async_mode=bool(payload.get("async_mode", True)),
                )
                self._send_json(res)
                return

            if path == "/api/approve-work-order":
                res = CONTROLLER.review_and_approve_work_order(
                    order_id=payload.get("order_id", ""),
                    decision=payload.get("decision", "APPROVE"),
                    feedback_note=payload.get("feedback_note", ""),
                )
                self._send_json(res)
                return

            if path == "/api/simulate-wave":
                res = CONTROLLER.trigger_simulated_company_wave()
                self._send_json(res)
                return

            self._send_json({"error": f"Unknown POST route {path}"}, status=404)
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=500)


class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


def run_server(host: str = "0.0.0.0", port: int = 8090) -> None:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    primary_server = ReusableThreadingHTTPServer((host, port), VirtualOfficeHTTPHandler)
    print(f"🏢 Virtual AI Company Command Center listening at http://{host}:{port}", flush=True)

    if port != 80:
        try:
            http80_server = ReusableThreadingHTTPServer((host, 80), VirtualOfficeHTTPHandler)
            threading.Thread(target=http80_server.serve_forever, daemon=True).start()
            print(f"🌐 Standard HTTP Port 80 also active at http://{host}:80", flush=True)
        except OSError as exc:
            print(f"ℹ️ Port 80 bind skipped: {exc}", flush=True)

    primary_server.serve_forever()


if __name__ == "__main__":
    port_num = int(os.environ.get("VIRTUAL_OFFICE_PORT", "8090"))
    run_server(port=port_num)
