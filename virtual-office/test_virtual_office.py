#!/usr/bin/env python3
"""
End-to-End Verification Suite for the Real-Time Interactive Virtual Office & Command Center
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
    print("🚀 BẮT ĐẦU KIỂM THỬ TRUNG TÂM MÔ PHỎNG VĂN PHÒNG ẢO & ĐIỀU HÀNH TRỰC QUAN 16 PHÒNG BAN")
    print("=" * 88)

    # 1. Verify Full Company State Snapshot
    state = CONTROLLER.get_full_company_state("CAMP_MASSAGE_11")
    assert len(state["departments"]) == 16
    assert len(state["integrated_engines"]) >= 5
    print(
        f"✅ [Sơ Đồ Văn Phòng Ảo 2D]: Đã nạp trực quan {len(state['departments'])}/16 bàn làm việc AI "
        f"cùng tọa độ, trạng thái Realtime & {len(state['media_vault'])} sản phẩm Media."
    )

    # 2. Verify Direct Task Delegation from UI (e.g. assigning task to #12 Sale / Twenty CRM)
    del_res = CONTROLLER.delegate_and_execute_department_task(
        department_id="12_sale",
        task_title="Chốt đơn VIP từ Giao Diện Điều Hành",
        instructions="Ưu tiên khách hàng đặt 2 máy Massage AI Pro tại Hà Nội & TPHCM.",
        campaign_id="CAMP_MASSAGE_11",
    )
    assert del_res["ok"] is True
    order_id = del_res["order_id"]
    print(
        f"✅ [Giao Việc Trực Tiếp Trên Giao Diện]: Đã phát lệnh '{order_id}' tới Phòng Sale (#12) -> "
        f"Kết quả: {del_res['execution_summary']}"
    )

    # 3. Verify Human-in-the-Loop Approval (`APPROVE`)
    app_res = CONTROLLER.review_and_approve_work_order(
        order_id=order_id,
        decision="APPROVE",
        feedback_note="Đã kiểm tra danh sách Deal WON trên Twenty CRM, duyệt xuất kho!",
    )
    assert app_res["ok"] is True and app_res["new_status"] == "APPROVED_BY_DIRECTOR"
    print(f"✅ [Cổng Phê Duyệt Trực Tiếp (APPROVE)]: {app_res['message']}")

    # 4. Verify Human-in-the-Loop Rejection + Auto Kaizen Prompt Patch (`REJECT_KAIZEN`)
    kaizen_res = CONTROLLER.review_and_approve_work_order(
        order_id=order_id,
        decision="REJECT_KAIZEN",
        feedback_note="Khi gửi tin nhắn Zalo chốt đơn phải đính kèm video đóng gói Simple Replay để tăng 100% niềm tin.",
    )
    assert kaizen_res["ok"] is True and kaizen_res["new_status"] == "REJECTED_WITH_KAIZEN"
    print(f"✅ [Cổng Yêu Cầu Sửa & Tự Động Vá Prompt Kaizen (REJECT_KAIZEN)]: {kaizen_res['message']}")

    # 5. Verify Simulated 16-Department Wave
    wave_res = CONTROLLER.trigger_simulated_company_wave()
    assert wave_res["ok"] is True and wave_res["wave_steps_scheduled"] == 10
    print(
        f"✅ [Mô Phỏng Sóng Phối Hợp 16 Phòng Ban]: Đã kích hoạt {wave_res['wave_steps_scheduled']} "
        f"luồng chuyển giao công việc Realtime trên sơ đồ văn phòng ảo."
    )

    print("=" * 88)
    print("🎉 NGHIỆM THU TRUNG TÂM ĐIỀU HÀNH & MÔ PHỎNG VĂN PHÒNG ẢO: 100% TEST PASS!")
    print("=" * 88)


if __name__ == "__main__":
    run_virtual_office_verification()
