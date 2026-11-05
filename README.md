# Autonomous AI Company Ecosystem (16-Department AI Factory)

Hệ sinh thái **Tự Động Hóa Toàn Diện (Content, Media, Video, SEO/AIO/SAO, Livestream, Ads & CRM)** vận hành bởi **16 Nhân Sự Phòng Ban AI** và **Bộ Não Thứ 2 Toàn Công Ty (3-Tier Corporate Second Brain)**.

## Cấu trúc dự án

- [`docs/master_plan_autonomous_factory.md`](docs/master_plan_autonomous_factory.md): Bản thiết kế tổng thể 16 phòng ban nhân sự AI, ma trận công cụ 0đ, lộ trình triển khai cuốn chiếu & kiến trúc Bộ não thứ 2.
- `00-ai-company-agents/`: Các framework điều phối công ty AI (`agency-agents`, `agency-agents-zh`, `CompanyOS`, `MetaGPT`, `crewAI`, `ChatDev`).
- `01-media-video/`: Sản xuất Video Shorts/Reels/TikTok tự động (`MoneyPrinterTurbo`, `NarratoAI`, `pyvideotrans`, `Douyin_TikTok_Download_API`, `ComfyUI`, `LivePortrait`).
- `02-seo-research/`: Cào dữ liệu, nghiên cứu thị trường & tối ưu SEO/AIO/SAO (`crawl4ai`, `gpt-researcher`, `firecrawl`).
- `03-antidetect-browser/`: Trình duyệt chống phát hiện & điều khiển bằng AI (`camoufox`, `browser-use`, `skyvern`).
- `04-distribution-livestream-crm/`: Điều phối tự động, đăng bài đa kênh, phát Livestream 24/7 & CRM (`n8n`, `postiz-app`, `chatwoot`, `listmonk`, `mediamtx`, `srs`).
- `agents/`: Hồ sơ nhân sự 16 phòng ban & quy trình vận hành chuẩn (SOP).
- `second-brain/`: Module Bộ Não Thứ 2 Toàn Công Ty (`SqliteAiMemoryStore` + `mem0` + `LightRAG`).
- [`scripts/bootstrap.sh`](scripts/bootstrap.sh): Script cài đặt tự động toàn bộ môi trường, submodules, `.venv`, binaries và Git auto-push hooks.
- [`scripts/sync-github.sh`](scripts/sync-github.sh): Script tự động commit & push tức thì mọi thay đổi lên GitHub.
