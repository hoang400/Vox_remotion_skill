# Hướng Dẫn Cộng Đồng — Skill VOX Remotion cho Muse AI (v2.1)

Gói skill tự chứa 100% (không phụ thuộc ngữ cảnh cũ), giúp bạn tạo video ngắn phong cách báo chí giải thích kiểu **VOX** (`1080x1920`, `60fps`) hoàn toàn bằng code Remotion trên **Muse AI (`https://muse.ai`)** — **0% VEO 3**, không cần biết lập trình.

---

## 1. Trong file `vox-remotion-muse-skill.zip` có gì? (9 file gọn trong thư mục `vox-remotion/`)
- `vox-remotion/SKILL.md` — Luật đạo diễn, 4 thành phần prompt, quy trình 6 bước & cổng kiểm tra QA.
- `vox-remotion/VOX_COMPONENTS_RECIPES.md` — Công thức dựng giấy xé, halftone, Polaroid, highlight dạ quang, phụ đề từng từ.
- `vox-remotion/VOX_GITHUB_REPOS.md` & `.json` — Danh sách thư viện mã nguồn mở thay thế VEO 3.
- `vox-remotion/README_CONG_DONG.md` — Tài liệu hướng dẫn nhanh này.
- `vox-remotion/tools/fetch_real_assets.py` — Script CLI tải ảnh Public Domain/CC từ NASA & Wikimedia Commons.
- `vox-remotion/tools/cutout_maker.py` — Script CLI tách nền, halftone, khung giấy xé, Polaroid & nền báo.
- `vox-remotion/tools/make-sfx.py` — Script tổng hợp 7 hiệu ứng SFX giấy, shutter, whoosh, chime.
- `vox-remotion/tools/update-timeline.py` — Script CLI tự tạo `src/timeline.ts` đồng bộ phụ đề từng từ khi đổi giọng.

---

## 2. Cách nạp Skill trên Muse AI Web (`https://muse.ai`) — Khuyên dùng 100%

> **Lưu ý quan trọng:** Bản web `https://muse.ai` chạy trên máy ảo Linux đám mây riêng và thanh bên trái **không có mục "Skills"**. Bạn không cần chạy lệnh `Copy-Item` trên Windows.

1. Mở `https://muse.ai` → bấm dấu **`+`** cạnh dòng **`Đoạn chat phụ`** ở cột danh sách chat bên trái để tạo luồng sạch.
2. Bấm nút **`+` (`Đính kèm file`)** ở góc trái thanh **`Nhắn tin`** → chọn thẳng file **`vox-remotion-muse-skill.zip`**.
3. Gửi lệnh nạp 1 lần (chỉ rõ giải nén vào thư mục riêng và xác nhận đủ 9 file):

```text
Hãy giải nén file vox-remotion-muse-skill.zip vào thư mục ~/workspace/custom-skills/ (unzip -o ... -d ~/workspace/custom-skills/), liệt kê đủ 9 file trong vox-remotion/, đọc kỹ SKILL.md và xác nhận đã sẵn sàng trước khi mình gửi yêu cầu dựng video.
```

---

## 3. Tư duy viết Prompt 4 Thành Phần (Áp dụng cho MỌI chủ đề)

Đừng chỉ gõ 1 câu chung chung kiểu *"Làm video VOX về phim X giúp mình"* — AI sẽ dễ bịa số liệu và cắt cảnh rời rạc. Hãy luôn xây Prompt đủ **4 thành phần**:

1. **Mục tiêu & Gọi đúng Skill:** Chỉ rõ dùng skill `vox-remotion` vừa nạp + đối tượng khán giả.
2. **Nguồn dữ liệu thật (`Nguồn:`):** Dán đường link bài viết uy tín (Wikipedia, NASA, báo chính thống...) để Muse trích số liệu cứng, **0% tự bịa**.
3. **Góc khai thác (`Ý tưởng:`):** Ghi rõ điểm Hook gây tò mò + 3–4 luận điểm chính muốn làm nổi bật (thay vì nêu tên chủ đề chung chung).
4. **Ràng buộc Đầu ra & Kiểm tra QA:** Chốt tỉ lệ khung hình (`1080x1920`), thời lượng (`~45s`), giọng đọc (`edge-tts` tiếng Việt hoặc file thu sẵn) và **yêu cầu Muse chụp ảnh QA từng cảnh để bạn duyệt trước khi render MP4**.

### Ví dụ áp dụng đầy đủ:
```text
Áp dụng skill VOX Remotion vừa nạp trong ~/workspace/custom-skills/vox-remotion/ để dựng video giải thích cho khán giả phổ thông.
Nguồn: https://www.nasa.gov/mission/apollo-11/
Ý tưởng: Giải mã chuyến bay Apollo 11 (1969) — Hook bằng máy tính dẫn đường AGC yếu hơn cả cục sạc hiện đại, so sánh lực đẩy tên lửa Saturn V, khoảnh khắc hạ cánh Eagle và 3 con số ấn tượng nhất.
Đầu ra: Dọc 1080x1920, 60fps, ~45 giây, giọng đọc tiếng Việt rõ nhịp + phụ đề từng từ. Chụp ảnh QA từng beat cho mình duyệt trước khi render MP4.
```

---

## 4. Tùy chọn cho người dùng Local / Agent CLI
Nếu bạn dùng Remotion local trên máy cá nhân (Node.js 20+, FFmpeg, Python 3.10+), chỉ cần giải nén `vox-remotion-muse-skill.zip` vào thư mục skill của công cụ và gọi các script trong `vox-remotion/tools/` bằng `--help` để xem tham số.
