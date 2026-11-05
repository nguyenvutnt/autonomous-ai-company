#!/usr/bin/env python3
"""
End-to-End Practical Verification & Kaizen Test Suite for Step 6:
CFO (#13), Accountant & Simple Replay Video Audit (#14), IT/DevOps (#16),
and Complete 16-Department Closed-Loop Master Pipeline (`n8n` Workflow Export).
"""

from __future__ import annotations

import sys
from pathlib import Path

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "second-brain"))
sys.path.insert(0, str(ECOSYSTEM_ROOT / "agents"))

from engine import CorporateSecondBrain
from finance_it_pipeline_division import FinanceITAndMasterPipelineDivision


def run_step6_verification() -> None:
    print("=" * 88)
    print("🚀 BẮT ĐẦU KIỂM THỬ THỰC TẾ BƯỚC 6: CFO (#13) + KẾ TOÁN (#14) + IT (#16) & KHÉP KÍN 16 PHÒNG")
    print("=" * 88)

    brain = CorporateSecondBrain()
    division = FinanceITAndMasterPipelineDivision(brain)

    res = division.execute_step6_and_close_all_16_work_orders(
        campaign_id="CAMP_MASSAGE_11",
        product_name="Máy Massage Cổ Vai Gáy AI Pro",
        unit_cogs_vnd=290000.0,
    )

    # 1. Verify CFO (#13) P&L Statement & Capital Allocation Directive
    pnl = res["cfo_pnl_report"]
    assert pnl["gross_revenue_vnd"] > 0 and pnl["net_operating_profit_vnd"] > 0
    assert pnl["cfo_directive"] == "APPROVE_SCALE_UP_30_PERCENT"
    print(
        f"✅ [CFO #13 - Báo Cáo Lãi/Lỗ P&L & Quyết Định Ngân Sách]:\n"
        f"   • Doanh thu gộp: {pnl['gross_revenue_vnd']:,.0f}đ ({pnl['total_orders']} đơn) | Giá vốn (COGS): {pnl['cogs_total_vnd']:,.0f}đ\n"
        f"   • Phí sàn & vận chuyển: {pnl['platform_and_shipping_fees_vnd']:,.0f}đ | Thuế dự phòng: {pnl['tax_reserve_vnd']:,.0f}đ | Chi phí Ads: {pnl['ad_and_operating_spend_vnd']:,.0f}đ\n"
        f"   • Lợi nhuận ròng sau thuế & giá vốn: {pnl['net_operating_profit_vnd']:,.0f}đ (Biên lãi ròng: {pnl['net_margin_percent']}%, ROAS: {pnl['actual_roas']}x)\n"
        f"   • Lệnh của CFO: {pnl['cfo_directive']}"
    )

    # 2. Verify Accountant (#14) Vouchers & Simple Replay Packing Proof MP4
    acc = res["accountant_reconciliation"]
    assert acc["reconciled_orders_count"] >= 4
    sample_vch = acc["vouchers"][0]
    assert Path(sample_vch["packing_video_path"]).exists()
    print(
        f"✅ [Kế Toán #14 - Hạch Toán Chứng Từ & Video Đóng Gói Simple Replay]:\n"
        f"   • Đã lập chứng từ & xuất {acc['reconciled_orders_count']} Video bằng chứng đóng gói (.mp4).\n"
        f"   • Mẫu đơn #{sample_vch['order_code']} ({sample_vch['customer_name']} - {sample_vch['customer_phone']}): "
        f"'{sample_vch['packing_video_path']}' (SHA-256: {sample_vch['packing_video_sha256'][:24]}...)"
    )

    # 3. Verify IT/DevOps (#16) Infrastructure Audit, 26 Submodules & 2FA TOTP
    it = res["it_infrastructure_audit"]
    assert it["status"] == "HEALTHY_100_PERCENT"
    assert it["submodules_registered"] == 26
    assert it["totp_2fa_engine_verified"] is True
    print(
        f"✅ [IT/DevOps #16 - Giám Sát Hạ Tầng & Bảo Mật 2FA]:\n"
        f"   • Trạng thái: {it['status']} | Submodules đã kết nối: {it['submodules_registered']}/26\n"
        f"   • MCP Binaries: zalo-mcp={it['mcp_binaries']['zalo_mcp']}, second-brain-mcp={it['mcp_binaries']['second_brain_mcp']}\n"
        f"   • Bộ sinh mã 2FA TOTP (RFC 6238): OK (Mã mẫu: {it['sample_2fa_code']})"
    )

    # 4. Verify n8n Workflow Export & All 16 Departments Completed
    n8n = res["n8n_workflow_export"]
    assert Path(n8n["workflow_path"]).exists() and n8n["nodes_count"] == 6
    assert res["departments_completed_count"] == 16
    print(
        f"✅ [Chuỗi Tự Động Hóa Khép Kín n8n & Nghiệm Thu 16/16 Phòng Ban]:\n"
        f"   • Đã xuất file n8n Workflow: '{n8n['workflow_path']}' ({n8n['nodes_count']} nodes, {n8n['size_bytes']:,} bytes)\n"
        f"   • Tổng số Phòng Ban hoàn thành Work Order: {res['departments_completed_count']}/16 Phòng Ban!"
    )

    print("=" * 88)
    print("🎉 NGHIỆM THU BƯỚC 6 & TOÀN BỘ 16 PHÒNG BAN HOÀN TẤT: 100% TEST PASS!")
    print("=" * 88)


if __name__ == "__main__":
    run_step6_verification()
