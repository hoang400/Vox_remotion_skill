VOX Remotion — Hướng dẫn sử dụng skill
Skill làm video giải thích phong cách VOX bằng giấy cắt (paper-cut), dựng 100% bằng code Remotion, 0% VEO 3, không tốn tiền render AI video.
Bạn chỉ cần gửi 2 ô, còn lại AI làm hết.

1. Bạn cần gửi gì?
Chỉ 2 dòng:
Nguồn: <link bài báo / video / tài liệu gốc>
Ý tưởng: <chủ đề video muốn làm>
Ví dụ thật đã chạy:
Nguồn: https://tuoitre.vn/vanh-dai-3-tphcm-vao-chang-cuoi-dien-mao-tuyen-phia-dong-da-ro-net-100260810234359736.htm
Ý tưởng: 3 nút vàng Nhơn Trạch - Tân Vạn - Long Thành
Nguồn: phải là link hoặc tài liệu thật, còn truy cập được. Link chết thì báo lại, không tự bịa.
Ý tưởng: là chủ đề, góc nhìn, đối tượng xem. Nếu bạn chưa có ý tưởng cụ thể, nhờ AI gợi ý 3 ý rồi bạn chọn 1.
Thiếu 1 trong 2 ô, AI sẽ hỏi lại đúng ô đó.
Bạn cũng nên nói thêm (không bắt buộc):
Độ dài mong muốn (mặc định 30–60 giây)
Khổ dọc 1080x1920 (mặc định) hay ngang 1920x1080
Giọng đọc: giọng miễn phí hay file ElevenLabs bạn gửi
Có hiện giá hay không (mặc định: không hiện giá)

2. AI làm gì sau khi nhận 2 ô? — Quy trình 6 bước
Bước 1 — Nghiên cứu nguồn, trích fact cứng
AI đọc kỹ nguồn, chỉ lấy fact có trong nguồn:
số liệu, ngày tháng, tên người, tên địa danh. Số nào chưa chắc thì bỏ, không bịa, không "ước chừng" rồi ghi như fact.
Gom fact thành 5–7 nhóm ý — mỗi nhóm thành 1 beat.
Bước 2 — Chia kịch bản thành 5–7 beats + viết VO
Mỗi beat 4–8 giây, 1 ý chính duy nhất.
Viết lời thoại ngắn gọn, tốc độ đọc tự nhiên ~160–220 từ/phút.
  Ví dụ: video ~46 giây cần ~170 từ.
Chia VO thành word cues: từng từ + thời gian bắt đầu/kết thúc, để phụ đề khớp từng từ.
File timeline chuẩn là src/timeline.ts (PHASE_FRAMES + WORD_CUES + VOICE_FILE).
3 luật viết kịch bản (bắt buộc, cập nhật 2026-11-25):
Hook 1–3 giây đầu: câu đầu tiên phải là câu hỏi, con số sốc, hoặc nghịch lý.
   Không mở đầu chung chung kiểu "Hôm nay chúng ta sẽ tìm hiểu...".
Viết lại, không đọc lại nguồn: giữ nguyên fact cứng và số liệu, nhưng viết lại
   bằng giọng kể, thêm so sánh, đào sâu "vì sao fact này quan trọng". Không đọc nguyên văn bài báo.
Giữ chân từng beat: cuối mỗi beat (trừ beat cuối) để lại 1 câu mở / câu hỏi /
   con số hé lộ khiến người xem muốn xem beat sau. **Mỗi câu hook / giữ chân đều phải có
   1 visual riêng đi kèm, không để chữ trơ trọi.**
Bước 3 — Chuẩn bị ảnh + lắp component
Thác nguồn ảnh 4 tầng, ưu tiên hợp pháp bản quyền:
Ảnh bạn gửi kèm (nếu có).
Ảnh Public Domain / Creative Commons từ NASA Images API và Wikimedia Commons,
   tải bằng tools/fetch_real_assets.py, lưu bản quyền vào SOURCES.json.
Đạo cụ minh họa tĩnh trên nền trắng (không tạo chữ trên ảnh AI).
Xử lý bằng tools/cutout_maker.py thành PNG nền trong suốt, Polaroid, viền giấy xé.
Tuyệt đối không dùng VEO 3 tạo video. Ảnh nào không đúng thực tế thì chú thích
chỉ ghi địa danh, không ghi sai thành địa danh khác.
Bố cục theo VOX_COMPONENTS_RECIPES.md (11 recipe): nền giấy, nền blueprint,
Polaroid, sợi chỉ đỏ, con dấu, wipe giấy chuyển beat, biểu đồ cột, timeline, caption word-timed.
Luật reveal (bản v4 trở đi):
Đầu beat chỉ có tiêu đề + nền, ảnh/thẻ số chỉ hiện khi giọng đọc tới đúng đoạn đó,
  kèm hiệu ứng (rơi xuống, đóng dấu, trượt vào, nảy lên).
Riêng ảnh hero của beat 1 hiện ngay từ frame 0, cùng lúc với hook.
Chuyển beat có wipe giấy, không cắt cứng.
Bước 4 — Giọng đọc + phụ đề + SFX
Giọng miễn phí — edge-tts:
vi-VN-HoaiMyNeural (nữ) / vi-VN-NamMinhNeural (nam).
Giọng ElevenLabs — bạn gửi file MP3:
Gửi MP3 (tốt nhất 7 file beat-1.mp3…beat-7.mp3, 1 file full cũng được),
  kèm tên giọng + Voice ID, timestamps JSON nếu có.
Không gửi API key ElevenLabs trong chat.
Script dán vào ElevenLabs phải BỎ nhãn "Beat 1:" — nếu không giọng sẽ đọc
  cả nhãn thành tiếng, phải cắt bỏ sau.
Đổi giọng chỉ cần: file mp3 mới vào public/audio/ + timestamps JSON +
  chạy lại tools/update-timeline.py — không sửa component.
Kiểm tra file giọng trước khi làm timeline (bắt buộc):
File có đủ toàn bộ kịch bản không? Đếm từ + đo thời lượng trước.
  File Hoàng Anh v4 từng thiếu gần hết beat 7, chỉ còn "bản đồ mới của khu Đông".
Số liệu có đọc đúng không? Kiểm tra bằng Whisper, không tin bản auto-transcript trong chat.
Từ Whisper nghe nhầm ("giải" thay "dải", "Nhân Trạch" thay "Nhơn Trạch") phải đối chiếu
  với kịch bản gốc và sửa trong dữ liệu caption — không để máy tự quyết.
Phụ đề word-timed: thẻ giấy rách 1–3 từ, hiện theo từng từ giọng đọc.
SFX giấy (0 đồng): whoosh, click, pop, chime — chạy python3 tools/make-sfx.py.
Bước 5 — QA stills (bắt buộc, trước khi render MP4)
Render ảnh tĩnh mỗi beat 2 ảnh: 1 ảnh đầu beat + 1 ảnh giữa beat, xem trực tiếp bằng mắt.
Ảnh đầu beat chứng minh reveal chưa lộ sớm; ảnh giữa beat chứng minh hình đã hiện đủ, không tràn chữ, không ngắt dòng, không chồng caption.
npx tsc --noEmit = 0 lỗi là chưa đủ — tsc không bắt được lỗi layout.
Sửa lỗi xong phải render lại ảnh đó và xem lại, rồi mới đi tiếp.
Bước 6 — Render MP4 + kiểm chứng
npx remotion render <CompositionId> out/<ten-file>.mp4
Khổ 1080x1920, 60fps, H.264 + AAC.
Kiểm tra file MP4 thật bằng ffprobe (độ dài, fps, codec) + trích vài frame từ chính file MP4 ra xem lại, không chỉ tin frame preview.
Đặt tên file MP4 mới cho mỗi bản, không ghi đè bản cũ. Đặt tên file giọng mới cho mỗi giọng, không dùng chung tên file.

3. Quy chuẩn bắt buộc
Hạng mục
Quy chuẩn
Video AI
0% VEO 3 — thuần code Remotion 100%
Khổ hình
1080x1920 dọc (9:16), 60fps. Ngang: 1920x1080
Font
Segoe UI, Roboto, Arial — không dùng Inter đứng đầu
Màu
Giấy kem #F2ECE1, bảng tối #132124, băng keo #C3B284, dạ quang #F5C542, đỏ đất #C9573C, xanh STK #0098F8
Safe Area
Chừa vùng trên/dưới/phải — không để UI TikTok/Reels che chữ
Bố cục
Tối đa 3 lớp/cảnh: tiêu đề 2 dòng trên + 1 hero visual giữa + phụ đề 1–4 từ dưới
Giá tiền
Không hiện giá trừ khi bạn yêu cầu
Fact
Chỉ dùng fact có trong nguồn hoặc kiểm chứng được, không bịa số

4. File trong skill
File
Nội dung
SKILL.md
Quy trình 6 bước + thác nguồn ảnh + quy chuẩn (file này là luật chính)
README.md
Hướng dẫn sử dụng này
VOX_COMPONENTS_RECIPES.md
11 recipe TSX (Paper, StopMotion 12fps, Backdrops, RedThread, Stamp...)
tools/fetch_real_assets.py
Tải ảnh PD/CC thật từ NASA Images & Wikimedia Commons API
tools/cutout_maker.py
Tách nền trắng, halftone báo B&W, Polaroid & viền giấy xé
tools/make-sfx.py
Tổng hợp SFX giấy miễn phí bằng numpy
tools/update-timeline.py
Sinh src/timeline.ts tự động từ JSON timestamps
VOX_GITHUB_REPOS.md / .json
Bảng repo tham chiếu
README_CONG_DONG.md
Cài skill trong 1 phút + ví dụ mẫu

5. Checklist trước khi bàn giao
Đủ 2 ô Nguồn + Ý tưởng, link nguồn còn sống
Mọi fact trên màn hình đều có nguồn, số liệu không bịa
Kịch bản đã viết lại (sinh động, sâu sắc), không đọc nguyên văn nguồn
1–3 giây đầu có hook (câu hỏi / con số sốc / nghịch lý), không mở đầu chung chung
Mỗi beat (trừ beat cuối) có câu giữ chân sang beat sau
Mỗi câu hook / giữ chân có visual riêng đi kèm
Audio thật đã render trước khi khóa timeline, word cues khớp từng nhịp
File giọng đã kiểm tra đủ toàn bộ kịch bản, số liệu đọc đúng
Caption đã đối chiếu từng từ với kịch bản gốc
tsc --noEmit = 0 lỗi
QA stills đủ 7 beats (2 ảnh/beat), đã xem bằng mắt, đã sửa lỗi
MP4 render thật đã kiểm tra bằng ffprobe + trích frame
Không có chữ nào bị Safe Area / UI TikTok che, không đè dấu tiếng Việt

6. Các lỗi hay gặp — đã rút ra từ thực tế
Dùng chung tên file cho các giọng khác nhau → app phát nhầm bản cũ trong cache.
   Mỗi giọng 1 tên file riêng, có ngày tháng.
F0 trung vị giống nhau không chứng minh cùng giọng → phải kiểm tra sóng âm
   mẫu-chính-xác, tương quan > 0,99 mới kết luận.
Tin mù Whisper → từ nghe nhầm lọt vào caption ("giải" thay "dải").
   Đối chiếu từng từ caption với kịch bản gốc.
Script gửi ElevenLabs còn nhãn "Beat 1:" → giọng đọc cả nhãn thành tiếng.
   Bỏ hết nhãn beat trước khi dán.
Không kiểm tra file giọng đủ kịch bản → beat cuối bị cụt.
   Đếm từ + đo thời lượng trước khi làm timeline.
Chỉ tin tsc 0 lỗi → vẫn lọt lỗi layout, tràn chữ, ngắt dòng.
   Chỉ có xem ảnh QA bằng mắt mới bắt được.
Hiệu ứng pop (spring) overshoot ~10% → element sát vùng caption có thể chạm
   caption trong ~0,3 giây đầu reveal. Với element đó dùng fade thay vì pop.
Element nằm ngoài Reveal → lộ sớm ở frame đầu beat.
   Mọi element phải nằm trong Reveal, reveal gắn vào word-timing, không hard-code frame.

7. Ví dụ chạy thật
Nguồn: https://en.wikipedia.org/wiki/Interstellar_(film)
Ý tưởng: Giải mã phim INTERSTELLAR (2014) — hố đen Gargantua, giãn thời gian, Oscar & doanh thu
→ Video 46,6 giây, 2800 frames, 7 beats:
Bìa báo, 2. Hồ sơ phim, 3. Hố đen Gargantua, 4. Số liệu render,
Giãn thời gian Miller, 6. Oscar + doanh thu, 7. Tổng kết + CTA.
