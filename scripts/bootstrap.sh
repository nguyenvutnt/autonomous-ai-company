#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/5] Khởi tạo và cập nhật toàn bộ 24 Git Submodules..."
git submodule update --init --recursive

echo "[2/5] Khởi tạo môi trường Python (.venv) và cài đặt thư viện..."
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "[3/5] Tải trình duyệt chống phát hiện Camoufox..."
.venv/bin/camoufox fetch || true

echo "[4/5] Kiểm tra MediaMTX RTMP Server..."
if [ ! -f "04-distribution-livestream-crm/mediamtx/mediamtx-bin" ]; then
  mkdir -p 04-distribution-livestream-crm/mediamtx
  curl -L -s https://github.com/bluenviron/mediamtx/releases/download/v1.11.3/mediamtx_v1.11.3_linux_amd64.tar.gz -o 04-distribution-livestream-crm/mediamtx/mediamtx.tar.gz
  tar -xzf 04-distribution-livestream-crm/mediamtx/mediamtx.tar.gz -C 04-distribution-livestream-crm/mediamtx/
  mv 04-distribution-livestream-crm/mediamtx/mediamtx 04-distribution-livestream-crm/mediamtx/mediamtx-bin || true
fi

echo "[5/5] Kích hoạt Git Hook tự động push lên GitHub sau mỗi commit..."
mkdir -p .git/hooks
cat << 'HOOK' > .git/hooks/post-commit
#!/usr/bin/env bash
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "[Auto-Push] Đang đẩy commit mới nhất lên GitHub (nhánh: $BRANCH)..."
git push origin "$BRANCH" 2>/dev/null || git push -u origin "$BRANCH" || true
HOOK
chmod +x .git/hooks/post-commit

echo "✅ Hoàn tất cài đặt hệ sinh thái Autonomous AI Company!"
