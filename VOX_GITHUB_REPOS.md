# VOX GitHub Repos — Repo tham chiếu cho pipeline video VOX paper-cut

> Toàn bộ link dưới đây đã được kiểm chứng bằng `curl -I -L` ngày **2026-11-18**. Trạng thái ghi theo kết quả kiểm chứng thực tế. Cùng dữ liệu ở dạng machine-readable: xem `VOX_GITHUB_REPOS.json`.

## Bảng repo

| # | Repo | Mô tả ngắn | Vai trò trong pipeline | Trạng thái (18/11/2026) |
|---|---|---|---|---|
| 1 | [0xS4N4TG/papercut-explainer](https://github.com/0xS4N4TG/papercut-explainer) | Repo tham chiếu phong cách paper-cut explainer — cách cắt, dán, xếp lớp giấy thành video giải thích | **Tham chiếu phong cách chính**: học cách dựng cảnh giấy cắt, bố cục lớp giấy, chuyển động "dán giấy" | ✅ OK 200 |
| 2 | [cyberlesterr/paper-collage-video](https://github.com/cyberlesterr/paper-collage-video) | Repo tham chiếu video collage giấy — kỹ thuật ghép ảnh giấy, texture, mép rách | **Tham chiếu kỹ thuật collage**: texture giấy, mép rách, cách xếp lớp collage không rối | ✅ OK 200 |
| 3 | [Vincentwei1021/anything2explainer](https://github.com/Vincentwei1021/anything2explainer) | Công cụ biến "bất cứ nguồn nào" thành video giải thích — ý tưởng pipeline tự động từ nguồn → video | **Tham chiếu pipeline**: mô hình "nhận nguồn → ra video giải thích" mà cơ chế 2 ô nhập liệu của skill này học theo | ✅ OK 200 |
| 4 | [cooperchx/paper-cutout-story](https://github.com/cooperchx/paper-cutout-story) | Repo tham chiếu kể chuyện bằng paper-cutout — nhịp kể chuyện, phân cảnh theo beat | **Tham chiếu kể chuyện**: cách chia câu chuyện thành beat/cảnh, nhịp chuyển cảnh giấy | ✅ OK 200 |
| 5 | [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | Skill tư duy chuyển động: timing, easing, 12 nguyên tắc Disney | **Bước 1 — Skills**: chuẩn timing/easing cho mọi chuyển động trong video | ✅ OK 200 |
| 6 | [remotion-dev/skills](https://github.com/remotion-dev/skills) | Skill chính thức viết video Remotion | **Bước 4 — Code**: skill chính thức để viết code Remotion đúng chuẩn | ✅ OK 200 |
| 7 | [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) | Bộ công cụ xử lý audio/video chuẩn công nghiệp | **Bước 6 — Export**: ghép âm thanh, phụ đề, xuất MP4 (H.264 + AAC) | ✅ OK 200 |
| 8 | [Openverse API](https://api.openverse.org/v1/) | API tìm nhạc & hiệu ứng âm thanh miễn phí, không cần key (CC0/CC-BY) | **Bước 5 — Sound**: nhạc nền + SFX giấy miễn phí, có giấy phép rõ ràng | ✅ OK 200 |
| 9 | [rany2/edge-tts](https://github.com/rany2/edge-tts) | Thư viện text-to-speech miễn phí dùng giọng Microsoft Edge (có giọng Việt NamMinh, HoaiMy) | **Bước 5 — Voice**: voiceover miễn phí, xuất MP3 + timestamps word-timed | ✅ OK 200 |

## Ghi chú kiểm chứng

- **Phương pháp:** `curl -s -o /dev/null -w "%{http_code}" -I -L --max-time 20 <url>` cho từng link, ngày 2026-11-18.
- **Kết quả:** 9/9 link trả về **HTTP 200 OK**, không redirect lỗi, không link chết.
- **Lưu ý thực tế:**
  - **Freesound CDN chặn tải trực tiếp** từ máy này (403) — SFX giấy nên tự tổng hợp bằng Python/numpy hoặc lấy từ Openverse, đừng tốn thời gian thử Freesound.
  - **edge-tts trên sandbox:** proxy egress là MITM chặn TLS — cần nối CA `/run/hatch/egress-tls/ca-bundle.pem` vào bundle certifi của venv, và dùng client socket thô (xem `SKILL.md` bước 5) thay vì CLI trực tiếp.
  - Repo 1–4 là **repo tham chiếu ý tưởng/phong cách**, không phải thư viện cài đặt — đọc để học, không cần `npm install`.
