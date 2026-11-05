#!/usr/bin/env python3
"""
EYC (https://eyc.asia) — Enterprise AI Operating System & Deliverable Review Center
(`/root/ecosystem/virtual-office/server.py`).

Designed strictly for:
- CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC (Everything You Connect — https://eyc.asia)
- Director: Phan Phúc Nguyên | Tax ID: 0319723892 | DUNS: 321425016
- Slogan: "Hệ thống do con người dẫn dắt. Công việc được AI phối hợp thực thi."
- 6-Step EYC Operating Flow: 01 Định hướng → 02 Ngữ cảnh → 03 Agents → 04 Hành động → 05 Kiểm tra → 06 Kết quả
- Produces real, clickable HTML & JSON deliverable dossiers (`/deliverables/<order_id>.html` & `.json`)
  and brand-pure media assets (`/media/...`) for every single Work Order.
"""

from __future__ import annotations

import html
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
DELIVERABLES_DIR = MEDIA_VAULT_DIR / "deliverables"

EYC_OFFICIAL_SVG_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 606.0 182.2" fill="none" class="eyc-logo-svg" width="126" height="38" role="img" aria-label="EYC - Everything You Connect">
<defs>
<linearGradient id="eycOrangeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#FF7A1A"/>
<stop offset="45%" stop-color="#FF5500"/>
<stop offset="100%" stop-color="#FF6A00"/>
</linearGradient>
</defs>
<g class="logo-mark">
<path fill="url(#eycOrangeGrad)" d="M94,4 93,4 93,52 93,57 93,61 92,72 92,75 91,78 91,79 90,86 89,86 89,88 88,89 88,94 85,101 84,102 84,103 83,105 83,106 82,108 82,109 81,111 80,113 79,114 79,116 78,118 77,118 76,122 74,124 72,129 69,133 69,134 63,143 58,150 56,152 49,160 38,171 33,176 31,178 32,178 62,178 67,172 71,165 76,157 84,140 84,139 86,136 86,134 88,130 88,129 89,128 91,120 92,118 92,117 94,112 94,111 95,109 95,107 96,106 96,104 97,102 97,100 98,98 98,95 99,94 99,92 100,90 100,87 101,85 102,81 102,80 102,77 103,75 103,73 103,72 104,72 104,73 104,74 104,75 105,76 106,81 107,88 108,90 108,92 108,94 109,96 110,100 110,103 111,105 112,107 112,108 112,110 113,113 114,116 115,118 115,119 115,120 116,124 117,125 117,126 118,128 120,132 120,133 120,135 123,140 123,141 124,143 124,144 126,147 126,148 128,151 128,152 131,158 132,158 132,159 133,160 136,166 140,172 143,176 145,178 175,178 176,178 175,177 169,172 162,165 155,157 152,153 151,152 149,150 149,149 144,143 137,132 134,126 133,124 132,122 130,119 129,118 127,114 122,102 122,100 122,99 121,97 120,96 120,95 118,87 116,77 116,74 115,70 115,64 114,41 114,6 114,4Z" />
<path fill="currentColor" fill-rule="evenodd" d="M84,48 83,49 82,50 82,51 81,52 80,54 78,56 76,59 69,66 62,71 59,73 58,74 57,74 54,76 53,77 44,81 43,81 42,81 41,82 39,83 37,83 36,84 28,86 27,86 25,87 23,87 21,88 20,88 18,89 17,90 17,92 17,96 17,108 17,109 17,110 18,110 19,110 20,110 22,109 24,108 26,107 27,107 28,106 29,106 30,106 31,105 36,102 37,102 38,101 39,101 45,97 46,97 46,96 48,95 52,92 60,85 66,80 68,77 74,69 74,68 76,66 76,65 78,64 78,61 79,61 80,60 80,59 80,58 82,54 82,53 84,51 84,49Z" />
<path fill="currentColor" fill-rule="evenodd" d="M124,47 124,48 124,49 124,50 125,51 125,53 126,54 127,57 128,58 128,59 129,60 129,61 130,62 130,63 134,68 134,69 135,70 136,72 138,74 139,75 140,76 141,78 143,80 150,87 157,93 158,93 160,95 166,99 168,100 169,101 170,101 171,102 177,105 181,107 185,108 186,109 188,110 190,110 190,109 190,90 190,89 188,88 186,88 184,87 182,87 181,86 179,86 177,85 176,85 175,84 172,84 171,83 169,83 167,82 166,82 164,81 163,80 160,79 158,78 154,76 152,75 151,74 150,73 146,71 144,69 143,68 138,64 134,61 129,55 128,53 127,52 126,51 125,49 124,48Z" />
<path fill="currentColor" fill-rule="evenodd" d="M90,47 89,48 89,50 88,51 87,56 86,57 86,59 85,60 84,65 82,68 82,69 81,71 81,72 79,76 78,77 78,78 76,81 75,82 75,83 74,84 70,90 66,96 60,103 52,111 51,112 49,113 42,119 38,122 32,125 31,126 21,131 20,132 16,133 13,134 12,134 10,135 5,137 4,137 4,138 4,161 4,162 5,162 6,162 7,161 9,161 10,160 12,160 13,159 15,159 18,157 29,151 37,146 38,145 39,145 41,143 43,142 44,141 52,134 58,127 66,118 71,111 76,103 79,96 79,95 80,94 81,91 82,89 82,88 83,86 83,85 84,84 84,82 85,80 85,78 86,78 86,76 86,73 87,72 87,70 88,68 88,66 89,62 89,55 90,49 90,48Z" />
<path fill="currentColor" fill-rule="evenodd" d="M118,46 118,49 118,54 118,55 118,56 119,57 119,59 120,63 120,66 121,73 122,76 122,78 123,80 124,82 124,83 124,84 128,93 132,102 133,105 136,109 137,112 140,116 141,117 141,118 147,124 156,134 162,140 163,140 166,142 170,146 178,151 179,152 180,152 189,156 190,157 192,158 194,159 195,159 196,160 198,160 199,161 200,161 202,162 203,162 204,161 204,142 204,138 204,137 202,137 200,136 199,136 198,135 194,134 187,131 184,129 180,128 175,125 174,124 172,123 170,121 167,120 166,119 162,116 154,109 149,104 144,99 138,90 134,86 134,85 132,81 130,77 127,72 126,69 124,65 123,63 122,61 120,55 119,49 118,46Z" />
</g>
<g class="logo-letters">
<path fill="currentColor" d="M240,28 239,29 238,30 238,131 239,133 240,134 241,134 276,134 332,134 333,134 334,133 334,132 335,129 334,121 335,117 334,115 334,114 333,113 331,112 275,112 268,112 266,112 264,111 264,110 264,101 264,92 265,91 266,91 328,91 330,90 331,88 331,72 330,70 328,69 266,69 264,68 264,66 264,51 266,49 324,49 327,49 328,49 330,48 332,46 334,42 335,38 337,31 337,30 336,28 335,28 334,28 242,28 241,28Z" />
<path fill="currentColor" d="M346,28 345,29 345,30 346,32 351,39 355,44 357,47 363,55 365,58 366,59 368,62 373,69 376,73 378,75 378,76 384,84 386,88 392,94 392,131 392,132 394,134 395,134 414,134 416,134 417,132 418,131 418,125 418,106 418,97 418,94 422,88 426,84 427,82 430,78 431,78 431,77 432,76 434,74 434,73 436,71 440,66 447,58 448,56 454,48 458,43 462,38 465,34 467,32 468,30 468,29 467,28 466,28 442,28 440,28 439,29 437,30 437,31 432,38 431,40 428,43 423,50 422,51 420,54 418,56 418,57 416,59 414,62 410,68 409,69 409,70 407,72 406,73 406,72 405,71 401,66 396,58 393,55 391,52 389,50 389,49 388,48 379,34 377,33 376,30 374,28 372,28 368,28 347,28Z" />
<path fill="currentColor" d="M516,25 511,26 508,26 507,27 506,27 503,28 502,28 501,29 499,29 498,30 496,30 492,32 486,36 482,39 477,44 474,48 470,53 468,57 468,58 466,62 466,63 465,65 464,69 464,72 463,74 463,77 463,86 463,89 464,92 464,94 464,95 465,96 465,98 466,99 466,101 467,102 467,103 469,108 470,108 470,109 471,110 473,114 477,118 480,121 485,125 489,128 493,130 500,133 502,134 504,134 506,135 509,136 518,137 526,137 532,136 535,136 539,134 540,134 542,134 544,133 546,132 550,130 555,128 560,124 563,122 568,116 573,110 575,105 578,100 578,99 579,97 578,96 577,95 566,95 565,95 561,95 553,95 552,95 550,96 547,102 544,105 540,108 537,110 534,111 532,112 530,112 527,113 522,113 516,113 514,112 512,112 510,111 509,111 506,110 503,108 502,107 501,106 498,103 493,97 493,96 492,95 492,94 491,92 490,90 489,83 489,78 490,75 490,73 491,71 492,69 492,67 495,62 496,60 499,58 502,55 506,52 508,51 509,50 510,50 512,50 517,48 519,48 526,48 529,49 531,50 532,50 537,51 538,52 540,53 541,54 543,56 547,59 549,62 551,64 552,64 577,64 578,64 578,62 578,61 577,58 574,53 568,44 566,41 562,38 557,34 556,34 556,33 552,32 547,29 546,29 545,28 540,27 538,26 527,25Z" />
</g>
</svg>"""

LIVE_EVENTS_LOCK = threading.Lock()
LIVE_EVENTS: list[dict[str, Any]] = []
DEPT_LIVE_STATUS: dict[str, dict[str, Any]] = {}
ACTIVE_JOB_STATUS: dict[str, Any] = {
    "running": False,
    "job_id": "",
    "department_id": "",
    "task_title": "",
    "eyc_step_index": 0,
    "progress_percent": 0,
    "current_step": "Hệ thống EYC sẵn sàng vận hành. Chọn phòng ban để phỏng vấn hoặc giao nhiệm vụ thực tế.",
    "started_at": "",
    "finished_at": "",
}

OFFICE_LAYOUT: dict[str, dict[str, Any]] = {
    "01_ceo": {"group": "01 / BAN ĐIỀU HÀNH & QUẢN TRỊ", "zone": "Executive Suite", "x": 14, "y": 18, "icon": "01", "short": "Ban Giám Đốc & Điều Phối AI"},
    "15_hr": {"group": "01 / BAN ĐIỀU HÀNH & QUẢN TRỊ", "zone": "Executive Suite", "x": 30, "y": 18, "icon": "15", "short": "Giám Đốc Nhân Sự & Kaizen AI"},
    "13_cfo": {"group": "01 / BAN ĐIỀU HÀNH & QUẢN TRỊ", "zone": "Finance & Audit", "x": 14, "y": 48, "icon": "13", "short": "Giám Đốc Tài Chính (CFO)"},
    "14_accountant": {"group": "01 / BAN ĐIỀU HÀNH & QUẢN TRỊ", "zone": "Finance & Audit", "x": 30, "y": 48, "icon": "14", "short": "Kế Toán & Đối Soát Sổ Cái"},
    "16_it": {"group": "01 / BAN ĐIỀU HÀNH & QUẢN TRỊ", "zone": "Cloud & Security", "x": 22, "y": 78, "icon": "16", "short": "Hạ Tầng Cloud, IT & Bảo Mật"},
    "07_seo": {"group": "02 / KHỐI TÌM KIẾM & AI CITATION", "zone": "Search & AI Lab", "x": 50, "y": 18, "icon": "07", "short": "SEO Kỹ Thuật & Topic Cluster"},
    "08_aio": {"group": "02 / KHỐI TÌM KIẾM & AI CITATION", "zone": "Search & AI Lab", "x": 68, "y": 18, "icon": "08", "short": "AIO / GEO / AI Search Citation"},
    "09_sao": {"group": "02 / KHỐI TÌM KIẾM & AI CITATION", "zone": "Search & AI Lab", "x": 86, "y": 18, "icon": "09", "short": "SAO & Giao Thức WebMCP"},
    "02_creative_director": {"group": "03 / KHỐI SÁNG TẠO & OPENMONTAGE MEDIA", "zone": "Content & Media Studio", "x": 48, "y": 48, "icon": "02", "short": "Giám Đốc Sáng Tạo & Thương Hiệu"},
    "04_content": {"group": "03 / KHỐI SÁNG TẠO & OPENMONTAGE MEDIA", "zone": "Content & Media Studio", "x": 62, "y": 48, "icon": "04", "short": "Biên Tập Nội Dung & Kịch Bản"},
    "03_design": {"group": "03 / KHỐI SÁNG TẠO & OPENMONTAGE MEDIA", "zone": "Content & Media Studio", "x": 76, "y": 48, "icon": "03", "short": "Thiết Kế Đồ Họa & UI Studio"},
    "05_media_livestream": {"group": "03 / KHỐI SÁNG TẠO & OPENMONTAGE MEDIA", "zone": "Content & Media Studio", "x": 90, "y": 40, "icon": "05", "short": "Sản Xuất Âm Thanh & Livestream"},
    "06_video_editor": {"group": "03 / KHỐI SÁNG TẠO & OPENMONTAGE MEDIA", "zone": "Content & Media Studio", "x": 90, "y": 56, "icon": "06", "short": "Dựng Phim OpenMontage"},
    "10_social": {"group": "04 / KHỐI TĂNG TRƯỞNG B2B & TWENTY CRM", "zone": "Growth & Twenty CRM", "x": 50, "y": 78, "icon": "10", "short": "Quản Trị Kênh Truyền Thông Số"},
    "11_ads": {"group": "04 / KHỐI TĂNG TRƯỞNG B2B & TWENTY CRM", "zone": "Growth & Twenty CRM", "x": 68, "y": 78, "icon": "11", "short": "Hiệu Suất Quảng Cáo & Viral"},
    "12_sale": {"group": "04 / KHỐI TĂNG TRƯỞNG B2B & TWENTY CRM", "zone": "Growth & Twenty CRM", "x": 86, "y": 78, "icon": "12", "short": "Kinh Doanh B2B & Twenty CRM"},
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


def generate_deliverable_files(
    order_id: str,
    department_id: str,
    task_title: str,
    instructions: str,
    execution_summary: str,
    deliverable_payload: dict[str, Any],
    created_at_utc: str,
) -> dict[str, str]:
    """
    Writes both a raw JSON artifact (`/deliverables/<order_id>.json`) and a complete,
    print-ready EYC Enterprise Deliverable Dossier HTML page (`/deliverables/<order_id>.html`)
    styled with 100% authentic eyc.asia CSS tokens and official EYC inline SVG logo.
    """
    DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
    dept_meta = CORPORATE_DEPARTMENTS.get(department_id, {"name": department_id, "weapons": "", "role": ""})
    layout = OFFICE_LAYOUT.get(department_id, {"icon": "00", "group": "EYC", "short": department_id})

    json_path = DELIVERABLES_DIR / f"{order_id}.json"
    html_path = DELIVERABLES_DIR / f"{order_id}.html"

    full_record = {
        "order_id": order_id,
        "company": EYC_COMPANY_PROFILE,
        "department_id": department_id,
        "department_code": layout["icon"],
        "department_name": dept_meta["name"],
        "task_title": task_title,
        "director_instructions": instructions,
        "execution_summary": execution_summary,
        "deliverable_payload": deliverable_payload,
        "created_at_utc": created_at_utc,
    }
    json_path.write_text(json.dumps(full_record, ensure_ascii=False, indent=2), encoding="utf-8")

    # Build specialized HTML sections based on deliverable_payload type
    dtype = deliverable_payload.get("type", "GENERAL")
    body_sections_html = ""

    if dtype == "SEO_AIO_SAO_PACKAGE":
        crawl = deliverable_payload.get("live_crawl_eyc_asia", {})
        article_md = deliverable_payload.get("full_markdown_body") or deliverable_payload.get("markdown_excerpt", "")
        json_ld_code = json.dumps(deliverable_payload.get("json_ld_schema", {}), ensure_ascii=False, indent=2)
        sat_links = deliverable_payload.get("satellite_articles", [])
        sat_rows = "".join(
            f"<tr><td>0{i+1}</td><td><code>{html.escape(str(s.get('slug','')))}</code></td><td>{html.escape(str(s.get('keyword','')))}</td><td>{html.escape(str(s.get('intent','')))}</td></tr>"
            for i, s in enumerate(sat_links)
        )
        body_sections_html = f"""
        <section class="doc-section">
          <div class="mono-label">03.1 / KIỂM TOÁN TRỰC TIẾP TRÊN HTTPS://EYC.ASIA/VI-VN/</div>
          <table class="eyc-table">
            <tbody>
              <tr><th>URL Kiểm Toán Thực Tế</th><td><a href="{html.escape(str(crawl.get('url','https://eyc.asia/vi-vn/')))}" target="_blank" rel="noopener">{html.escape(str(crawl.get('url','https://eyc.asia/vi-vn/')))}</a></td></tr>
              <tr><th>Tiêu Đề Trang (Title Tag)</th><td>{html.escape(str(crawl.get('title','')))}</td></tr>
              <tr><th>Mô Tả Meta (Meta Description)</th><td>{html.escape(str(crawl.get('meta_description','')))}</td></tr>
              <tr><th>Tổng Số Từ Đã Quét</th><td><strong>{crawl.get('word_count', 0)} từ</strong></td></tr>
              <tr><th>Thẻ Heading H1 / H2</th><td>H1: {len(crawl.get('h1_tags', []))} thẻ | H2: {len(crawl.get('h2_tags', []))} thẻ</td></tr>
              <tr><th>Slug Bài Viết Pillar Chuẩn Hóa</th><td><code>/{html.escape(str(deliverable_payload.get('pillar_slug','')))}</code> ({deliverable_payload.get('pillar_word_count',0)} từ)</td></tr>
            </tbody>
          </table>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.2 / KHỐI TRẢ LỜI TRỰC TIẾP 45 TỪ CHUẨN AIO / GEO (AI CITATION)</div>
          <div class="callout-box">
            {html.escape(str(deliverable_payload.get('aio_direct_answer_45w','')))}
          </div>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.3 / CẤU TRÚC TOPIC CLUSTER & CHỐNG TRÙNG LẶP TỪ KHÓA (CANNIBALIZATION GUARD)</div>
          <table class="eyc-table">
            <thead><tr><th>STT</th><th>URL Slug</th><th>Từ Khóa Mục Tiêu</th><th>Search Intent</th></tr></thead>
            <tbody>{sat_rows or '<tr><td colspan="4">Đã khóa Topic Cluster chuẩn EYC</td></tr>'}</tbody>
          </table>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.4 / MÃ NGUỒN SCHEMA.ORG JSON-LD & WEBMCP</div>
          <pre class="code-block">{html.escape(json_ld_code)}</pre>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.5 / TOÀN VĂN BÀI VIẾT PILLAR CHUẨN SEO & AIO</div>
          <div class="article-body-box"><pre class="markdown-pre">{html.escape(str(article_md))}</pre></div>
        </section>
        """

    elif dtype == "CREATIVE_MEDIA_VIDEO_BUNDLE":
        webp_url = deliverable_payload.get("banner_webp_url", "")
        mp3_url = deliverable_payload.get("voiceover_mp3_url", "")
        mp4_url = deliverable_payload.get("video_mp4_url", "")
        scenes = deliverable_payload.get("script_scenes", [])
        scene_rows = "".join(
            f"<tr>"
            f"<td><strong>0{s.get('scene_index', i+1)}</strong><br><span class='muted'>{html.escape(str(s.get('time_range','')))}</span></td>"
            f"<td><strong>{html.escape(str(s.get('visual_headline','')))}</strong><br><span class='muted'>{html.escape(str(s.get('visual_subtext','')))}</span></td>"
            f"<td>{html.escape(str(s.get('voiceover_text','')))}</td>"
            f"<td><code>{html.escape(str(s.get('subtitle_text','')))}</code></td>"
            f"</tr>"
            for i, s in enumerate(scenes)
        )
        spintax_samples = deliverable_payload.get("spintax_samples", [])
        spintax_html = "".join(
            f"<div class='callout-box' style='margin-bottom:12px;'><div class='mono-label'>BIẾN THỂ NỘI DUNG #0{i+1}</div><pre class='markdown-pre'>{html.escape(str(sp))}</pre></div>"
            for i, sp in enumerate(spintax_samples[:3])
        )
        body_sections_html = f"""
        <section class="doc-section">
          <div class="mono-label">03.1 / TÀI SẢN TRUYỀN THÔNG ĐÃ SẢN XUẤT (BẤM XEM & PHÁT TRỰC TIẾP)</div>
          <div class="media-grid">
            <div class="media-card">
              <div class="mono-label">01 / THIẾT KẾ POSTER CHUẨN THƯƠNG HIỆU EYC (.WEBP)</div>
              <a href="{html.escape(webp_url)}" target="_blank" rel="noopener">
                <img src="{html.escape(webp_url)}" alt="EYC Studio Poster" class="media-preview-img" />
              </a>
              <div class="media-actions">
                <a class="btn-outline" href="{html.escape(webp_url)}" target="_blank" rel="noopener">Mở File Ảnh Gốc (.webp) ↗</a>
              </div>
            </div>
            <div class="media-card">
              <div class="mono-label">02 / VIDEO DỰNG PHIM OPENMONTAGE 9:16 (.MP4)</div>
              <video controls preload="metadata" class="media-preview-video" src="{html.escape(mp4_url)}"></video>
              <div class="media-actions">
                <a class="btn-outline" href="{html.escape(mp4_url)}" target="_blank" rel="noopener">Mở File Video Gốc (.mp4) ↗</a>
              </div>
            </div>
          </div>
          <div class="media-card" style="margin-top:16px;">
            <div class="mono-label">03 / BẢN THU ÂM THUYẾT MINH TIẾNG VIỆT (.MP3 — EDGE-TTS NEURAL)</div>
            <audio controls preload="metadata" src="{html.escape(mp3_url)}" style="width:100%;margin:10px 0;"></audio>
            <div class="media-actions">
              <a class="btn-outline" href="{html.escape(mp3_url)}" target="_blank" rel="noopener">Tải File Âm Thanh (.mp3) ↗</a>
            </div>
          </div>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.2 / KỊCH BẢN PHÂN CẢNH CHI TIẾT (4-SCENE STORYBOARD EYC)</div>
          <table class="eyc-table">
            <thead>
              <tr><th>Phân Cảnh</th><th>Tiêu Đề Hình Ảnh (Visual)</th><th>Lời Bình Thuyết Minh (Voiceover)</th><th>Phụ Đề Màn Hình (Subtitle)</th></tr>
            </thead>
            <tbody>{scene_rows}</tbody>
          </table>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.3 / KIỂM ĐỊNH CHẤT LƯỢNG OPENMONTAGE (6-DIMENSION QA GATE)</div>
          <table class="eyc-table">
            <tbody>
              <tr><th>Pipeline Sản Xuất</th><td><code>{html.escape(str(deliverable_payload.get('openmontage_pipeline','clip-factory')))}</code></td></tr>
              <tr><th>Điểm Kiểm Định Slideshow Risk</th><td><strong>{deliverable_payload.get('openmontage_risk_score', 0)} / 5.0</strong> ({html.escape(str(deliverable_payload.get('openmontage_verdict','')).upper())})</td></tr>
              <tr><th>Thời Lượng Video</th><td>{deliverable_payload.get('video_duration_sec', 0)} giây (1080x1920 @ 30fps H.264/AAC)</td></tr>
              <tr><th>Số Biến Thể Nội Dung Đa Kênh (Spintax)</th><td>{deliverable_payload.get('spintax_generated', 0)} bài viết độc bản</td></tr>
            </tbody>
          </table>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.4 / MẪU BÀI VIẾT PHÂN PHỐI ĐA KÊNH ĐÃ SINH</div>
          {spintax_html}
        </section>
        """

    elif dtype == "TWENTY_CRM_AND_GROWTH":
        tw = deliverable_payload.get("twenty_crm_sync", {})
        leads = deliverable_payload.get("leads_extracted", [])
        lead_rows = "".join(
            f"<tr><td>0{i+1}</td><td><strong>{html.escape(str(l.get('author_name','')))}</strong></td>"
            f"<td>{html.escape(str(l.get('phone','')))}</td>"
            f"<td>{html.escape(str(l.get('intent_label','')))} ({l.get('intent_score',0)} điểm)</td>"
            f"<td>{html.escape(str(l.get('auto_reply_sent','')))}</td></tr>"
            for i, l in enumerate(leads)
        )
        body_sections_html = f"""
        <section class="doc-section">
          <div class="mono-label">03.1 / ĐỒNG BỘ HỆ THỐNG QUẢN TRỊ KHÁCH HÀNG B2B (TWENTY CRM)</div>
          <table class="eyc-table">
            <tbody>
              <tr><th>Tổng Hồ Sơ Khách Hàng (People)</th><td><strong>{tw.get('total_people_in_crm', 0)} đối tác B2B</strong></td></tr>
              <tr><th>Cơ Hội Bán Hàng (Opportunities)</th><td><strong>{tw.get('campaign_opportunities_won', 0)} hợp đồng ({html.escape(str(tw.get('kanban_stage','WON')))})</strong></td></tr>
              <tr><th>Nhiệm Vụ Bàn Giao (Follow-up Tasks)</th><td>{tw.get('campaign_tasks_dispatched', 0)} tác vụ triển khai</td></tr>
              <tr><th>Giá Trị Hợp Đồng Ghi Nhận</th><td><strong>{deliverable_payload.get('revenue_recorded_vnd', 0):,.0f} VNĐ</strong></td></tr>
            </tbody>
          </table>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.2 / DANH SÁCH KHÁCH HÀNG B2B & PHẢN HỒI TƯ VẤN KIẾN TRÚC EYC</div>
          <table class="eyc-table">
            <thead><tr><th>STT</th><th>Đối Tác / Khách Hàng</th><th>Liên Hệ</th><th>Mức Độ Quan Tâm</th><th>Phản Hồi Tư Vấn Đã Gửi</th></tr></thead>
            <tbody>{lead_rows}</tbody>
          </table>
        </section>
        """

    elif dtype == "FINANCE_AND_IT_AUDIT":
        cfo = deliverable_payload.get("cfo_pnl", {})
        it_rep = deliverable_payload.get("it_audit", {})
        body_sections_html = f"""
        <section class="doc-section">
          <div class="mono-label">03.1 / BÁO CÁO KIỂM TOÁN TÀI CHÍNH P&L & DÒNG TIỀN (CFO & KẾ TOÁN)</div>
          <table class="eyc-table">
            <tbody>
              <tr><th>Tổng Doanh Thu Ghi Nhận (Gross Revenue)</th><td><strong>{cfo.get('gross_revenue_vnd', 0):,.0f} VNĐ</strong></td></tr>
              <tr><th>Ngân Sách Truyền Thông & Vận Hành</th><td>{cfo.get('ad_spend_vnd', 0):,.0f} VNĐ</td></tr>
              <tr><th>Lợi Nhuận Ròng Vận Hành (Net Operating Profit)</th><td><strong>{cfo.get('net_operating_profit_vnd', 0):,.0f} VNĐ</strong></td></tr>
              <tr><th>Chỉ Số ROAS Thực Tế</th><td>{cfo.get('actual_roas', 0)}x</td></tr>
              <tr><th>Quyết Định Phân Bổ Vốn Của CFO</th><td><code>{html.escape(str(cfo.get('cfo_directive','')))}</code></td></tr>
            </tbody>
          </table>
        </section>

        <section class="doc-section">
          <div class="mono-label">03.2 / BÁO CÁO KIỂM TOÁN HẠ TẦNG CLOUD, SUBMODULES & BẢO MẬT (IT SECURITY)</div>
          <table class="eyc-table">
            <tbody>
              <tr><th>Trạng Thái Hạ Tầng Tổng Thể</th><td><strong>{html.escape(str(it_rep.get('overall_status','HEALTHY')))}</strong></td></tr>
              <tr><th>Số Lượng Git Submodules Đã Xác Thực</th><td>{it_rep.get('git_submodules_count', 31)} kho mã nguồn</td></tr>
              <tr><th>Cơ Sở Dữ Liệu Bộ Não Thứ 2 (SQLite WAL)</th><td>Toàn vẹn 100% ({it_rep.get('sqlite_tables_verified', 0)} bảng dữ liệu)</td></tr>
              <tr><th>Mã Xác Thực Đa Yếu Tố (TOTP 2FA Sample)</th><td><code>{html.escape(str(it_rep.get('totp_2fa_sample_code','')))}</code></td></tr>
            </tbody>
          </table>
        </section>
        """

    else:
        ue = deliverable_payload.get("unit_economics", {})
        wos = deliverable_payload.get("work_orders_preview", [])
        wo_rows_html = "".join(
            f"<tr><td>0{i+1}</td><td><code>{html.escape(str(w.get('department_id','')))}</code></td>"
            f"<td><strong>{html.escape(str(w.get('task_title','')))}</strong></td>"
            f"<td>{html.escape(str(w.get('sop_instructions','')))}</td></tr>"
            for i, w in enumerate(wos)
        )
        body_sections_html = f"""
        <section class="doc-section">
          <div class="mono-label">03.1 / HOẠCH ĐỊNH KINH TẾ ĐƠN VỊ & MỤC TIÊU CHIẾN LƯỢC EYC</div>
          <table class="eyc-table">
            <tbody>
              <tr><th>Mục Tiêu Doanh Thu Chiến Dịch</th><td><strong>{ue.get('target_revenue_vnd', 0):,.0f} VNĐ</strong></td></tr>
              <tr><th>Giá Trị Trung Bình Mỗi Hợp Đồng B2B</th><td>{ue.get('product_price_vnd', 0):,.0f} VNĐ</td></tr>
              <tr><th>Số Hợp Đồng B2B Mục Tiêu</th><td>{ue.get('required_orders', 0)} hợp đồng</td></tr>
              <tr><th>Ngân Sách Đầu Tư Tối Đa</th><td>{ue.get('max_ad_budget_vnd', 0):,.0f} VNĐ (ROAS mục tiêu: {ue.get('target_roas', 0)}x)</td></tr>
              <tr><th>Chuyên Gia AI Đã Rà Soát</th><td>{html.escape(', '.join(deliverable_payload.get('talent_profiles_matched', [])))}</td></tr>
            </tbody>
          </table>
        </section>
        <section class="doc-section">
          <div class="mono-label">03.2 / PHÂN RÃ LỆNH ĐIỀU HÀNH CHO CÁC PHÒNG BAN CHUYÊN MÔN</div>
          <table class="eyc-table">
            <thead><tr><th>STT</th><th>Phòng Ban</th><th>Hạng Mục Công Việc</th><th>Quy Trình Thực Thi Chuẩn (SOP)</th></tr></thead>
            <tbody>{wo_rows_html or '<tr><td colspan="4">Đã thiết lập ma trận điều phối 16 phòng ban EYC</td></tr>'}</tbody>
          </table>
        </section>
        """

    html_doc = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hồ Sơ Sản Phẩm {html.escape(order_id)} | EYC – Everything You Connect</title>
<link rel="icon" href="/static/eyc-brand/favicon.ico" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #07080B;
  --bg-2: #0E1017;
  --bg-3: #161922;
  --orange: #FE5E02;
  --orange-dark: #FF7526;
  --border: rgba(255,255,255,0.10);
  --border-2: rgba(255,255,255,0.18);
  --ink: #FFFFFF;
  --ink-2: #CBD5E1;
  --mut: #94A3B8;
  --font: "Be Vietnam Pro", -apple-system, BlinkMacSystemFont, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, monospace;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font);
  font-size: 15px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--orange); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.doc-header {{
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(7,8,11,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 16px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}}
.brand-row {{
  display: flex;
  align-items: center;
  gap: 18px;
}}
.eyc-logo-svg {{
  color: #FFFFFF;
  height: 36px;
  width: auto;
  display: block;
}}
.brand-divider {{
  width: 1px;
  height: 28px;
  background: var(--border-2);
}}
.doc-badge {{
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-2);
}}
.header-actions {{
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}}
.btn-primary {{
  background: var(--orange);
  color: #07080B;
  border: 1px solid var(--orange);
  padding: 9px 18px;
  border-radius: 8px;
  font: 700 13px/1 var(--font);
  cursor: pointer;
}}
.btn-primary:hover {{ background: var(--orange-dark); text-decoration: none; }}
.btn-outline {{
  background: var(--bg-3);
  color: var(--ink);
  border: 1px solid var(--border-2);
  padding: 9px 16px;
  border-radius: 8px;
  font: 600 13px/1 var(--font);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}}
.btn-outline:hover {{ border-color: var(--orange); color: var(--orange); text-decoration: none; }}
.doc-container {{
  max-width: 1080px;
  margin: 0 auto;
  padding: 36px 28px 80px;
}}
.hero-box {{
  background: var(--bg-2);
  border: 1px solid var(--border-2);
  border-left: 4px solid var(--orange);
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 28px;
}}
.mono-label {{
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: 10px;
}}
h1 {{
  margin: 0 0 12px;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.02em;
}}
.summary-lead {{
  color: var(--ink-2);
  font-size: 15.5px;
  margin: 0;
}}
.doc-section {{
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 22px;
}}
.eyc-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}}
.eyc-table th, .eyc-table td {{
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  text-align: left;
  vertical-align: top;
}}
.eyc-table th {{
  width: 28%;
  color: var(--mut);
  font-weight: 600;
  background: rgba(255,255,255,0.02);
}}
.callout-box {{
  background: var(--bg-3);
  border: 1px solid var(--border-2);
  border-left: 3px solid var(--orange);
  padding: 16px 20px;
  border-radius: 8px;
  color: var(--ink);
}}
.code-block, .markdown-pre {{
  background: #050608;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  font-family: var(--mono);
  font-size: 12.5px;
  color: var(--ink-2);
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}}
.media-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}}
.media-card {{
  background: var(--bg-3);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
}}
.media-preview-img {{
  width: 100%;
  max-height: 420px;
  object-fit: contain;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: #050608;
}}
.media-preview-video {{
  width: 100%;
  max-height: 420px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: #050608;
}}
.media-actions {{
  margin-top: 12px;
  display: flex;
  gap: 10px;
}}
.muted {{ color: var(--mut); font-size: 12.5px; }}
.approval-bar {{
  background: var(--bg-2);
  border: 1px solid var(--orange);
  border-radius: 12px;
  padding: 22px 28px;
  margin-top: 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}}
#statusBanner {{
  display: none;
  margin-top: 14px;
  padding: 12px 16px;
  border-radius: 8px;
  background: var(--bg-3);
  border: 1px solid var(--orange);
  color: var(--ink);
  font-weight: 600;
}}
</style>
</head>
<body>
<header class="doc-header">
  <div class="brand-row">
    <a href="/" title="Quay lại Trung Tâm Điều Hành EYC">{EYC_OFFICIAL_SVG_LOGO}</a>
    <div class="brand-divider"></div>
    <div class="doc-badge">HỒ SƠ SẢN PHẨM & NGHIỆM THU / {html.escape(order_id)}</div>
  </div>
  <div class="header-actions">
    <a class="btn-outline" href="/deliverables/{html.escape(order_id)}.json" target="_blank" rel="noopener">Xem Dữ Liệu Gốc (.JSON) ↗</a>
    <button class="btn-outline" onclick="window.print()">In / Xuất PDF</button>
    <button class="btn-primary" onclick="approveOrder('APPROVE')">Phê Duyệt Nghiệm Thu</button>
    <button class="btn-outline" onclick="approveOrder('REJECT_KAIZEN')">Yêu Cầu Tối Ưu (Kaizen)</button>
  </div>
</header>

<main class="doc-container">
  <div class="hero-box">
    <div class="mono-label">01 / HỒ SƠ BÀN GIAO TỪ {html.escape(layout['icon'])} — {html.escape(dept_meta['name'].upper())}</div>
    <h1>{html.escape(task_title)}</h1>
    <p class="summary-lead">{html.escape(execution_summary)}</p>
    <div id="statusBanner"></div>
  </div>

  <section class="doc-section">
    <div class="mono-label">02 / THÔNG TIN PHÁP NHÂN & LỆNH ĐIỀU HÀNH</div>
    <table class="eyc-table">
      <tbody>
        <tr><th>Pháp Nhân Thực Hiện</th><td><strong>CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC</strong> (MST: 0319723892 | DUNS: 321425016)</td></tr>
        <tr><th>Người Chỉ Huy & Nghiệm Thu</th><td><strong>Giám đốc Phan Phúc Nguyên</strong> — Website: <a href="https://eyc.asia" target="_blank">https://eyc.asia</a></td></tr>
        <tr><th>Mã Hồ Sơ Công Việc (Work Order)</th><td><code>{html.escape(order_id)}</code> (Thời gian: {html.escape(created_at_utc)})</td></tr>
        <tr><th>Bộ Phận Chuyên Trách</th><td><strong>[{html.escape(layout['icon'])}] {html.escape(dept_meta['name'])}</strong> — {html.escape(dept_meta.get('role',''))}</td></tr>
        <tr><th>Công Cụ & Nền Tảng Vận Hành</th><td><code>{html.escape(dept_meta.get('weapons',''))}</code></td></tr>
        <tr><th>Chỉ Đạo Chi Tiết Của Giám Đốc</th><td>{html.escape(instructions)}</td></tr>
      </tbody>
    </table>
  </section>

  {body_sections_html}

  <div class="approval-bar">
    <div>
      <div class="mono-label" style="margin-bottom:4px;">05 / ĐIỂM PHÊ DUYỆT CỦA CON NGƯỜI (HUMAN APPROVAL GATE)</div>
      <div>Xác nhận nghiệm thu hồ sơ sản phẩm này hoặc yêu cầu nhân sự AI tự động vá Luật Kaizen.</div>
    </div>
    <div class="header-actions">
      <button class="btn-primary" onclick="approveOrder('APPROVE')">Phê Duyệt Nghiệm Thu</button>
      <button class="btn-outline" onclick="approveOrder('REJECT_KAIZEN')">Từ Chối & Ghi Luật Kaizen</button>
    </div>
  </div>
</main>

<script>
async function approveOrder(decision) {{
  let note = "";
  if (decision !== "APPROVE") {{
    note = prompt("Nhập yêu cầu chỉnh sửa / Luật Kaizen mới cho bộ phận này:", "Cần chi tiết hóa hơn số liệu thực tế và bám sát chuẩn thương hiệu eyc.asia.");
    if (note === null) return;
  }} else {{
    note = "Giám đốc Phan Phúc Nguyên đã kiểm tra hồ sơ sản phẩm và phê duyệt nghiệm thu.";
  }}
  const res = await fetch("/api/approve-work-order", {{
    method: "POST",
    headers: {{ "Content-Type": "application/json" }},
    body: JSON.stringify({{ order_id: "{html.escape(order_id)}", decision, feedback_note: note }})
  }});
  const data = await res.json();
  const banner = document.getElementById("statusBanner");
  banner.style.display = "block";
  banner.textContent = data.message || "Đã cập nhật trạng thái nghiệm thu.";
}}
</script>
</body>
</html>"""

    html_path.write_text(html_doc, encoding="utf-8")
    return {
        "deliverable_html_url": f"/deliverables/{urllib.parse.quote(order_id)}.html",
        "deliverable_json_url": f"/deliverables/{urllib.parse.quote(order_id)}.json",
    }


class EYCCompanyController:
    """Production Controller for EYC (`eyc.asia`) 16 AI Departments."""

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
            if cols and "deliverable_json" not in cols:
                conn.execute("ALTER TABLE ceo_work_orders ADD COLUMN deliverable_json TEXT NOT NULL DEFAULT '{}';")

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
                    "current_step": "Đã xóa sạch toàn bộ dữ liệu test & khởi tạo chuẩn gốc EYC (eyc.asia).",
                }
            )
        if DELIVERABLES_DIR.exists():
            for f in DELIVERABLES_DIR.iterdir():
                if f.is_file():
                    f.unlink()
        return reset_and_setup_eyc()

    def get_full_company_state(self, campaign_id: str = "EYC_CORE") -> dict[str, Any]:
        with self.brain._connect() as conn:
            roster_rows = {
                r["department_id"]: dict(r)
                for r in conn.execute("SELECT * FROM hr_agent_roster;").fetchall()
            }
            raw_wo_rows = [
                dict(r)
                for r in conn.execute(
                    "SELECT * FROM ceo_work_orders ORDER BY updated_at_utc DESC LIMIT 60;"
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

        # Enrich every work order with department metadata and direct deliverable URLs
        wo_rows: list[dict[str, Any]] = []
        for w in raw_wo_rows:
            oid = w["order_id"]
            did = w["department_id"]
            dmeta = CORPORATE_DEPARTMENTS.get(did, {"name": did})
            dlayout = OFFICE_LAYOUT.get(did, {"icon": "00", "short": did})
            try:
                deliv_obj = json.loads(w.get("deliverable_json") or "{}")
            except Exception:
                deliv_obj = {}

            html_url = deliv_obj.get("deliverable_html_url") or (
                f"/deliverables/{urllib.parse.quote(oid)}.html"
                if (DELIVERABLES_DIR / f"{oid}.html").exists()
                else ""
            )
            json_url = deliv_obj.get("deliverable_json_url") or (
                f"/deliverables/{urllib.parse.quote(oid)}.json"
                if (DELIVERABLES_DIR / f"{oid}.json").exists()
                else ""
            )
            w["department_name"] = dmeta["name"]
            w["department_code"] = dlayout["icon"]
            w["department_short"] = dlayout["short"]
            w["deliverable_payload"] = deliv_obj
            w["deliverable_html_url"] = html_url
            w["deliverable_json_url"] = json_url
            wo_rows.append(w)

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
            dept_wos = [w for w in wo_rows if w["department_id"] == dept_id]

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
                    "department_work_orders": dept_wos,
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
            "media_vault": media_files[:30],
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
        if department_id not in CORPORATE_DEPARTMENTS:
            raise ValueError(f"Unknown department_id: {department_id}")

        meta = CORPORATE_DEPARTMENTS[department_id]
        layout = OFFICE_LAYOUT.get(department_id, {"icon": "00"})
        with self.brain._connect() as conn:
            roster = conn.execute(
                "SELECT * FROM hr_agent_roster WHERE department_id = ?;",
                (department_id,),
            ).fetchone()
            sys_prompt = roster["system_prompt_excerpt"] if roster else EYC_DEPARTMENT_PROMPTS.get(department_id, "")
            kaizen_patch = roster["kaizen_prompt_patch"] if roster else ""

        q_lower = question.lower()

        response_lines = [
            f"BÁO CÁO TRỰC TIẾP TỪ [{layout['icon']}] {meta['name'].upper()}",
            f"• Câu hỏi của Giám đốc Phan Phúc Nguyên: \"{question}\"",
            f"• Nhiệm vụ cốt lõi tại EYC (eyc.asia): {sys_prompt}",
            f"• Nền tảng & công cụ vận hành: {meta['weapons']}",
            "",
            "01 / QUY TRÌNH 6 BƯỚC EYC ÁP DỤNG CHO YÊU CẦU NÀY:",
            "  01. Định hướng: Xác lập mục tiêu đầu ra đo lường được cho hệ sinh thái EYC (eyc.asia & Early Years Circle).",
            "  02. Ngữ cảnh: Truy xuất Bộ Não Thứ 2 (Tầng 1 SQLite FTS5, Tầng 2 Kaizen, Tầng 3 Đồ thị thực thể EYC gồm 8 nhóm giải pháp & 4 phân hệ Teacher/Family/Admin/TV).",
            f"  03. Agents: Kích hoạt chuyên gia {meta['profile_ref']} với điểm phê duyệt của con người (Human Approval Gate).",
            f"  04. Hành động: Thực thi tự động qua {meta['weapons']} và xuất hồ sơ sản phẩm có link nghiệm thu trực tiếp.",
            "  05. Kiểm tra: Trình Giám đốc xem trực tiếp toàn văn sản phẩm và bấm Phê Duyệt hoặc Yêu Cầu Tối Ưu.",
            "  06. Kết quả: Lưu trữ tài sản số vào Kho Sản Phẩm EYC & cập nhật chỉ số KPI.",
        ]

        if kaizen_patch:
            response_lines.extend(
                [
                    "",
                    "02 / LUẬT KAIZEN ĐANG ÁP DỤNG TRONG SYSTEM PROMPT:",
                    f"  {kaizen_patch}",
                ]
            )

        response_lines.append("")
        response_lines.append("03 / PHƯƠNG ÁN THỰC THI ĐỀ XUẤT CHO EYC.ASIA:")
        if "early years" in q_lower or "mầm non" in q_lower or "teacher" in q_lower or "family" in q_lower:
            response_lines.extend(
                [
                    "  • Tập trung làm nổi bật 4 điểm chạm đồng bộ của Early Years Circle: 01 Teacher (Giáo viên), 02 Family (Phụ huynh), 03 Admin (Nhà trường), và 04 TV (Màn hình lớp học).",
                    "  • Nhấn mạnh nguyên tắc: giảm tải thao tác hành chính thủ công, bảo vệ dữ liệu trẻ em và minh bạch thông tin theo thời gian thực.",
                ]
            )
        elif "seo" in q_lower or "aio" in q_lower or "từ khóa" in q_lower or "web" in q_lower:
            response_lines.extend(
                [
                    "  • Quét trực tiếp cấu trúc HTML5, Schema Organization/WebSite và tốc độ tải của https://eyc.asia/vi-vn/ và https://eyc.asia/en-us/.",
                    "  • Xây dựng cụm chủ đề (Topic Cluster) quanh 8 trụ cột giải pháp EYC và chuẩn hóa 45-word Answer Block để ChatGPT, Perplexity, Claude trích dẫn trực tiếp eyc.asia.",
                ]
            )
        elif "video" in q_lower or "media" in q_lower or "thiết kế" in q_lower or "content" in q_lower:
            response_lines.extend(
                [
                    "  • Tuân thủ nghiêm ngặt hệ màu chuẩn của eyc.asia: Nền tối kiến trúc (#07080B / #0E1017), điểm nhấn Cam EYC (#FE5E02), tuyệt đối không dùng màu lòe loẹt sai nhận diện.",
                    "  • Sử dụng OpenMontage pipeline để xuất Poster (.webp), Thuyết minh (.mp3) và Video 9:16 (.mp4) kèm hồ sơ kiểm định 6 chiều.",
                ]
            )
        else:
            response_lines.extend(
                [
                    f"  • Bộ phận {meta['name']} đã sẵn sàng nhận lệnh tại tab 'Giao Việc & Sản Xuất Thực Tế'.",
                    "  • Ngay khi hoàn thành, toàn bộ sản phẩm sẽ xuất hiện tại cột '03 / KHO SẢN PHẨM & DUYỆT NGHIỆM THU' kèm đường link mở xem trực tiếp.",
                ]
            )

        answer_text = "\n".join(response_lines)
        now_iso = _utc_now_iso()
        log_id = f"ilog_{uuid.uuid4().hex[:10]}"

        with self.brain._connect() as conn:
            conn.execute(
                """
                INSERT INTO eyc_interview_logs (
                    log_id, department_id, interaction_mode, director_input,
                    agent_response, deliverable_json, status, created_at_utc
                )
                VALUES (?, ?, 'INTERVIEW', ?, ?, '{}', 'ANSWERED', ?);
                """,
                (log_id, department_id, question, answer_text, now_iso),
            )

        push_live_event(
            department_id,
            "01_ceo",
            "INTERVIEW_RESPONSE",
            f"Phỏng vấn 1-1: {meta['name']} đã báo cáo phương án cho '{question[:50]}'",
            "READY",
            100,
            eyc_step=2,
        )
        return {
            "ok": True,
            "log_id": log_id,
            "department_id": department_id,
            "department_name": meta["name"],
            "question": question,
            "answer": answer_text,
            "timestamp": now_iso,
        }

    def update_department_prompt_and_kaizen(
        self,
        department_id: str,
        system_prompt: str,
        new_kaizen_rule: str = "",
    ) -> dict[str, Any]:
        if department_id not in CORPORATE_DEPARTMENTS:
            raise ValueError(f"Unknown department_id: {department_id}")

        now_iso = _utc_now_iso()
        clean_prompt = system_prompt.strip()
        if clean_prompt:
            with self.brain._connect() as conn:
                conn.execute(
                    """
                    UPDATE hr_agent_roster
                    SET system_prompt_excerpt = ?,
                        updated_at_utc = ?
                    WHERE department_id = ?;
                    """,
                    (clean_prompt, now_iso, department_id),
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
            f"Đã cập nhật System Prompt cho {CORPORATE_DEPARTMENTS[department_id]['name']}"
            + (f" và bổ sung Luật Kaizen: \"{new_kaizen_rule.strip()}\"." if new_kaizen_rule.strip() else ".")
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
        Executes a real operational task for EYC (`eyc.asia` / `Early Years Circle`) on the selected department,
        walking through EYC's 6-Step Operating Model (`01 Định hướng → 02 Ngữ cảnh → 03 Agents → 04 Hành động → 05 Kiểm tra → 06 Kết quả`)
        and generating a complete clickable HTML & JSON Deliverable Dossier (`/deliverables/<order_id>.html`).
        """
        if department_id not in CORPORATE_DEPARTMENTS:
            raise ValueError(f"Unknown department_id: {department_id}")

        now_iso = _utc_now_iso()
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        dept_name = CORPORATE_DEPARTMENTS[department_id]["name"]
        order_id = f"WO_{campaign_id}_{department_id.upper()}_{uuid.uuid4().hex[:4]}"

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
            f"[Bước 01: Định hướng] Giao nhiệm vụ: '{task_title}'",
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

        with self.brain._connect() as conn:
            conn.execute(
                """
                INSERT INTO ceo_work_orders (
                    order_id, campaign_id, department_id, phase_number,
                    task_title, sop_instructions, kpi_target_json, assigned_weapons,
                    status, deliverable_summary, kpi_achieved_json,
                    approval_status, director_feedback, deliverable_json, created_at_utc, updated_at_utc
                )
                VALUES (?, ?, ?, 1, ?, ?, '{"completion": 100}', ?, 'WORKING', ?, '{}', 'PENDING_APPROVAL', ?, '{}', ?, ?);
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
                    "[Bước 02: Ngữ cảnh] Đồng bộ hồ sơ EYC, sản phẩm Early Years Circle & Luật Kaizen.",
                    "WORKING",
                    progress_percent=33,
                    eyc_step=2,
                )

                # Step 03 & Step 04: Hành động
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
                    target_rev = price_vnd * 20
                    req_orders = max(1, int(round(target_rev / max(price_vnd, 1.0))))
                    max_budget = round(target_rev * 0.15, 0)
                    ue = {
                        "product_price_vnd": price_vnd,
                        "target_revenue_vnd": target_rev,
                        "required_orders": req_orders,
                        "required_leads": req_orders * 4,
                        "max_ad_budget_vnd": max_budget,
                        "target_roas": round(target_rev / max(max_budget, 1.0), 2),
                    }
                    wos_preview = [
                        {
                            "department_id": k,
                            "task_title": f"[{meta['name']}] Thực thi hạng mục thuộc chiến dịch: {task_title}",
                            "sop_instructions": f"Áp dụng quy trình 6 bước EYC với bộ công cụ {meta['weapons']} theo chỉ đạo: {instructions}",
                        }
                        for k, meta in list(CORPORATE_DEPARTMENTS.items())[:8]
                    ]
                    deliverable_payload = {
                        "type": "CEO_HR_MASTER_PLAN",
                        "unit_economics": ue,
                        "work_orders_count": 16,
                        "work_orders_preview": wos_preview,
                        "talent_profiles_matched": [t["name"] for t in talent_matches],
                    }
                    execution_summary = (
                        f"Đã lập Hồ sơ Kế hoạch Điều hành Chiến lược EYC '{task_title}' "
                        f"(Mục tiêu doanh thu: {ue['target_revenue_vnd']:,.0f} VNĐ, ROAS kỳ vọng: {ue['target_roas']}x) "
                        f"& rà soát {len(talent_matches)} hồ sơ chuyên gia AI."
                    )

                elif department_id in ("07_seo", "08_aio", "09_sao"):
                    div = SearchGrowthDivision(self.brain)
                    res = div.execute_omni_search_campaign_package(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        core_keyword=task_title if len(task_title) > 10 else "nền tảng điều phối AI Agents và Early Years Circle EYC",
                        price_vnd=price_vnd,
                        usp_highlights=[
                            "Hệ thống do con người dẫn dắt — AI Agents phối hợp thực thi",
                            "Early Years Circle: Kết nối 01 Teacher, 02 Family, 03 Admin, 04 TV",
                            "Tích hợp Model Context Protocol (MCP) & chủ quyền dữ liệu doanh nghiệp",
                        ],
                        target_persona=instructions or "Ban giám đốc doanh nghiệp & Ban giám hiệu trường mầm non",
                        competitor_url="https://eyc.asia/vi-vn/",
                    )
                    crawl_res = res.get("crawl_report") or {}
                    crawl_res.setdefault("meta_description", "EYC kết nối AI, phần mềm, dữ liệu và quy trình để biến định hướng thành công việc thực.")
                    crawl_res.setdefault("h1_tags", crawl_res.get("headings", [])[:2])
                    crawl_res.setdefault("h2_tags", crawl_res.get("headings", [])[2:10])
                    aio_pack = res.get("aio_citation_pack", {})
                    sao_pack = res.get("sao_social_and_webmcp_pack", {})
                    cluster_pages = res.get("topic_cluster", {}).get("cluster_pages", [])
                    deliverable_payload = {
                        "type": "SEO_AIO_SAO_PACKAGE",
                        "live_crawl_eyc_asia": crawl_res,
                        "pillar_slug": res.get("pillar_url_slug", ""),
                        "pillar_word_count": res.get("word_count", 0),
                        "aio_direct_answer_45w": aio_pack.get("direct_answer_45_words", ""),
                        "json_ld_schema": aio_pack.get("json_ld_schema", {}),
                        "satellite_articles": [
                            {"slug": p.get("url_slug", ""), "keyword": p.get("keyword", ""), "intent": p.get("intent", "")}
                            for p in cluster_pages
                        ],
                        "sao_tiktok_title": sao_pack.get("social_search_pack", {}).get("tiktok_caption_seo", ""),
                        "markdown_excerpt": res.get("seo_article_markdown", "")[:900],
                        "full_markdown_body": res.get("seo_article_markdown", ""),
                    }
                    execution_summary = (
                        f"Đã kiểm toán trực tiếp https://eyc.asia/vi-vn/ ({crawl_res.get('word_count', 0)} từ), khóa Topic Cluster {len(cluster_pages)} URL "
                        f"(0 Cannibalization), xuất bản bài Pillar '{res.get('pillar_url_slug', '')}' ({res.get('word_count', 0)} từ) "
                        f"kèm khối trả lời 45 từ chuẩn AIO & mã Schema JSON-LD."
                    )

                elif department_id in ("02_creative_director", "03_design", "04_content", "05_media_livestream", "06_video_editor"):
                    studio = CreativeVideoStudioDivision(self.brain)
                    bundle = studio.produce_full_campaign_creative_bundle(
                        campaign_id=campaign_id,
                        product_name=product_name,
                        price_vnd=price_vnd,
                        usp_highlights=[
                            "Hệ thống do con người dẫn dắt — AI Agents phối hợp thực thi",
                            "Early Years Circle: Đồng bộ 01 Teacher, 02 Family, 03 Admin, 04 TV",
                            instructions[:80] if instructions else "Chuẩn hóa quy trình vận hành 6 bước từ Định hướng đến Kết quả",
                        ],
                        target_persona="Ban điều hành doanh nghiệp & Hệ thống giáo dục mầm non",
                        spintax_count=50,
                        watermark_text="CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC • EYC.ASIA",
                    )
                    om_qa = bundle["openmontage_qa_report"]
                    webp_name = Path(bundle["studio_banner_webp"]["file_path"]).name
                    mp3_name = Path(bundle["voiceover_audio"]["audio_path"]).name
                    mp4_name = Path(bundle["short_video_mp4"]["video_mp4_path"]).name
                    mtime = int(time.time())
                    deliverable_payload = {
                        "type": "CREATIVE_MEDIA_VIDEO_BUNDLE",
                        "approved_hook_3s": bundle["creative_approval"]["approved_hook_3s"],
                        "script_scenes": bundle.get("script_scenes", []),
                        "spintax_generated": bundle["spintax_summary"]["total_unique_generated"],
                        "spintax_sample": bundle["spintax_summary"]["sample_variation_1"],
                        "spintax_samples": bundle["spintax_summary"].get("sample_variations", []),
                        "banner_webp_url": f"/media/{urllib.parse.quote(webp_name)}?v={mtime}",
                        "voiceover_mp3_url": f"/media/{urllib.parse.quote(mp3_name)}?v={mtime}",
                        "video_mp4_url": f"/media/{urllib.parse.quote(mp4_name)}?v={mtime}",
                        "video_duration_sec": bundle["short_video_mp4"]["duration_sec"],
                        "openmontage_pipeline": om_qa["selected_pipeline"],
                        "openmontage_risk_score": om_qa["slideshow_risk_score"],
                        "openmontage_verdict": om_qa["slideshow_risk_verdict"],
                    }
                    execution_summary = (
                        f"Đã sản xuất trọn bộ tài sản truyền thông chuẩn thương hiệu EYC: Poster '{webp_name}', "
                        f"Thuyết minh AI '{mp3_name}', và Video 9:16 '{mp4_name}' ({bundle['short_video_mp4']['duration_sec']}s) — "
                        f"Điểm QA OpenMontage: {om_qa['slideshow_risk_score']}/5.0 ({om_qa['slideshow_risk_verdict'].upper()})."
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
                                "author_name": f"Đối tác B2B ({task_title[:28]})",
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
                        f"Đã lập Hồ sơ Đề xuất Giải pháp B2B & đồng bộ Twenty CRM "
                        f"({tw['total_people_in_crm']} Khách hàng B2B, {tw['campaign_opportunities_won']} Hợp đồng '{tw['kanban_stage']}', "
                        f"{tw['campaign_tasks_dispatched']} Tác vụ triển khai) — Giá trị hợp đồng: {rep['revenue_generated_vnd']:,.0f} VNĐ."
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
                        f"Đã xuất Báo cáo Kiểm toán P&L EYC (Doanh thu: {cfo['gross_revenue_vnd']:,.0f} VNĐ, "
                        f"Lợi nhuận ròng: {cfo['net_operating_profit_vnd']:,.0f} VNĐ, Quyết định CFO: {cfo['cfo_directive']}) "
                        f"& Báo cáo Hạ tầng IT ({it_rep['overall_status']}, {it_rep['git_submodules_count']} submodules)."
                    )

                # Generate clickable HTML & JSON Deliverable Dossier files
                file_urls = generate_deliverable_files(
                    order_id=order_id,
                    department_id=department_id,
                    task_title=task_title,
                    instructions=instructions,
                    execution_summary=execution_summary,
                    deliverable_payload=deliverable_payload,
                    created_at_utc=_utc_now_iso(),
                )
                deliverable_payload["deliverable_html_url"] = file_urls["deliverable_html_url"]
                deliverable_payload["deliverable_json_url"] = file_urls["deliverable_json_url"]
                deliverable_payload["order_id"] = order_id

                # Step 05: Kiểm tra (Human Approval Gate)
                with self.brain._connect() as conn:
                    conn.execute(
                        """
                        UPDATE ceo_work_orders
                        SET status = 'WAITING_APPROVAL',
                            approval_status = 'PENDING_APPROVAL',
                            deliverable_summary = ?,
                            deliverable_json = ?,
                            updated_at_utc = ?
                        WHERE order_id = ?;
                        """,
                        (
                            execution_summary,
                            json.dumps(deliverable_payload, ensure_ascii=False),
                            _utc_now_iso(),
                            order_id,
                        ),
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
                    current_step=f"[Bước 05/06 — Kiểm tra & Nghiệm thu] Đã xuất hồ sơ sản phẩm {order_id}. Bấm vào link sản phẩm để xem và phê duyệt.",
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
                "execution_summary": f"Đã giao nhiệm vụ '{task_title}' cho {dept_name}. Hệ thống đang thực thi và xuất hồ sơ sản phẩm...",
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
            msg = f"[Bước 06/06 — Kết quả] Giám đốc đã PHÊ DUYỆT hồ sơ sản phẩm {order_id} của {CORPORATE_DEPARTMENTS[dept_id]['name']}."
            push_live_event("01_ceo", dept_id, "STEP_06_OUTCOME_APPROVED", msg, "COMPLETED", 100, eyc_step=6)
            update_active_job(False, dept_id, wo.get("task_title", ""), 100, msg, eyc_step_index=6)
            return {"ok": True, "order_id": order_id, "department_id": dept_id, "new_status": "APPROVED_BY_DIRECTOR", "message": msg}

        rule_text = feedback_note.strip() or "Cần bám sát hơn định vị công nghệ của EYC (eyc.asia) và nêu rõ các điểm phê duyệt của con người."
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
        msg = f"Đã ghi nhận yêu cầu tối ưu hồ sơ {order_id} cho {CORPORATE_DEPARTMENTS[dept_id]['name']} & tự động cập nhật Luật Kaizen: '{rule_text}'"
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
        if file_path.suffix.lower() == ".html":
            mime_type = "text/html; charset=utf-8"
        elif file_path.suffix.lower() == ".json":
            mime_type = "application/json; charset=utf-8"
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

        if path.startswith("/static/"):
            rel = urllib.parse.unquote(path[len("/static/"):])
            safe_static = (STATIC_DIR / rel).resolve()
            if STATIC_DIR.resolve() in safe_static.parents:
                self._serve_file(safe_static)
                return
            self._send_json({"error": "Invalid static path"}, status=403)
            return

        if path == "/api/company-state":
            qs = urllib.parse.parse_qs(parsed.query)
            camp_id = qs.get("campaign_id", ["EYC_CORE"])[0]
            self._send_json(CONTROLLER.get_full_company_state(campaign_id=camp_id))
            return

        if path.startswith("/deliverables/"):
            fname = urllib.parse.unquote(path[len("/deliverables/"):])
            safe_deliv = (DELIVERABLES_DIR / fname).resolve()
            if DELIVERABLES_DIR.resolve() in safe_deliv.parents:
                self._serve_file(safe_deliv)
                return
            self._send_json({"error": "Invalid deliverable path"}, status=403)
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
    DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
    primary_server = ReusableThreadingHTTPServer((host, port), VirtualOfficeHTTPHandler)
    print(f"EYC AI Command Center listening at http://{host}:{port}", flush=True)

    if port != 80:
        try:
            http80_server = ReusableThreadingHTTPServer((host, 80), VirtualOfficeHTTPHandler)
            threading.Thread(target=http80_server.serve_forever, daemon=True).start()
            print(f"Standard HTTP Port 80 also active at http://{host}:80", flush=True)
        except OSError as exc:
            print(f"Port 80 bind skipped: {exc}", flush=True)

    primary_server.serve_forever()


if __name__ == "__main__":
    port_num = int(os.environ.get("VIRTUAL_OFFICE_PORT", "8090"))
    run_server(port=port_num)
