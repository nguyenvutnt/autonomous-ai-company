#!/usr/bin/env python3
"""
Generates the 7-Day Personal Branding, Storytelling, Viral & B2B Lead-Gen Content Plan
for Facebook Page: Nhung Bản Gốc (@NhungBanGoc - https://www.facebook.com/NhungBanGoc/)
Positioning: Chuyên viên Kinh doanh Giải pháp Công nghệ & AI tại EYC (https://eyc.asia)
Also produces real media assets (.webp, .mp3, .mp4) and registers clickable Deliverables
in the EYC Enterprise Command Center (Column 03: Kho Sản Phẩm & Duyệt Nghiệm Thu).
"""

from __future__ import annotations

import json
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path("/root/ecosystem")
sys.path.insert(0, str(ROOT_DIR / "second-brain"))
sys.path.insert(0, str(ROOT_DIR / "agents"))
sys.path.insert(0, str(ROOT_DIR / "virtual-office"))

from engine import CorporateSecondBrain
from creative_video_division import CreativeVideoStudioDivision
from server import EYC_OFFICIAL_SVG_LOGO as EYC_INLINE_LOGO_SVG, DELIVERABLES_DIR

SEVEN_DAY_PLAN = [
    {
        "day_code": "NGÀY 01 — THỨ HAI",
        "best_time": "07:45 Sáng (Giờ vàng đầu tuần cho Chủ doanh nghiệp & Quản lý)",
        "pillar": "Định Vị Thương Hiệu Cá Nhân ('Bản Gốc') + Triết Lý Công Nghệ EYC",
        "format": "Bài viết Storytelling chiều sâu + Bộ ảnh chân dung công sở Nhung tại EYC (Carousel 4 ảnh)",
        "goal": "Định vị lý do tên kênh là 'Nhung Bản Gốc' — Người thật, Việc thật, Giải pháp thật tại EYC (eyc.asia), phá băng và tạo thiện cảm tin cậy.",
        "hook_headline": "TẠI SAO GIỮA THỜI ĐẠI AI CÁI GÌ CŨNG 'TỰ ĐỘNG', MÌNH LẠI ĐẶT TÊN KÊNH LÀ 'NHUNG BẢN GỐC'?",
        "post_copy": """Sáng đầu tuần đi gặp một anh Giám đốc doanh nghiệp ở Quận 1, anh hỏi mình một câu rất thật:
"Nhung ơi, làm ở công ty AI như EYC (eyc.asia), chắc tụi em cho AI nói chuyện với khách hết rồi hả? Anh sợ nhất là nhắn tin tư vấn mà cứ gặp bot trả lời văn mẫu vô hồn!"

Mình cười bảo anh:
"Dạ không anh ơi, ở EYC tụi em có một nguyên tắc bất di bất dịch: AI hỗ trợ, nhưng CON NGƯỜI mới là người quyết định. Đó cũng là lý do em lập kênh Nhung Bản Gốc này!"

Làm Sale công nghệ tại EYC, mỗi ngày nhìn hàng chục doanh nghiệp và trường học loay hoay giữa một rừng phần mềm rời rạc, mình nhận ra 3 sự thật:

1️⃣ Khách hàng không cần một "công cụ AI màu mè". Khách hàng cần một quy trình chạy mượt để tối về ngủ ngon, không phải thức khuya cộng sổ tay hay lục tìm tin nhắn Zalo bị trôi.
2️⃣ Công nghệ sinh ra không phải để biến con người thành cái máy, mà để gánh hết những việc lặp đi lặp lại — trả lại cho chúng ta phiên bản "Bản Gốc" giàu cảm xúc, sáng tạo và tận tâm nhất.
3️⃣ Một phần mềm tốt không nằm ở slide thuyết trình bóng bẩy, mà nằm ở lúc nhân viên vận hành, giáo viên đứng lớp hay kế toán bấm vào thấy nhẹ đầu ngay lập tức.

Trên trang Nhung Bản Gốc (@NhungBanGoc) này, bạn sẽ thấy tất cả những góc thật nhất của mình:
• Chuyện hậu trường đi "gỡ rối" quy trình, CRM, Zalo OA & AI Agents cho các doanh nghiệp cùng đội ngũ kỹ sư EYC.
• Những khoảnh khắc đời thường, âm nhạc nguyên bản, góc nhìn sống thật sau giờ làm.
• Và cả những bài toán thực tế giúp chủ doanh nghiệp, hiệu trưởng trường mầm non tiết kiệm hàng trăm giờ vận hành mỗi tháng.

Chào mừng bạn đến với nhà của Nhung Bản Gốc! 🧡
Nếu doanh nghiệp hoặc trường học của bạn đang có một khâu vận hành nào làm bạn "đau đầu" nhất mỗi sáng thứ Hai, cứ thả nhẹ dưới bình luận hoặc nhắn cho Nhung nhé — người thật 100% nghe máy và cùng bạn tháo gỡ!

---
📍 Nhung Bản Gốc — Chuyên viên Tư vấn Giải pháp Công nghệ & AI tại EYC (https://eyc.asia)
#NhungBanGoc #EYC #EverythingYouConnect #ChuyenDoiSoThucChien #AIAgents #LifeAtEYC""",
        "visual_concept": "Ảnh 1: Nhung cầm ly cà phê sáng trước không gian làm việc hiện đại chuẩn tông đen-cam #FE5E02 của EYC. Ảnh 2: Cận cảnh sổ tay ghi chú sơ đồ 6 bước EYC (Định hướng -> Ngữ cảnh -> Agents -> Hành động -> Kiểm tra -> Kết quả). Ảnh 3: Khoảnh khắc trao đổi cùng kỹ sư EYC. Ảnh 4: Quote card 'AI gánh việc lặp lại — Để con người giữ trọn Bản Gốc'.",
        "reels_script_60s": """• [00s–03s | HOOK]: (Nhung đang bước đi nhanh ở sảnh tòa nhà Nguyễn Huệ, quay lại nhìn thẳng camera) "Làm Sale ở công ty Trí tuệ Nhân tạo mà lại đặt tên là Nhung Bản Gốc? Nghe sai sai đúng không?"
• [03s–20s | STORY]: "Nhiều người nghĩ làm công nghệ là suốt ngày nói chuyện bằng thuật toán. Nhưng ở EYC, tụi mình luôn bắt đầu từ quy trình thật của con người trước khi viết bất kỳ dòng code nào."
• [20s–45s | VALUE]: Quay nhanh màn hình hệ thống EYC kết nối Zalo OA + CRM + AI Agents có bước phê duyệt của con người.
• [45s–60s | CTA]: "Follow Nhung Bản Gốc để xem công nghệ thực chiến giúp mình và khách hàng 'nhàn' đi mỗi ngày như thế nào nhé!" """,
        "cta_lead_magnet": "Bình luận từ khóa 'QUY TRÌNH' hoặc Inbox trực tiếp để Nhung gửi tặng Checklist 9 Bước Chuẩn Hóa Quy Trình Trước Khi Áp Dụng AI của EYC."
    },
    {
        "day_code": "NGÀY 02 — THỨ BA",
        "best_time": "11:45 Trưa (Giờ nghỉ trưa — Tối ưu kéo tương tác & thảo luận B2B)",
        "pillar": "Pain-Point Doanh Nghiệp (Zalo OA + CRM + AI Agent) — Thu Hút Lead SME",
        "format": "Reels 9:16 Hậu trường giải cứu khách hàng + Bài viết phân tích thực chiến",
        "goal": "Đánh trúng nỗi đau 'rơi khách, quên lịch hẹn, dữ liệu nằm rải rác trên 10 nhóm Zalo' của các chủ doanh nghiệp SME.",
        "hook_headline": "ĐỔ 50 TRIỆU CHẠY QUẢNG CÁO MỖI THÁNG, NHƯNG MẤT 40% KHÁCH CHỈ VÌ... TRÔI TIN NHẮN ZALO LÚC 10 GIỜ ĐÊM!",
        "post_copy": """Hôm qua ngồi kiểm tra luồng bán hàng cùng một chị chủ chuỗi thẩm mỹ & bán lẻ, chị mở điện thoại cho mình xem mà mình xót tiền thay chị thực sự.

Chị chạy Ads rất giỏi, khách nhắn về Zalo OA và Fanpage nườm nượp. Nhưng:
❌ Khách hỏi lúc 22h30 tối -> Sáng hôm sau 8h30 sale mới trả lời -> Khách đã chốt bên đối thủ từ đêm qua.
❌ Sale nghỉ việc -> Toàn bộ lịch sử chăm sóc khách hàng trên Zalo cá nhân bay màu theo.
❌ Cuối tháng hỏi: "Khách từ nguồn nào chốt nhiều nhất?" -> Không ai trả lời được vì dữ liệu nằm trên 5 file Excel khác nhau!

Đó là lúc Nhung và đội ngũ kỹ sư EYC (eyc.asia) vào cuộc để thiết lập luồng "3 Trong 1":
✅ Kết nối trực tiếp Zalo OA + CRM + AI Agent chuẩn dữ liệu một nguồn.
✅ Khách nhắn lúc 11h đêm? AI Agent (được nạp đúng kiến thức sản phẩm & bảng giá thật của công ty) phản hồi tự động trong 3 giây, xin số điện thoại và phân loại nhu cầu.
✅ Đến bước báo giá đặc biệt hoặc chốt hợp đồng lớn? Hệ thống lập tức thông báo cho nhân viên Sale thật nhảy vào tiếp quản ngay trên một màn hình duy nhất!

Kết quả sau 3 tuần vận hành: Tỷ lệ phản hồi khách hàng đạt 99.4%, không còn một lead nào bị bỏ quên qua đêm, mà nhân viên Sale lại bớt được 70% thao tác copy-paste thủ công.

Doanh nghiệp của anh/chị hiện đang quản lý khách hàng bằng CRM tập trung hay vẫn đang dùng "Excel + Trí nhớ + Zalo cá nhân"?
Comment thật lòng bên dưới, Nhung gửi ngay sơ đồ kiến trúc tích hợp Zalo OA + CRM + AI Agent của EYC để anh/chị tham khảo nhé! 👇

---
📍 Nhung Bản Gốc — Tư vấn Chuyển đổi số & AI Thực chiến tại EYC (https://eyc.asia/vi-vn/resources/tich-hop-zalo-oa-crm-ai-agent/)
#NhungBanGoc #EYC #ZaloOA #CRM #AIAgent #ToiUuBanHang #B2BSales""",
        "visual_concept": "Infographic tối giản chuẩn màu thương hiệu EYC (#07080B nền tối, #FE5E02 điểm nhấn cam): So sánh 'Trước khi kết nối EYC (5 app rời rạc, rớt 40% khách)' vs 'Sau khi kết nối Zalo OA + CRM + AI Agent EYC (1 nguồn dữ liệu duy nhất)'.",
        "reels_script_60s": """• [00s–03s | HOOK]: "Đừng đổ thêm tiền chạy quảng cáo nữa nếu bạn vẫn đang để nhân viên chăm khách qua Zalo cá nhân và 5 file Excel!"
• [03s–25s | PROBLEM]: Diễn tả cảnh khách nhắn lúc 23h đêm không ai rep, sáng ra khách đã mua chỗ khác.
• [25s–50s | SOLUTION]: Quay trực tiếp sơ đồ luồng Zalo OA -> Webhook -> CRM -> AI Agent của EYC xử lý trong 3 giây và chuyển thông báo cho Sale.
• [50s–60s | CTA]: "Nhắn ngay chữ 'ZALO' cho Nhung Bản Gốc để mình demo trực tiếp luồng này cho doanh nghiệp của bạn nhé!" """,
        "cta_lead_magnet": "Inbox từ khóa 'ZALO CRM' để nhận Bản Demo luồng tự động hóa Zalo OA + CRM + AI Agent và ước tính chi phí triển khai từ Nhung."
    },
    {
        "day_code": "NGÀY 03 — THỨ TƯ",
        "best_time": "19:30 Tối (Giờ vàng Phụ huynh, Giáo viên & Chủ trường mầm non online)",
        "pillar": "Sản Phẩm Chủ Lực Early Years Circle (Mầm Non Cloud EYC) — Storytelling Chạm Cảm Xúc",
        "format": "Bài viết Storytelling + Video ngắn 9:16 quay thực tế 4 điểm chạm (01 Teacher, 02 Family, 03 Admin, 04 TV)",
        "goal": "Giới thiệu hệ sinh thái mầm non Early Years Circle (eyc.asia) qua góc nhìn nhân văn: Giải phóng giáo viên khỏi sổ sách để yêu thương trẻ trọn vẹn.",
        "hook_headline": "CÔ GIÁO MẦM NON ĐÁNG LẼ PHẢI ĐƯỢC ÔM CON TRẺ, CHỨ KHÔNG PHẢI ÔM ĐIỆN THOẠI TRẢ LỜI 30 NHÓM CHAT!",
        "post_copy": """Tuần trước Nhung đi khảo sát thực tế tại một trường mầm non tư thục để triển khai hệ thống Early Years Circle của EYC.

Hình ảnh làm mình nhớ mãi là lúc 4 giờ chiều: Một tay cô giáo bế bé đang khóc, tay kia cô vẫn phải cố gõ tin nhắn lên nhóm Zalo lớp để báo từng phụ huynh hôm nay bé ăn mấy chén cơm, ngủ mấy tiếng, uống thuốc lúc mấy giờ...
Cô tâm sự với mình: "Nhiều lúc thương tụi nhỏ lắm chị Nhung, mà không nhắn liền thì ba mẹ ở nhà sốt ruột, còn tối về cô lại phải chép lại vào sổ theo dõi của nhà trường."

Đó chính là lý do đội ngũ kỹ sư EYC đã dành trọn tâm huyết xây dựng **Early Years Circle** — không phải là một app rời rạc, mà là 4 phân hệ kết nối đồng bộ theo thời gian thực:

🔸 **01 / Teacher (Ứng dụng Giáo viên):** Điểm danh, ghi nhận bữa ăn, giấc ngủ, sức khỏe và gửi ảnh cho cả lớp chỉ bằng vài chạm trong chưa đầy 60 giây.
🔸 **02 / Family (Ứng dụng Phụ huynh):** Ba mẹ mở điện thoại thấy ngay dòng thời gian trong ngày của riêng con mình, nhắn dặn thuốc có xác nhận giờ cô đã cho uống — không còn cảnh trôi tin trong group chat ồn ào.
🔸 **03 / Admin (Quản trị Nhà trường):** Ban giám hiệu nắm trọn sĩ số, thực đơn dinh dưỡng, học phí và báo cáo đa cơ sở trên một nguồn dữ liệu duy nhất.
🔸 **04 / TV (Màn hình Lớp học & Sảnh đón):** Hiển thị lịch hoạt động, thông báo đón trẻ an toàn và hình ảnh lớp học trực quan ngay tại trường.

Khi công nghệ làm đúng việc của nó, cô giáo được trả lại "Bản Gốc" dịu dàng và trọn vẹn nhất bên các con! 🧡

Nếu bạn là Chủ trường, Hiệu trưởng mầm non, hoặc có người thân đang vận hành trường mầm non muốn trải nghiệm thử cả 4 phân hệ này ngay tại trường, hãy nhắn cho Nhung nhé!

---
📍 Nhung Bản Gốc — Tư vấn Giải pháp Giáo dục Số Early Years Circle (https://eyc.asia/vi-vn/industries/)
#NhungBanGoc #EarlyYearsCircle #EYC #PhanMemMamNon #QuanLyTruongMamNon #GiaoDucMamNon""",
        "visual_concept": "Bộ ảnh 4 khung hình trực quan (4 Touchpoints của Early Years Circle trên nền thương hiệu EYC): 01 Teacher trên máy tính bảng lớp học, 02 Family trên iPhone của phụ huynh, 03 Admin trên Macbook của Hiệu trưởng, và 04 TV trên màn hình lớn tại sảnh trường.",
        "reels_script_60s": """• [00s–04s | HOOK]: "Một cô giáo mầm non tốn bao nhiêu phút mỗi ngày chỉ để... copy ảnh và gõ tin nhắn vào nhóm Zalo lớp?"
• [04s–25s | EMPATHY]: Kể lại câu chuyện thực tế khi Nhung đi khảo sát trường mầm non lúc 4h chiều.
• [25s–50s | DEMO 4 TOUCHPOINTS]: Trình diễn nhanh thao tác 1 chạm từ App Cô giáo (01 Teacher) -> nhảy tức thì sang App Phụ huynh (02 Family), Màn hình TV lớp (04 TV) và Dashboard Hiệu trưởng (03 Admin).
• [50s–60s | CTA]: "Các thầy cô và chủ trường mầm non chấm (.) dưới bình luận để Nhung mang bộ thiết bị Demo Early Years Circle qua tận trường mình trải nghiệm miễn phí nhé!" """,
        "cta_lead_magnet": "Đăng ký lịch Demo trực tiếp 1-1 bộ 4 phân hệ Early Years Circle (Teacher - Family - Admin - TV) miễn phí cho trường mầm non."
    },
    {
        "day_code": "NGÀY 04 — THỨ NĂM",
        "best_time": "12:00 Trưa (Khung giờ tương tác giải trí & chia sẻ góc nhìn nghề nghiệp)",
        "pillar": "Góc Hài Hước / Đời Thường Của Sale Công Nghệ + Chuyên Môn Phát Triển Phần Mềm 9 Giai Đoạn",
        "format": "Meme / Carousel Chuyện nghề Sale IT & Công nghệ + Bài viết bóc tách sự thật",
        "goal": "Tăng tương tác tự nhiên (Viral, Share, Tag bạn bè), đồng thời giáo dục thị trường về Quy trình phát triển phần mềm 9 giai đoạn minh bạch của EYC.",
        "hook_headline": "KHÁCH HÀNG BẢO: 'LÀM CHO ANH CÁI APP ĐƠN GIẢN NHƯ GRAB THÔI, TUẦN SAU XONG KHÔNG EM?' 😂",
        "post_copy": """Làm Sale công nghệ tại EYC, có những câu nói của khách hàng nghe xong vừa thương vừa buồn cười:
💬 "Anh chỉ cần một cái web/app nho nhỏ thôi, bấm 1 nút là ra hết báo cáo toàn công ty, chi phí tầm vài triệu, tuần sau chạy luôn được không Nhung?"

Nếu là một bên chỉ muốn ký hợp đồng lấy tiền cọc nhanh, họ sẽ gật đầu cái rụp: "Dạ được anh ơi, dễ ợt!"
Và kết quả 3 tháng sau: Dự án đắp chiếu, code lỗi tùm lum, không bàn giao được, hai bên nhìn nhau thở dài!

Nhưng ở EYC (eyc.asia) — và với tính cách của "Nhung Bản Gốc" — mình luôn chọn nói THẬT ngay từ buổi đầu tiên:
"Dạ anh ơi, làm phần mềm dùng thật trong doanh nghiệp không thể đốt cháy giai đoạn được. Tụi em thà mất thêm 1 tuần đầu để vẽ đúng quy trình thật của anh, còn hơn làm nhanh một thứ không nhân viên nào dùng được!"

Tại EYC, mọi dự án phần mềm thiết kế riêng đều đi qua **Quy Trình 9 Giai Đoạn Chuẩn Kỹ Thuật** (do chính Giám đốc kỹ thuật Phan Phúc Nguyên thiết lập):
01. Khảo sát quy trình thực tế (Discovery) — Quy trình trước tính năng.
02. Phân tích vai trò & phân quyền thật của từng phòng ban.
03. Thiết kế kiến trúc dữ liệu một nguồn & API/Cloud.
04. Thiết kế giao diện UI/UX nguyên mẫu (Prototype) để khách hàng bấm thử trước khi code.
05. Phát triển theo từng Sprint ngắn — nghiệm thu từng phân hệ.
06. Kiểm thử tự động, kiểm thử tải & bảo mật dữ liệu (đặc biệt là Nghị định bảo vệ dữ liệu cá nhân).
07. Chạy thử nghiệm thực tế (UAT) cùng nhân sự trực tiếp sử dụng.
08. Đào tạo vận hành & chuẩn hóa tài liệu kỹ thuật.
09. Bàn giao toàn diện mã nguồn, hạ tầng & đồng hành bảo trì dài hạn.

Ai từng đi đặt làm phần mềm hoặc mua phần mềm về mà gặp cảnh "Lúc tư vấn như thiên đường — Lúc bàn giao như mê cung" thì vào đây điểm danh với Nhung nào! 👇

---
📍 Nhung Bản Gốc — Người nói thật về Công nghệ tại EYC (https://eyc.asia/vi-vn/resources/quy-trinh-phat-trien-phan-mem-theo-yeu-cau/)
#NhungBanGoc #ChuyenNgheSale #PhatTrienPhanMem #EYC #SoftwareDevelopment #GocNhinThucChien""",
        "visual_concept": "Carousel 5 tấm thiết kế sắc nét chuẩn font Be Vietnam Pro & IBM Plex Mono: Tấm 1 'Kỳ vọng vs Thực tế khi làm phần mềm doanh nghiệp', Tấm 2-4 '9 Giai đoạn làm phần mềm không bao giờ đắp chiếu tại EYC', Tấm 5 'Checklist tự kiểm tra trước khi thuê viết phần mềm'.",
        "reels_script_60s": """• [00s–05s | POV COMEDY]: POV: Khi khách hàng bảo "Làm cho anh cái hệ thống ERP tích hợp AI đơn giản thôi, thứ Hai tuần sau chạy nhé!" — Nhung đứng hình 3 giây rồi mở bảng 9 giai đoạn kỹ thuật của EYC ra giải thích cực duyên dáng.
• [05s–45s | INSIGHT]: Giải thích ngắn gọn vì sao phần mềm doanh nghiệp hay thất bại ở bước "làm tính năng trước khi hiểu quy trình" và cách EYC cho khách duyệt Prototype trước khi code.
• [45s–60s | CTA]: "Đừng để mất tiền học phí oan khi làm phần mềm! Lưu ngay video này hoặc nhắn cho Nhung Bản Gốc trước khi ký hợp đồng phần mềm nhé!" """,
        "cta_lead_magnet": "Comment '9 GIAI ĐOẠN' để nhận mẫu Hồ sơ Yêu cầu Kỹ thuật (RFP Template) giúp doanh nghiệp đặt hàng phần mềm không bao giờ bị đội chi phí."
    },
    {
        "day_code": "NGÀY 05 — THỨ SÁU",
        "best_time": "16:30 Chiều (Giờ tổng kết tuần — Chủ đề Chiến lược & Tối ưu Chi phí cho CEO/CFO)",
        "pillar": "B2B Thought Leadership — Lộ Trình 90 Ngày Tự Động Hóa & Kiểm Soát Chi Phí AI/Cloud",
        "format": "Case Study Phân tích Số liệu thực tế + Infographic Lộ trình 30-60-90 ngày",
        "goal": "Thuyết phục nhóm khách hàng B2B cấp cao (CEO, CFO, Giám đốc vận hành) bằng tư duy tài chính (ROI, tiết kiệm chi phí Cloud & LLM API).",
        "hook_headline": "ĐỪNG ĐẬP ĐI XÂY LẠI TOÀN BỘ HỆ THỐNG! ĐÂY LÀ LỘ TRÌNH 90 NGÀY ĐỂ DOANH NGHIỆP ÁP DỤNG AI MÀ KHÔNG BỊ 'ĐỐT TIỀN'",
        "post_copy": """Rất nhiều anh/chị chủ doanh nghiệp tâm sự với Nhung:
"Anh biết phải chuyển đổi số và dùng AI rồi, nhưng sợ nhất là bày ra một đại dự án kéo dài cả năm trời, tốn hàng trăm triệu mà nhân viên lại phản đối vì khó dùng."

Ở EYC (eyc.asia), khi Nhung cùng đội ngũ kỹ sư ngồi xuống với một doanh nghiệp, tụi mình không bao giờ khuyên khách hàng "đập đi xây lại tất cả cùng lúc". Thay vào đó là **Lộ Trình 90 Ngày Thực Chiến (30 - 60 - 90)**:

🔹 **30 Ngày Đầu — Gỡ Điểm Nghẽn & Gom Dữ Liệu Về Một Nguồn:**
Chọn đúng 1 quy trình tốn nhiều giờ công thủ công nhất (ví dụ: tổng hợp đơn hàng từ Zalo/Sàn về CRM/Kế toán, hoặc đối soát công nợ cuối ngày). Chuẩn hóa dữ liệu để không ai phải nhập liệu 2 lần.

🔹 **60 Ngày Tiếp Theo — Đưa AI Agents Vào Hỗ Trợ Có Kiểm Soát:**
Khi dữ liệu đã sạch, kết nối AI Agents qua chuẩn MCP & RAG nội bộ để tự động phân loại yêu cầu, soạn báo giá nháp, trả lời tra cứu kỹ thuật — nhưng luôn có **Điểm Phê Duyệt Của Con Người (Human Approval Gate)** ở các bước nhạy cảm.

🔹 **90 Ngày Hoàn Thiện — Đo Lường ROI & Tối Ưu Chi Phí Vận Hành:**
Áp dụng 12 phương pháp tối ưu chi phí hạ tầng Cloud (Cloudflare, GreenNode, Azure, GCP) và kiểm soát ngân sách LLM API (Semantic Caching, Model Routing) để chi phí vận hành hàng tháng nhẹ nhất mà tốc độ phản hồi dưới 100ms.

Chuyển đổi số thành công là khi tuần thứ 4 nhìn lại, nhân sự của bạn mỉm cười vì hết cảnh tăng ca vô lý, còn bảng P&L của CFO thì rõ ràng từng con số!

Cuối tuần này Nhung còn trống **02 suất Khám Sức Khỏe Quy Trình & Hạ Tầng Số (1-1 cùng Kỹ sư EYC)** hoàn toàn miễn phí cho các doanh nghiệp đăng ký sớm. Anh/chị nhắn trực tiếp cho Nhung để giữ lịch nhé!

---
📍 Nhung Bản Gốc — Đồng hành Chuyển đổi số & AI Doanh nghiệp tại EYC (https://eyc.asia/vi-vn/resources/lo-trinh-90-ngay-tu-dong-hoa-quy-trinh/)
#NhungBanGoc #EYC #LoTrinh90Ngay #TuDongHoaQuyTrinh #CloudOptimization #ROICongNghe""",
        "visual_concept": "Sơ đồ lộ trình 30 - 60 - 90 Ngày thiết kế chuẩn phong cách kỹ thuật của eyc.asia: Nền #07080B, lưới kiến trúc mảnh, các cột mốc được đánh số 01 - 02 - 03 bằng font IBM Plex Mono màu cam #FE5E02.",
        "reels_script_60s": """• [00s–04s | HOOK]: "80% dự án AI trong doanh nghiệp thất bại vì... muốn làm một phát ăn ngay cả công ty!"
• [04s–45s | ROADMAP]: Nhung vẽ nhanh trên bảng kính 3 cột mốc 30 ngày (Chuẩn hóa dữ liệu), 60 ngày (AI Agent có điểm duyệt con người), 90 ngày (Đo lường ROI & tối ưu Cloud).
• [45s–60s | CTA]: "Inbox ngay chữ '90 NGÀY' cho Nhung Bản Gốc để nhận bản đánh giá quy trình miễn phí cùng đội ngũ kỹ sư EYC nhé!" """,
        "cta_lead_magnet": "Đặt lịch phiên 'Audit Quy Trình & Tối Ưu Chi Phí Cloud/AI 1-1' (45 phút) cùng Nhung và Kỹ sư giải pháp EYC."
    },
    {
        "day_code": "NGÀY 06 — THỨ BẢY",
        "best_time": "20:00 Tối (Cuối tuần thư giãn — Âm nhạc Nguyên Bản, Nghệ Thuật & Cảm Hứng Sống)",
        "pillar": "Cảm Hứng Nguyên Bản ('Những Bản Gốc' — Âm Nhạc, Nghệ Thuật & Giá Trị Con Người)",
        "format": "Video Acoustic / Đĩa than / Góc nhỏ cuối tuần của Nhung + Tâm sự sâu sắc",
        "goal": "Kết nối cảm xúc sâu sắc với người theo dõi qua âm nhạc và nghệ thuật nguyên bản, làm mềm hóa hình ảnh Sale công nghệ và tăng độ yêu thích thương hiệu cá nhân.",
        "hook_headline": "THỨ BẢY TẮT MÀN HÌNH CODE, BẬT MỘT 'BẢN GỐC' XƯA — ĐỂ NHỚ VÌ SAO CHÚNG TA CẦN CÔNG NGHỆ!",
        "post_copy": """Tối thứ Bảy, sau một tuần chạy hết công suất cùng những dự án phần mềm và AI tại EYC, thói quen yêu thích nhất của mình là pha một ấm trà nóng, bật lại những bản thu âm gốc mộc mạc của những thập niên cũ.

Nghe tiếng đàn guitar thùng mộc, tiếng lấy hơi rất thật của người nghệ sĩ trong phòng thu xưa — không autotune quá đà, không cắt ghép công nghiệp — tự nhiên lòng dịu lại lạ kỳ.

Nhiều bạn hỏi mình: "Nhung vừa mê những thứ nguyên bản, hoài niệm như âm nhạc xưa, vừa làm trong ngành Trí tuệ nhân tạo tối tân nhất, hai thứ đó có mâu thuẫn nhau không?"

Mình thấy không hề mâu thuẫn, mà ngược lại, chúng sinh ra để bảo vệ nhau!
Chính vì mình trân quý những "Bản Gốc" — một giọng hát mộc chạm vào tim, một bữa cơm tối ba mẹ không phải nhìn điện thoại trả lời việc công ty, một buổi chiều cô giáo mầm non thảnh thơi kể chuyện cho học trò nghe — nên mình mới càng yêu công việc tại EYC.

Bởi sứ mệnh đẹp nhất của công nghệ và AI không phải là thay thế cảm xúc con người, mà là dọn sạch những bộn bề cơ học để mỗi chúng ta có thêm một tối thứ Bảy thảnh thơi sống đúng với "Bản Gốc" của mình. 🎶🧡

Tối nay bạn đang nghe bản nhạc nào để nạp lại năng lượng sau một tuần làm việc?
Chia sẻ tên bài hát "Bản Gốc" bạn yêu thích nhất dưới phần bình luận để tối nay Nhung cùng nghe với nhé! 👇

---
📍 Nhung Bản Gốc (@NhungBanGoc) — Sống thật, Làm công nghệ thật
#NhungBanGoc #NhungBanThuGoc #CuoiTuanThongDong #CamHungSong #EYCLife #HumanFirstAI""",
        "visual_concept": "Video ngắn / Ảnh góc phòng ấm áp ánh đèn vàng cam (#FE5E02) buổi tối thứ Bảy: Loa/máy đĩa than đang phát nhạc mộc, bên cạnh là cuốn sách và chiếc cốc sứ, tạo cảm giác nghệ thuật, chân thành và gần gũi.",
        "reels_script_60s": """• [00s–05s | AMBIENCE]: Tiếng nhạc acoustic mộc mạc vang lên, cảnh Nhung gấp chiếc laptop lại sau một tuần làm việc và bật bản nhạc yêu thích.
• [05s–45s | VOICEOVER]: Giọng đọc trầm ấm của Nhung chia sẻ về vẻ đẹp của những tác phẩm nguyên bản và lý do công nghệ EYC tồn tại để trả lại thời gian sống thật cho con người.
• [45s–60s | INTERACTION]: "Còn bạn, bài hát nào là 'Bản Gốc' không thể thay thế trong lòng bạn? Bình luận bên dưới cho Nhung biết nhé!" """,
        "cta_lead_magnet": "Tương tác cộng đồng: Chia sẻ bài hát 'Bản Gốc' yêu thích nhất để kết nối cảm xúc tự nhiên và mở rộng tệp người theo dõi."
    },
    {
        "day_code": "NGÀY 07 — CHỦ NHẬT",
        "best_time": "19:45 Tối (Giờ vàng tối Chủ Nhật chuẩn bị cho tuần làm việc mới)",
        "pillar": "Tổng Kết Tuần + Cẩm Nang Miễn Phí (Lead Magnet) + Mở Lịch Tư Vấn Tuần Mới",
        "format": "Bài viết Tổng hợp Giá trị (Save/Share cao) + Call-to-Action Đặt lịch Tư vấn 1-1",
        "goal": "Chuyển đổi lượng tương tác cả tuần thành danh sách khách hàng tiềm năng (Leads) vào hệ thống Twenty CRM của EYC cho tuần kế tiếp.",
        "hook_headline": "TỔNG HỢP 4 BỘ TÀI LIỆU CÔNG NGHỆ & AI THỰC CHIẾN TỪ EYC (TẶNG MIỄN PHÍ CHO TUẦN MỚI BỨT PHÁ)",
        "post_copy": """Tối Chủ Nhật ngồi nhìn lại một tuần làm việc đầy năng lượng:
• Đi khảo sát thực tế tại trường mầm non để chuẩn bị bàn giao hệ thống **Early Years Circle**.
• Cùng các anh kỹ sư EYC tháo gỡ luồng **Zalo OA + CRM + AI Agent** cho 3 doanh nghiệp SME.
• Và vui nhất là nhận được hàng chục tin nhắn hỏi thăm, tâm sự của anh/chị bạn bè trên kênh **Nhung Bản Gốc** này!

Để chuẩn bị cho một tuần mới làm việc thông minh hơn, ít thao tác thủ công hơn, Nhung đã xin phép Ban Giám đốc EYC tổng hợp lại **04 Bộ Cẩm Nang Thực Chiến** (viết bằng ngôn ngữ cực dễ hiểu cho người điều hành, không lý thuyết sáo rỗng) để gửi tặng miễn phí cho bạn bè trên trang:

🎁 **Bộ số 01:** Checklist 9 Giai Đoạn Đặt Hàng & Triển Khai Phần Mềm Theo Yêu Cầu (Tránh 100% rủi ro đội vốn, đắp chiếu).
🎁 **Bộ số 02:** Sơ Đồ Kiến Trúc Tích Hợp Zalo OA + CRM + AI Agent (Chống rơi khách hàng 24/7).
🎁 **Bộ số 03:** Hồ Sơ Giải Pháp Chuyển Đổi Số Trường Mầm Non **Early Years Circle** (Đồng bộ 01 Teacher - 02 Family - 03 Admin - 04 TV).
🎁 **Bộ số 04:** Lộ Trình 90 Ngày Tự Động Hóa Quy Trình & Kiểm Soát Chi Phí Cloud/AI Cho SME.

👉 **Cách nhận rất đơn giản:**
Bạn đang quan tâm nhất đến bộ số mấy (**01, 02, 03 hay 04** — hoặc gõ **"CẢ 4"**), hãy bình luận con số đó xuống bên dưới hoặc nhắn tin trực tiếp cho **Nhung Bản Gốc**. Tối nay Nhung sẽ gửi tận tay từng người và hỗ trợ giải đáp 1-1 cho bài toán riêng của đơn vị bạn trong tuần mới nhé!

Chúc cả nhà một tối Chủ Nhật bình yên và một tuần mới rực rỡ! 🧡🚀

---
📍 Nhung Bản Gốc — Chuyên viên Kinh doanh Giải pháp Công nghệ & AI
🏢 CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC
🌐 Website: https://eyc.asia | Địa chỉ: 68 Nguyễn Huệ, P. Sài Gòn, TP.HCM
#NhungBanGoc #EYC #EverythingYouConnect #EarlyYearsCircle #ZaloOA #AIAgents #ChuyenDoiSo""",
        "visual_concept": "Mockup 4 bìa hồ sơ tài liệu chuẩn nhận diện EYC (Nền đen kiến trúc #07080B, chữ trắng tinh khiết, đánh số 01 - 02 - 03 - 04 màu cam #FE5E02 kèm logo chính thức EYC) giúp tăng tỷ lệ bấm xem và bình luận xin tài liệu.",
        "reels_script_60s": """• [00s–04s | HOOK]: "Trước khi bắt đầu sáng thứ Hai tuần mới, hãy lấy ngay 4 bộ tài liệu công nghệ thực chiến này từ EYC!"
• [04s–45s | SHOWCASE]: Nhung lật từng bộ tài liệu trên iPad/màn hình: (01) Quy trình 9 bước làm phần mềm, (02) Luồng Zalo OA + CRM + AI Agent, (03) Hệ sinh thái mầm non Early Years Circle, (04) Lộ trình tự động hóa 90 ngày.
• [45s–60s | CTA]: "Bình luận số 01, 02, 03, 04 hoặc chữ 'CẢ 4' ngay bên dưới, Nhung Bản Gốc gửi tặng bạn liền tay trong tối nay nhé!" """,
        "cta_lead_magnet": "Thu phễu Lead B2B đa phân khúc (01 Phần mềm riêng, 02 Zalo+CRM+AI, 03 Mầm non Early Years Circle, 04 Tự động hóa 90 ngày) đồng bộ thẳng vào Twenty CRM của EYC."
    }
]


def build_html_dossier(
    order_id: str,
    banner_url: str,
    audio_url: str,
    video_url: str,
    created_at_utc: str,
) -> str:
    days_html = []
    for idx, d in enumerate(SEVEN_DAY_PLAN, start=1):
        days_html.append(
            f"""
            <div class="day-card">
              <div class="day-header">
                <div>
                  <span class="day-badge">{d['day_code']}</span>
                  <span class="time-badge">⏰ {d['best_time']}</span>
                </div>
                <span class="pillar-badge">{d['pillar']}</span>
              </div>

              <div class="meta-strip">
                <div><strong>Định dạng:</strong> {d['format']}</div>
                <div><strong>Mục tiêu chuyển đổi:</strong> {d['goal']}</div>
              </div>

              <div class="section-label">01 / TIÊU ĐỀ HOOK & NỘI DUNG BÀI ĐĂNG FACEBOOK (COPY & ĐĂNG NGAY)</div>
              <div class="hook-box">{d['hook_headline']}</div>
              <pre class="copy-box">{d['post_copy']}</pre>

              <div class="two-col">
                <div class="sub-box">
                  <div class="section-label">02 / CONCEPT HÌNH ẢNH / CAROUSEL CHUẨN EYC</div>
                  <p>{d['visual_concept']}</p>
                </div>
                <div class="sub-box">
                  <div class="section-label">03 / KỊCH BẢN REELS / TIKTOK 9:16 (60 GIÂY)</div>
                  <pre class="script-pre">{d['reels_script_60s']}</pre>
                </div>
              </div>

              <div class="cta-bar">
                <strong>🎯 PHỄU THU LEAD B2B VỀ TWENTY CRM:</strong> {d['cta_lead_magnet']}
              </div>
            </div>
            """
        )

    days_joined = "\n".join(days_html)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{order_id} — Kế Hoạch Nội Dung 7 Ngày Kênh Nhung Bản Gốc (@NhungBanGoc) | EYC</title>
  <link rel="icon" href="/static/eyc-brand/favicon.ico" />
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #07080B;
      --bg-2: #0E1017;
      --bg-3: #161922;
      --orange: #FE5E02;
      --border: rgba(255, 255, 255, 0.12);
      --ink: #FFFFFF;
      --ink-2: #CBD5E1;
      --mut: #94A3B8;
      --font: "Be Vietnam Pro", sans-serif;
      --mono: "IBM Plex Mono", monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--ink);
      font-family: var(--font);
      line-height: 1.65;
      padding: 28px 20px 60px;
    }}
    .container {{
      max-width: 1080px;
      margin: 0 auto;
    }}
    .dossier-header {{
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-top: 3px solid var(--orange);
      border-radius: 12px;
      padding: 24px 28px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 20px;
      flex-wrap: wrap;
    }}
    .eyc-logo-wrap {{
      color: var(--ink);
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .header__logo-svg {{
      height: 38px;
      width: auto;
    }}
    .dossier-title {{
      font-size: 22px;
      font-weight: 700;
      margin-top: 12px;
      color: var(--ink);
    }}
    .dossier-sub {{
      font-family: var(--mono);
      font-size: 12px;
      color: var(--orange);
      margin-top: 4px;
    }}
    .media-showcase {{
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }}
    .media-box {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
    }}
    .media-box img, .media-box video {{
      width: 100%;
      max-height: 360px;
      object-fit: contain;
      border-radius: 6px;
      background: #050608;
      margin-top: 8px;
    }}
    .day-card {{
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-left: 3px solid var(--orange);
      border-radius: 12px;
      padding: 22px 24px;
      margin-bottom: 20px;
    }}
    .day-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 12px;
    }}
    .day-badge {{
      font-family: var(--mono);
      font-size: 12px;
      font-weight: 700;
      background: var(--orange);
      color: #07080B;
      padding: 4px 10px;
      border-radius: 5px;
      margin-right: 8px;
    }}
    .time-badge {{
      font-family: var(--mono);
      font-size: 11.5px;
      color: var(--ink-2);
    }}
    .pillar-badge {{
      font-family: var(--mono);
      font-size: 11px;
      color: var(--orange);
      border: 1px solid var(--orange);
      padding: 3px 9px;
      border-radius: 5px;
    }}
    .meta-strip {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      font-size: 13px;
      color: var(--ink-2);
      margin-bottom: 14px;
      background: var(--bg);
      padding: 10px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
    .section-label {{
      font-family: var(--mono);
      font-size: 10.5px;
      font-weight: 600;
      letter-spacing: 0.08em;
      color: var(--orange);
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .hook-box {{
      font-size: 15px;
      font-weight: 700;
      color: var(--ink);
      background: rgba(254, 94, 2, 0.12);
      border: 1px solid var(--orange);
      padding: 10px 14px;
      border-radius: 7px;
      margin-bottom: 10px;
    }}
    .copy-box {{
      white-space: pre-wrap;
      font-family: var(--font);
      font-size: 13.5px;
      color: var(--ink-2);
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 14px;
      line-height: 1.7;
    }}
    .two-col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 14px;
    }}
    .sub-box {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      font-size: 13px;
      color: var(--ink-2);
    }}
    .script-pre {{
      white-space: pre-wrap;
      font-family: var(--font);
      font-size: 12.5px;
      color: var(--ink-2);
      line-height: 1.6;
    }}
    .cta-bar {{
      background: var(--bg-3);
      border: 1px solid var(--border);
      border-radius: 7px;
      padding: 10px 14px;
      font-size: 13px;
      color: var(--ink);
    }}
    .cta-bar strong {{ color: var(--orange); }}
  </style>
</head>
<body>
  <div class="container">
    <div class="dossier-header">
      <div>
        <div class="eyc-logo-wrap">
          {EYC_INLINE_LOGO_SVG}
          <div>
            <div style="font-weight:700;font-size:13px;">CÔNG TY TNHH CÔNG NGHỆ VÀ TRÍ TUỆ NHÂN TẠO EYC</div>
            <div style="font-family:var(--mono);font-size:11px;color:var(--mut);">PHÒNG 04 CONTENT × PHÒNG 10 SOCIAL × PHÒNG 12 SALE B2B</div>
          </div>
        </div>
        <h1 class="dossier-title">KẾ HOẠCH BÀI ĐĂNG & KỊCH BẢN REELS 7 NGÀY — KÊNH "NHUNG BẢN GỐC" (@NhungBanGoc)</h1>
        <div class="dossier-sub">LINK KÊNH: HTTPS://WWW.FACEBOOK.COM/NHUNGBANGOC/ • ĐỊNH VỊ: CHUYÊN VIÊN KINH DOANH GIẢI PHÁP CÔNG NGHỆ & AI TẠI EYC (EYC.ASIA)</div>
      </div>
      <div style="text-align:right;font-family:var(--mono);font-size:11px;color:var(--mut);">
        <div>MÃ HỒ SƠ: <strong style="color:var(--orange);">{order_id}</strong></div>
        <div>NGÀY XUẤT BẢN: {created_at_utc}</div>
        <div>TRẠNG THÁI: CHỜ GIÁM ĐỐC PHAN PHÚC NGUYÊN DUYỆT</div>
      </div>
    </div>

    <div class="media-showcase">
      <div class="media-box">
        <div class="section-label">ẤN PHẨM POSTER ĐỊNH VỊ KÊNH NHUNG BẢN GỐC × EYC (.WEBP)</div>
        <a href="{banner_url}" target="_blank"><img src="{banner_url}" alt="Poster Nhung Bản Gốc EYC" /></a>
        <div style="margin-top:10px;">
          <div class="section-label">THUYẾT MINH AI REELS GIỚI THIỆU KÊNH (.MP3)</div>
          <audio controls preload="metadata" src="{audio_url}" style="width:100%;margin-top:4px;"></audio>
        </div>
      </div>
      <div class="media-box">
        <div class="section-label">VIDEO REELS 9:16 DỰNG SẴN CHO NGÀY 01 (.MP4)</div>
        <video controls preload="metadata" src="{video_url}"></video>
      </div>
    </div>

    {days_joined}
  </div>
</body>
</html>
"""


def main() -> None:
    brain = CorporateSecondBrain()
    studio = CreativeVideoStudioDivision(brain)

    bundle = studio.produce_full_campaign_creative_bundle(
        campaign_id="EYC_NHUNGBANGOC_7D",
        product_name="Nhung Bản Gốc (@NhungBanGoc) — Chuyên Viên Giải Pháp Công Nghệ & AI EYC",
        price_vnd=25000000,
        usp_highlights=[
            "Người thật - Việc thật - Giải pháp công nghệ thật tại EYC (eyc.asia)",
            "Tư vấn Zalo OA + CRM + AI Agent & Nền tảng Mầm non Early Years Circle",
            "Lộ trình 90 ngày tự động hóa quy trình & Phát triển phần mềm 9 giai đoạn",
        ],
        target_persona="Chủ doanh nghiệp SME, Ban giám hiệu trường mầm non & Cộng đồng yêu công nghệ",
        spintax_count=50,
        watermark_text="NHUNG BẢN GỐC (@NHUNGBANGOC) • EYC.ASIA",
    )

    webp_name = Path(bundle["studio_banner_webp"]["file_path"]).name
    mp3_name = Path(bundle["voiceover_audio"]["audio_path"]).name
    mp4_name = Path(bundle["short_video_mp4"]["video_mp4_path"]).name
    mtime = int(time.time())

    banner_url = f"/media/{urllib.parse.quote(webp_name)}?v={mtime}"
    audio_url = f"/media/{urllib.parse.quote(mp3_name)}?v={mtime}"
    video_url = f"/media/{urllib.parse.quote(mp4_name)}?v={mtime}"

    order_id = "WO_EYC_NHUNGBANGOC_7DAYS"
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
    html_path = DELIVERABLES_DIR / f"{order_id}.html"
    json_path = DELIVERABLES_DIR / f"{order_id}.json"

    html_url = f"/deliverables/{order_id}.html"
    json_url = f"/deliverables/{order_id}.json"

    deliverable_payload = {
        "type": "NHUNGBANGOC_7DAY_CONTENT_CALENDAR",
        "order_id": order_id,
        "target_facebook_page": "https://www.facebook.com/NhungBanGoc/",
        "page_name": "Nhung Bản Gốc (@NhungBanGoc)",
        "role_at_eyc": "Chuyên viên Kinh doanh Giải pháp Công nghệ & AI tại EYC (eyc.asia)",
        "seven_day_calendar": SEVEN_DAY_PLAN,
        "banner_webp_url": banner_url,
        "voiceover_mp3_url": audio_url,
        "video_mp4_url": video_url,
        "deliverable_html_url": html_url,
        "deliverable_json_url": json_url,
        "created_at_utc": now_iso,
    }

    html_content = build_html_dossier(
        order_id=order_id,
        banner_url=banner_url,
        audio_url=audio_url,
        video_url=video_url,
        created_at_utc=now_iso,
    )
    html_path.write_text(html_content, encoding="utf-8")
    json_path.write_text(json.dumps(deliverable_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_text = (
        "Đã xuất bản Kế hoạch Nội dung 7 Ngày (Thứ Hai -> Chủ Nhật) cho trang Facebook 'Nhung Bản Gốc' (@NhungBanGoc — "
        "Kênh Thương hiệu cá nhân của Nhân viên Sale EYC): Gồm 7 bài viết chiều sâu, 7 kịch bản Reels 9:16, 7 concept hình ảnh/carousel, "
        "phễu thu Lead B2B (Zalo OA+CRM+AI, Early Years Circle, Phần mềm 9 giai đoạn, Lộ trình 90 ngày) kèm Poster .webp, Voice .mp3 & Video .mp4."
    )

    with brain._connect() as conn:
        conn.execute("DELETE FROM ceo_work_orders WHERE order_id = ?;", (order_id,))
        conn.execute(
            """
            INSERT INTO ceo_work_orders (
                order_id, campaign_id, department_id, phase_number,
                task_title, sop_instructions, kpi_target_json, assigned_weapons,
                status, deliverable_summary, kpi_achieved_json,
                approval_status, director_feedback, deliverable_json, created_at_utc, updated_at_utc
            )
            VALUES (?, 'EYC_CORE', '04_content', 1, ?, ?, '{"posts": 7, "reels": 7}', ?, 'WAITING_APPROVAL', ?, '{"posts": 7, "reels": 7}', 'PENDING_APPROVAL', ?, ?, ?, ?);
            """,
            (
                order_id,
                "Kế Hoạch Bài Đăng 1 Tuần (7 Ngày) Cho Trang Facebook Nhung Bản Gốc (@NhungBanGoc — Sale EYC)",
                "Kết hợp 4 trụ cột: Thương hiệu cá nhân Sale EYC + Storytelling/Vlog + Tư vấn giải pháp EYC (Early Years Circle, Zalo OA+CRM+AI, Phần mềm 9 giai đoạn) + Cảm hứng nguyên bản.",
                "EYC Content Studio, Social Calendar, OpenMontage",
                summary_text,
                "Soạn bài đăng 1 tuần cho trang https://www.facebook.com/NhungBanGoc/ (Kênh của nhân viên Sale EYC)",
                json.dumps(deliverable_payload, ensure_ascii=False),
                now_iso,
                now_iso,
            ),
        )
        conn.execute(
            """
            INSERT INTO eyc_interview_logs (
                log_id, department_id, interaction_mode, director_input,
                agent_response, deliverable_json, status, created_at_utc
            )
            VALUES (?, '04_content', 'TASK_EXECUTION', ?, ?, ?, 'WAITING_APPROVAL', ?);
            """,
            (
                "ilog_nhungbangoc_7d",
                "Soạn bài đăng 1 tuần (7 ngày) cho trang https://www.facebook.com/NhungBanGoc/ (Kênh nhân viên Sale EYC)",
                summary_text,
                json.dumps(deliverable_payload, ensure_ascii=False),
                now_iso,
            ),
        )

    print("SUCCESS:", order_id, "->", html_url)


if __name__ == "__main__":
    main()
