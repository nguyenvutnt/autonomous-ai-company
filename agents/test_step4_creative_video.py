#!/usr/bin/env python3
"""
End-to-End Practical Verification & Kaizen Test Suite for Step 4:
Creative Director (#2), Design (#3), Content (#4), Media (#5), and Video Editor (#6).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))
sys.path.insert(0, str(ECOSYSTEM_ROOT / "agents"))

from creative_video_division import CreativeVideoStudioDivision
from engine import CorporateSecondBrain


def run_step4_verification() -> None:
    print("=" * 84)
    print("🚀 BẮT ĐẦU KIỂM THỬ THỰC TẾ BƯỚC 4: KHỐI SÁNG TẠO, ĐỒ HỌA, MEDIA & DỰNG PHIM (#2..#6)")
    print("=" * 84)

    brain = CorporateSecondBrain()
    studio = CreativeVideoStudioDivision(brain)

    bundle = studio.produce_full_campaign_creative_bundle(
        campaign_id="CAMP_MASSAGE_11",
        product_name="Máy Massage Cổ Vai Gáy AI Pro",
        price_vnd=890000,
        usp_highlights=[
            "Xung điện TENS kép tác động sâu",
            "Chườm ấm hồng ngoại chuẩn 42°C",
            "Pin 15 ngày - Bảo hành 1 đổi 1 trong 12 tháng",
        ],
        target_persona="Dân văn phòng & Lập trình viên ngồi máy tính 8 tiếng/ngày",
        spintax_count=200,
    )

    # 1. Verify Creative Director (#2)
    approval = bundle["creative_approval"]
    assert approval["approved"] is True
    print(
        f"✅ [Creative Director #2 - Duyệt Hook 3s & Tuân Thủ Chính Sách]:\n"
        f"   • Hook 3s được duyệt: '{approval['approved_hook_3s']}'\n"
        f"   • Luật Kaizen áp dụng: '{approval['enforced_kaizen_rule'][:85]}...'"
    )

    # 2. Verify Content Copywriter (#4) Spintax 200x
    spintax = bundle["spintax_summary"]
    assert spintax["total_unique_generated"] == 200
    print(
        f"✅ [Content #4 - Kịch Bản & Spintax 200x]: Đã sinh {spintax['total_unique_generated']} bản nội dung quảng cáo/rải nhóm độc nhất 100% chống spam."
    )

    # 3. Verify Design Studio (#3) WebP Banner
    webp = bundle["studio_banner_webp"]
    assert Path(webp["file_path"]).exists() and webp["size_bytes"] > 5000
    print(
        f"✅ [Design #3 - Ảnh Sản Phẩm Studio WebP]: Đã xuất '{webp['file_path']}' "
        f"({webp['resolution']}, {webp['size_bytes']:,} bytes)."
    )

    # 4. Verify Media (#5) Vietnamese Neural TTS Audio
    audio = bundle["voiceover_audio"]
    assert Path(audio["audio_path"]).exists() and audio["size_bytes"] > 5000
    print(
        f"✅ [Media #5 - Lồng Tiếng AI Tiếng Việt ({audio['engine_used']})]: "
        f"Đã xuất '{audio['audio_path']}' (Giọng: {audio['voice']}, Thời lượng: {audio['duration_sec']}s, {audio['size_bytes']:,} bytes)."
    )

    # 5. Verify Video Editor (#6) Final 9:16 MP4 + SRT + MD5 Fingerprint
    video = bundle["short_video_mp4"]
    assert Path(video["video_mp4_path"]).exists() and video["size_bytes"] > 20000
    assert Path(video["subtitle_srt_path"]).exists()
    print(
        f"✅ [Dựng Phim #6 - Xuất Video Shorts/Reels/TikTok 9:16 MP4]:\n"
        f"   • File MP4: '{video['video_mp4_path']}' ({video['resolution']}, {video['fps']}fps, {video['duration_sec']}s, {video['size_bytes']:,} bytes)\n"
        f"   • Phụ đề SRT: '{video['subtitle_srt_path']}'\n"
        f"   • Mã băm chống quét trùng lặp (MD5): {video['md5_fingerprint']}"
    )

    print("=" * 84)
    print("🎉 NGHIỆM THU BƯỚC 4 HOÀN TẤT: 100% TEST PASS!")
    print("=" * 84)


if __name__ == "__main__":
    run_step4_verification()
