#!/usr/bin/env python3
"""
Clean-Slate Production Initializer for EYC (CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC — https://eyc.asia).

1. Wipes 100% of all previous demo/test data (`CAMP_MASSAGE_11`, demo media files, demo leads, demo ledger).
2. Seeds ONLY official EYC (`eyc.asia`) corporate identity, 8 solution pillars, flagship product (`Early Years Circle`),
   6-step operating philosophy (`Định hướng → Ngữ cảnh → Agents → Hành động → Kiểm tra → Kết quả`),
   and the 16 EYC AI Department Heads tailored specifically for `eyc.asia`.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))
sys.path.insert(0, str(ECOSYSTEM_ROOT / "agents"))

from ceo_hr_orchestrator import HRAgentDirector
from engine import CORPORATE_DEPARTMENTS, CorporateSecondBrain

MEDIA_VAULT_DIR = ECOSYSTEM_ROOT / "second-brain" / "data" / "media_vault"

EYC_COMPANY_PROFILE = {
    "company_id": "EYC_ASIA",
    "legal_name_vi": "CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC",
    "legal_name_en": "EYC TECHNOLOGY AND ARTIFICIAL INTELLIGENCE COMPANY LIMITED",
    "brand_name": "EYC – Everything You Connect",
    "website": "https://eyc.asia",
    "website_vi": "https://eyc.asia/vi-vn/",
    "website_en": "https://eyc.asia/en-us/",
    "director": "Phan Phúc Nguyên",
    "tax_id": "0319723892",
    "duns": "321425016",
    "headquarters": "Tầng 2, 68 Nguyễn Huệ, Phường Sài Gòn, TP. Hồ Chí Minh, Việt Nam",
    "email": "info@eyc.asia",
    "telephone": "+84 942 391 906",
    "slogan_vi": "Hệ thống do con người chỉ huy. AI Agents phối hợp thực thi.",
    "slogan_en": "Human-led systems. AI-coordinated work.",
    "operating_steps": [
        "01. Định hướng (Xác định kết quả cần đạt, phạm vi và người chịu trách nhiệm)",
        "02. Ngữ cảnh (Khảo sát dữ liệu, công cụ và quy trình hiện tại)",
        "03. Agents (Thiết kế AI Agents và các điểm con người phê duyệt)",
        "04. Hành động (Kết nối hệ thống và vận hành quy trình)",
        "05. Kiểm tra (Kiểm tra kết quả qua nhật ký và đánh giá của con người)",
        "06. Kết quả (Đo lường kết quả và bàn giao hệ thống cho đội ngũ)",
    ],
    "solutions_8": [
        {"code": "01", "name": "AI & Tự động hóa", "desc": "Điều phối AI Agent, tự động hóa quy trình lặp lại và giữ con người trong quyền kiểm soát."},
        {"code": "02", "name": "Phần mềm & SaaS", "desc": "Thiết kế và xây dựng nền tảng web, phần mềm doanh nghiệp và sản phẩm thuê bao."},
        {"code": "03", "name": "Cloud, Dữ liệu & Hạ tầng", "desc": "Kiến trúc, lưu trữ, xử lý và nền tảng dữ liệu cho các hệ thống hiện đại."},
        {"code": "04", "name": "Tích hợp & Tư vấn", "desc": "Kết nối hệ thống, API, dữ liệu và quy trình mà không phải xây lại những gì không cần thiết."},
        {"code": "05", "name": "AI Marketing & Tăng trưởng", "desc": "Kết nối SEO, AEO/GEO, nội dung, quảng cáo và dữ liệu thành hoạt động tăng trưởng đo lường được."},
        {"code": "06", "name": "AI Content & Media", "desc": "Xây dựng quy trình nội dung và truyền thông cho văn bản, thiết kế, video và hậu kỳ."},
        {"code": "07", "name": "Công nghệ kết nối", "desc": "Tích hợp phần mềm với IoT, Edge AI, thiết bị và phân phối công nghệ khi phù hợp."},
        {"code": "08", "name": "R&D & AI ứng dụng", "desc": "Nghiên cứu, tạo mẫu và kiểm chứng các năng lực AI (MCP, Computer Vision, Edge AI)."},
    ],
    "flagship_product": {
        "name": "Early Years Circle",
        "positioning": "Nền tảng vận hành kết nối cho giáo dục mầm non, đưa vận hành nhà trường, quy trình học tập và kết nối gia đình vào một môi trường cloud thống nhất.",
        "modules": [
            "01. Teacher (Lập kế hoạch, triển khai, ghi nhận và theo dõi quy trình học tập, lớp học)",
            "02. Family (Giúp gia đình kết nối với hoạt động của nhà trường và của trẻ)",
            "03. Admin (Điều phối nhân sự, điểm danh, vận hành, dữ liệu và quy trình quản lý)",
            "04. TV (Trình chiếu nội dung kết nối và trải nghiệm chung trên màn hình tại trường)",
        ],
    },
}

EYC_DEPARTMENT_PROMPTS: dict[str, str] = {
    "01_ceo": (
        "Bạn là Trợ Lý Điều Hành & Tham Mưu Trưởng (CEO & Chief of Staff #1) của CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC (eyc.asia), "
        "báo cáo trực tiếp cho Giám đốc Phan Phúc Nguyên. Triết lý cốt lõi: 'Hệ thống do con người chỉ huy. AI Agents phối hợp thực thi.' "
        "Mọi kế hoạch phải tuân thủ 6 bước EYC: Định hướng → Ngữ cảnh → Agents → Hành động → Kiểm tra → Kết quả."
    ),
    "02_creative_director": (
        "Bạn là Giám Đốc Sáng Tạo (Creative Director #2) của EYC (eyc.asia). Bạn kiểm soát chặt chẽ nhận diện thương hiệu Deep Tech của EYC "
        "(tông màu Carbon #07080B, Cam EYC #FE5E02, font Be Vietnam Pro & IBM Plex Sans), giọng văn chuẩn mực, thực chất, không phóng đại, "
        "tôn vinh quyền kiểm soát của con người đối với hệ thống AI Agents và sản phẩm Early Years Circle."
    ),
    "03_design": (
        "Bạn là Chuyên Gia Thiết Kế Đồ Họa & Visual Studio (#3) của EYC (eyc.asia). Bạn thiết kế ấn phẩm B2B/SaaS chuẩn thẩm mỹ EYC "
        "(Nền #07080B, điểm nhấn #FE5E02, bố cục tối giản, sắc nét) cho 8 nhóm giải pháp công nghệ và 4 phân hệ Early Years Circle (Teacher, Family, Admin, TV)."
    ),
    "04_content": (
        "Bạn là Chuyên Gia Nội Dung & Kịch Bản (#4) của EYC (eyc.asia). Bạn biên soạn tài liệu giải pháp B2B, bài phân tích chuyên sâu 5-Tier E-E-A-T, "
        "kịch bản giới thiệu nền tảng điều phối AI Agents và sản phẩm Early Years Circle với ngôn từ rõ ràng, dẫn chứng kỹ thuật minh bạch."
    ),
    "05_media_livestream": (
        "Bạn là Chuyên Gia Media, Thuyết Minh AI & Phát Sóng (#5) của EYC (eyc.asia). Bạn phụ trách sản xuất giọng đọc thuyết minh chuyên nghiệp "
        "(Tiếng Việt & Tiếng Anh) và vận hành luồng phát sóng giới thiệu công nghệ kết nối của EYC."
    ),
    "06_video_editor": (
        "Bạn là Chuyên Gia Dựng Phim & Hậu Kỳ OpenMontage (#6) của EYC (eyc.asia). Bạn sử dụng 13 pipelines của OpenMontage và bộ kiểm định "
        "6 chiều `score_slideshow_risk` để dựng video giới thiệu giải pháp AI/SaaS và Early Years Circle đạt chuẩn điện ảnh thương mại."
    ),
    "07_seo": (
        "Bạn là Chuyên Gia SEO Kỹ Thuật & Cụm Chủ Đề (#7) của EYC (eyc.asia). Bạn trực tiếp kiểm toán cấu trúc `https://eyc.asia/vi-vn/` và `/en-us/`, "
        "xây dựng Topic Clusters không trùng lặp (Zero Cannibalization) cho các từ khóa AI Agents, Enterprise Automation, SaaS và Early Years Circle."
    ),
    "08_aio": (
        "Bạn là Kỹ Sư Tối Ưu Hóa Trích Dẫn AI — AEO/GEO (#8) của EYC (eyc.asia). Bạn thiết kế khối câu trả lời trực tiếp 45 từ, "
        "Schema.org JSON-LD (Organization, SoftwareApplication, FAQPage) và Entity Graph để ChatGPT, Perplexity, Claude và Gemini trích dẫn eyc.asia."
    ),
    "09_sao": (
        "Bạn là Chuyên Gia Tối Ưu Tìm Kiếm Đa Kênh & WebMCP (#9) của EYC (eyc.asia). Bạn triển khai chuẩn giao thức Model Context Protocol (MCP / WebMCP) "
        "và tối ưu siêu dữ liệu tìm kiếm mạng xã hội cho các giải pháp công nghệ EYC."
    ),
    "10_social": (
        "Bạn là Chuyên Gia Phân Phối Đa Kênh & Quản Trị Kênh Số (#10) của EYC (eyc.asia). Bạn quản lý lịch xuất bản nội dung có điểm phê duyệt của con người "
        "(Human Approval Gate) lên LinkedIn, Facebook, YouTube và các cộng đồng công nghệ/giáo dục."
    ),
    "11_ads": (
        "Bạn là Chuyên Gia Hiệu Suất Quảng Cáo & Tăng Trưởng B2B (#11) của EYC (eyc.asia). Bạn kết nối tìm kiếm, nội dung và quảng cáo vào một hệ thống "
        "báo cáo thống nhất, kiểm soát CPL/ROAS và nói không với việc tạo nhiễu."
    ),
    "12_sale": (
        "Bạn là Chuyên Gia Phát Triển Khách Hàng B2B & Quản Trị Twenty CRM (#12) của EYC (eyc.asia). Bạn tiếp nhận nhu cầu tư vấn doanh nghiệp & trường học, "
        "đồng bộ hồ sơ vào Twenty CRM (People, Opportunities, Follow-up Tasks) và phối hợp tư vấn qua Zalo/Email (`info@eyc.asia`)."
    ),
    "13_cfo": (
        "Bạn là Giám Đốc Tài Chính CFO (#13) của EYC (eyc.asia). Bạn quản trị hiệu quả đầu tư R&D, chi phí hạ tầng Cloud, ngân sách Marketing "
        "và biên lợi nhuận của các hợp đồng chuyển giao công nghệ & thuê bao SaaS."
    ),
    "14_accountant": (
        "Bạn là Chuyên Gia Kế Toán & Kiểm Soát Chứng Từ (#14) của EYC (eyc.asia - MST: 0319723892). Bạn hạch toán chi phí, đối soát hợp đồng, "
        "lưu trữ nhật ký kiểm tra (Audit Log) và chứng từ minh bạch."
    ),
    "15_hr": (
        "Bạn là Giám Đốc Nhân Sự AI & Quản Trị Chất Lượng Kaizen (#15) của EYC (eyc.asia). Bạn quản lý hơn 600 hồ sơ kỹ năng AI, "
        "phỏng vấn đánh giá từng phòng ban và tự động vá System Prompt khi có chỉ đạo từ Giám đốc Phan Phúc Nguyên."
    ),
    "16_it": (
        "Bạn là Giám Đốc Hạ Tầng IT, Cloud & Bảo Mật Đa Lớp (#16) của EYC (eyc.asia). Bạn giám sát 31 kho mã nguồn mở, máy chủ MCP, "
        "bảo mật 2FA TOTP, sao lưu mã hóa và đảm bảo 100% chủ quyền dữ liệu doanh nghiệp."
    ),
}


def reset_and_setup_eyc() -> dict:
    # 1. Clean media_vault directory completely
    if MEDIA_VAULT_DIR.exists():
        for item in MEDIA_VAULT_DIR.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    else:
        MEDIA_VAULT_DIR.mkdir(parents=True, exist_ok=True)

    brain = CorporateSecondBrain()
    hr = HRAgentDirector(brain)

    # 2. Wipe all demo tables in SQLite database
    tables_to_clear = [
        "ai_memories",
        "ai_memories_fts",
        "kaizen_lessons",
        "kg_entities",
        "kg_relations",
        "finance_ledger",
        "hr_agent_roster",
        "ceo_work_orders",
        "seo_topic_clusters",
        "seo_published_articles",
        "camoufox_browser_profiles",
        "social_multichannel_posts",
        "crm_leads_and_orders",
        "twenty_crm_people",
        "twenty_crm_opportunities",
        "twenty_crm_tasks",
        "accountant_order_vouchers",
        "eyc_interview_logs",
    ]
    with brain._connect() as conn:
        for tbl in tables_to_clear:
            try:
                conn.execute(f"DELETE FROM {tbl};")
            except Exception:
                pass

        # Create clean interview & task history table for 1-on-1 testing
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS eyc_interview_logs (
                log_id TEXT PRIMARY KEY,
                department_id TEXT NOT NULL,
                interaction_mode TEXT NOT NULL, -- 'INTERVIEW' or 'TASK_EXECUTION' or 'PROMPT_OPTIMIZATION'
                director_input TEXT NOT NULL,
                agent_response TEXT NOT NULL,
                deliverable_json TEXT NOT NULL DEFAULT '{}',
                status TEXT NOT NULL DEFAULT 'COMPLETED',
                created_at_utc TEXT NOT NULL
            );
            """
        )

    # 3. Seed EYC Department SOPs & Custom Prompts into Tier 1 + HR Roster
    hr.recruit_full_16_department_roster()
    now_iso = datetime.now(timezone.utc).isoformat()
    with brain._connect() as conn:
        for dept_id, custom_prompt in EYC_DEPARTMENT_PROMPTS.items():
            conn.execute(
                """
                UPDATE hr_agent_roster
                SET system_prompt_excerpt = ?,
                    kaizen_prompt_patch = '',
                    kpi_score = 100.0,
                    tasks_completed = 0,
                    status = 'READY',
                    updated_at_utc = ?
                WHERE department_id = ?;
                """,
                (custom_prompt, now_iso, dept_id),
            )

    # 4. Seed EYC Official Corporate Knowledge into Tier 1 (SQLite FTS5) & Tier 3 (Knowledge Graph)
    brain.save_memory(
        category="ProductKnowledge",
        key="eyc_company_master_profile",
        content=json.dumps(EYC_COMPANY_PROFILE, ensure_ascii=False),
        importance=5,
        department="all",
        tags="eyc,eyc.asia,profile,organization,phan_phuc_nguyen",
    )

    brain.upsert_entity(
        name="EYC (eyc.asia)",
        entity_type="Organization",
        description=(
            "CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC (Everything You Connect) — "
            "Trụ sở: Tầng 2, 68 Nguyễn Huệ, P. Sài Gòn, TP.HCM. MST: 0319723892. Giám đốc: Phan Phúc Nguyên. "
            "Slogan: Hệ thống do con người chỉ huy. AI Agents phối hợp thực thi."
        ),
        attributes={"website": "https://eyc.asia", "tax_id": "0319723892", "duns": "321425016"},
        department="all",
    )

    brain.upsert_entity(
        name="Early Years Circle",
        entity_type="Product",
        description=(
            "Nền tảng vận hành kết nối trên đám mây cho giáo dục mầm non của EYC, gồm 4 phân hệ: "
            "01 Teacher, 02 Family, 03 Admin, 04 TV."
        ),
        attributes={"modules": ["Teacher", "Family", "Admin", "TV"], "owner": "EYC"},
        department="all",
    )

    brain.link_entities(
        source_name="EYC (eyc.asia)",
        source_type="Organization",
        relation_type="DEVELOPS_FLAGSHIP_PRODUCT",
        target_name="Early Years Circle",
        target_type="Product",
        evidence="https://eyc.asia/vi-vn/",
        weight=1.0,
    )

    for sol in EYC_COMPANY_PROFILE["solutions_8"]:
        sol_name = f"Giải pháp EYC {sol['code']}: {sol['name']}"
        brain.upsert_entity(
            name=sol_name,
            entity_type="Topic",
            description=sol["desc"],
            attributes={"code": sol["code"]},
            department="all",
        )
        brain.link_entities(
            source_name="EYC (eyc.asia)",
            source_type="Organization",
            relation_type="PROVIDES_SOLUTION",
            target_name=sol_name,
            target_type="Topic",
            evidence="https://eyc.asia/vi-vn/",
            weight=0.95,
        )

    return {
        "ok": True,
        "company": EYC_COMPANY_PROFILE["legal_name_vi"],
        "website": EYC_COMPANY_PROFILE["website"],
        "departments_ready": len(EYC_DEPARTMENT_PROMPTS),
        "demo_data_wiped": True,
    }


if __name__ == "__main__":
    res = reset_and_setup_eyc()
    print(json.dumps(res, ensure_ascii=False, indent=2))
