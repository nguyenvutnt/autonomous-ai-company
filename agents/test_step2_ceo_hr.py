#!/usr/bin/env python3
"""
End-to-End Practical Verification & Kaizen Test Suite for Step 2:
Department #1 (CEO & Chief of Staff) & Department #15 (HR & Agent Kaizen Director).
"""

from __future__ import annotations

import sys
from pathlib import Path

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))
sys.path.insert(0, str(ECOSYSTEM_ROOT / "agents"))

from ceo_hr_orchestrator import CEOExecutiveAgent, HRAgentDirector
from engine import CorporateSecondBrain


def run_step2_verification() -> None:
    print("=" * 80)
    print("🚀 BẮT ĐẦU KIỂM THỬ THỰC TẾ BƯỚC 2: CEO (#1) & GIÁM ĐỐC NHÂN SỰ HR (#15)")
    print("=" * 80)

    brain = CorporateSecondBrain()
    hr = HRAgentDirector(brain)
    ceo = CEOExecutiveAgent(brain, hr)

    # 1. Test HR Talent Pool Scanner across 600+ profiles (`agency-agents` + `agency-agents-zh`)
    seo_candidates = hr.scan_talent_pool(keyword="seo", limit=10)
    video_candidates = hr.scan_talent_pool(keyword="video", limit=10)
    assert len(seo_candidates) >= 2 and len(video_candidates) >= 2
    print(
        f"✅ [HR #15 - Quét Kho Nhân Tài 600+ Hồ Sơ] Tìm thấy {len(seo_candidates)} chuyên gia SEO "
        f"(VD: '{seo_candidates[0]['name']}') & {len(video_candidates)} chuyên gia Video "
        f"(VD: '{video_candidates[0]['name']}')."
    )

    # 2. Test Recruiting & Binding Full 16-Department Roster with Active Kaizen Prompt Patching
    roster = hr.recruit_full_16_department_roster()
    assert len(roster) == 16
    print(
        f"✅ [HR #15 - Biên Chế 16 Phòng Ban] Đã tuyển dụng & kích hoạt {len(roster)}/16 Trưởng bộ phận AI "
        f"cùng vũ khí chuyên dụng và bản vá Kaizen tự động."
    )

    # 3. Test CEO Strategic Campaign Launch (Backward Unit Economics + 16 Work Orders)
    plan = ceo.launch_strategic_campaign(
        campaign_name="Chiến Dịch Đột Phá Doanh Thu Máy Massage Cổ Vai Gáy AI Pro T11",
        product_name="Máy Massage Cổ Vai Gáy AI Pro",
        product_price_vnd=890000,
        target_revenue_vnd=267000000,  # 267 triệu VNĐ (~300 đơn)
        duration_days=30,
        max_ad_budget_ratio=0.15,
        estimated_close_rate=0.25,
        target_audience="Dân văn phòng, lập trình viên, tài xế đau mỏi cổ vai gáy 25-45 tuổi",
    )

    ue = plan["unit_economics"]
    assert ue["orders_needed"] == 300
    assert ue["leads_needed"] == 1200
    assert len(plan["work_orders"]) == 16
    print(
        f"✅ [CEO #1 - Lập Kế Hoạch & Unit Economics] Mục tiêu {ue['target_revenue_vnd']:,.0f}đ -> "
        f"Cần {ue['orders_needed']} đơn ({ue['daily_orders_target']} đơn/ngày), "
        f"{ue['leads_needed']} leads ({ue['daily_leads_target']} leads/ngày), "
        f"Ngân sách tối đa {ue['max_budget_vnd']:,.0f}đ (ROAS >= {ue['target_roas']}x, CPL <= {ue['target_cpl_vnd']:,.0f}đ)."
    )
    print(
        f"✅ [CEO #1 - Giao Việc 16 Phòng Ban] Đã phát hành {plan['work_orders_count']} Work Orders "
        f"chia theo 6 Giai đoạn (Định mức: {ue['quotas']['seo_aio_articles']} bài SEO/AIO, "
        f"{ue['quotas']['short_videos_reels_tiktok']} video Shorts/TikTok, "
        f"{ue['quotas']['social_group_posts']} bài Social/Group, {ue['quotas']['livestream_hours_24_7']} giờ Livestream)."
    )

    # 4. Test HR KPI Evaluation & Automatic Kaizen Prompt Patching (WIN + LOSS simulation)
    eval_win = hr.evaluate_department_kpi_and_kaizen(
        department_id="06_video_editor",
        campaign_id=plan["campaign_id"],
        kpi_achieved={"short_videos_rendered": 105, "avg_hook_retention_target": 0.52},
        kpi_target={"short_videos_rendered": 90, "avg_hook_retention_target": 0.45},
        notes="Video dùng sub karaoke vàng đen + tốc độ đọc 1.15x giữ chân người xem 3s đầu đạt 52%.",
    )
    assert eval_win["outcome_status"] == "WIN" and eval_win["kpi_score"] > 100.0

    eval_loss = hr.evaluate_department_kpi_and_kaizen(
        department_id="11_ads",
        campaign_id=plan["campaign_id"],
        kpi_achieved={"leads_generated": 800, "max_cpl_vnd": 45000},
        kpi_target={"leads_generated": 1200, "max_cpl_vnd": 33375},
        notes="Nhóm quảng cáo ảnh tĩnh có CPL cao (45.000đ). Bắt buộc chuyển 100% ngân sách sang Reels Video Hook B.",
    )
    assert eval_loss["outcome_status"] == "LOSS" and eval_loss["kpi_score"] < 95.0

    print(
        f"✅ [HR #15 - Đánh Giá KPI & Tự Động Vá Prompt Kaizen]\n"
        f"   • Phòng Dựng Phim (06_video_editor): Điểm KPI = {eval_win['kpi_score']}% [{eval_win['outcome_status']}]\n"
        f"   • Phòng Ads (11_ads): Điểm KPI = {eval_loss['kpi_score']}% [{eval_loss['outcome_status']}] -> Đã tự động ghi luật chấn chỉnh vào System Prompt."
    )

    # 5. Test Executive Board Report
    board = ceo.get_executive_board_report(plan["campaign_id"])
    assert len(board["hr_roster_health"]) == 16
    assert len(board["active_work_orders"]) == 16
    print(
        f"✅ [Báo Cáo Giao Ban CEO + HR + CFO] Tổng hợp thời gian thực 16 phòng ban, "
        f"{len(board['active_work_orders'])} lệnh sản xuất & {len(board['latest_kaizen_lessons'])} luật Kaizen thực chiến."
    )
    print("=" * 80)
    print("🎉 NGHIỆM THU BƯỚC 2 HOÀN TẤT: 100% TEST PASS!")
    print("=" * 80)


if __name__ == "__main__":
    run_step2_verification()
