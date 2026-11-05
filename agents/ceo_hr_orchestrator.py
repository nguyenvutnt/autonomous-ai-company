"""
Step 2 Implementation:
- Department #1: CEO & Chief of Staff (`CEOExecutiveAgent`)
- Department #15: HR & Agent Operations Director (`HRAgentDirector`)

Integrates:
1. `00-ai-company-agents/agency-agents` (330+ specialist markdown profiles)
2. `00-ai-company-agents/agency-agents-zh` (277+ localized & e-commerce profiles)
3. `second-brain/engine.py` (`CorporateSecondBrain` 3-Tier Memory, Kaizen & Knowledge Graph)
"""

from __future__ import annotations

import json
import math
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))

from engine import CORPORATE_DEPARTMENTS, CorporateSecondBrain, _strip_accents

AGENCY_AGENTS_DIR = ECOSYSTEM_ROOT / "00-ai-company-agents" / "agency-agents"
AGENCY_AGENTS_ZH_DIR = ECOSYSTEM_ROOT / "00-ai-company-agents" / "agency-agents-zh"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_frontmatter(md_text: str) -> dict[str, str]:
    """Extracts YAML frontmatter fields (`name`, `description`, `vibe`, `emoji`) from an agent markdown file."""
    meta: dict[str, str] = {}
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


class HRAgentDirector:
    """
    Department #15: Giám Đốc Nhân Sự & Quản Trị Agent (HR & Agent Kaizen Director).

    Responsibilities:
    - Scans and indexes all 330+ specialist profiles from `agency-agents` and `agency-agents-zh`.
    - Recruits and assigns the best specialist persona for each of the 16 departments.
    - Evaluates department KPIs, detects bottlenecks, and auto-patches System Prompts via Kaizen lessons.
    """

    def __init__(self, brain: CorporateSecondBrain | None = None) -> None:
        self.brain = brain or CorporateSecondBrain()
        self._init_hr_tables()

    def _init_hr_tables(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS hr_agent_roster (
            agent_id TEXT PRIMARY KEY,
            department_id TEXT NOT NULL,
            department_name TEXT NOT NULL,
            specialist_name TEXT NOT NULL,
            profile_path TEXT NOT NULL,
            description TEXT NOT NULL,
            system_prompt_excerpt TEXT NOT NULL,
            kaizen_prompt_patch TEXT NOT NULL DEFAULT '',
            kpi_score REAL NOT NULL DEFAULT 100.0,
            tasks_completed INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            updated_at_utc TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ceo_work_orders (
            order_id TEXT PRIMARY KEY,
            campaign_id TEXT NOT NULL,
            department_id TEXT NOT NULL,
            phase_number INTEGER NOT NULL,
            task_title TEXT NOT NULL,
            sop_instructions TEXT NOT NULL,
            kpi_target_json TEXT NOT NULL,
            assigned_weapons TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'READY',
            deliverable_summary TEXT NOT NULL DEFAULT '',
            kpi_achieved_json TEXT NOT NULL DEFAULT '{}',
            created_at_utc TEXT NOT NULL,
            updated_at_utc TEXT NOT NULL
        );
        """
        with self.brain._connect() as conn:
            conn.executescript(sql)

    def scan_talent_pool(self, keyword: str | None = None, limit: int = 30) -> list[dict[str, Any]]:
        """
        Scans the 330+ specialist agent markdown profiles in `00-ai-company-agents/agency-agents`
        and returns matching profiles.
        """
        results: list[dict[str, Any]] = []
        norm_kw = _strip_accents(keyword) if keyword else None

        search_dirs = [d for d in [AGENCY_AGENTS_DIR, AGENCY_AGENTS_ZH_DIR] if d.exists()]
        for base_dir in search_dirs:
            for md_path in sorted(base_dir.rglob("*.md")):
                if md_path.name.upper() in {"README.MD", "CONTRIBUTING.MD", "CONTRIBUTING_ZH-CN.MD", "SECURITY.MD", "LICENSE"}:
                    continue
                if ".github" in md_path.parts or "examples" in md_path.parts or "integrations" in md_path.parts:
                    continue

                rel_path = str(md_path.relative_to(base_dir))
                try:
                    raw = md_path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue

                meta = _parse_frontmatter(raw)
                name = meta.get("name") or md_path.stem.replace("-", " ").title()
                desc = meta.get("description") or ""
                division = md_path.parent.name

                if norm_kw:
                    haystack = _strip_accents(f"{rel_path} {name} {desc} {division}")
                    if not all(tok in haystack for tok in norm_kw.split()):
                        continue

                results.append(
                    {
                        "name": name,
                        "division": division,
                        "relative_path": rel_path,
                        "full_path": str(md_path),
                        "description": desc,
                        "vibe": meta.get("vibe", ""),
                    }
                )
                if len(results) >= limit:
                    return results

        return results

    def recruit_full_16_department_roster(self) -> list[dict[str, Any]]:
        """
        Recruits and binds the official 16 Department Heads & Specialists from `agency-agents`
        into `hr_agent_roster` and Tier 1 memory, enriching each with any active Kaizen prompt rules.
        """
        now_iso = _utc_now_iso()
        roster: list[dict[str, Any]] = []

        for dept_id, dept_info in CORPORATE_DEPARTMENTS.items():
            ref_rel = dept_info["profile_ref"]
            md_file = AGENCY_AGENTS_DIR / ref_rel
            raw_md = ""
            if md_file.exists():
                raw_md = md_file.read_text(encoding="utf-8", errors="ignore")

            meta = _parse_frontmatter(raw_md)
            spec_name = meta.get("name") or dept_info["name"]
            desc = meta.get("description") or dept_info["role"]
            excerpt = raw_md[:1200].strip() if raw_md else dept_info["role"]

            # Pull latest Kaizen rules for this department to inject into the agent's prompt patch
            kaizen_lessons = self.brain.get_kaizen_lessons(department=dept_id, limit=5)
            kaizen_patch = "\n".join(
                f"- [{kz['outcome_status']}] {kz['extracted_rule']}"
                for kz in kaizen_lessons
            )

            agent_id = f"agent_{dept_id}"
            with self.brain._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO hr_agent_roster (
                        agent_id, department_id, department_name, specialist_name,
                        profile_path, description, system_prompt_excerpt, kaizen_prompt_patch,
                        kpi_score, tasks_completed, status, updated_at_utc
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 100.0, 0, 'ACTIVE', ?)
                    ON CONFLICT(agent_id) DO UPDATE SET
                        specialist_name = excluded.specialist_name,
                        profile_path = excluded.profile_path,
                        description = excluded.description,
                        system_prompt_excerpt = excluded.system_prompt_excerpt,
                        kaizen_prompt_patch = excluded.kaizen_prompt_patch,
                        updated_at_utc = excluded.updated_at_utc;
                    """,
                    (
                        agent_id,
                        dept_id,
                        dept_info["name"],
                        spec_name,
                        ref_rel,
                        desc,
                        excerpt,
                        kaizen_patch,
                        now_iso,
                    ),
                )

            roster.append(
                {
                    "agent_id": agent_id,
                    "department_id": dept_id,
                    "department_name": dept_info["name"],
                    "specialist_name": spec_name,
                    "profile_path": ref_rel,
                    "weapons": dept_info["weapons"],
                    "kaizen_rules_loaded": len(kaizen_lessons),
                    "status": "ACTIVE",
                }
            )

        return roster

    def evaluate_department_kpi_and_kaizen(
        self,
        department_id: str,
        campaign_id: str,
        kpi_achieved: dict[str, Any],
        kpi_target: dict[str, Any],
        notes: str = "",
    ) -> dict[str, Any]:
        """
        HR & Operations Manager DMAIC evaluation:
        Compares achieved KPI vs target KPI, updates the department's KPI score in `hr_agent_roster`,
        and records a Kaizen self-learning rule in Tier 2 (`kaizen_lessons`) + updates the agent's prompt patch.
        """
        ratios: list[float] = []
        for metric_key, target_val in kpi_target.items():
            if isinstance(target_val, (int, float)) and target_val > 0 and metric_key in kpi_achieved:
                actual_val = float(kpi_achieved[metric_key])
                # For cost metrics (cpl, cpa, spend), lower is better
                if "cost" in metric_key.lower() or "cpl" in metric_key.lower() or "cpa" in metric_key.lower():
                    ratio = target_val / max(actual_val, 1.0)
                else:
                    ratio = actual_val / target_val
                ratios.append(ratio)

        avg_ratio = sum(ratios) / len(ratios) if ratios else 1.0
        kpi_score = round(min(150.0, max(10.0, avg_ratio * 100.0)), 1)
        outcome = "WIN" if kpi_score >= 95.0 else "LOSS"

        rule = (
            f"Đạt {kpi_score}% KPI mục tiêu trong chiến dịch {campaign_id}. "
            f"{notes or ('Duy trì quy trình chuẩn SOP hiện tại.' if outcome == 'WIN' else 'Cần tối ưu lại Hook và tỷ lệ chuyển đổi ngay lập tức.')}"
        )

        kz = self.brain.record_kaizen_lesson(
            department=department_id,
            campaign_or_task=campaign_id,
            action_taken=f"Thực thi Work Order chiến dịch {campaign_id} | Target={json.dumps(kpi_target, ensure_ascii=False)}",
            outcome_status=outcome,
            extracted_rule=rule,
            metrics={"kpi_score": kpi_score, "achieved": kpi_achieved, "target": kpi_target},
            importance=5 if outcome == "LOSS" else 4,
            applied_to_departments=department_id,
        )

        now_iso = _utc_now_iso()
        with self.brain._connect() as conn:
            conn.execute(
                """
                UPDATE hr_agent_roster
                SET kpi_score = ?,
                    tasks_completed = tasks_completed + 1,
                    kaizen_prompt_patch = CASE
                        WHEN kaizen_prompt_patch = '' THEN ?
                        ELSE kaizen_prompt_patch || char(10) || ?
                    END,
                    updated_at_utc = ?
                WHERE department_id = ?;
                """,
                (kpi_score, f"- [{outcome}] {rule}", f"- [{outcome}] {rule}", now_iso, department_id),
            )

        return {
            "department_id": department_id,
            "campaign_id": campaign_id,
            "kpi_score": kpi_score,
            "outcome_status": outcome,
            "kaizen_lesson": kz,
        }


class CEOExecutiveAgent:
    """
    Department #1: CEO & Chief of Staff (`CEOExecutiveAgent`).

    Responsibilities:
    - Receives high-level business & revenue goals from the Founder/User.
    - Calculates backward unit economics (Revenue Target -> Orders -> Leads -> Traffic/Views -> Content/Video/Ads Quota).
    - Generates a structured 6-Phase Master Campaign Plan and dispatches Concrete Work Orders (`ceo_work_orders`)
      to all 16 departments via the Corporate Second Brain.
    - Conducts Executive Board Reviews combining CFO Financials, HR Agent Scorecards, and Kaizen Lessons.
    """

    def __init__(
        self,
        brain: CorporateSecondBrain | None = None,
        hr_director: HRAgentDirector | None = None,
    ) -> None:
        self.brain = brain or CorporateSecondBrain()
        self.hr = hr_director or HRAgentDirector(self.brain)

    def launch_strategic_campaign(
        self,
        campaign_name: str,
        product_name: str,
        product_price_vnd: float,
        target_revenue_vnd: float,
        duration_days: int = 30,
        max_ad_budget_ratio: float = 0.15,
        estimated_close_rate: float = 0.25,
        target_audience: str = "Khách hàng mục tiêu trên Facebook, Zalo, TikTok & Google",
    ) -> dict[str, Any]:
        """
        Translates a revenue goal into unit economics, registers the campaign in Tier 1 & Tier 3,
        recruits/verifies all 16 departments via HR, and issues 16 synchronized Department Work Orders.
        """
        campaign_id = f"CAMP_{_strip_accents(product_name).upper().replace(' ', '_')[:16]}_{uuid.uuid4().hex[:4].upper()}"
        now_iso = _utc_now_iso()

        # 1. Ensure all 16 Department Specialists are recruited and active
        roster = self.hr.recruit_full_16_department_roster()

        # 2. Calculate Backward Unit Economics
        orders_needed = max(1, math.ceil(target_revenue_vnd / max(product_price_vnd, 1.0)))
        leads_needed = max(1, math.ceil(orders_needed / max(estimated_close_rate, 0.05)))
        daily_orders = max(1, math.ceil(orders_needed / max(duration_days, 1)))
        daily_leads = max(1, math.ceil(leads_needed / max(duration_days, 1)))
        max_budget_vnd = round(target_revenue_vnd * max_ad_budget_ratio, 0)
        target_roas = round(1.0 / max(max_ad_budget_ratio, 0.01), 2)
        target_cpl_vnd = round(max_budget_vnd / leads_needed, 0)

        # Estimate content/media volume needed to generate `leads_needed`
        seo_articles_needed = max(10, duration_days * 2)
        short_videos_needed = max(30, duration_days * 3)
        social_posts_needed = max(60, duration_days * 10)
        livestream_hours = duration_days * 12

        unit_economics = {
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "product_name": product_name,
            "product_price_vnd": product_price_vnd,
            "target_revenue_vnd": target_revenue_vnd,
            "duration_days": duration_days,
            "orders_needed": orders_needed,
            "daily_orders_target": daily_orders,
            "leads_needed": leads_needed,
            "daily_leads_target": daily_leads,
            "max_budget_vnd": max_budget_vnd,
            "target_roas": target_roas,
            "target_cpl_vnd": target_cpl_vnd,
            "quotas": {
                "seo_aio_articles": seo_articles_needed,
                "short_videos_reels_tiktok": short_videos_needed,
                "social_group_posts": social_posts_needed,
                "livestream_hours_24_7": livestream_hours,
            },
        }

        # 3. Persist Strategic Plan & Entities in Corporate Second Brain
        self.brain.save_memory(
            category="CampaignRule",
            key=f"ceo_master_plan_{campaign_id.lower()}",
            content=(
                f"Chiến dịch '{campaign_name}' ({campaign_id}) cho SP '{product_name}' (Giá {product_price_vnd:,.0f}đ): "
                f"Mục tiêu doanh thu {target_revenue_vnd:,.0f}đ trong {duration_days} ngày -> "
                f"Cần {orders_needed} đơn ({daily_orders} đơn/ngày), {leads_needed} leads ({daily_leads} leads/ngày), "
                f"Ngân sách tối đa {max_budget_vnd:,.0f}đ (ROAS mục tiêu >= {target_roas}x, CPL <= {target_cpl_vnd:,.0f}đ)."
            ),
            importance=5,
            department="all",
            tags=f"ceo,campaign,{campaign_id.lower()}",
        )

        self.brain.upsert_entity(
            name=product_name,
            entity_type="Product",
            description=f"Sản phẩm chủ lực chiến dịch {campaign_name} (Giá {product_price_vnd:,.0f}đ)",
            attributes=unit_economics,
        )
        self.brain.upsert_entity(
            name=target_audience,
            entity_type="Persona",
            description=f"Tệp khách hàng mục tiêu của chiến dịch {campaign_name}",
            attributes={"campaign_id": campaign_id},
        )
        self.brain.link_entities(
            source_name=product_name,
            source_type="Product",
            relation_type="TARGETS_PERSONA",
            target_name=target_audience,
            target_type="Persona",
            evidence=f"CEO Master Plan {campaign_id}",
            weight=1.0,
        )

        # 4. Create 16 Department Work Orders across 6 Execution Waves
        work_orders_spec: list[dict[str, Any]] = [
            {
                "department_id": "01_ceo",
                "phase": 1,
                "title": f"Điều phối tổng thể & kiểm soát KPI chiến dịch {campaign_name}",
                "sop": "Giám sát tiến độ 16 phòng ban mỗi 24h, duyệt ngân sách dựa trên ROAS thực tế.",
                "kpi": {"target_revenue_vnd": target_revenue_vnd, "target_roas": target_roas},
            },
            {
                "department_id": "15_hr",
                "phase": 1,
                "title": "Đảm bảo 16 Agent chuẩn SOP & cập nhật luật Kaizen sau mỗi ca chạy",
                "sop": "Rà soát điểm KPI của 16 phòng ban, tự động vá System Prompt khi phát hiện lệch chuẩn.",
                "kpi": {"active_departments": 16, "min_department_kpi_score": 95.0},
            },
            {
                "department_id": "16_it",
                "phase": 1,
                "title": "Đảm bảo Uptime 100% cho MCP, n8n, Camoufox Anti-Detect & Proxy Pool",
                "sop": "Kiểm tra kết nối Zalo MCP, Facebook.Net, xoay Proxy sạch và tự động vượt lỗi DOM.",
                "kpi": {"uptime_percent": 99.9, "checkpoint_rate_max": 0.01},
            },
            {
                "department_id": "07_seo",
                "phase": 2,
                "title": f"Quét đối thủ bằng Crawl4AI & xuất bản {seo_articles_needed} bài SEO Topic Cluster",
                "sop": f"Dùng crawl4ai & firecrawl phân tích Top 10 đối thủ ngành '{product_name}', phủ từ khóa ngách chuyển đổi cao.",
                "kpi": {"seo_articles_published": seo_articles_needed, "organic_leads": math.ceil(leads_needed * 0.2)},
            },
            {
                "department_id": "08_aio",
                "phase": 2,
                "title": f"Tối ưu Entity Graph & Schema JSON-LD để AI (ChatGPT/Perplexity/Gemini) trích dẫn '{product_name}'",
                "sop": "Xây dựng bảng so sánh trực diện, FAQ chuẩn AEO/GEO và liên kết thực thể trong LightRAG.",
                "kpi": {"ai_citation_entities": 20, "aeo_faq_blocks": seo_articles_needed},
            },
            {
                "department_id": "09_sao",
                "phase": 2,
                "title": f"Tối ưu từ khóa tìm kiếm mạng xã hội (TikTok/FB/Zalo/Shopee Search) cho '{product_name}'",
                "sop": "Chèn từ khóa xu hướng tìm kiếm vào tiêu đề video, mô tả, bình luận ghim và hashtags.",
                "kpi": {"social_search_keywords_ranked": 30},
            },
            {
                "department_id": "02_creative_director",
                "phase": 3,
                "title": f"Phê duyệt Concept chủ đạo, Brand Voice & 10 góc Hook 3 giây cho '{product_name}'",
                "sop": "Kiểm duyệt chặt chẽ mọi kịch bản theo luật Kaizen (ưu tiên cảnh nỗi đau thực tế 3s đầu).",
                "kpi": {"approved_hook_angles": 10, "brand_compliance_rate": 100.0},
            },
            {
                "department_id": "04_content",
                "phase": 3,
                "title": f"Biên soạn {seo_articles_needed} bài E-E-A-T, {short_videos_needed} kịch bản Shorts & Spintax 200x",
                "sop": "Kết hợp gpt-researcher và bài học Kaizen để viết nội dung không trùng lặp, đúng nỗi đau khách hàng.",
                "kpi": {"scripts_and_articles": seo_articles_needed + short_videos_needed, "spintax_variations": 200},
            },
            {
                "department_id": "03_design",
                "phase": 3,
                "title": f"Sản xuất bộ ảnh Studio, Thumbnail CTR cao & đồng nhất mẫu AI cho '{product_name}'",
                "sop": "Dùng ComfyUI & ImageSharp xuất ảnh sản phẩm sắc nét, chèn khung lợi ích và nén chuẩn WebP.",
                "kpi": {"visual_assets_created": short_videos_needed * 2},
            },
            {
                "department_id": "06_video_editor",
                "phase": 3,
                "title": f"Sản xuất & Việt hóa {short_videos_needed} video Shorts/Reels/TikTok bằng MoneyPrinterTurbo & pyvideotrans",
                "sop": "Tải nguồn Douyin/TikTok không logo bằng dtk, lồng tiếng Việt, đóng sub vàng chữ đen nổi bật 3s đầu.",
                "kpi": {"short_videos_rendered": short_videos_needed, "avg_hook_retention_target": 0.45},
            },
            {
                "department_id": "05_media_livestream",
                "phase": 4,
                "title": f"Vận hành {livestream_hours} giờ Livestream/Re-stream đa kênh 24/7 qua MediaMTX & SRS",
                "sop": "Ghép giọng đọc edge-tts tự nhiên với LivePortrait và phát đồng thời lên FB, TikTok, YT, Shopee.",
                "kpi": {"livestream_hours": livestream_hours, "concurrent_channels": 5},
            },
            {
                "department_id": "10_social",
                "phase": 4,
                "title": f"Phân phối {social_posts_needed} bài đăng đa kênh & rải Group bằng dàn nick Camoufox",
                "sop": "Dùng Postiz-app và Facebook.Net đăng tự động lên 12 mạng xã hội và các hội nhóm đúng tệp.",
                "kpi": {"multi_channel_posts": social_posts_needed, "group_reach_posts": social_posts_needed * 3},
            },
            {
                "department_id": "11_ads",
                "phase": 5,
                "title": f"Chạy chiến dịch Ads & Auto Seeding/Up tin mang về {leads_needed} leads với CPL <= {target_cpl_vnd:,.0f}đ",
                "sop": "Bơm seeding chéo tạo hiệu ứng đám đông, tự động tắt nhóm quảng cáo có CPL vượt ngưỡng.",
                "kpi": {"leads_generated": leads_needed, "max_cpl_vnd": target_cpl_vnd},
            },
            {
                "department_id": "12_sale",
                "phase": 5,
                "title": f"Quét SĐT/UID nóng, kết bạn Zalo.Net tự động & chốt {orders_needed} đơn hàng ({target_revenue_vnd:,.0f}đ)",
                "sop": "Dùng FBGlobal quét khách bình luận, kết bạn & nhắn tin Zalo.Net + trực Chatwoot/Listmonk chốt đơn trong 5 phút.",
                "kpi": {"orders_closed": orders_needed, "revenue_vnd": target_revenue_vnd},
            },
            {
                "department_id": "13_cfo",
                "phase": 6,
                "title": f"Kiểm soát ngân sách {max_budget_vnd:,.0f}đ & đảm bảo ROAS >= {target_roas}x",
                "sop": "Theo dõi tỷ lệ chi phí/doanh thu theo ngày, cảnh báo ngay nếu ROAS tụt dưới ngưỡng an toàn.",
                "kpi": {"target_roas": target_roas, "max_budget_vnd": max_budget_vnd},
            },
            {
                "department_id": "14_accountant",
                "phase": 6,
                "title": f"Hạch toán thu-chi từng đơn & lưu video đóng gói đối soát cho {orders_needed} đơn hàng",
                "sop": "Ghi sổ cái FinanceLedger chính xác 100%, gắn mã vận đơn với video Simple Replay chống hoàn hàng gian lận.",
                "kpi": {"reconciled_orders": orders_needed, "ledger_accuracy_percent": 100.0},
            },
        ]

        created_orders: list[dict[str, Any]] = []
        with self.brain._connect() as conn:
            for item in work_orders_spec:
                dept_id = item["department_id"]
                order_id = f"WO_{campaign_id}_{dept_id.upper()}"
                weapons = CORPORATE_DEPARTMENTS[dept_id]["weapons"]
                kpi_json = json.dumps(item["kpi"], ensure_ascii=False)

                conn.execute(
                    """
                    INSERT INTO ceo_work_orders (
                        order_id, campaign_id, department_id, phase_number,
                        task_title, sop_instructions, kpi_target_json, assigned_weapons,
                        status, created_at_utc, updated_at_utc
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'READY', ?, ?)
                    ON CONFLICT(order_id) DO UPDATE SET
                        task_title = excluded.task_title,
                        sop_instructions = excluded.sop_instructions,
                        kpi_target_json = excluded.kpi_target_json,
                        updated_at_utc = excluded.updated_at_utc;
                    """,
                    (
                        order_id,
                        campaign_id,
                        dept_id,
                        item["phase"],
                        item["title"],
                        item["sop"],
                        kpi_json,
                        weapons,
                        now_iso,
                        now_iso,
                    ),
                )

                created_orders.append(
                    {
                        "order_id": order_id,
                        "phase": item["phase"],
                        "department_id": dept_id,
                        "department_name": CORPORATE_DEPARTMENTS[dept_id]["name"],
                        "task_title": item["title"],
                        "kpi_target": item["kpi"],
                        "assigned_weapons": weapons,
                        "status": "READY",
                    }
                )

        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "unit_economics": unit_economics,
            "recruited_departments_count": len(roster),
            "work_orders_count": len(created_orders),
            "work_orders": created_orders,
        }

    def get_executive_board_report(self, campaign_id: str | None = None) -> dict[str, Any]:
        """
        Generates a real-time CEO + HR + CFO Executive Board Report across all 16 departments.
        """
        with self.brain._connect() as conn:
            roster_rows = conn.execute(
                "SELECT department_id, department_name, specialist_name, kpi_score, tasks_completed, status FROM hr_agent_roster ORDER BY department_id;"
            ).fetchall()
            order_rows = conn.execute(
                """
                SELECT order_id, campaign_id, department_id, phase_number, task_title, kpi_target_json, status
                FROM ceo_work_orders
                WHERE (? IS NULL OR campaign_id = ?)
                ORDER BY phase_number ASC, department_id ASC;
                """,
                (campaign_id, campaign_id),
            ).fetchall()

        finance = self.brain.get_financial_summary(campaign_id)
        recent_kaizen = self.brain.get_kaizen_lessons(limit=10)

        return {
            "campaign_filter": campaign_id or "ALL_CAMPAIGNS",
            "cfo_financial_summary": finance,
            "hr_roster_health": [dict(r) for r in roster_rows],
            "active_work_orders": [
                {
                    "order_id": r["order_id"],
                    "campaign_id": r["campaign_id"],
                    "department_id": r["department_id"],
                    "phase": r["phase_number"],
                    "task_title": r["task_title"],
                    "kpi_target": json.loads(r["kpi_target_json"] or "{}"),
                    "status": r["status"],
                }
                for r in order_rows
            ],
            "latest_kaizen_lessons": recent_kaizen,
        }
