#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"

echo "=========================================================================================="
echo "🏢 KHỞI ĐỘNG DÂY CHUYỀN TỰ ĐỘNG HÓA 16 PHÒNG BAN AI (AUTONOMOUS AI COMPANY PIPELINE)"
echo "=========================================================================================="

"$PYTHON_BIN" "$ROOT_DIR/second-brain/test_second_brain.py"
"$PYTHON_BIN" "$ROOT_DIR/agents/test_step2_ceo_hr.py"
"$PYTHON_BIN" "$ROOT_DIR/agents/test_step3_seo_aio_sao.py"
"$PYTHON_BIN" "$ROOT_DIR/agents/test_step4_creative_video.py"
"$PYTHON_BIN" "$ROOT_DIR/agents/test_step5_social_ads_sale.py"
"$PYTHON_BIN" "$ROOT_DIR/agents/test_step6_finance_it_master.py"
"$PYTHON_BIN" "$ROOT_DIR/virtual-office/test_virtual_office.py"

echo "=========================================================================================="
echo "✅ TOÀN BỘ 6 GIAI ĐOẠN, 16 PHÒNG BAN & VĂN PHÒNG ẢO REALTIME ĐÃ VẬN HÀNH THÀNH CÔNG 100%!"
echo "=========================================================================================="
