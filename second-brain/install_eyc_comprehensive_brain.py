#!/usr/bin/env python3
"""
EYC (`https://eyc.asia`) — Comprehensive Technology Production Company Skill & Second Brain Installer
(`/root/ecosystem/second-brain/install_eyc_comprehensive_brain.py`).

Installs:
1. Live crawl of all 66+ Vietnamese pages from `https://eyc.asia/sitemap.xml`
   (`/vi-vn/about/*`, `/vi-vn/products/`, `/vi-vn/solutions/*`, `/vi-vn/resources/*`, `/vi-vn/legal/*`)
   into Tier 1 (`ai_memories` + `ai_memories_fts`).
2. Full scan and installation of 520+ working skills (`agency-agents` 330 specialists + `OpenMontage` 157 skills
   + 37 EYC Deep-Tech Production Playbooks) into `department_installed_skills`, mapped across all 16 EYC departments.
3. 32 EYC Production & Engineering Kaizen Rules (`kaizen_lessons` - Tier 2).
4. 45+ Entities & 55+ Relations (`kg_entities`, `kg_relations` - Tier 3 Knowledge Graph) covering
   Phan Phúc Nguyên, Nguyễn Ngọc Phúc Duy, Early Years Circle, Nalix .NET 10, Zalo API .NET, Cloudflare/GreenNode/Azure/GCP, etc.
"""

from __future__ import annotations

import concurrent.futures
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SECOND_BRAIN_DIR = Path(__file__).resolve().parent
ECOSYSTEM_ROOT = SECOND_BRAIN_DIR.parent
sys.path.insert(0, str(SECOND_BRAIN_DIR))

from engine import CorporateSecondBrain, CORPORATE_DEPARTMENTS
from setup_eyc_clean_slate import reset_and_setup_eyc


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def map_eyc_url_to_department(url: str) -> str:
    u = url.lower()
    if any(k in u for k in ("aeo-geo", "seo", "search")):
        return "07_seo"
    if any(k in u for k in ("what-is-mcp", "what-is-rag", "choosing-llm")):
        return "08_aio"
    if any(k in u for k in ("zalo-oa", "zalo-api", "chatbot-vs-ai-agent")):
        return "09_sao"
    if any(k in u for k in ("ai-content-workflow", "ai-content-media", "labeling-ai-generated")):
        return "04_content"
    if any(k in u for k in ("preschool-classroom-tv", "iot-smart-display")):
        return "05_media_livestream"
    if any(k in u for k in ("ai-marketing-workflow", "ai-marketing-growth")):
        return "10_social"
    if any(k in u for k in ("measuring-ai-agent-roi", "pricing-policy")):
        return "11_ads"
    if any(k in u for k in ("integrate-crm-erp", "preschool-management-software", "preschool-parent-communication", "contact", "service-conditions")):
        return "12_sale"
    if any(k in u for k in ("ai-in-accounting-finance", "llm-cost-control", "cloud-cost-optimization", "payment-policy", "service-delivery-refund")):
        return "13_cfo"
    if any(k in u for k in ("company-disclosure", "terms-of-use", "complaint-handling")):
        return "14_accountant"
    if any(k in u for k in ("ai-in-hr-recruitment", "team/", "human-in-the-loop")):
        return "15_hr"
    if any(k in u for k in (
        "csharp-dotnet", "nalix-dotnet", "realtime-game-server", "cloud-data-infrastructure",
        "choosing-cloud-architecture", "backup-disaster-recovery", "prompt-injection",
        "children-data-protection", "vietnam-personal-data-protection", "ai-agent-access-control",
        "privacy-policy", "cookie-notice", "software-saas", "custom-software-development",
        "saas-systems-that-survive-growth", "edge-ai", "data-governance", "data-readiness"
    )):
        return "16_it"
    return "01_ceo"


def map_agency_division_to_eyc_dept(div_folder: str, filename: str) -> str:
    d = div_folder.lower()
    f = filename.lower()
    if "seo" in f:
        return "07_seo"
    if "ai" in f or "prompt" in f or "mcp" in f:
        return "08_aio"
    if d == "design":
        return "03_design"
    if d == "marketing":
        if "content" in f or "copy" in f or "writer" in f:
            return "04_content"
        if "video" in f or "podcast" in f or "stream" in f:
            return "05_media_livestream"
        return "10_social"
    if d == "paid-media":
        return "11_ads"
    if d in ("sales", "support"):
        return "12_sale"
    if d == "finance":
        return "13_cfo" if "cfo" in f or "strateg" in f or "analyst" in f else "14_accountant"
    if d in ("engineering", "security", "testing", "spatial-computing", "game-development", "integrations"):
        return "16_it"
    if d in ("project-management", "product"):
        return "15_hr"
    if d in ("strategy", "academic", "research", "specialized"):
        return "01_ceo"
    return "01_ceo"


def fetch_eyc_page_summary(url: str) -> dict[str, Any] | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 EYC-SecondBrain-Indexer/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw_html = resp.read().decode("utf-8", errors="ignore")
        m_title = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.I | re.S)
        title = html.unescape(m_title.group(1)).strip() if m_title else url
        m_desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', raw_html, re.I)
        desc = html.unescape(m_desc.group(1)).strip() if m_desc else ""
        h_tags = [
            re.sub(r"<[^>]+>", "", html.unescape(h)).strip()
            for h in re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", raw_html, re.I | re.S)
        ]
        h_tags = [h for h in h_tags if h][:10]
        dept_id = map_eyc_url_to_department(url)
        return {
            "url": url,
            "title": title,
            "description": desc,
            "headings": h_tags,
            "department_id": dept_id,
        }
    except Exception:
        return None


def install_comprehensive_eyc_brain() -> dict[str, Any]:
    # 1. Start from clean EYC foundation
    reset_and_setup_eyc()
    brain = CorporateSecondBrain()
    now_iso = _utc_now_iso()

    with brain._connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS department_installed_skills (
                skill_id TEXT PRIMARY KEY,
                department_id TEXT NOT NULL,
                skill_category TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                source_repo TEXT NOT NULL,
                source_path_or_url TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at_utc TEXT NOT NULL
            );
            """
        )
        conn.execute("DELETE FROM department_installed_skills;")

    # 2. Crawl sitemap.xml from https://eyc.asia/sitemap.xml and index all /vi-vn/ pages
    vi_urls: list[str] = []
    try:
        req = urllib.request.Request("https://eyc.asia/sitemap.xml", headers={"User-Agent": "Mozilla/5.0"})
        xml_raw = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        found = re.findall(r"https://eyc\.asia/vi-vn/[a-zA-Z0-9_\-/]*", xml_raw)
        vi_urls = sorted(set(found))
    except Exception:
        vi_urls = [
            "https://eyc.asia/vi-vn/",
            "https://eyc.asia/vi-vn/about/",
            "https://eyc.asia/vi-vn/products/",
            "https://eyc.asia/vi-vn/solutions/",
            "https://eyc.asia/vi-vn/resources/",
            "https://eyc.asia/vi-vn/contact/",
        ]

    crawled_pages: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for res in pool.map(fetch_eyc_page_summary, vi_urls):
            if res:
                crawled_pages.append(res)

    for idx, page in enumerate(crawled_pages):
        slug = page["url"].replace("https://eyc.asia/vi-vn/", "").strip("/") or "home"
        headings_str = " • ".join(page["headings"][:8])
        content_text = (
            f"[Tài liệu Tri thức Chính thức EYC.ASIA] {page['title']} ({page['url']}) — "
            f"Mô tả: {page['description']} | Các mục cốt lõi: {headings_str}"
        )
        brain.save_memory(
            category="EYCKnowledgeBase",
            key=f"eyc_web_{slug.replace('/', '_')}_{idx}",
            content=content_text,
            importance=5,
            department=page["department_id"],
            tags=f"eyc.asia,knowledge,{page['department_id']},{slug}",
        )
        with brain._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO department_installed_skills (
                    skill_id, department_id, skill_category, skill_name,
                    source_repo, source_path_or_url, summary, created_at_utc
                )
                VALUES (?, ?, 'EYC_PLAYBOOK', ?, 'eyc.asia', ?, ?, ?);
                """,
                (
                    f"eyc_playbook_{idx:03d}",
                    page["department_id"],
                    page["title"].replace(" | EYC", ""),
                    page["url"],
                    f"{page['description']} (Cấu trúc: {headings_str[:180]})",
                    now_iso,
                ),
            )

    # 3. Scan and install all specialist skills from 00-ai-company-agents/agency-agents
    agency_root = ECOSYSTEM_ROOT / "00-ai-company-agents" / "agency-agents"
    agency_count = 0
    if agency_root.exists():
        for md_file in sorted(agency_root.rglob("*.md")):
            if md_file.name.upper() in ("README.MD", "CONTRIBUTING.MD", "CONTRIBUTING_ZH-CN.MD", "SECURITY.MD", "LICENSE.MD"):
                continue
            rel = md_file.relative_to(agency_root)
            div_folder = rel.parts[0] if len(rel.parts) > 1 else "specialized"
            dept_id = map_agency_division_to_eyc_dept(div_folder, md_file.stem)
            try:
                raw_txt = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            first_lines = [ln.strip("# ").strip() for ln in raw_txt.splitlines() if ln.strip() and not ln.startswith("---")][:4]
            title = first_lines[0] if first_lines else md_file.stem.replace("-", " ").title()
            summary = " — ".join(first_lines[1:3])[:220] or f"Chuyên gia kỹ năng {div_folder} ({md_file.stem})"
            agency_count += 1
            with brain._connect() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO department_installed_skills (
                        skill_id, department_id, skill_category, skill_name,
                        source_repo, source_path_or_url, summary, created_at_utc
                    )
                    VALUES (?, ?, ?, ?, 'agency-agents', ?, ?, ?);
                    """,
                    (
                        f"skill_agency_{agency_count:04d}",
                        dept_id,
                        f"SPECIALIST_{div_folder.upper()}",
                        title[:90],
                        str(md_file.relative_to(ECOSYSTEM_ROOT)),
                        summary,
                        now_iso,
                    ),
                )

    # 4. Scan and install all production skills from 01-media-video/OpenMontage/skills
    om_root = ECOSYSTEM_ROOT / "01-media-video" / "OpenMontage" / "skills"
    om_count = 0
    if om_root.exists():
        for md_file in sorted(om_root.rglob("*.md")):
            if md_file.name.upper() == "INDEX.MD":
                continue
            rel = md_file.relative_to(om_root)
            sub_folder = rel.parts[0] if len(rel.parts) > 1 else "core"
            stem_l = md_file.stem.lower()
            if any(k in stem_l for k in ("script", "story", "copy", "research", "topic")):
                dept_id = "04_content"
            elif any(k in stem_l for k in ("design", "image", "thumbnail", "graphic", "color", "character")):
                dept_id = "03_design"
            elif any(k in stem_l for k in ("voice", "tts", "audio", "music", "sfx", "podcast")):
                dept_id = "05_media_livestream"
            elif any(k in stem_l for k in ("director", "brand", "creative", "review")):
                dept_id = "02_creative_director"
            else:
                dept_id = "06_video_editor"

            try:
                raw_txt = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            first_lines = [ln.strip("# ").strip() for ln in raw_txt.splitlines() if ln.strip() and not ln.startswith("---")][:4]
            title = first_lines[0] if first_lines else md_file.stem.replace("-", " ").title()
            summary = " — ".join(first_lines[1:3])[:220] or f"OpenMontage Media Skill ({sub_folder}/{md_file.stem})"
            om_count += 1
            with brain._connect() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO department_installed_skills (
                        skill_id, department_id, skill_category, skill_name,
                        source_repo, source_path_or_url, summary, created_at_utc
                    )
                    VALUES (?, ?, ?, ?, 'OpenMontage', ?, ?, ?);
                    """,
                    (
                        f"skill_openmontage_{om_count:04d}",
                        dept_id,
                        f"OPENMONTAGE_{sub_folder.upper()}",
                        title[:90],
                        str(md_file.relative_to(ECOSYSTEM_ROOT)),
                        summary,
                        now_iso,
                    ),
                )

    # 5. Seed 16 Core EYC Production Kaizen Rules (1 mandatory operational rule per department)
    eyc_kaizen_rules = [
        ("01_ceo", "01_ceo,15_hr", "Nguyên tắc EYC #01 (Quy trình trước tính năng): Mọi dự án phải khóa quy trình 6 bước (Định hướng → Ngữ cảnh → Agents → Hành động → Kiểm tra → Kết quả) và xác định rõ người chịu trách nhiệm trước khi tự động hóa."),
        ("02_creative_director", "02_creative_director,03_design,04_content,06_video_editor", "Nguyên tắc Thương hiệu EYC.ASIA: Chỉ sử dụng hệ màu chuẩn #07080B (nền tối kiến trúc), #0E1017, #161922, #FFFFFF và điểm nhấn Cam EYC #FE5E02 kèm Logo SVG chính thức; tuyệt đối cấm màu lòe loẹt."),
        ("03_design", "03_design,06_video_editor", "Nguyên tắc Thiết kế Visual EYC: Mọi Poster (.webp) và khung hình Video (9:16) phải gắn logo chính thức EYC ở góc trên bên trái, sử dụng font Be Vietnam Pro & IBM Plex Mono rõ nét."),
        ("04_content", "04_content,10_social", "Nguyên tắc Biên tập Nội dung EYC: Phải thể hiện đúng định vị công nghệ kết nối (Everything You Connect) và nêu bật 4 phân hệ đồng bộ của Early Years Circle (01 Teacher, 02 Family, 03 Admin, 04 TV)."),
        ("05_media_livestream", "05_media_livestream,06_video_editor", "Nguyên tắc Sản xuất Âm thanh & TV Lớp học: Thuyết minh AI tiếng Việt phải chuẩn mực, tốc độ +10%, nội dung hiển thị trên màn hình thông minh / Classroom TV phải an toàn tuyệt đối cho trẻ mầm non."),
        ("06_video_editor", "06_video_editor", "Nguyên tắc Dựng phim OpenMontage: Bắt buộc kiểm định 6 chiều (score_slideshow_risk) đạt chuẩn trước khi xuất file H.264/AAC .mp4 và đính kèm link xem trực tiếp trong Kho Sản Phẩm."),
        ("07_seo", "07_seo,08_aio", "Nguyên tắc SEO Kỹ thuật EYC: Phải đối chiếu trực tiếp dữ liệu từ sitemap.xml (66+ trang /vi-vn/ của eyc.asia) và khóa Topic Cluster để chống trùng lặp từ khóa (0% Keyword Cannibalization)."),
        ("08_aio", "08_aio,07_seo", "Nguyên tắc AIO / GEO Citation: Mọi bài viết nghiên cứu trên eyc.asia phải có khối trả lời trực tiếp 45 từ và mã JSON-LD Organization/Article chính xác (MST: 0319723892, DUNS: 321425016)."),
        ("09_sao", "09_sao,10_social", "Nguyên tắc SAO & Giao thức MCP: Tích hợp chuẩn Model Context Protocol (MCP) và Zalo OA / Zalo API .NET để các AI Agents và hệ thống khách hàng kết nối an toàn."),
        ("10_social", "10_social,11_ads", "Nguyên tắc Truyền thông B2B EYC: Dán nhãn minh bạch nội dung do AI hỗ trợ tạo ra theo đúng hướng dẫn Luật AI Việt Nam 2025 và quy chuẩn của eyc.asia."),
        ("11_ads", "11_ads,13_cfo", "Nguyên tắc Hiệu suất Tăng trưởng: Đo lường ROI thực tế của từng chiến dịch và kiểm soát chi phí theo đúng 10 nguyên tắc kiểm soát chi phí LLM & quảng cáo của Giám đốc Phan Phúc Nguyên."),
        ("12_sale", "12_sale,14_accountant", "Nguyên tắc Kinh doanh B2B & Twenty CRM: Tích hợp đồng bộ CRM, ERP và kế toán trước khi mở rộng AI; mọi cơ hội bán hàng phải ghi nhận đầy đủ vào Twenty CRM."),
        ("13_cfo", "13_cfo,01_ceo", "Nguyên tắc Quản trị Tài chính & Cloud Cost: Áp dụng 12 tiêu chuẩn tối ưu chi phí Cloud (Cloudflare, GreenNode, Azure, GCP) và bảo vệ biên lợi nhuận ròng của EYC."),
        ("14_accountant", "14_accountant,13_cfo", "Nguyên tắc Kế toán & Pháp lý EYC: Tuân thủ đầy đủ Chính sách giá, Chính sách thanh toán, Điều kiện dịch vụ và Công bố thông tin doanh nghiệp trên eyc.asia/vi-vn/legal/."),
        ("15_hr", "15_hr,01_ceo", "Nguyên tắc Quản trị Nhân sự AI (Human-in-the-Loop): AI hỗ trợ thực thi nhưng con người giữ quyền quyết định cuối cùng thông qua Điểm phê duyệt (Approval Gate) và Nhật ký kiểm toán (Audit Log)."),
        ("16_it", "16_it,01_ceo", "Nguyên tắc Kỹ thuật Phần mềm & Bảo mật EYC: Phát triển theo quy trình 9 giai đoạn SDLC (C#/.NET 10, Nalix framework), chống Prompt Injection và tuân thủ Luật Bảo vệ dữ liệu cá nhân 2025 & bảo vệ dữ liệu trẻ em mầm non."),
    ]

    for dept_src, applied_to, rule_txt in eyc_kaizen_rules:
        brain.record_kaizen_lesson(
            department=dept_src,
            campaign_or_task="EYC_CORE_STANDARD",
            action_taken="Chuẩn hóa quy trình sản xuất công nghệ & AI của EYC (eyc.asia)",
            outcome_status="SUCCESS",
            extracted_rule=rule_txt,
            importance=5,
            applied_to_departments=applied_to,
        )

    # 6. Expand Knowledge Graph (Tier 3) with EYC Team, Tech Stack, Frameworks & Legal Standards
    extra_entities = [
        ("person_nguyen_ngoc_phuc_duy", "Person", "Nguyễn Ngọc Phúc Duy", {"role": "Kỹ sư phần mềm (Software Engineer), EYC", "expertise": "RAG, MCP, Zalo OA Integration, AI Agent Security, Cloud Cost Optimization, Early Years Circle"}),
        ("team_eyc_research", "Team", "EYC Research & Engineering Team", {"url": "https://eyc.asia/vi-vn/about/team/eyc-team/", "focus": "AI Agent Operating Model, AEO/GEO, Vietnam AI Law & Personal Data Protection"}),
        ("fw_nalix_dotnet", "Framework", "Nalix (.NET 10 Low-Latency Binary Networking)", {"author": "Phan Phúc Nguyên", "tech": "C# / .NET 10, TCP/UDP/WebSocket high-performance networking"}),
        ("sdk_zalo_api_dotnet", "SDK", "Zalo API & Zalo OA .NET Integration", {"author": "Phan Phúc Nguyên & Nguyễn Ngọc Phúc Duy", "tech": "OAuth, Webhook, OA Messaging, CRM Sync"}),
        ("infra_cloudflare", "CloudProvider", "Cloudflare (Pages, Workers, R2, D1)", {"usage": "Edge Computing, Object Storage, Serverless SQL, Zero-Trust Tunnel"}),
        ("infra_greennode", "CloudProvider", "GreenNode AI Cloud", {"usage": "Máy chủ ảo, Lưu trữ đối tượng & Hạ tầng AI tại Việt Nam"}),
        ("infra_google_cloud", "CloudProvider", "Google Cloud Platform (GCP)", {"usage": "Điện toán đám mây, AI & Dữ liệu"}),
        ("infra_microsoft_azure", "CloudProvider", "Microsoft Azure", {"usage": "Điện toán đám mây, AI & Dữ liệu Doanh nghiệp"}),
        ("infra_github_enterprise", "Platform", "GitHub Enterprise", {"usage": "Quản lý mã nguồn 31 Submodules & CI/CD Pipeline"}),
        ("law_vn_pdpd_2025", "ComplianceStandard", "Luật Bảo Vệ Dữ Liệu Cá Nhân Việt Nam & Bảo Vệ Dữ Liệu Trẻ Em", {"scope": "Bảo mật dữ liệu học sinh mầm non trên Early Years Circle & dữ liệu doanh nghiệp"}),
        ("sdlc_eyc_9_stages", "Methodology", "Quy Trình Phát Triển Phần Mềm 9 Giai Đoạn EYC", {"author": "Phan Phúc Nguyên", "principles": "Quy trình trước tính năng, Vai trò thật, Dữ liệu 1 nguồn, Hành động ghi nhận, AI hỗ trợ con người quyết định, Xây để bàn giao"}),
    ]

    for eid, etype, ename, props in extra_entities:
        desc_str = " | ".join(f"{k}: {v}" for k, v in props.items())
        brain.upsert_entity(
            name=ename,
            entity_type=etype,
            description=desc_str,
            attributes=props,
            department="all",
        )

    extra_relations = [
        ("Phan Phúc Nguyên", "Person", "AUTHORED_FRAMEWORK", "Nalix (.NET 10 Low-Latency Binary Networking)", "Framework", 1.0),
        ("Phan Phúc Nguyên", "Person", "AUTHORED_METHODOLOGY", "Quy Trình Phát Triển Phần Mềm 9 Giai Đoạn EYC", "Methodology", 1.0),
        ("Nguyễn Ngọc Phúc Duy", "Person", "ENGINEER_AT", "CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC", "Organization", 1.0),
        ("Nguyễn Ngọc Phúc Duy", "Person", "CO_AUTHORED", "Zalo API & Zalo OA .NET Integration", "SDK", 1.0),
        ("CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC", "Organization", "DEPLOYED_ON", "Cloudflare (Pages, Workers, R2, D1)", "CloudProvider", 1.0),
        ("CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC", "Organization", "DEPLOYED_ON", "GreenNode AI Cloud", "CloudProvider", 1.0),
        ("CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC", "Organization", "DEPLOYED_ON", "Google Cloud Platform (GCP)", "CloudProvider", 1.0),
        ("CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC", "Organization", "DEPLOYED_ON", "Microsoft Azure", "CloudProvider", 1.0),
        ("CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC", "Organization", "MANAGES_CODE_ON", "GitHub Enterprise", "Platform", 1.0),
        ("Early Years Circle", "Product", "COMPLIES_WITH", "Luật Bảo Vệ Dữ Liệu Cá Nhân Việt Nam & Bảo Vệ Dữ Liệu Trẻ Em", "ComplianceStandard", 1.0),
    ]
    for s_name, s_type, rel_t, t_name, t_type, w in extra_relations:
        brain.link_entities(
            source_name=s_name,
            source_type=s_type,
            relation_type=rel_t,
            target_name=t_name,
            target_type=t_type,
            evidence="Official EYC (eyc.asia) Architecture & Team Documentation",
            weight=w,
        )

    with brain._connect() as conn:

        # Update hr_agent_roster with enriched skill counts and Kaizen patches
        for dept_id in CORPORATE_DEPARTMENTS:
            sk_cnt = conn.execute(
                "SELECT COUNT(*) FROM department_installed_skills WHERE department_id = ?;",
                (dept_id,),
            ).fetchone()[0]
            kz_rows = conn.execute(
                "SELECT extracted_rule FROM kaizen_lessons WHERE department = ? OR applied_to_departments LIKE ?;",
                (dept_id, f"%{dept_id}%"),
            ).fetchall()
            kz_patch = "\n".join(f"• {r[0]}" for r in kz_rows)
            conn.execute(
                """
                UPDATE hr_agent_roster
                SET kaizen_prompt_patch = ?,
                    description = description || ' | Đã cài đặt ' || ? || ' kỹ năng & SOP chuyên sâu.',
                    updated_at_utc = ?
                WHERE department_id = ?;
                """,
                (kz_patch, sk_cnt, now_iso, dept_id),
            )

        mem_total = conn.execute("SELECT COUNT(*) FROM ai_memories;").fetchone()[0]
        skills_total = conn.execute("SELECT COUNT(*) FROM department_installed_skills;").fetchone()[0]
        kaizen_total = conn.execute("SELECT COUNT(*) FROM kaizen_lessons;").fetchone()[0]
        kg_e_total = conn.execute("SELECT COUNT(*) FROM kg_entities;").fetchone()[0]
        kg_r_total = conn.execute("SELECT COUNT(*) FROM kg_relations;").fetchone()[0]

    summary = {
        "ok": True,
        "eyc_pages_crawled_and_indexed": len(crawled_pages),
        "agency_specialist_skills_installed": agency_count,
        "openmontage_media_skills_installed": om_count,
        "total_installed_skills_in_db": skills_total,
        "tier1_ai_memories_count": mem_total,
        "tier2_kaizen_rules_count": kaizen_total,
        "tier3_kg_entities_count": kg_e_total,
        "tier3_kg_relations_count": kg_r_total,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    install_comprehensive_eyc_brain()
