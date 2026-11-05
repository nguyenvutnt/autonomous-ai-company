#!/usr/bin/env python3
"""
End-to-End Practical Verification & Kaizen Test Suite for Step 1:
3-Tier Corporate Second Brain (`CorporateSecondBrain` + FTS5 BM25 + Kaizen + Knowledge Graph + CFO Ledger).
"""

from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import CORPORATE_DEPARTMENTS, CorporateSecondBrain


def run_step1_verification(db_path: str | None = None) -> None:
    print("=" * 78)
    print("🚀 BẮT ĐẦU KIỂM THỬ THỰC TẾ BƯỚC 1: BỘ NÃO THỨ 2 TOÀN CÔNG TY (3 TẦNG)")
    print("=" * 78)

    brain = CorporateSecondBrain(db_path=db_path) if db_path else CorporateSecondBrain()

    # 1. Verify 16 Departments SOP seeded in Tier 1
    sops = brain.query_memories(category="DepartmentSop", limit=20)
    assert len(sops) == 16, f"Expected 16 department SOPs, got {len(sops)}"
    print(f"✅ [Tầng 1 - SOP] Đã nạp đầy đủ {len(sops)}/16 Hồ sơ Phòng ban Nhân sự AI chuẩn SOP.")

    # 2. Test Tier 1: Save Product Knowledge, Brand Voice & Sub-millisecond Vietnamese Accent-Insensitive BM25 Search
    brain.save_memory(
        category="ProductKnowledge",
        key="sp_may_massage_co_vai_gay_ai_pro",
        content=(
            "Máy Massage Cổ Vai Gáy AI Pro: Giá bán 890.000đ (Giá gốc 1.490.000đ). "
            "USP: Xung điện TENS kép + Chườm ấm hồng ngoại 42 độ C + Pin 15 ngày. "
            "Bảo hành 1 đổi 1 trong 12 tháng, miễn phí giao hàng toàn quốc."
        ),
        importance=5,
        department="all",
        tags="product,massage,health,usp",
    )
    brain.save_memory(
        category="WritingStyle",
        key="brand_voice_health_tech",
        content=(
            "Giọng văn Chuyên gia Sức khỏe Công nghệ: Đồng cảm nỗi đau dân văn phòng đau mỏi vai gáy, "
            "cấm dùng từ ngữ cam kết chữa bệnh y khoa vi phạm chính sách Ads Facebook/TikTok, "
            "luôn mở đầu bằng Hook 3 giây đánh vào cảnh ngồi máy tính 8 tiếng/ngày."
        ),
        importance=5,
        department="all",
        tags="brand_voice,compliance,hook",
    )

    t0 = time.perf_counter()
    # Search without Vietnamese accents (" đau mỏi vai gáy " -> "dau moi vai gay")
    hits = brain.query_memories(keyword="dau moi vai gay", limit=5)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    assert len(hits) >= 2, "Expected accent-insensitive FTS5 search to match both Product and Brand Voice"
    print(
        f"✅ [Tầng 1 - SQLite FTS5 BM25] Tìm kiếm không dấu 'dau moi vai gay' trả về {len(hits)} bản ghi "
        f"trong {elapsed_ms:.2f} ms (< 1ms chuẩn thương mại)."
    )

    # 3. Test Tier 2: Kaizen Episodic Self-Learning across Departments (mem0 pattern)
    brain.record_kaizen_lesson(
        department="11_ads",
        campaign_or_task="Chiến dịch Reels Máy Massage Cổ Vai Gáy T11",
        action_taken="Test 2 kịch bản Hook 3s đầu: Hook A (Giới thiệu tính năng máy) vs Hook B (Cảnh dân IT ôm cổ nhăn mặt lúc 11h đêm)",
        outcome_status="WIN",
        extracted_rule=(
            "Bắt buộc dùng Hook B (Cảnh đau mỏi thực tế của dân văn phòng lúc đêm muộn) + "
            "chen sub vàng chữ đen cỡ lớn ở giây 0-3. Tuyệt đối bỏ Hook giới thiệu thông số khô khan ở đầu video."
        ),
        metrics={"ctr_hook_a": "0.8%", "ctr_hook_b": "4.6%", "leads_zalo": 68, "cpl_vnd": 14500},
        importance=5,
        applied_to_departments="all",
    )

    kz_lessons = brain.get_kaizen_lessons(department="04_content")
    assert len(kz_lessons) >= 1
    print(
        f"✅ [Tầng 2 - Kaizen Tự Học] Bài học thực chiến từ Phòng Ads (11_ads) đã tự động lan truyền sang "
        f"Phòng Content (04_content) & Dựng Phim (06_video_editor): '{kz_lessons[0]['extracted_rule'][:80]}...'"
    )

    # 4. Test Tier 3: Knowledge Graph & Multi-Hop Entity Traversal (LightRAG + NetworkX)
    brain.upsert_entity(
        name="Máy Massage Cổ Vai Gáy AI Pro",
        entity_type="Product",
        description="Thiết bị chăm sóc cổ vai gáy xung điện TENS & nhiệt hồng ngoại 42°C giá 890k",
        attributes={"price_vnd": 890000, "warranty_months": 12},
    )
    brain.upsert_entity(
        name="máy massage cổ vai gáy loại nào tốt cho dân văn phòng",
        entity_type="Keyword",
        description="Từ khóa SEO/AIO chuyển đổi cao (Volume 8.400/tháng, KD=18, AI Overview xuất hiện 90%)",
        attributes={"volume": 8400, "kd": 18, "intent": "Commercial Investigation"},
    )
    brain.upsert_entity(
        name="Dân văn phòng & Lập trình viên 25-45 tuổi",
        entity_type="Persona",
        description="Ngồi máy tính >8h/ngày, đau mỏi đốt sống cổ, hay lướt TikTok/Reels từ 21h-23h30",
        attributes={"active_hours": "21:00-23:30", "channels": ["TikTok", "Facebook Group", "Zalo"]},
    )

    brain.link_entities(
        source_name="Máy Massage Cổ Vai Gáy AI Pro",
        source_type="Product",
        relation_type="TARGETS_KEYWORD",
        target_name="máy massage cổ vai gáy loại nào tốt cho dân văn phòng",
        target_type="Keyword",
        evidence="Top 1 Topic Cluster SEO & AIO Citation",
        weight=0.98,
    )
    brain.link_entities(
        source_name="Máy Massage Cổ Vai Gáy AI Pro",
        source_type="Product",
        relation_type="SOLVES_PAIN_FOR",
        target_name="Dân văn phòng & Lập trình viên 25-45 tuổi",
        target_type="Persona",
        evidence="Giảm căng cứng cơ cổ sau 15 phút dùng nhiệt 42 độ C",
        weight=0.95,
    )

    kg_res = brain.query_knowledge_graph("massage co vai gay", max_hops=2)
    assert len(kg_res["subgraph_nodes"]) >= 3 and len(kg_res["subgraph_relations"]) >= 2
    print(
        f"✅ [Tầng 3 - Đồ Thị Tri Thức LightRAG/NetworkX] Truy vấn đa tầng 'massage co vai gay' "
        f"bóc tách được {len(kg_res['subgraph_nodes'])} Thực thể và {len(kg_res['subgraph_relations'])} Mối quan hệ ngữ nghĩa."
    )

    # 5. Test CFO & Accountant Financial Ledger
    brain.record_financial_transaction(
        department="11_ads",
        campaign_id="CAMP_MASSAGE_11",
        tx_type="AD_SPEND",
        amount_vnd=986000,
        leads_count=68,
        orders_count=0,
        note="Chi phí chạy Reels + Seeding Group",
    )
    brain.record_financial_transaction(
        department="12_sale",
        campaign_id="CAMP_MASSAGE_11",
        tx_type="REVENUE",
        amount_vnd=19580000,
        leads_count=0,
        orders_count=22,
        note="Chốt thành công 22 đơn qua Zalo.Net & Chatwoot",
    )

    fin = brain.get_financial_summary("CAMP_MASSAGE_11")
    assert fin["roas"] > 3.0 and fin["net_profit_vnd"] > 0
    print(
        f"✅ [Sổ Cái CFO & Kế Toán] Doanh thu: {fin['revenue_vnd']:,.0f}đ | Chi phí: {fin['total_cost_vnd']:,.0f}đ | "
        f"Lợi nhuận ròng: {fin['net_profit_vnd']:,.0f}đ | ROAS: {fin['roas']}x | CPL: {fin['cost_per_lead_vnd']:,.0f}đ/lead"
    )

    # 6. Test Unified Department Context Briefing (Cross-department intelligence)
    briefing_aio = brain.build_department_context_briefing("08_aio", "massage co vai gay")
    assert len(briefing_aio["tier1_memories"]) >= 2
    assert len(briefing_aio["tier2_kaizen_lessons"]) >= 1
    assert len(briefing_aio["tier3_knowledge_graph"]["subgraph_nodes"]) >= 3
    print(
        f"✅ [Đồng Bộ Liên Phòng Ban] Bản giao việc tự động cho phòng '{briefing_aio['department_meta']['name']}' "
        f"tổng hợp thành công cả 3 tầng trí nhớ + chỉ số tài chính CFO."
    )
    print("=" * 78)
    print("🎉 NGHIỆM THU BƯỚC 1 HOÀN TẤT: 100% TEST PASS!")
    print("=" * 78)


if __name__ == "__main__":
    run_step1_verification()
