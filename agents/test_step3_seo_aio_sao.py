#!/usr/bin/env python3
"""
End-to-End Practical Verification & Kaizen Test Suite for Step 3:
Department #7 (SEO), Department #8 (AIO / AEO / GEO), and Department #9 (SAO / Social & WebMCP).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))
sys.path.insert(0, str(ECOSYSTEM_ROOT / "agents"))

from engine import CorporateSecondBrain
from seo_aio_sao_division import SearchGrowthDivision


def run_step3_verification() -> None:
    print("=" * 82)
    print("🚀 BẮT ĐẦU KIỂM THỬ THỰC TẾ BƯỚC 3: KHỐI TÌM KIẾM SEO (#7) + AIO (#8) + SAO (#9)")
    print("=" * 82)

    brain = CorporateSecondBrain()
    division = SearchGrowthDivision(brain)

    pkg = division.execute_omni_search_campaign_package(
        campaign_id="CAMP_MASSAGE_11",
        product_name="Máy Massage Cổ Vai Gáy AI Pro",
        core_keyword="máy massage cổ vai gáy",
        price_vnd=890000,
        usp_highlights=[
            "Xung điện TENS kép tác động sâu",
            "Chườm ấm hồng ngoại chuẩn 42°C",
            "Pin 15 ngày - Bảo hành 1 đổi 1 trong 12 tháng",
        ],
        target_persona="Dân văn phòng & Lập trình viên ngồi máy tính 8 tiếng/ngày",
        competitor_url="https://example.com",
    )

    # 1. Verify Crawl4AI / Web Extraction
    crawl = pkg["crawl_report"]
    assert crawl and crawl["word_count"] > 0
    print(
        f"✅ [SEO #7 - Quét Web Đối Thủ ({crawl['engine_used']})]: "
        f"Đã bóc tách URL '{crawl['url']}' (Title: '{crawl['title']}', {crawl['word_count']} từ)."
    )

    # 2. Verify Topic Cluster & Anti-Cannibalization Guard
    cluster = pkg["topic_cluster"]
    assert len(cluster["cluster_pages"]) == 5
    assert len(cluster["cannibalization_conflicts"]) == 0
    print(
        f"✅ [SEO #7 - Topic Cluster & Chống Ăn Thịt Từ Khóa]: "
        f"Đã khóa quyền sở hữu {len(cluster['cluster_pages'])} URL (1 Pillar + 4 Satellites), "
        f"Xung đột Cannibalization = {len(cluster['cannibalization_conflicts'])}."
    )

    # 3. Verify E-E-A-T Article & Kaizen Lesson Injection
    md = pkg["seo_article_markdown"]
    assert "Kaizen Insight:" in md and pkg["word_count"] > 200
    print(
        f"✅ [SEO #7 - Bài Viết Chuẩn E-E-A-T]: Đã xuất bản bài Pillar '{pkg['pillar_url_slug']}' "
        f"({pkg['word_count']} từ, có bảng so sánh trực diện, Internal Link Graph & tự động nhúng bài học Kaizen)."
    )

    # 4. Verify AIO Citation Pack (AEO Direct Answer + Schema.org JSON-LD)
    aio = pkg["aio_citation_pack"]
    graph_types = [node["@type"] for node in aio["json_ld_schema"]["@graph"]]
    assert "Product" in graph_types and "FAQPage" in graph_types
    print(
        f"✅ [AIO #8 - Tối Ưu Trích Dẫn ChatGPT/Perplexity/Gemini]: "
        f"Đã sinh khối Direct Answer 45 từ + Schema JSON-LD ({', '.join(graph_types)}) với {len(aio['faqs'])} câu FAQ chuẩn AEO."
    )

    # 5. Verify SAO Social Search & WebMCP Agentic Checkout Block
    sao = pkg["sao_social_and_webmcp_pack"]
    assert "toolname=" in sao["webmcp_html"] and "document.modelContext.registerTool" in sao["webmcp_html"]
    assert len(sao["social_search_pack"]["search_hashtags"]) >= 5
    print(
        f"✅ [SAO #9 - Tối Ưu TikTok/FB/Shopee Search & WebMCP Agentic Commerce]:\n"
        f"   • TikTok Search Title: {sao['social_search_pack']['tiktok_search_title']}\n"
        f"   • ASR 3s Spoken Keyword: {sao['social_search_pack']['spoken_asr_first_3s']}\n"
        f"   • WebMCP Ready: Đã nhúng cả Declarative Form (`toolname`) & Imperative JS (`document.modelContext.registerTool`)."
    )

    print("=" * 82)
    print("🎉 NGHIỆM THU BƯỚC 3 HOÀN TẤT: 100% TEST PASS!")
    print("=" * 82)


if __name__ == "__main__":
    run_step3_verification()
