#!/usr/bin/env python3
"""
7-Day Raw, Authentic Vietnamese Facebook Content Plan for "Nhung Bản Gốc" (@NhungBanGoc)
Strict Kaizen Anti-AI-Slop Rules Applied:
- ZERO emoji/icon spam (no 1️⃣, ✅, ❌, 🎁, 🚀, 👇)
- ZERO fake AI openings ("Sáng đầu tuần gặp anh Giám đốc Quận 1...", "Pha ấm trà nóng...")
- ZERO corporate brochure footers, links, or hashtag dumps that kill Facebook reach
- 100% real Vietnamese Facebook voice: short, punchy, candid, conversational, soft-sell.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path("/root/ecosystem")
sys.path.insert(0, str(ROOT_DIR / "second-brain"))
sys.path.insert(0, str(ROOT_DIR / "agents"))
sys.path.insert(0, str(ROOT_DIR / "virtual-office"))

from engine import CorporateSecondBrain
from ceo_hr_orchestrator import HRAgentDirector as HRKaizenAgent
from server import EYC_OFFICIAL_SVG_LOGO as EYC_INLINE_LOGO_SVG, DELIVERABLES_DIR

KAIZEN_ANTI_SLOP_RULE = (
    "[LUẬT CẤM VĂN MẪU AI - BẮT BUỘC CHO PHÒNG 04 CONTENT & 10 SOCIAL]: "
    "1. Tuyệt đối cấm dùng icon rác (1️⃣, ✅, ❌, 🎁, 🚀, 👇, 🧡). "
    "2. Cấm bịa chuyện sến súa kiểu 'Sáng đầu tuần gặp anh Giám đốc Quận 1', 'Tối thứ Bảy pha ấm trà nghe đĩa than'. "
    "3. Cấm chèn chữ ký công ty, địa chỉ, link web và một đống hashtag ở cuối bài (làm tụt reach Facebook). "
    "4. Viết đúng giọng người thật đi làm: câu ngắn, từ đời thường, nhìn thẳng vào vấn đề, kết bài mở tự nhiên không xin comment kiểu bot."
)

SEVEN_DAY_PLAN = [
    {
        "day_code": "THỨ HAI",
        "best_time": "08:15",
        "pillar": "Phá băng & Định vị cá nhân (Tại sao là Nhung Bản Gốc)",
        "format": "Status chữ thuần (Text-only trên nền trắng hoặc kèm 1 ảnh chụp đời thường bằng cam thường tại bàn làm việc)",
        "goal": "Gây ấn tượng đây là tài khoản của người thật, nói thẳng, không màu mè.",
        "hook_headline": "Đi làm ở công ty công nghệ nhưng thứ mình ghét nhất lại là văn mẫu của AI.",
        "post_copy": """Đi làm ở công ty công nghệ nhưng thứ mình ghét nhất lại là văn mẫu của AI.

Mấy nay lướt Facebook đâu cũng thấy những bài viết giống hệt nhau. Mở đầu lúc nào cũng là một câu đạo lý, giữa bài gạch đầu dòng 1-2-3 kèm đủ thứ icon xanh đỏ, cuối bài lại chúc cả nhà một ngày tốt lành. Đọc tới dòng thứ hai là biết không phải người viết.

Khách hàng của mình cũng vậy. Họ là chủ doanh nghiệp, là người quản lý, cả ngày đã đủ thứ việc ngập đầu. Khi họ tìm đến mình để hỏi về làm phần mềm hay tự động hóa, thứ họ cần là một người nghe hiểu đúng chỗ họ đang tắc, nói thẳng cái nào làm được, cái nào tốn tiền vô ích — chứ không phải nghe một bài thuyết trình sáo rỗng.

Lập cái trang Nhung Bản Gốc này cũng chỉ vì muốn giữ lại cái nết đó. Có sao nói vậy, làm được gì kể nấy, sai đâu sửa đó, không phông bạt.

Ở đây có ai cứ thấy tin nhắn tư vấn mà sặc mùi bot trả lời tự động là tắt ngang giống mình không?""",
        "visual_concept": "1 tấm ảnh chụp bằng điện thoại góc bàn làm việc thật: màn hình máy tính đang mở dở tài liệu quy trình, ly cà phê uống dở, không chỉnh màu cầu kỳ.",
        "reels_script_60s": """[Quay cam trước cầm tay vừa đi bộ vừa nói, hoặc ngồi tại bàn làm việc, không nhạc nền giật đùng đùng]
- Câu 1 (0-4s): "Làm ở công ty làm về AI mà thứ mình dị ứng nhất lại là văn mẫu ChatGPT."
- Nội dung (4-30s): "Thật sự luôn. Giờ khách nhắn tin hỏi giải pháp mà bên tư vấn cứ gửi nguyên một sớ văn mẫu dài ngoằng, gạch đầu dòng xanh đỏ là khách người ta ngán tận cổ. Người đi làm việc thật người ta chỉ cần hỏi 3 câu: Hệ thống cũ đang kẹt ở đâu? Sửa mất bao lâu? Và nhân viên có chịu dùng không? Hết."
- Kết (30-40s): "Bởi vậy trên kênh này mình chỉ nói chuyện người thật việc thật thôi, không văn mẫu." """
    },
    {
        "day_code": "THỨ BA",
        "best_time": "12:10",
        "pillar": "Chuyện nghề thực tế — Lỗ hổng quản lý khách qua Zalo cá nhân",
        "format": "Bài kể chuyện ngắn (180 chữ) + 1 ảnh chụp màn hình sơ đồ luồng vẽ tay trên giấy hoặc bảng trắng",
        "goal": "Chạm đúng nỗi đau mất khách của chủ doanh nghiệp nhỏ mà không cần quảng cáo lộ liễu.",
        "hook_headline": "Cách nhanh nhất để mất sạch khách cũ là giao toàn bộ khách cho Zalo cá nhân của nhân viên.",
        "post_copy": """Cách nhanh nhất để mất sạch khách cũ là giao toàn bộ khách cho Zalo cá nhân của nhân viên.

Tuần rồi mình ngồi rà lại quy trình bán hàng cho một bên làm dịch vụ. Chạy quảng cáo một tháng ngốn gần trăm triệu, khách nhắn về rất đều, nhưng doanh thu cứ giậm chân tại chỗ.

Mở ra mới thấy cảnh quen thuộc: khách nhắn trên trang xong, sale xin số rồi kéo hết về Zalo cá nhân để tư vấn cho tiện.

Tiện đâu chưa thấy, chỉ thấy 3 cái khổ:
- Tối 10h khách hỏi giá, sale đi ngủ rồi, sáng hôm sau mới trả lời thì khách đã chuyển khoản cho bên khác.
- Quản lý muốn biết hôm nay có bao nhiêu khách hẹn lịch cũng phải đi hỏi miệng từng đứa.
- Đỉnh điểm là tháng trước có một bạn sale cứng nghỉ việc, mang theo luôn cái sim và toàn bộ danh bạ khách VIP suốt 2 năm. Công ty không còn một dòng lịch sử nào.

Bài toán này thật ra không cần mua phần mềm gì quá đắt đỏ. Chỉ cần gom toàn bộ luồng tin nhắn về một cổng chính thức, nối thẳng vào sổ quản lý khách hàng chung. Đêm hôm khách hỏi cơ bản thì cho hệ thống tự trả lời giữ chân trước, tới khúc chốt giá mới báo về máy cho sale nhảy vào. Nhân sự nào nghỉ thì lịch sử khách vẫn nằm nguyên ở công ty.

Đơn giản vậy thôi mà cứu được cả đống tiền quảng cáo đổ sông đổ biển mỗi tháng.""",
        "visual_concept": "Ảnh chụp tờ giấy A4 hoặc bảng trắng vẽ tay bằng bút lông 2 luồng: Bên trái gạch chéo (Khách -> Zalo cá nhân Sale -> Mất dấu), Bên phải đóng khung (Khách -> Zalo OA chung + Hệ thống lưu trữ -> Sale chỉ việc chốt).",
        "reels_script_60s": """[Ngồi trước bảng trắng hoặc cầm tờ giấy vẽ sơ đồ]
- Mở đầu (0-4s): "Nếu nhân viên sale của bạn nghỉ việc ngày mai, khách cũ thuộc về công ty hay đi theo nhân viên luôn?"
- Thân (4-35s): Chỉ vào tờ giấy phân tích vì sao thói quen kéo khách về Zalo cá nhân làm chủ doanh nghiệp mất quyền kiểm soát dữ liệu và rơi khách ban đêm. Giải thích cách tách bạch: Tài khoản công ty giữ dữ liệu gốc, AI trực ca đêm trả lời câu hỏi lặp lại, còn nhân viên sale chỉ tập trung chốt đơn.
- Kết (35-45s): "Ai đang đau đầu vụ quản lý tin nhắn của sale thì cứ nhắn mình, mình chỉ cho cách gom lại trong 1 nốt nhạc." """
    },
    {
        "day_code": "THỨ TƯ",
        "best_time": "19:45",
        "pillar": "Góc nhìn sản phẩm thực tế — Chuyện ở trường mầm non (Early Years Circle)",
        "format": "Bài viết góc nhìn quan sát thực tế (không nhắc tên sản phẩm ở 3 đoạn đầu)",
        "goal": "Khiến chủ trường mầm non, giáo viên và phụ huynh đồng cảm tuyệt đối và tự hỏi giải pháp.",
        "hook_headline": "4 giờ chiều ở trường mầm non là khung giờ tội nghiệp các cô giáo nhất.",
        "post_copy": """4 giờ chiều ở trường mầm non là khung giờ tội nghiệp các cô giáo nhất.

Đứa thì vừa ngủ dậy quấy khóc, đứa thì tới giờ uống thuốc, ba mẹ thì bắt đầu đứng ngoài cổng đón. Vậy mà tay cô vẫn phải kè kè cái điện thoại để lọc từng tấm ảnh, gõ từng dòng báo cáo xem hôm nay con ăn hết suất không, ngủ được mấy tiếng để gửi vào nhóm lớp cho phụ huynh yên tâm.

Có cô nói thật với mình: "Đi dạy chăm hai chục bé cả ngày không mệt bằng khoản tối về ngồi chép lại sổ điểm danh với trả lời tin nhắn riêng của từng phụ huynh."

Trong khi đó, ở chiều ngược lại, ba mẹ đi làm chỉ muốn mở điện thoại ra là thấy ngay thông tin của đúng con mình, chứ không phải lội ngược hơn trăm tin nhắn thông báo chung trong nhóm lớp để tìm một tấm ảnh của con.

Lúc tụi mình xuống trường làm hệ thống quản lý mầm non, đề bài đặt ra chỉ có một câu: Làm sao để cô giáo chỉ cần bấm chấm điểm danh, bữa ăn, giấc ngủ trên máy tính bảng lớp học trong đúng 1 phút là thông tin tự khắc chạy về điện thoại của riêng từng phụ huynh và bảng tổng hợp của nhà trường.

Bớt đi 30 phút gõ phím vô nghĩa mỗi chiều là các cô có thêm 30 phút trọn vẹn chơi cùng tụi nhỏ trước giờ tan trường.""",
        "visual_concept": "Ảnh chụp thực tế (hoặc góc chụp qua vai) màn hình máy tính bảng giao diện điểm danh cực kỳ tối giản, sạch sẽ, không chèn chữ quảng cáo đè lên ảnh.",
        "reels_script_60s": """[Quay cận cảnh thao tác tay trên màn hình máy tính bảng/điện thoại]
- Mở đầu (0-4s): "Làm sao để cô giáo mầm non không phải ôm điện thoại nhắn tin vào nhóm Zalo suốt buổi chiều?"
- Thân (4-35s): Quay trực tiếp màn hình thao tác: Cô giáo bấm tích chọn bữa ăn/giấc ngủ/uống thuốc đúng 3 chạm trên màn hình lớp -> Mở chiếc điện thoại bên cạnh (đóng vai phụ huynh) nhận thông báo riêng của đúng bé đó ngay lập tức, không làm phiền phụ huynh khác.
- Kết (35-45s): "Trường nào đang muốn bỏ hẳn sổ tay giấy và cảnh trôi tin nhắn nhóm lớp thì nhắn mình gửi bản dùng thử cho các cô bấm thử nhé." """
    },
    {
        "day_code": "THỨ NĂM",
        "best_time": "11:50",
        "pillar": "Thẳng thắn trong nghề — Tại sao nhiều công ty mua phần mềm về rồi bỏ xó?",
        "format": "Status ngắn, sắc, nói thẳng sự thật mất lòng trong ngành làm phần mềm",
        "goal": "Tạo tranh luận sôi nổi dưới phần bình luận từ những người từng đi làm/mua phần mềm.",
        "hook_headline": "80% phần mềm mua về bị nhân viên tìm cách chống đối không chịu dùng.",
        "post_copy": """80% phần mềm mua về bị nhân viên tìm cách chống đối không chịu dùng.

Không phải vì nhân viên lười, mà vì người đi mua phần mềm và người trực tiếp bấm phần mềm mỗi ngày là hai người khác nhau.

Sếp đi mua thì thích nhìn bảng biểu đẹp, nhiều tính năng, cái gì cũng muốn nhét vào. Còn nhân viên ở dưới — từ kế toán, kho cho tới sale — đang làm trên bảng tính mất có 2 thao tác, giờ bắt mở phần mềm mới phải bấm qua 9 bước, điền 15 ô bắt buộc mới lưu được một cái đơn. Thế là được hai tuần, cả phòng rủ nhau quay về làm file cũ, đến cuối tháng mới cử một người ngồi gõ đối phó lên phần mềm cho sếp xem.

Đi tư vấn triển khai cho khách, câu đầu tiên mình luôn hỏi không phải là "Anh muốn làm tính năng gì?", mà là "Cho em ngồi cạnh bạn nhân viên đang làm việc đó nửa buổi xem bạn ấy đang thao tác thế nào."

Quy trình dưới đất chưa gọn mà đã vội đổ bê tông lên phần mềm thì kiểu gì cũng phải đập đi làm lại. Chậm một tuần khảo sát kỹ ở đầu, nhưng đỡ mất cả trăm triệu tiền làm ra một thứ chỉ để trưng.""",
        "visual_concept": "Không cần ảnh, để dạng chữ thuần (Text post) cho nổi bật trên bảng tin, hoặc kèm 1 ảnh chụp cuốn sổ ghi chép tay quy trình thực tế.",
        "reels_script_60s": """[Nói chuyện trực diện, tông giọng điềm tĩnh, dứt khoát]
- Mở đầu (0-4s): "Lý do lớn nhất khiến doanh nghiệp bỏ tiền trăm triệu làm phần mềm xong đắp chiếu là gì?"
- Thân (4-35s): "Là làm phần mềm cho sếp ngắm chứ không phải cho nhân viên dùng. Nhân viên đang làm mất 10 giây, giờ phần mềm bắt nhập 20 trường thông tin mất 5 phút thì họ sẽ tìm mọi cách né. Muốn phần mềm sống được, bước đầu tiên là phải cắt bớt thao tác thừa cho người dùng cuối trước, báo cáo cho sếp tự khắc sinh ra từ đó."
- Kết (35-45s): "Công ty bạn có phần mềm nào mua về mà nhân viên chỉ nhập liệu đối phó không?" """
    },
    {
        "day_code": "THỨ SÁU",
        "best_time": "16:30",
        "pillar": "Chuyện hậu trường đi gặp khách — Khi nào nên từ chối khách hàng?",
        "format": "Bài viết kể lại 1 ca tư vấn thực tế trong tuần",
        "goal": "Xây dựng uy tín cực cao: Một người Sale dám can khách hàng đừng tiêu tiền sai chỗ.",
        "hook_headline": "Hôm nay mình vừa khuyên một khách hàng khoan hãy ký hợp đồng với bên mình.",
        "post_copy": """Hôm nay mình vừa khuyên một khách hàng khoan hãy ký hợp đồng làm AI với bên mình.

Nghe ngược đời với nghề sale, nhưng mình nghĩ làm nghề này muốn đi đường dài thì không được phép thấy khách sẵn tiền là gật.

Khách tìm đến muốn làm một con trợ lý ảo tự động báo giá và lên đơn cho hơn 400 mã hàng. Nhưng khi mình hỏi xin file bảng giá và tồn kho hiện tại, thì 3 bộ phận trong công ty gửi ra 3 file lệch nhau hoàn toàn. Mã hàng bên kho đặt một kiểu, bên kế toán viết một kiểu, giá chiết khấu thì nằm trong sổ tay riêng của trưởng phòng kinh doanh.

Mình nói thẳng với anh chủ: "Dữ liệu gốc của anh đang vênh nhau thế này, giờ tụi em có cắm con AI xịn nhất vào thì nó cũng chỉ báo giá sai với tốc độ nhanh gấp 10 lần con người thôi. Tiền phạt đền đơn còn quá tiền làm phần mềm."

Hai bên thống nhất dừng toàn bộ phần AI lại. Tháng đầu tiên chỉ làm đúng một việc: gom sạch danh mục hàng hóa và bảng giá về một nguồn duy nhất, phân quyền rõ ai được sửa giá, ai chỉ được xem. Khi nào một nguồn dữ liệu đó chạy chuẩn không lệch một đồng, lúc đó cắm tự động hóa vào mới ra tiền.

Làm công nghệ mà cứ thần thánh hóa AI như thuốc tiên là hại khách.""",
        "visual_concept": "Ảnh chụp màn hình một bảng dữ liệu mẫu bị lệch mã hàng (đã che tên công ty) để minh họa trực quan câu chuyện 'dữ liệu rác thì AI cũng chịu'.",
        "reels_script_60s": """[Quay tại bàn làm việc cuối buổi chiều thứ Sáu]
- Mở đầu (0-4s): "Làm sale mà đi khuyên khách khoan hãy mua hàng của mình, nghe dại đúng không?"
- Thân (4-35s): Kể lại câu chuyện khách đòi gắn AI báo giá trong khi bảng giá nội bộ của kho và kế toán còn lệch nhau. Giải thích nguyên tắc sống còn: Dữ liệu có một nguồn chuẩn trước, rồi mới tới tự động hóa.
- Kết (35-45s): "Thà mất một hợp đồng lớn lúc đầu để làm từng bước nhỏ mà chắc, còn hơn nhận bừa rồi cả hai bên cùng mệt." """
    },
    {
        "day_code": "THỨ BẢY",
        "best_time": "20:15",
        "pillar": "Đời sống cá nhân / Góc riêng cuối tuần của Nhung",
        "format": "Bài viết cực ngắn (dưới 100 chữ) + Ảnh đời thường cuối tuần (quán quen, phố xá, âm nhạc)",
        "goal": "Giữ nhịp tương tác tự nhiên với bạn bè trên Facebook, không nói chuyện công việc khô khan vào tối thứ Bảy.",
        "hook_headline": "Cả tuần mở miệng ra là quy trình với dữ liệu, tới tối thứ Bảy chỉ thèm nghe một cái gì đó thật mộc.",
        "post_copy": """Cả tuần mở miệng ra là quy trình với dữ liệu, tới tối thứ Bảy chỉ thèm nghe một cái gì đó thật mộc.

Dạo này mình thích nghe lại mấy bản thu âm cũ hồi xưa, kiểu thu trực tiếp cả ban nhạc trong phòng thu, đôi chỗ tiếng lấy hơi hay tiếng ngón tay miết trên dây đàn vẫn còn nghe rõ mồn một. Nó không tròn trịa hoàn hảo như nhạc chỉnh bằng máy bây giờ, nhưng nghe câu nào thấm câu đó.

Chắc tính mình từ công việc ra tới ngoài đời vẫn vậy, cứ cái gì nguyên bản, thật thà một chút là thích.

Cuối tuần của mọi người sao rồi, có bài nhạc cũ nào nghe hoài mấy năm chưa chán không, cho mình xin tên nghe ké với.""",
        "visual_concept": "Ảnh thật chụp góc quán cà phê acoustic buổi tối, hoặc ảnh màn hình điện thoại đang phát một bản nhạc xưa yêu thích.",
        "reels_script_60s": """[Video ngắn 15-20s quay không gian buổi tối cuối tuần, tiếng nhạc mộc tự nhiên, chèn 2 dòng chữ ngắn trên màn hình: "Tắt máy tính. Trả lại cuối tuần cho những thứ nguyên bản."]"""
    },
    {
        "day_code": "CHỦ NHẬT",
        "best_time": "20:00",
        "pillar": "Chia sẻ tài liệu làm việc thật (Bộ khung rà soát quy trình trước khi làm phần mềm)",
        "format": "Bài chia sẻ kinh nghiệm thực tế + Ảnh chụp trang đầu bộ câu hỏi khảo sát thật mà Nhung hay dùng",
        "goal": "Thu hút những chủ doanh nghiệp đang có nhu cầu thật chủ động nhắn tin trao đổi mà không cần dùng chiêu trò câu comment rẻ tiền.",
        "hook_headline": "Bộ 12 câu hỏi mình luôn dùng để tự kiểm tra xem một công ty đã sẵn sàng làm phần mềm hay chưa.",
        "post_copy": """Bộ 12 câu hỏi mình luôn dùng để tự kiểm tra xem một công ty đã sẵn sàng làm phần mềm hay chưa.

Mỗi lần đi gặp khách hàng mới, trước khi bàn tới chuyện viết code hay báo giá, mình luôn mở đúng trang giấy gồm 12 câu hỏi này ra ngồi rà cùng chủ doanh nghiệp.

Toàn những câu rất cơ bản nhưng nhiều nơi trả lời xong mới giật mình nhận ra lỗ hổng nằm ở đâu:
- Một đơn hàng từ lúc khách hỏi tới lúc thu tiền về đi qua mấy người, ai là người chốt cuối cùng?
- Có bước nào nhân viên đang phải gõ lại cùng một thông tin từ phần mềm này sang phần mềm khác không?
- Nếu ngày mai bạn nhân sự phụ trách khâu đó nghỉ ốm 3 ngày, người khác nhìn vào màn hình có làm thay ngay được không hay phải gọi điện hỏi?
- Bước nào bắt buộc phải có chữ ký hoặc cái gật đầu của sếp mới được chạy tiếp, bước nào cho phép chạy tự động?

Chỉ cần trả lời thật rõ 12 câu này trên giấy, tự khắc bạn sẽ biết ngay công ty mình cần làm cái gì trước, cái gì chưa cần tốn tiền mua, kể cả khi bạn tự làm nội bộ chứ không thuê bên mình.

Mình vừa gõ lại bộ 12 câu hỏi kèm bảng tự chấm điểm này ra một file gọn gàng. Anh chị nào tuần tới đang tính sắp xếp lại quy trình làm việc cho gọn thì cứ nhắn mình gửi file qua cho mà dùng.""",
        "visual_concept": "Ảnh chụp màn hình trực tiếp trang tài liệu Word/Notion trình bày sạch sẽ '12 Câu Hỏi Rà Soát Quy Trình Vận Hành Trước Khi Làm Phần Mềm' (chụp thật, rõ chữ để người đọc đọc thử được 3-4 câu đầu ngay trên ảnh).",
        "reels_script_60s": """[Quay màn hình máy tính đang mở file 12 câu hỏi khảo sát quy trình thực tế]
- Mở đầu (0-4s): "Trước khi bỏ tiền thuê viết phần mềm hay mua công cụ AI, hãy tự trả lời 4 câu hỏi này trên giấy trước đã."
- Thân (4-35s): Chỉ thẳng vào màn hình đọc và giải thích ngắn gọn 4 câu hỏi xương sống giúp chủ doanh nghiệp phát hiện chỗ kẹt trong vận hành.
- Kết (35-45s): "Mình có soạn sẵn trọn bộ 12 câu hỏi này thành một file biểu mẫu rất gọn. Ai cần lấy về tự rà soát cho công ty mình thì nhắn tin cho mình, mình gửi file qua cho nhé." """
    }
]


def build_html_dossier(order_id: str, created_at_utc: str) -> str:
    days_html = []
    for d in SEVEN_DAY_PLAN:
        days_html.append(
            f"""
            <div class="day-card">
              <div class="day-header">
                <div>
                  <span class="day-badge">{d['day_code']}</span>
                  <span class="time-badge">Khung giờ đăng: {d['best_time']}</span>
                </div>
                <span class="pillar-badge">{d['pillar']}</span>
              </div>

              <div class="meta-strip">
                <div><strong>Định dạng hiển thị:</strong> {d['format']}</div>
                <div><strong>Mục tiêu thực tế:</strong> {d['goal']}</div>
              </div>

              <div class="section-label">NỘI DUNG BÀI ĐĂNG FACEBOOK (GIỌNG NGƯỜI THẬT 100% — KHÔNG ICON RÁC, KHÔNG VĂN MẪU AI)</div>
              <pre class="copy-box">{d['post_copy']}</pre>

              <div class="two-col">
                <div class="sub-box">
                  <div class="section-label">HÌNH ẢNH ĐI KÈM (CHỤP THẬT / TỐI GIẢN)</div>
                  <p>{d['visual_concept']}</p>
                </div>
                <div class="sub-box">
                  <div class="section-label">KỊCH BẢN VIDEO NGẮN / REELS NÓI CHUYỆN TRỰC DIỆN</div>
                  <pre class="script-pre">{d['reels_script_60s']}</pre>
                </div>
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
  <title>{order_id} — [Bản Chuẩn Hóa Kaizen] 7 Bài Đăng Thực Chiến Cho Nhung Bản Gốc (@NhungBanGoc)</title>
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
      --ink-2: #E2E8F0;
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
    .container {{ max-width: 1020px; margin: 0 auto; }}
    .dossier-header {{
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-top: 3px solid var(--orange);
      border-radius: 12px;
      padding: 24px 28px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 20px;
      flex-wrap: wrap;
    }}
    .eyc-logo-wrap {{ color: var(--ink); display: flex; align-items: center; gap: 16px; }}
    .dossier-title {{ font-size: 20px; font-weight: 700; margin-top: 12px; color: var(--ink); }}
    .dossier-sub {{ font-family: var(--mono); font-size: 11.5px; color: var(--orange); margin-top: 4px; }}
    .kaizen-banner {{
      background: rgba(254, 94, 2, 0.10);
      border: 1px solid var(--orange);
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 22px;
      font-size: 13px;
      color: var(--ink-2);
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
    .time-badge {{ font-family: var(--mono); font-size: 11.5px; color: var(--ink-2); }}
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
    .copy-box {{
      white-space: pre-wrap;
      font-family: var(--font);
      font-size: 14px;
      color: var(--ink);
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 14px;
      line-height: 1.75;
    }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
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
      line-height: 1.65;
    }}
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
            <div style="font-family:var(--mono);font-size:11px;color:var(--mut);">PHÒNG 04 CONTENT × PHÒNG 10 SOCIAL — BẢN ĐÃ TỐI ƯU KAIZEN</div>
          </div>
        </div>
        <h1 class="dossier-title">7 BÀI ĐĂNG FACEBOOK NGƯỜI THẬT VIỆC THẬT — KÊNH "NHUNG BẢN GỐC" (@NhungBanGoc)</h1>
        <div class="dossier-sub">ĐÃ LOẠI BỎ 100% VĂN MẪU AI, ICON RÁC, HASHTAG RÁC & QUẢNG CÁO LỘ LIỄU</div>
      </div>
      <div style="text-align:right;font-family:var(--mono);font-size:11px;color:var(--mut);">
        <div>MÃ HỒ SƠ: <strong style="color:var(--orange);">{order_id}</strong></div>
        <div>CẬP NHẬT: {created_at_utc}</div>
      </div>
    </div>

    <div class="kaizen-banner">
      <strong style="color:var(--orange);">LUẬT KAIZEN ĐÃ KHÓA VÀO BỘ NÃO EYC (PHÒNG 04 & PHÒNG 10):</strong><br/>
      {KAIZEN_ANTI_SLOP_RULE}
    </div>

    {days_joined}
  </div>
</body>
</html>
"""


def main() -> None:
    brain = CorporateSecondBrain()
    hr = HRKaizenAgent(brain)

    # Record Kaizen lesson into both 04_content and 10_social so they never write AI slop again
    for dept_id in ("04_content", "10_social"):
        hr.evaluate_department_kpi_and_kaizen(
            department_id=dept_id,
            campaign_id="EYC_CORE",
            kpi_achieved={"human_authenticity": 65.0},
            kpi_target={"human_authenticity": 100.0},
            notes=KAIZEN_ANTI_SLOP_RULE,
        )

    order_id = "WO_EYC_NHUNGBANGOC_7DAYS"
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
    html_path = DELIVERABLES_DIR / f"{order_id}.html"
    json_path = DELIVERABLES_DIR / f"{order_id}.json"

    html_url = f"/deliverables/{order_id}.html"
    json_url = f"/deliverables/{order_id}.json"

    deliverable_payload = {
        "type": "NHUNGBANGOC_7DAY_HUMAN_CONTENT",
        "order_id": order_id,
        "kaizen_rule_applied": KAIZEN_ANTI_SLOP_RULE,
        "target_facebook_page": "https://www.facebook.com/NhungBanGoc/",
        "seven_day_calendar": SEVEN_DAY_PLAN,
        "deliverable_html_url": html_url,
        "deliverable_json_url": json_url,
        "created_at_utc": now_iso,
    }

    html_path.write_text(build_html_dossier(order_id, now_iso), encoding="utf-8")
    json_path.write_text(json.dumps(deliverable_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_text = (
        "[Đã Tối Ưu Kaizen — Xóa 100% Văn Mẫu AI & Icon Rác] Bộ 7 bài đăng Facebook giọng người thật đi làm thực tế "
        "cho kênh Nhung Bản Gốc (@NhungBanGoc): Không emoji xanh đỏ, không chèn link/hashtag bóp reach, kể chuyện sắc bén từ thực tế làm nghề."
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
            VALUES (?, 'EYC_CORE', '04_content', 1, ?, ?, '{"posts": 7}', ?, 'WAITING_APPROVAL', ?, '{"posts": 7}', 'PENDING_APPROVAL', ?, ?, ?, ?);
            """,
            (
                order_id,
                "[Bản Chuẩn Người Thật - Không Văn Mẫu AI] 7 Bài Đăng Facebook Cho Kênh Nhung Bản Gốc (@NhungBanGoc)",
                KAIZEN_ANTI_SLOP_RULE,
                "EYC Content Studio, Kaizen Anti-Slop Filter",
                summary_text,
                "Bản trước là rác văn mẫu AI, đã viết lại 100% theo giọng người thật đi làm thực tế và khóa Luật Kaizen.",
                json.dumps(deliverable_payload, ensure_ascii=False),
                now_iso,
                now_iso,
            ),
        )

    print("UPDATED:", order_id, "->", html_url)


if __name__ == "__main__":
    main()
