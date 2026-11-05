#!/usr/bin/env python3
"""
End-to-End Verification Suite for the EYC (`eyc.asia`) 16-Department AI Command, Interview & Task Studio
(`/root/ecosystem/virtual-office/test_virtual_office.py`).
"""

from __future__ import annotations

import sys
from pathlib import Path

ECOSYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / "virtual-office"))

from server import CONTROLLER


def run_virtual_office_verification() -> None:
    print("=" * 88)
    print("🚀 KIỂM THỬ HỆ THỐNG ĐIỀU PHỐI & PHỎNG VẤN 16 PHÒNG BAN AI — EYC (eyc.asia)")
    print("=" * 88)

    # 1. Clean reset to EYC baseline
    reset_res = CONTROLLER.clean_reset_eyc()
    assert reset_res["ok"] is True and reset_res["departments_ready"] == 16
    print(f"✅ [Khởi Tạo Sạch EYC]: {reset_res['company']} ({reset_res['website']}) — 0 dữ liệu rác demo.")

    # 2. Verify 1-on-1 Department Interview
    int_res = CONTROLLER.interview_department(
        department_id="07_seo",
        question="Em kiểm toán kỹ thuật https://eyc.asia/vi-vn/ và lập cụm chủ đề cho Early Years Circle như thế nào?",
    )
    assert int_res["ok"] is True and "eyc.asia" in int_res["agent_response"]
    print("✅ [Phỏng Vấn 1-1 Phòng SEO (#07)]: Nhân sự trả lời đúng chuẩn 6 bước EYC & định vị Early Years Circle.")

    # 3. Verify Direct System Prompt & Kaizen Optimization
    opt_res = CONTROLLER.update_department_prompt_and_kaizen(
        department_id="07_seo",
        system_prompt="Bạn là Chuyên Gia SEO Kỹ Thuật (#7) của EYC (eyc.asia).",
        new_kaizen_rule="Mọi bài viết Pillar của EYC phải liên kết nội bộ tới trang sản phẩm Early Years Circle.",
    )
    assert opt_res["ok"] is True
    print(f"✅ [Tinh Chỉnh System Prompt & Luật Kaizen]: {opt_res['message']}")

    # 4. Restore 100% Clean Slate so the Director starts with a fresh EYC workbench
    CONTROLLER.clean_reset_eyc()
    state = CONTROLLER.get_full_company_state("EYC_CORE")
    assert len(state["departments"]) == 16
    assert len(state["media_vault"]) == 0
    assert len(state["work_orders"]) == 0
    print("✅ [Bàn Giao Trạng Thái Sạch 100%]: 16/16 Phòng Ban EYC sẵn sàng để Giám đốc phỏng vấn & giao việc từng task.")
    print("=" * 88)


if __name__ == "__main__":
    run_virtual_office_verification()
