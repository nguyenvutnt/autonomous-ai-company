#!/usr/bin/env python3
"""
End-to-End Practical Verification & Kaizen Test Suite for Step 5:
Social Distribution (#10), Ads & Viral Seeding (#11), and Sale Lead Closer (#12).
"""

from __future__ import annotations

import sys
from pathlib import Path

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))
sys.path.insert(0, str(ECOSYSTEM_ROOT / "agents"))

from creative_video_division import ContentCopywriterAgent
from engine import CorporateSecondBrain
from social_ads_sale_division import SocialAdsSaleDivision


def run_step5_verification() -> None:
    print("=" * 86)
    print("🚀 BẮT ĐẦU KIỂM THỬ THỰC TẾ BƯỚC 5: SOCIAL (#10) + ADS SEEDING (#11) + SALE (#12)")
    print("=" * 86)

    brain = CorporateSecondBrain()
    copywriter = ContentCopywriterAgent(brain)
    division = SocialAdsSaleDivision(brain)

    spintax_list = copywriter.generate_spintax_variations(
        product_name="Máy Massage Cổ Vai Gáy AI Pro",
        price_vnd=890000,
        usp_highlights=["Xung điện TENS kép", "Chườm ấm hồng ngoại 42°C"],
        count=50,
    )["all_variations"]

    target_groups = [
        "Hội Dân Văn Phòng Hà Nội - TP.HCM",
        "Cộng Đồng Lập Trình Viên Việt Nam (IT Dev)",
        "Hội Kế Toán Trưởng & Tài Chính Doanh Nghiệp",
        "Review Thiết Bị Chăm Sóc Sức Khỏe Thông Minh",
        "Chợ Săn Sale Đồ Công Nghệ Chính Hãng",
        "Hội Tài Xế Công Nghệ Đường Dài",
        "Cộng Đồng Freelancer & Làm Việc Tại Nhà",
        "Hội Chị Em Văn Phòng Sành Điệu",
    ]

    ad_sets = [
        {
            "adset_id": "ADS_REELS_HOOK_B_01",
            "name": "Reels 9:16 - Hook Cảnh Dân IT Đau Mỏi Lúc 11h Đêm",
            "spend_vnd": 650000,
            "leads": 32,
            "ctr_percent": 4.8,
        },
        {
            "adset_id": "ADS_STATIC_IMG_02",
            "name": "Ảnh Tĩnh Thông Số Kỹ Thuật Cũ",
            "spend_vnd": 420000,
            "leads": 7,
            "ctr_percent": 0.9,
        },
    ]

    raw_comments = [
        {
            "channel": "Facebook Reels",
            "uid": "100055112233",
            "author_name": "Nguyễn Minh Tuấn",
            "comment": "Mình ngồi code mỏi cổ quá, chốt cho mình 1 máy tới Cầu Giấy nhé, sđt 098.765.4321",
        },
        {
            "channel": "TikTok Live",
            "uid": "tiktok_user_889",
            "author_name": "Trần Thu Hà",
            "comment": "Shop ơi đặt 2 chiếc tặng bố mẹ có được freeship không? Gọi mình số O912 345 678 nha",
        },
        {
            "channel": "Facebook Group",
            "uid": "100099887766",
            "author_name": "Lê Hoàng Nam",
            "comment": "Tư vấn kỹ giúp mình chế độ bảo hành 1 đổi 1 qua zalo +84 903 112 233 và mail nam.le@techcorp.vn",
        },
        {
            "channel": "Youtube Shorts",
            "uid": "yt_viewer_04",
            "author_name": "Phạm Hương",
            "comment": "Mua ngay 1 máy giao về Quận 1 TPHCM, số điện thoại 0977-888-999",
        },
        {
            "channel": "Facebook Page",
            "uid": "100011122233",
            "author_name": "Viewer Vãng Lai",
            "comment": "Video hay quá shop ơi!",
        },
    ]

    video_mp4 = "/root/ecosystem/second-brain/data/media_vault/short_may-massage-co-vai-gay-ai-pro_final.mp4"

    report = division.execute_full_distribution_ads_and_sale_cycle(
        campaign_id="CAMP_MASSAGE_11",
        product_name="Máy Massage Cổ Vai Gáy AI Pro",
        price_vnd=890000,
        max_cpl_vnd=33375,
        video_mp4_path=video_mp4,
        spintax_variations=spintax_list,
        target_groups=target_groups,
        ad_sets=ad_sets,
        raw_comments=raw_comments,
    )

    # 1. Verify Camoufox Anti-Detect Farm & Multi-Channel Dispatch (#10)
    assert report["camoufox_profiles_active"] == 10
    dsp = report["social_dispatch_report"]
    assert dsp["platforms_covered"] == 12 and dsp["facebook_groups_posted"] == 8
    print(
        f"✅ [Social #10 - Camoufox Anti-Detect & Rải Bài Đa Kênh]:\n"
        f"   • Đã cấp phát {report['camoufox_profiles_active']} Profile Camoufox độc lập (Canvas/WebGL/Proxy riêng chống Checkpoint).\n"
        f"   • Đã phân phối {dsp['total_dispatched']} bài viết Spintax độc nhất lên {dsp['platforms_covered']} Mạng xã hội & {dsp['facebook_groups_posted']} Group Facebook."
    )

    # 2. Verify 24/7 Livestream Re-streamer Config (#10)
    live = report["livestream_24_7_config"]
    assert len(live["concurrent_restream_targets"]) == 5
    print(
        f"✅ [Social #10 - Livestream & Re-stream 24/7 (MediaMTX + FFmpeg)]:\n"
        f"   • Nguồn phát: '{live['source_video']}' -> Nhân bản đồng thời ra {len(live['concurrent_restream_targets'])} kênh (FB, TikTok, YT, Shopee, Lazada)."
    )

    # 3. Verify Ads CPL Guardrail & Viral Seeding (#11)
    ads_rep = report["ads_and_seeding_report"]
    actions = {d["adset_id"]: d["action_taken"] for d in ads_rep["adset_decisions"]}
    assert actions["ADS_REELS_HOOK_B_01"] == "SCALE_BUDGET_2X"
    assert actions["ADS_STATIC_IMG_02"] == "AUTO_PAUSE_ADSET"
    print(
        f"✅ [Ads #11 - Tự Động Tối Ưu Ngân Sách & Seeding Chéo]:\n"
        f"   • Nhóm '{ad_sets[0]['name']}': CPL = 20,312đ <= Trần 33,375đ -> Lệnh: {actions['ADS_REELS_HOOK_B_01']}\n"
        f"   • Nhóm '{ad_sets[1]['name']}': CPL = 60,000đ > Trần 33,375đ -> Lệnh: {actions['ADS_STATIC_IMG_02']}\n"
        f"   • Đã kích hoạt {len(ads_rep['viral_seeding_actions'])} luồng Seeding & Auto Up Tin hội nhóm."
    )

    # 4. Verify Sale Lead Mining (Obfuscated VN Phones) & Zalo.Net / Chatwoot / Twenty CRM Auto-Closing (#12)
    sale_rep = report["sale_lead_and_closing_report"]
    tw_crm = sale_rep["twenty_crm_sync"]
    assert sale_rep["hot_leads_extracted"] == 4
    assert sale_rep["orders_closed"] == 4
    assert sale_rep["revenue_generated_vnd"] == 4 * 890000
    assert tw_crm["total_people_in_crm"] >= 4
    assert tw_crm["campaign_opportunities_won"] >= 4
    assert tw_crm["campaign_tasks_dispatched"] >= 4
    phones = [l["phone_normalized"] for l in sale_rep["leads"]]
    assert "0987654321" in phones and "0912345678" in phones and "0903112233" in phones
    print(
        f"✅ [Sale #12 - Quét SĐT Ẩn/Lách Luật & Chốt Đơn Tự Động (Zalo.Net + Chatwoot + Twenty CRM)]:\n"
        f"   • Quét {sale_rep['comments_scanned']} bình luận -> Bóc tách chuẩn xác {sale_rep['hot_leads_extracted']} SĐT/Email nóng: {phones}\n"
        f"   • Tự động gửi tin nhắn Zalo.Net & đồng bộ Chatwoot -> Chốt thành công {sale_rep['orders_closed']} đơn ({sale_rep['revenue_generated_vnd']:,.0f} VNĐ).\n"
        f"   • Twenty CRM Native Sync: {tw_crm['total_people_in_crm']} People | {tw_crm['campaign_opportunities_won']} Opportunities ({tw_crm['kanban_stage']}) | {tw_crm['campaign_tasks_dispatched']} Follow-up Tasks."
    )

    fin = report["updated_cfo_summary"]
    print(
        f"✅ [Đồng Bộ Sổ Cái CFO Thời Gian Thực]: Tổng doanh thu lũy kế = {fin['revenue_vnd']:,.0f}đ | "
        f"Tổng chi phí Ads = {fin['total_cost_vnd']:,.0f}đ | Lợi nhuận ròng = {fin['net_profit_vnd']:,.0f}đ (ROAS = {fin['roas']}x)."
    )

    print("=" * 86)
    print("🎉 NGHIỆM THU BƯỚC 5 HOÀN TẤT: 100% TEST PASS!")
    print("=" * 86)


if __name__ == "__main__":
    run_step5_verification()
