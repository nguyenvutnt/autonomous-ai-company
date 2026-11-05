#!/usr/bin/env python3
"""
MCP Server for the 3-Tier Corporate Second Brain (`corporate-second-brain`).
Exposes Tier 1 (SQLite FTS5 BM25), Tier 2 (Kaizen Episodic Learning),
Tier 3 (Entity Knowledge Graph), and CFO Financial Ledger to all AI Agents & CLIs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agents"))

from mcp.server.fastmcp import FastMCP
from engine import (
    CORPORATE_DEPARTMENTS,
    MEMORY_CATEGORIES,
    CorporateSecondBrain,
)
from ceo_hr_orchestrator import CEOExecutiveAgent, HRAgentDirector
from seo_aio_sao_division import SearchGrowthDivision

mcp = FastMCP("corporate-second-brain")
brain = CorporateSecondBrain()
hr_director = HRAgentDirector(brain)
ceo_agent = CEOExecutiveAgent(brain, hr_director)
search_division = SearchGrowthDivision(brain)


@mcp.tool()
def brain_list_departments() -> str:
    """Liệt kê toàn bộ 16 phòng ban nhân sự AI, chức năng SOP và vũ khí điều khiển."""
    return json.dumps(CORPORATE_DEPARTMENTS, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_save_memory(
    category: str,
    key: str,
    content: str,
    importance: int = 3,
    department: str = "all",
    tags: str = "",
) -> str:
    """
    Lưu kiến thức dài hạn vào Tầng 1 (SQLite FTS5 BM25) của Bộ Não Thứ 2 Toàn Công Ty.
    Categories hợp lệ: General, UserPreference, ProductKnowledge, WritingStyle,
    CampaignRule, GroupStrategy, LeadPlaybook, DepartmentSop, KaizenLesson,
    EntityGraph, FinanceLedger, MediaAssetVault.
    """
    res = brain.save_memory(
        category=category,
        key=key,
        content=content,
        importance=importance,
        department=department,
        tags=tags,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_query_memories(
    keyword: str = "",
    category: str = "",
    department: str = "",
    limit: int = 20,
) -> str:
    """Truy vấn siêu tốc (<1ms) kiến thức Tầng 1 theo từ khóa (hỗ trợ tiếng Việt không dấu), danh mục và phòng ban."""
    res = brain.query_memories(
        keyword=keyword or None,
        category=category or None,
        department=department or None,
        limit=limit,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_record_kaizen(
    department: str,
    campaign_or_task: str,
    action_taken: str,
    outcome_status: str,
    extracted_rule: str,
    metrics_json: str = "{}",
    importance: int = 5,
    applied_to_departments: str = "all",
) -> str:
    """
    Ghi nhận bài học thực chiến Kaizen vào Tầng 2 (WIN / LOSS / INSIGHT) sau mỗi chiến dịch
    và tự động đồng bộ quy tắc mới sang các phòng ban liên quan.
    """
    try:
        metrics: dict[str, Any] = json.loads(metrics_json) if metrics_json else {}
    except Exception:
        metrics = {"raw": metrics_json}

    res = brain.record_kaizen_lesson(
        department=department,
        campaign_or_task=campaign_or_task,
        action_taken=action_taken,
        outcome_status=outcome_status,
        extracted_rule=extracted_rule,
        metrics=metrics,
        importance=importance,
        applied_to_departments=applied_to_departments,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_get_kaizen_lessons(
    department: str = "",
    outcome_status: str = "",
    limit: int = 20,
) -> str:
    """Lấy danh sách các bài học Kaizen (thắng/thua/kinh nghiệm thực chiến) cho phòng ban."""
    res = brain.get_kaizen_lessons(
        department=department or None,
        outcome_status=outcome_status or None,
        limit=limit,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_upsert_entity(
    name: str,
    entity_type: str,
    description: str,
    attributes_json: str = "{}",
    department: str = "all",
) -> str:
    """
    Thêm hoặc cập nhật Thực thể (Product, Keyword, Competitor, Persona, Channel, Hook)
    vào Tầng 3 (Đồ thị Tri thức LightRAG/NetworkX) phục vụ SEO/AIO/SAO & Creative.
    """
    try:
        attrs = json.loads(attributes_json) if attributes_json else {}
    except Exception:
        attrs = {"raw": attributes_json}

    res = brain.upsert_entity(
        name=name,
        entity_type=entity_type,
        description=description,
        attributes=attrs,
        department=department,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_link_entities(
    source_name: str,
    source_type: str,
    relation_type: str,
    target_name: str,
    target_type: str,
    evidence: str = "",
    weight: float = 1.0,
) -> str:
    """Liên kết 2 Thực thể trong Đồ thị Tri thức Tầng 3 (VD: Product -> TARGETS_KEYWORD -> Keyword)."""
    res = brain.link_entities(
        source_name=source_name,
        source_type=source_type,
        relation_type=relation_type,
        target_name=target_name,
        target_type=target_type,
        evidence=evidence,
        weight=weight,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_query_knowledge_graph(query_term: str, max_hops: int = 2) -> str:
    """Truy vấn đa tầng (Multi-hop Subgraph) trên Đồ thị Tri thức Tầng 3 quanh một chủ đề/sản phẩm."""
    res = brain.query_knowledge_graph(query_term=query_term, max_hops=max_hops)
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_record_finance(
    department: str,
    campaign_id: str,
    tx_type: str,
    amount_vnd: float,
    leads_count: int = 0,
    orders_count: int = 0,
    note: str = "",
) -> str:
    """Ghi sổ cái tài chính (REVENUE, AD_SPEND, PROXY_COST, TOOL_COST, REFUND) cho CFO & Kế toán."""
    res = brain.record_financial_transaction(
        department=department,
        campaign_id=campaign_id,
        tx_type=tx_type,
        amount_vnd=amount_vnd,
        leads_count=leads_count,
        orders_count=orders_count,
        note=note,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def brain_get_department_briefing(
    department_id: str,
    topic_or_product: str = "",
) -> str:
    """
    Tổng hợp Bản Giao Việc & Ngữ Cảnh Hợp Nhất 3 Tầng (SOP + Kiến thức SP + Luật Kaizen +
    Sơ đồ Thực thể + Chỉ số ROAS) cho bất kỳ phòng ban nào trong 16 phòng ban.
    """
    res = brain.build_department_context_briefing(
        department_id=department_id,
        topic_or_product=topic_or_product or None,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def ceo_launch_campaign(
    campaign_name: str,
    product_name: str,
    product_price_vnd: float,
    target_revenue_vnd: float,
    duration_days: int = 30,
    max_ad_budget_ratio: float = 0.15,
    estimated_close_rate: float = 0.25,
    target_audience: str = "Khách hàng mục tiêu trên Facebook, Zalo, TikTok & Google",
) -> str:
    """
    [CEO #1] Nhận mục tiêu doanh thu từ Founder -> Tự động tính toán Unit Economics ngược
    (Số đơn, Số Lead, Ngân sách tối đa, ROAS mục tiêu, Định mức bài SEO/Video/Social/Livestream)
    và phát lệnh giao việc (16 Work Orders) xuống toàn bộ 16 phòng ban.
    """
    res = ceo_agent.launch_strategic_campaign(
        campaign_name=campaign_name,
        product_name=product_name,
        product_price_vnd=product_price_vnd,
        target_revenue_vnd=target_revenue_vnd,
        duration_days=duration_days,
        max_ad_budget_ratio=max_ad_budget_ratio,
        estimated_close_rate=estimated_close_rate,
        target_audience=target_audience,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def ceo_board_report(campaign_id: str = "") -> str:
    """
    [CEO #1 + CFO #13 + HR #15] Xuất Báo cáo Giao ban Ban Giám Đốc theo thời gian thực:
    Tổng hợp Doanh thu/ROAS, Bảng điểm KPI 16 phòng ban, Danh sách 16 Work Orders và Luật Kaizen mới nhất.
    """
    res = ceo_agent.get_executive_board_report(campaign_id=campaign_id or None)
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def hr_scan_talent_pool(keyword: str = "", limit: int = 25) -> str:
    """
    [HR #15] Quét kho 600+ hồ sơ chuyên gia AI (`agency-agents` & `agency-agents-zh`)
    theo từ khóa chuyên môn để tuyển dụng hoặc bổ sung kỹ năng cho phòng ban.
    """
    res = hr_director.scan_talent_pool(keyword=keyword or None, limit=limit)
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def hr_evaluate_department_kpi(
    department_id: str,
    campaign_id: str,
    kpi_achieved_json: str,
    kpi_target_json: str,
    notes: str = "",
) -> str:
    """
    [HR #15] Chấm điểm KPI thực tế của phòng ban so với mục tiêu CEO giao,
    tự động rút ra bài học Kaizen (WIN/LOSS) và vá trực tiếp vào System Prompt của Agent.
    """
    achieved = json.loads(kpi_achieved_json) if kpi_achieved_json else {}
    target = json.loads(kpi_target_json) if kpi_target_json else {}
    res = hr_director.evaluate_department_kpi_and_kaizen(
        department_id=department_id,
        campaign_id=campaign_id,
        kpi_achieved=achieved,
        kpi_target=target,
        notes=notes,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def seo_crawl_url(url: str) -> str:
    """
    [SEO #7] Quét và bóc tách nội dung đối thủ từ một URL bất kỳ bằng Crawl4AI
    và tự động lưu vào Bộ Não Thứ 2.
    """
    res = search_division.seo.crawl_competitor_url(url=url)
    return json.dumps(res, ensure_ascii=False, indent=2)


@mcp.tool()
def search_generate_omni_package(
    campaign_id: str,
    product_name: str,
    core_keyword: str,
    price_vnd: float,
    usp_list_json: str,
    target_persona: str,
    competitor_url: str = "",
) -> str:
    """
    [SEO #7 + AIO #8 + SAO #9] Tự động chạy trọn bộ:
    1. Kiểm tra chống ăn thịt từ khóa (Anti-Cannibalization) & lập Topic Cluster 5 bài.
    2. Viết bài chuẩn E-E-A-T kèm bảng so sánh & Internal Link Graph.
    3. Xuất Schema JSON-LD (`Product` + `FAQPage`) để ChatGPT/Perplexity/Google AI Overview trích dẫn.
    4. Xuất bộ từ khóa tìm kiếm TikTok/FB/Shopee Search + mã HTML/JS chuẩn WebMCP cho AI Shopping Agents.
    """
    try:
        usps = json.loads(usp_list_json) if usp_list_json else []
    except Exception:
        usps = [u.strip() for u in usp_list_json.split(",") if u.strip()]

    res = search_division.execute_omni_search_campaign_package(
        campaign_id=campaign_id,
        product_name=product_name,
        core_keyword=core_keyword,
        price_vnd=price_vnd,
        usp_highlights=usps,
        target_persona=target_persona,
        competitor_url=competitor_url or None,
    )
    return json.dumps(res, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
