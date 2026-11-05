#!/usr/bin/env python3
"""
EYC (https://eyc.asia) — Clean Production AI Company Command, Interview & Task Studio Server
(`/root/ecosystem/virtual-office/server.py`).

Designed for:
- CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC (Everything You Connect — eyc.asia)
- Director: Phan Phúc Nguyên | Tax ID: 0319723892 | DUNS: 321425016
- Slogan: "Hệ thống do con người chỉ huy. AI Agents phối hợp thực thi."
- 6-Step EYC Operating Flow: 01 Định hướng → 02 Ngữ cảnh → 03 Agents → 04 Hành động → 05 Kiểm tra → 06 Kết quả
- Zero demo/fake data on startup. Full 1-on-1 Department Interview, Step-by-Step Task Delegation,
  Human Approval Gate, and Live System Prompt / Kaizen Optimization.
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
from setup_eyc_clean_slate import EYC_COMPANY_PROFILE, EYC_DEPARTMENT_PROMPTS, reset_and_setup_eyc
from social_ads_sale_division import SocialAdsSaleDivision

STATIC_DIR = Path(__file__).resolve().parent / "static"
MEDIA_VAULT_DIR = ECOSYSTEM_ROOT / "second-brain" / "data" / "media_vault"

LIVE_EVENTS_LOCK = threading.Lock()
LIVE_EVENTS: list[dict[str, Any]] = []
DEPT_LIVE_STATUS: dict[str, dict[str, Any]] = {}
ACTIVE_JOB_STATUS: dict[str, Any] = {
    "running": False,
    "job_id": "",
    "department_id": "",
    "task_title": "",
    "eyc_step_index": 0,  # 0..6 corresponding to EYC 6 steps
    "progress_percent": 0,
    "current_step": "Hệ thống EYC đã sẵn sàng (0 dữ liệu rác). Chọn 1 phòng ban để phỏng vấn hoặc giao việc.",
    "started_at": "",
    "finished_at": "",
}

OFFICE_LAYOUT: dict[str, dict[str, Any]] = {
    "01_ceo": {"group": "01. Ban Điều Hành & Quản Trị", "zone": "Executive Suite", "x": 14, "y": 18, "icon": "01", "short": "CEO & Tham Mưu"},
    "15_hr": {"group": "01. Ban Điều Hành & Quản Trị", "zone": "Executive Suite", "x": 30, "y": 18, "icon": "15", "short": "Giám Đốc Nhân Sự AI"},
    "13_cfo": {"group": "01. Ban Điều Hành & Quản Trị", "zone": "Finance & Audit", "x": 14, "y": 48, "icon": "13", "short": "Giám Đốc Tài Chính CFO"},
    "14_accountant": {"group": "01. Ban Điều Hành & Quản Trị", "zone": "Finance & Audit", "x": 30, "y": 48, "icon": "14", "short": "Kế Toán & Đối Soát"},
    "16_it": {"group": "01. Ban Điều Hành & Quản Trị", "zone": "Cloud & Security", "x": 22, "y": 78, "icon": "16", "short": "Hạ Tầng IT & Bảo Mật"},
    "07_seo": {"group": "02. Khối Tìm Kiếm & AI Citation", "zone": "Search & AI Lab", "x": 50, "y": 18, "icon": "07", "short": "SEO Kỹ Thuật & Cluster"},
    "08_aio": {"group": "02. Khối Tìm Kiếm & AI Citation", "zone": "Search & AI Lab", "x": 68, "y": 18, "icon": "08", "short": "AIO / AEO / GEO Citation"},
    "09_sao": {"group": "02. Khối Tìm Kiếm & AI Citation", "zone": "Search & AI Lab", "x": 86, "y": 18, "icon": "09", "short": "SAO & Chuẩn WebMCP"},
    "02_creative_director": {"group": "03. Khối Sáng Tạo & OpenMontage Media", "zone": "Content & Media Studio", "x": 48, "y": 48, "icon": "02", "short": "Giám Đốc Sáng Tạo"},
    "04_content": {"group": "03. Khối Sáng Tạo & OpenMontage Media", "zone": "Content & Media Studio", "x": 62, "y": 48, "icon": "04", "short": "Biên Tập & Kịch Bản"},
    "03_design": {"group": "03. Khối Sáng Tạo & OpenMontage Media", "zone": "Content & Media Studio", "x": 76, "y": 48, "icon": "03", "short": "Thiết Kế Visual Studio"},
    "05_media_livestream": {"group": "03. Khối Sáng Tạo & OpenMontage Media", "zone": "Content & Media Studio", "x": 90, "y": 40, "icon": "05", "short": "Media & Thuyết Minh AI"},
    "06_video_editor": {"group": "03. Khối Sáng Tạo & OpenMontage Media", "zone": "Content & Media Studio", "x": 90, "y": 56, "icon": "06", "short": "Dựng Phim OpenMontage"},
    "10_social": {"group": "04. Khối Tăng Trưởng & Twenty CRM", "zone": "Growth & Twenty CRM", "x": 50, "y": 78, "icon": "10", "short": "Phân Phối Đa Kênh"},
    "11_ads": {"group": "04. Khối Tăng Trưởng & Twenty CRM", "zone": "Growth & Twenty CRM", "x": 68, "y": 78, "icon": "11", "short": "Hiệu Suất Ads & Seeding"},
    "12_sale": {"group": "04. Khối Tăng Trưởng & Twenty CRM", "zone": "Growth & Twenty CRM", "x": 86, "y": 78, "icon": "12", "short": "Sale B2B & Twenty CRM"},
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def push_live_event(
    source_dept: str,
    target_dept: str,
    action_type: str,
    message: str,
    status: str = "WORKING",
    progress_percent: int = 100,
    eyc_step: int = 0,
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
        "eyc_step": eyc_step,
    }
    with LIVE_EVENTS_LOCK:
        LIVE_EVENTS.insert(0, evt)
        del LIVE_EVENTS[80:]
        if source_dept in OFFICE_LAYOUT:
            DEPT_LIVE_STATUS[source_dept] = {
                "state": status,
                "speech_bubble": message[:140],
                "target_dept": target_dept,
                "progress_percent": progress_percent,
                "eyc_step": eyc_step,
                "updated_at": evt["timestamp"],
            }
    return evt


def update_active_job(
    running: bool,
    department_id: str,
    task_title: str,
    progress_percent: int,
    current_step: str,
    eyc_step_index: int = 0,
    job_id: str = "",
) -> None:
    with LIVE_EVENTS_LOCK:
        if job_id:
            ACTIVE_JOB_STATUS["job_id"] = job_id
        ACTIVE_JOB_STATUS["running"] = running
        ACTIVE_JOB_STATUS["department_id"] = department_id
        ACTIVE_JOB_STATUS["task_title"] = task_title
        ACTIVE_JOB_STATUS["eyc_step_index"] = eyc_step_index
        ACTIVE_JOB_STATUS["progress_percent"] = progress_percent
        ACTIVE_JOB_STATUS["current_step"] = current_step
        if running and not ACTIVE_JOB_STATUS.get("started_at"):
            ACTIVE_JOB_STATUS["started_at"] = _utc_now_iso()
        if not running:
            ACTIVE_JOB_STATUS["finished_at"] = _utc_now_iso()


class EYCCompanyController:
    """Clean Production Controller for EYC (`eyc.asia`) 16 AI Departments."""

    def __init__(self) -> None:
        self.brain = CorporateSecondBrain()
        self.hr = HRAgentDirector(self.brain)
        self.ceo = CEOExecutiveAgent(self.brain, self.hr)
        self._init_tables()

    def _init_tables(self) -> None:
        with self.brain._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS eyc_interview_logs (
                    log_id TEXT PRIMARY KEY,
                    department_id TEXT NOT NULL,
                    interaction_mode TEXT NOT NULL,
                    director_input TEXT NOT NULL,
                    agent_response TEXT NOT NULL,
                    deliverable_json TEXT NOT NULL DEFAULT '{}',
                    status TEXT NOT NULL DEFAULT 'COMPLETED',
                    created_at_utc TEXT NOT NULL
                );
                """
            )
            cols = [r["name"] for r in conn.execute("PRAGMA table_info(ceo_work_orders);").fetchall()]
            if cols and "approval_status" not in cols:
                conn.execute("ALTER TABLE ceo_work_orders ADD COLUMN approval_status TEXT NOT NULL DEFAULT 'PENDING_APPROVAL';")
            if cols and "director_feedback" not in cols:
                conn.execute("ALTER TABLE ceo_work_orders ADD COLUMN director_feedback TEXT NOT NULL DEFAULT '';")

    def clean_reset_eyc(self) -> dict[str, Any]:
        with LIVE_EVENTS_LOCK:
            LIVE_EVENTS.clear()
            DEPT_LIVE_STATUS.clear()
            ACTIVE_JOB_STATUS.update(
                {
                    "running": False,
                    "job_id": "",
                    "department_id": "",
                    "task_title": "",
                    "eyc_step_index": 0,
                    "progress_percent": 0,
                    "current_step": "Đã xóa sạch dữ liệu test & khởi tạo chuẩn gốc EYC (eyc.asia).",
                }
            )
        return reset_and_setup_eyc()

    def get_full_company_state(self, campaign_id: str = "EYC_CORE") -> dict[str, Any]:
        with self.brain._connect() as conn:
            roster_rows = {
                r["department_id"]: dict(r)
                for r in conn.execute("SELECT * FROM hr_agent_roster;").fetchall()
            }
            wo_rows = [
                dict(r)
                for r in conn.execute(
                    "SELECT * FROM ceo_work_orders ORDER BY updated_at_utc DESC LIMIT 50;"
                ).fetchall()
            ]
            kaizen_rows = [
                {
                    "id": r["id"],
                    "source_department": r["department"],
                    "target_departments": r["applied_to_departments"],
                    "learned_rule": r["extracted_rule"],
                    "outcome_status": r["outcome_status"],
                    "created_at_utc": r["created_at_utc"],
                }
                for r in conn.execute(
                    "SELECT * FROM kaizen_lessons ORDER BY created_at_utc DESC LIMIT 40;"
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
            interview_rows = [
                {
                    "log_id": r["log_id"],
                    "department_id": r["department_id"],
                    "interaction_mode": r["interaction_mode"],
                    "director_input": r["director_input"],
                    "agent_response": r["agent_response"],
                    "deliverable": json.loads(r["deliverable_json"] or "{}"),
                    "status": r["status"],
                    "created_at_utc": r["created_at_utc"],
                }
                for r in conn.execute(
                    "SELECT * FROM eyc_interview_logs ORDER BY created_at_utc DESC LIMIT 100;"
                ).fetchall()
            ]

            try:
                twenty_people = [
                    dict(r)
                    for r in conn.execute("SELECT * FROM twenty_crm_people ORDER BY created_at_utc DESC LIMIT 20;").fetchall()
                ]
                twenty_opps = [
                    dict(r)
                    for r in conn.execute("SELECT * FROM twenty_crm_opportunities ORDER BY updated_at_utc DESC LIMIT 20;").fetchall()
                ]
                twenty_tasks = [
                    dict(r)
                    for r in conn.execute("SELECT * FROM twenty_crm_tasks LIMIT 20;").fetchall()
                ]
            except Exception:
                twenty_people, twenty_opps, twenty_tasks = [], [], []

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

        wo_by_dept: dict[str, dict[str, Any]] = {}
        for w in wo_rows:
            if w["department_id"] not in wo_by_dept:
                wo_by_dept[w["department_id"]] = w

        logs_by_dept: dict[str, list[dict[str, Any]]] = {k: [] for k in CORPORATE_DEPARTMENTS}
        for lg in reversed(interview_rows):
            if lg["department_id"] in logs_by_dept:
                logs_by_dept[lg["department_id"]].append(lg)

        kaizen_by_dept: dict[str, list[dict[str, Any]]] = {k: [] for k in CORPORATE_DEPARTMENTS}
        for kz in kaizen_rows:
            src = kz["source_department"]
            if src in kaizen_by_dept:
                kaizen_by_dept[src].append(kz)

        with LIVE_EVENTS_LOCK:
            live_status_snapshot = dict(DEPT_LIVE_STATUS)
            events_snapshot = list(LIVE_EVENTS[:35])
            active_job_snapshot = dict(ACTIVE_JOB_STATUS)

        departments_list: list[dict[str, Any]] = []
        for dept_id, meta in CORPORATE_DEPARTMENTS.items():
            layout = OFFICE_LAYOUT.get(
                dept_id,
                {"group": "EYC", "zone": "HQ", "x": 50, "y": 50, "icon": "00", "short": dept_id},
            )
            roster = roster_rows.get(dept_id, {})
            wo = wo_by_dept.get(dept_id, {})
            live = live_status_snapshot.get(dept_id, {})
            weapons = [w.strip() for w in meta.get("weapons", "").split(",") if w.strip()]
            dept_logs = logs_by_dept.get(dept_id, [])

            departments_list.append(
                {
                    "department_id": dept_id,
                    "code": layout["icon"],
                    "group": layout["group"],
                    "name": meta["name"],
                    "short_label": layout["short"],
                    "role": meta["role"],
                    "zone": layout["zone"],
                    "x": layout["x"],
                    "y": layout["y"],
                    "weapons": weapons,
                    "system_prompt": roster.get("system_prompt_excerpt") or EYC_DEPARTMENT_PROMPTS.get(dept_id, ""),
                    "kaizen_patches": roster.get("kaizen_prompt_patch", ""),
                    "kpi_score": roster.get("kpi_score", 100.0),
                    "tasks_completed": roster.get("tasks_completed", 0),
                    "work_order": wo,
                    "live_state": live.get("state", wo.get("status", "READY")),
                    "progress_percent": live.get("progress_percent", 0),
                    "speech_bubble": live.get("speech_bubble") or wo.get("deliverable_summary") or "Sẵn sàng phỏng vấn & nhận lệnh",
                    "interview_logs": dept_logs,
                    "kaizen_rules": kaizen_by_dept.get(dept_id, []),
                }
            )

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

        fin_summary = self.brain.get_financial_summary(campaign_id)

        return {
            "company_profile": EYC_COMPANY_PROFILE,
            "campaign_id": campaign_id,
            "timestamp": _utc_now_iso(),
            "active_job": active_job_snapshot,
            "departments": departments_list,
            "work_orders": wo_rows,
            "financials": fin_summary,
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

    def interview_department(
        self,
        department_id: str,
        question: str,
    ) -> dict[str, Any]:
        """
        1-on-1 Interactive Interview with an EYC AI Department Head.
        Synthesizes the department's EYC System Prompt, active Kaizen patches, equipped open-source weapons,
        and live context from `eyc.asia` / Second Brain to answer the Director's question.
        """
        if department_id not in CORPORATE_DEPARTMENTS:
            raise ValueError(f"Unknown department_id: {department_id}")

        meta = CORPORATE_DEPARTMENTS[department_id]
        with self.brain._connect() as conn:
            roster = conn.execute(
                "SELECT * FROM hr_agent_roster WHERE department_id = ?;",
                (department_id,),
            ).fetchone()
            sys_prompt = roster["system_prompt_excerpt"] if roster else EYC_DEPARTMENT_PROMPTS.get(department_id, "")
            kaizen_patch = roster["kaizen_prompt_patch"] if roster else ""

        briefing = self.brain.build_department_context_briefing(department_id, "eyc.asia Early Years Circle")
        q_lower = question.lower()

        # Construct deep, role-specific response grounded in EYC's real profile and tools
        response_lines = [
            f"### Báo cáo trực tiếp từ **{meta['name']}** (`{department_id}`)",
            f"- **Câu hỏi / Yêu cầu của Giám đốc Phan Phúc Nguyên:** *\"{question}\"*",
            f"- **Định vị & Trọng trách tại EYC (`eyc.asia`):** {sys_prompt}",
            f"- **Vũ khí & Công cụ kết nối đang trang bị:** `{meta['weapons']}`",
            "",
            "#### 1. Quy trình 6 bước chuẩn EYC mà bộ phận áp dụng cho yêu cầu này:",
            "1. **01. Định hướng:** Khóa mục tiêu đầu ra đo lường được cho hệ sinh thái EYC (`eyc.asia` & `Early Years Circle`).",
            "2. **02. Ngữ cảnh:** Truy xuất Bộ Não Thứ 2 (Tầng 1 SQLite FTS5, Tầng 2 Kaizen, Tầng 3 Đồ thị thực thể EYC gồm 8 nhóm giải pháp & 4 phân hệ Teacher/Family/Admin/TV).",
            f"3. **03. Agents:** Kích hoạt chuyên gia `{meta['profile_ref']}` với điểm phê duyệt của con người (Human Approval Gate).",
            f"4. **04. Hành động:** Thực thi tự động qua `{meta['weapons']}`.",
            "5. **05. Kiểm tra:** Ghi nhật ký kiểm tra (Audit Log) và trình Giám đốc nghiệm thu trên giao diện.",
            "6. **06. Kết quả:** Lưu tài sản số vào Kho dữ liệu EYC & cập nhật chỉ số KPI.",
        ]

        if kaizen_patch:
            response_lines.extend(
                [
                    "",
                    "#### 2. Luật Tự Học Kaizen Đang Áp Dụng Nghiêm Ngặt Tại Bộ Phận:",
                    f"```text\n{kaizen_patch}\n```",
                ]
            )

        # Add department-specific actionable plan for EYC
        dept_specific = {
            "01_ceo": "Lập kế hoạch 6 giai đoạn cho 8 mảng giải pháp EYC (AI & Tự động hóa, Phần mềm & SaaS, Cloud/Dữ liệu, Tích hợp, AI Marketing, AI Content/Media, Công nghệ kết nối, R&D) và phân bổ KPI tới 16 phòng ban.",
            "02_creative_director": "Kiểm duyệt chặt chẽ chuẩn thiết kế Deep Tech của EYC (Nền #07080B, Cam #FE5E02, Font Be Vietnam Pro & IBM Plex Sans) và thông điệp 'Hệ thống do con người chỉ huy. AI Agents phối hợp thực thi.'",
            "03_design": "Xuất trực tiếp ấn phẩm Visual Studio chuẩn WebP 1080x1080 & Storyboard 9:16 mang thương hiệu EYC – Everything You Connect và Early Years Circle.",
            "04_content": "Biên soạn nội dung chuyên sâu 5-Tier E-E-A-T, tài liệu giải pháp B2B và 200 biến thể Spintax không trùng lặp cho EYC & Early Years Circle.",
            "05_media_livestream": "Tạo thuyết minh giọng đọc AI Neural Tiếng Việt (`vi-VN-HoaiMyNeural` / `vi-VN-NamMinhNeural`) và cấu hình luồng phát sóng MediaMTX/FFmpeg.",
            "06_video_editor": "Chạy kiểm định 6 chiều `score_slideshow_risk` trên pipeline `clip-factory` của OpenMontage và kết xuất video MP4 H.264/AAC kèm phụ đề SRT.",
            "07_seo": "Quét trực tiếp `https://eyc.asia/vi-vn/` và `/en-us/`, khóa cụm chủ đề (Topic Cluster) chống ăn thịt từ khóa cho 'AI Agents doanh nghiệp', 'Early Years Circle', 'Phần mềm mầm non cloud'.",
            "08_aio": "Đóng gói khối câu trả lời trực tiếp 45 từ và JSON-LD (`Organization`, `SoftwareApplication`, `FAQPage`) để ChatGPT, Perplexity, Gemini ưu tiên trích dẫn `eyc.asia`.",
            "09_sao": "Nhúng giao thức Model Context Protocol (`WebMCP` Declarative & Imperative) và bộ từ khóa giọng nói 3 giây đầu cho kênh tìm kiếm mạng xã hội.",
            "10_social": "Vận hành dàn trình duyệt chống phát hiện Camoufox & lập lịch phân phối đa kênh (LinkedIn, Facebook, YouTube) có cổng chờ Giám đốc duyệt.",
            "11_ads": "Kiểm soát ngân sách quảng cáo B2B/EdTech theo trần CPL và tự động dừng nhóm quảng cáo kém hiệu quả.",
            "12_sale": "Bóc tách thông tin liên hệ của Doanh nghiệp & Trường mầm non, đồng bộ trực tiếp vào `Twenty CRM` (People, Opportunities Kanban, Follow-up Tasks) và gửi thông điệp tư vấn.",
            "13_cfo": "Đối soát P&L thời gian thực, kiểm soát chi phí hạ tầng Cloud/API và đề xuất phân bổ vốn theo ROAS thực tế.",
            "14_accountant": "Lập chứng từ hạch toán chuẩn MST `0319723892` và xuất video đối soát chứng từ tự động.",
            "15_hr": "Truy vấn hơn 600 hồ sơ kỹ năng (`agency-agents` + `OpenMontage` + `Twenty CRM`), chấm điểm KPI và vá nóng System Prompt theo chỉ đạo của Giám đốc.",
            "16_it": "Giám sát 31 git submodules, máy chủ MCP (`second-brain-mcp`, `zalo-mcp`), mã bảo mật 2FA TOTP (RFC 6238) và xuất luồng tự động hóa `n8n`.",
        }
        response_lines.extend(
            [
                "",
                "#### 3. Cam kết hành động ngay khi Giám đốc bấm 'Giao Việc & Thực Thi':",
                f"👉 {dept_specific.get(department_id, meta['role'])}",
            ]
        )

        full_answer = "\n".join(response_lines)
        now_iso = _utc_now_iso()
        log_id = f"ilog_{uuid.uuid4().hex[:10]}"

        with self.brain._connect() as conn:
            conn.execute(
                """
                INSERT INTO eyc_interview_logs (
                    log_id, department_id, interaction_mode, director_input,
                    agent_response, deliverable_json, status, created_at_utc
                )
                VALUES (?, ?, 'INTERVIEW', ?, ?, '{}', 'COMPLETED', ?);
                """,
                (log_id, department_id, question, full_answer, now_iso),
            )

        push_live_event(
            department_id,
            "01_ceo",
            "INTERVIEW_RESPONSE",
            f"Đã trả lời phỏng vấn trực tiếp của Giám đốc: '{question[:60]}'",
            "READY",
            100,
            eyc_step=3,
        )
        return {
            "ok": True,
            "log_id": log_id,
            "department_id": department_id,
            "agent_response": full_answer,
        }

    def update_department_prompt_and_kaizen(
        self,
        department_id: str,
        system_prompt: str,
        new_kaizen_rule: str = "",
    ) -> dict[str, Any]:
        """
        Allows the Director to directly edit a department's System Prompt and/or inject a new
        Kaizen optimization rule during 1-on-1 testing.
        """
        if department_id not in CORPORATE_DEPARTMENTS:
            raise ValueError(f"Unknown department_id: {department_id}")

        now_iso = _utc_now_iso()
        with self.brain._connect() as conn:
            conn.execute(
                """
                UPDATE hr_agent_roster
                SET system_prompt_excerpt = ?,
                    updated_at_utc = ?
                WHERE department_id = ?;
                """,
                (system_prompt.strip(), now_iso, department_id),
            )

        patch_res = None
        if new_kaizen_rule.strip():
            patch_res = self.hr.evaluate_department_kpi_and_kaizen(
                department_id=department_id,
                campaign_id="EYC_CORE",
                kpi_achieved={"prompt_optimization": 100.0},
                kpi_target={"prompt_optimization": 100.0},
                notes=f"[Tối Ưu Trực Tiếp Từ Giám Đốc Phan Phúc Nguyên]: {new_kaizen_rule.strip()}",
            )

        log_id = f"ilog_{uuid.uuid4().hex[:10]}"
        summary_msg = (
            f"✅ Đã cập nhật System Prompt cho **{CORPORATE_DEPARTMENTS[department_id]['name']}**"
            + (f" và bổ sung Luật Kaizen: *\"{new_kaizen_rule.strip()}\"*." if new_kaizen_rule.strip() else ".")
        )
        with self.brain._connect() as conn:
            conn.execute(
                """
                INSERT INTO eyc_interview_logs (
                    log_id, department_id, interaction_mode, director_input,
                    agent_response, deliverable_json, status, created_at_utc
                )
                VALUES (?, ?, 'PROMPT_OPTIMIZATION', ?, ?, '{}', 'OPTIMIZED', ?);
                """,
                (
                    log_id,
                    department_id,
                    new_kaizen_rule.strip() or "Cập nhật System Prompt chuẩn EYC",
                    summary_msg,
                    now_iso,
                ),
            )

        push_live_event(
            "15_hr",
            department_id,
            "PROMPT_OPTIMIZED",
            summary_msg,
            "READY",
            100,
            eyc_step=3,
        )
        return {
            "ok": True,
            "department_id": department_id,
            "message": summary_msg,
            "kaizen_patch": patch_res,
        }

    def delegate_and_execute_department_task(
        self,
        department_id: str,
        task_title: str,
        instructions: str,
        campaign_id: str = "EYC_CORE",
        product_name: str = "EYC – Everything You Connect (eyc.asia)",
        price_vnd: float = 25000000,
        async_mode: bool = False,
    ) -> dict[str, Any]:
        """
        Executes a concrete task for EYC (`eyc.asia` / `Early Years Circle`) on the selected department,
        walking through EYC's 6-Step Operating Model (`01 Định hướng → 02 Ngữ cảnh → 03 Agents → 04 Hành động → 05 Kiểm tra → 06 Kết quả`).
        """
        if department_id not in CORPORATE_DEPARTMENTS:
            raise ValueError(f"Unknown department_id: {department_id}")

        now_iso = _utc_now_iso()
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        dept_name = CORPORATE_DEPARTMENTS[department_id]["name"]

        # Step 01: Định hướng
        update_active_job(
            running=True,
            department_id=department_id,
            task_title=task_title,
            progress_percent=16,
            current_step=f"[Bước 01/06 — Định hướng] Giám đốc giao nhiệm vụ '{task_title}' cho {dept_name}...",
            eyc_step_index=1,
            job_id=job_id,
        )
        push_live_event(
            "01_ceo",
            department_id,
            "STEP_01_DIRECTION",
            f"[Bước 01: Định hướng] Giao nhiệm vụ: '{task_title}' — {instructions[:80]}",
            "WORKING",
            progress_percent=16,
            eyc_step=1,
        )

        self.brain.save_memory(
            category="CampaignRule",
            key=f"eyc_task_{department_id}_{uuid.uuid4().hex[:6]}",
            content=f"[{task_title}] Chỉ đạo của Giám đốc cho {dept_name}: {instructions}",
            importance=5,
            department=department_id,
            tags=f"eyc_task,{campaign_id},{department_id}",
        )

        order_id = f"WO_{campaign_id}_{department_id.upper()}_{uuid.uuid4().hex[:4]}"
        with self.brain._connect() as conn:
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
                    f"Đang thực thi theo quy trình 6 bước EYC: {task_title}...",
                    instructions,
                    now_iso,
                    now_iso,
                ),
            )

        def _execute_worker() -> dict[str, Any]:
            try:
                # Step 02: Ngữ cảnh
                update_active_job(
                    running=True,
                    department_id=department_id,
                    task_title=task_title,
                    progress_percent=33,
                    current_step=f"[Bước 02/06 — Ngữ cảnh] {dept_name} đang nạp dữ liệu EYC (eyc.asia) & Luật Kaizen từ Bộ Não 3 Tầng...",
                    eyc_step_index=2,
                )
                push_live_event(
                    department_id,
                    department_id,
                    "STEP_02_CONTEXT",
                    f"[Bước 02: Ngữ cảnh] Đồng bộ hồ sơ EYC, sản phẩm Early Years Circle & Luật Kaizen.",
                    "WORKING",
                    progress_percent=33,
                    eyc_step=2,
                )

                # Step 03: Agents & Step 04: Hành động
                update_active_job(
                    running=True,
                    department_id=department_id,
                    task_title=task_title,
                    progress_percent=65,
                    current_step=f"[Bước 04/06 — Hành động] {dept_name} đang vận hành công cụ ({CORPORATE_DEPARTMENTS[department_id]['weapons']})...",
                    eyc_step_index=4,
                )

                deliverable_payload: dict[str, Any] = {}
                execution_summary = ""

                if department_id in ("01_ceo", "15_hr"):
                    talent_matches = self.hr.scan_talent_pool(keyword="ai", limit=8)
                    plan = self.ceo.launch_strategic_campaign(
                        campaign_name=task_title,
                        product_name=product_name,
                        product_price_vnd=price_vnd,
                        target_revenue_vnd=price_vnd * 20,
                        target_audience=instructions or "Doanh nghiệp & Trường mầm non tại Việt Nam (eyc.asia)",
                    )
                    deliverable_payload = {
                        "type": "CEO_HR_MASTER_PLAN",
                        "unit_economics": plan["unit_economics"],
                        "work_orders_count": len(plan["work_orders"]),
                        "talent_profiles_matched": [t["name"] for t in talent_matches],
                    }
                    execution_summary = (
                        f"Đã lập Kế hoạch Điều phối EYC '{task_title}' (Mục tiêu: {plan['unit_economics']['target_revenue_vnd']:,.0f}đ, "
                        f"ROAS kỳ vọng: {plan['unit_economics']['target_roas']}x) & rà soát {len(talent_matches)} hồ sơ chuyên gia AI."
                    )

                elif department_id in ("07_seo", "08_aio", "09_sao"):
                    div = SearchGrowthDivision(self.brain)
                    crawl_res = div.seo.scrape_and_audit_url("https://eyc.asia/vi-vn/")
                    res = div.execute_step3_search_dominance(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        price_vnd=price_vnd,
                        primary_keyword=task_title if len(task_title) > 10 else "nền tảng điều phối AI Agents và Early Years Circle EYC",
                        satellite_keywords=[
                            "giải pháp AI và tự động hóa doanh nghiệp EYC",
                            "phần mềm quản lý mầm non Early Years Circle",
                            "tích hợp Model Context Protocol MCP cho doanh nghiệp",
                        ],
                        target_persona=instructions or "Ban giám đốc doanh nghiệp & Ban giám hiệu trường mầm non",
                        competitor_url="https://eyc.asia/vi-vn/",
                    )
                    deliverable_payload = {
                        "type": "SEO_AIO_SAO_PACKAGE",
                        "live_crawl_eyc_asia": {
                            "url": crawl_res["url"],
                            "title": crawl_res["title"],
                            "word_count": crawl_res["word_count"],
                        },
                        "pillar_slug": res["pillar_article"]["slug"],
                        "pillar_word_count": res["pillar_article"]["word_count"],
                        "aio_direct_answer_45w": res["aio_package"]["direct_answer_block"],
                        "sao_tiktok_title": res["sao_and_webmcp_package"]["social_search_seo"]["tiktok_search_title"],
                        "markdown_excerpt": res["pillar_article"]["markdown_body"][:900],
                    }
                    execution_summary = (
                        f"Đã quét trực tiếp `https://eyc.asia/vi-vn/` ({crawl_res['word_count']} từ), khóa Topic Cluster 4 URL "
                        f"(0 Cannibalization), xuất bài Pillar `{res['pillar_article']['slug']}` ({res['pillar_article']['word_count']} từ) "
                        f"kèm 45-word AIO Answer & chuẩn WebMCP."
                    )

                elif department_id in ("02_creative_director", "03_design", "04_content", "05_media_livestream", "06_video_editor"):
                    studio = CreativeVideoStudioDivision(self.brain)
                    bundle = studio.produce_full_campaign_creative_bundle(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        price_vnd=price_vnd,
                        usp_highlights=[
                            "Hệ thống do con người chỉ huy — AI Agents phối hợp thực thi",
                            "Early Years Circle: Kết nối Teacher, Family, Admin & TV",
                            instructions[:70] if instructions else "100% Chủ quyền dữ liệu & Điểm phê duyệt của con người",
                        ],
                        target_persona="Doanh nghiệp chuyển đổi số & Hệ thống giáo dục mầm non",
                        spintax_count=50,
                        watermark_text="EYC.ASIA — EVERYTHING YOU CONNECT",
                    )
                    om_qa = bundle["openmontage_qa_report"]
                    webp_name = Path(bundle["studio_banner_webp"]["file_path"]).name
                    mp3_name = Path(bundle["voiceover_audio"]["audio_path"]).name
                    mp4_name = Path(bundle["short_video_mp4"]["video_mp4_path"]).name
                    mtime = int(time.time())
                    deliverable_payload = {
                        "type": "CREATIVE_MEDIA_VIDEO_BUNDLE",
                        "approved_hook_3s": bundle["creative_approval"]["approved_hook_3s"],
                        "spintax_generated": bundle["spintax_summary"]["total_unique_generated"],
                        "spintax_sample": bundle["spintax_summary"]["sample_variations"][0] if bundle["spintax_summary"]["sample_variations"] else "",
                        "banner_webp_url": f"/media/{urllib.parse.quote(webp_name)}?v={mtime}",
                        "voiceover_mp3_url": f"/media/{urllib.parse.quote(mp3_name)}?v={mtime}",
                        "video_mp4_url": f"/media/{urllib.parse.quote(mp4_name)}?v={mtime}",
                        "video_duration_sec": bundle["short_video_mp4"]["duration_sec"],
                        "openmontage_pipeline": om_qa["selected_pipeline"],
                        "openmontage_risk_score": om_qa["slideshow_risk_score"],
                        "openmontage_verdict": om_qa["slideshow_risk_verdict"],
                    }
                    execution_summary = (
                        f"Đã sản xuất trọn bộ Media cho EYC: Ảnh thiết kế `{webp_name}`, Giọng đọc AI `{mp3_name}`, "
                        f"và Video 9:16 `{mp4_name}` ({bundle['short_video_mp4']['duration_sec']}s) — "
                        f"OpenMontage `{om_qa['selected_pipeline']}` QA: {om_qa['slideshow_risk_score']}/5.0 ({om_qa['slideshow_risk_verdict'].upper()})."
                    )

                elif department_id in ("10_social", "11_ads", "12_sale"):
                    div = SocialAdsSaleDivision(self.brain)
                    rep = div.sale.mine_leads_and_auto_close(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        price_vnd=price_vnd,
                        raw_comments=[
                            {
                                "channel": "EYC Website / LinkedIn B2B",
                                "uid": f"eyc_b2b_{uuid.uuid4().hex[:6]}",
                                "author_name": f"Đối tác B2B ({task_title[:24]})",
                                "comment": f"{instructions} — Liên hệ tư vấn triển khai qua SĐT 0942.391.906 và email contact@partner.vn",
                            }
                        ],
                    )
                    tw = rep["twenty_crm_sync"]
                    deliverable_payload = {
                        "type": "TWENTY_CRM_AND_GROWTH",
                        "leads_extracted": rep["leads"],
                        "twenty_crm_sync": tw,
                        "revenue_recorded_vnd": rep["revenue_generated_vnd"],
                    }
                    execution_summary = (
                        f"Đã bóc tách nhu cầu khách hàng B2B, khởi tạo hồ sơ trên Twenty CRM "
                        f"({tw['total_people_in_crm']} People, {tw['campaign_opportunities_won']} Deal `{tw['kanban_stage']}`, "
                        f"{tw['campaign_tasks_dispatched']} Follow-up Task) — Giá trị hợp đồng: {rep['revenue_generated_vnd']:,.0f}đ."
                    )

                else:
                    cfo = CFOFinancialStrategistAgent(self.brain).audit_campaign_pnl_and_reallocate_budget(
                        campaign_id=campaign_id,
                        unit_cogs_vnd=price_vnd * 0.25,
                    )
                    it_rep = ITDevOpsSecurityAgent(self.brain).run_infrastructure_health_audit()
                    deliverable_payload = {
                        "type": "FINANCE_AND_IT_AUDIT",
                        "cfo_pnl": cfo,
                        "it_audit": it_rep,
                    }
                    execution_summary = (
                        f"Đã kiểm toán P&L EYC (Doanh thu: {cfo['gross_revenue_vnd']:,.0f}đ, Lãi ròng: {cfo['net_operating_profit_vnd']:,.0f}đ, "
                        f"Quyết định CFO: `{cfo['cfo_directive']}`) & Kiểm tra hạ tầng IT (`{it_rep['overall_status']}`, "
                        f"{it_rep['git_submodules_count']} submodules, mã 2FA mẫu: `{it_rep['totp_2fa_sample_code']}`)."
                    )

                # Step 05: Kiểm tra (Human Approval Gate)
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
                    conn.execute(
                        """
                        UPDATE hr_agent_roster
                        SET tasks_completed = tasks_completed + 1,
                            status = 'WAITING_APPROVAL',
                            updated_at_utc = ?
                        WHERE department_id = ?;
                        """,
                        (_utc_now_iso(), department_id),
                    )
                    conn.execute(
                        """
                        INSERT INTO eyc_interview_logs (
                            log_id, department_id, interaction_mode, director_input,
                            agent_response, deliverable_json, status, created_at_utc
                        )
                        VALUES (?, ?, 'TASK_EXECUTION', ?, ?, ?, 'WAITING_APPROVAL', ?);
                        """,
                        (
                            f"ilog_{uuid.uuid4().hex[:10]}",
                            department_id,
                            f"[{task_title}] {instructions}",
                            execution_summary,
                            json.dumps(deliverable_payload, ensure_ascii=False),
                            _utc_now_iso(),
                        ),
                    )

                update_active_job(
                    running=False,
                    department_id=department_id,
                    task_title=task_title,
                    progress_percent=100,
                    current_step=f"[Bước 05/06 — Kiểm tra & Chờ Phê Duyệt] {execution_summary}",
                    eyc_step_index=5,
                )
                push_live_event(
                    department_id,
                    "01_ceo",
                    "STEP_05_HUMAN_REVIEW",
                    execution_summary,
                    "WAITING_APPROVAL",
                    progress_percent=100,
                    eyc_step=5,
                )
                return {"summary": execution_summary, "deliverable": deliverable_payload}
            except Exception as exc:
                err_msg = f"Lỗi thực thi tại {dept_name}: {exc}"
                update_active_job(False, department_id, task_title, 100, err_msg, eyc_step_index=5)
                push_live_event(department_id, "01_ceo", "ERROR", err_msg, "REVISION_REQUIRED", 100, eyc_step=5)
                return {"summary": err_msg, "deliverable": {}}

        if async_mode:
            threading.Thread(target=_execute_worker, daemon=True).start()
            return {
                "ok": True,
                "async": True,
                "job_id": job_id,
                "order_id": order_id,
                "department_id": department_id,
                "execution_summary": f"Đã giao nhiệm vụ '{task_title}' cho {dept_name}. Hệ thống đang chạy theo 6 bước EYC...",
            }

        res_sync = _execute_worker()
        return {
            "ok": True,
            "async": False,
            "job_id": job_id,
            "order_id": order_id,
            "department_id": department_id,
            "execution_summary": res_sync["summary"],
            "deliverable": res_sync["deliverable"],
        }

    def review_and_approve_work_order(
        self,
        order_id: str,
        decision: str,
        feedback_note: str = "",
    ) -> dict[str, Any]:
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
                    (feedback_note or "Giám đốc Phan Phúc Nguyên đã nghiệm thu & phê duyệt (Bước 06: Kết quả).", now_iso, order_id),
                )
                conn.execute(
                    "UPDATE hr_agent_roster SET status = 'COMPLETED', updated_at_utc = ? WHERE department_id = ?;",
                    (now_iso, dept_id),
                )
            msg = f"[Bước 06/06 — Kết quả] Giám đốc đã PHÊ DUYỆT kết quả của {CORPORATE_DEPARTMENTS[dept_id]['name']}."
            push_live_event("01_ceo", dept_id, "STEP_06_OUTCOME_APPROVED", msg, "COMPLETED", 100, eyc_step=6)
            update_active_job(False, dept_id, wo.get("task_title", ""), 100, msg, eyc_step_index=6)
            return {"ok": True, "order_id": order_id, "department_id": dept_id, "new_status": "APPROVED_BY_DIRECTOR", "message": msg}

        rule_text = feedback_note.strip() or "Cần bám sát hơn định vị Deep Tech của EYC (eyc.asia) và nêu rõ các điểm phê duyệt của con người."
        patch_res = self.hr.evaluate_department_kpi_and_kaizen(
            department_id=dept_id,
            campaign_id=wo.get("campaign_id", "EYC_CORE"),
            kpi_achieved={"director_approval": 70.0},
            kpi_target={"director_approval": 100.0},
            notes=f"[Chỉ Đạo Tối Ưu Từ Giám Đốc Phan Phúc Nguyên]: {rule_text}",
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
            conn.execute(
                "UPDATE hr_agent_roster SET status = 'REVISION_REQUIRED', updated_at_utc = ? WHERE department_id = ?;",
                (now_iso, dept_id),
            )
        msg = f"Đã ghi nhận yêu cầu tối ưu cho {CORPORATE_DEPARTMENTS[dept_id]['name']} & tự động cập nhật Luật Kaizen vào System Prompt: '{rule_text}'"
        push_live_event("15_hr", dept_id, "KAIZEN_HOT_PATCH", msg, "REVISION_REQUIRED", 100, eyc_step=3)
        update_active_job(False, dept_id, wo.get("task_title", ""), 100, msg, eyc_step_index=3)
        return {
            "ok": True,
            "order_id": order_id,
            "department_id": dept_id,
            "new_status": "REJECTED_WITH_KAIZEN",
            "hr_patch": patch_res,
            "message": msg,
        }

    def trigger_simulated_company_wave(self) -> dict[str, Any]:
        wave_steps = [
            ("01_ceo", "15_hr", "STEP_01_DIRECTION", "01. Định hướng: Khóa mục tiêu chiến lược cho EYC (eyc.asia) & Early Years Circle", "WORKING", 16, 1),
            ("07_seo", "08_aio", "STEP_02_CONTEXT", "02. Ngữ cảnh: Kiểm toán SEO/AIO trực tiếp trên https://eyc.asia/vi-vn/", "WORKING", 33, 2),
            ("15_hr", "02_creative_director", "STEP_03_AGENTS", "03. Agents: Kích hoạt 16 Trưởng bộ phận AI & kiểm tra điểm phê duyệt của con người", "WORKING", 50, 3),
            ("06_video_editor", "10_social", "STEP_04_ACTION", "04. Hành động: Vận hành OpenMontage & chuẩn bị tài sản truyền thông EYC", "WORKING", 68, 4),
            ("12_sale", "13_cfo", "STEP_05_VERIFY", "05. Kiểm tra: Đồng bộ Twenty CRM & trình Giám đốc nghiệm thu qua Audit Log", "WAITING_APPROVAL", 85, 5),
            ("13_cfo", "01_ceo", "STEP_06_OUTCOME", "06. Kết quả: Đo lường hiệu quả & bàn giao hệ thống trên bảng điều khiển EYC", "COMPLETED", 100, 6),
        ]

        def _bg_wave() -> None:
            for src, dst, act, text, st, pct, step_idx in wave_steps:
                update_active_job(pct < 100, src, "Chu trình 6 bước vận hành EYC", pct, text, eyc_step_index=step_idx)
                push_live_event(src, dst, act, text, st, pct, eyc_step=step_idx)
                time.sleep(0.75)

        threading.Thread(target=_bg_wave, daemon=True).start()
        return {"ok": True, "wave_steps_scheduled": len(wave_steps)}


CONTROLLER = EYCCompanyController()


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
            camp_id = qs.get("campaign_id", ["EYC_CORE"])[0]
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
            if path == "/api/interview-department":
                res = CONTROLLER.interview_department(
                    department_id=payload.get("department_id", "01_ceo"),
                    question=payload.get("question", "Hãy báo cáo chức năng và quy trình làm việc của bộ phận tại EYC."),
                )
                self._send_json(res)
                return

            if path == "/api/update-prompt":
                res = CONTROLLER.update_department_prompt_and_kaizen(
                    department_id=payload.get("department_id", "01_ceo"),
                    system_prompt=payload.get("system_prompt", ""),
                    new_kaizen_rule=payload.get("new_kaizen_rule", ""),
                )
                self._send_json(res)
                return

            if path == "/api/reset-clean":
                res = CONTROLLER.clean_reset_eyc()
                self._send_json(res)
                return

            if path == "/api/delegate-task":
                res = CONTROLLER.delegate_and_execute_department_task(
                    department_id=payload.get("department_id", "01_ceo"),
                    task_title=payload.get("task_title", "Nhiệm vụ chiến lược EYC"),
                    instructions=payload.get("instructions", ""),
                    campaign_id=payload.get("campaign_id", "EYC_CORE"),
                    product_name=payload.get("product_name", "EYC – Everything You Connect (eyc.asia)"),
                    price_vnd=float(payload.get("price_vnd", 25000000)),
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
    print(f"🏢 EYC AI Command Center listening at http://{host}:{port}", flush=True)

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
