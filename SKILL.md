# VOX Remotion — Skill làm video giải thích phong cách VOX bằng giấy cắt (paper-cut)

> **Skill cộng đồng cho Muse AI.** Chỉ cần nhập 2 ô — **Nguồn:** và **Ý tưởng:** — là có video giải thích kiểu VOX, dựng 100% bằng code Remotion, **0% VEO 3**, không tốn tiền render AI video.

---

## 2 Ô NHẬP LIỆU — cơ chế hoạt động

Thành viên cộng đồng **không cần biết code**. Chỉ cần gửi đúng 2 dòng:

```
Nguồn: <link bài báo / video / tài liệu gốc — vd bài báo khoa học, Wikipedia, YouTube>
Ý tưởng: <chủ đề video muốn làm — vd "Giải mã hố đen Gargantua trong Interstellar">
```

Muse AI nhận 2 ô này rồi tự chạy toàn bộ quy trình 6 bước dưới đây. Nếu thiếu 1 trong 2 ô, Muse hỏi lại đúng ô còn thiếu, không tự bịa nguồn.

**Ví dụ chạy thật (project mẫu):**

```
Nguồn: https://en.wikipedia.org/wiki/Interstellar_(film)
Ý tưởng: Giải mã phim INTERSTELLAR (2014) — hố đen Gargantua, giãn thời gian, Oscar & doanh thu
```

→ Kết quả: video 46,6 giây, 2800 frames, 7 beats, xem được ngay trên Remotion Studio.

---

## Quy trình chuẩn 6 bước

### Bước 1 — Nhận 2 ô nhập liệu

- Đọc `Nguồn:` — phải là link hoặc tài liệu thật, truy cập được. Nếu link chết, báo lại và xin nguồn khác, **không tự bịa**.
- Đọc `Ý tưởng:` — chủ đề, góc nhìn, đối tượng xem (vd: người chưa xem phim, học sinh, fan khoa học).
- Thống nhất với người dùng trước khi làm tiếp: độ dài video (mặc định 30–60s), khổ dọc 1080x1920 hay ngang 1920x1080.

### Bước 2 — Nghiên cứu nguồn + trích fact cứng có số liệu

- Đọc kỹ nguồn, trích **fact cứng**: số liệu, ngày tháng, tên người, tên giải thưởng, con số so sánh.
- Mỗi fact ghi rõ nguồn gốc (trang nào, đoạn nào) để đối chiếu.
- **Quy tắc:** chỉ dùng fact có trong nguồn hoặc kiểm chứng được từ nguồn uy tín khác. Không bịa số liệu, không "ước chừng" rồi ghi như fact. Số nào chưa chắc thì bỏ, hoặc ghi rõ "chưa xác minh".
- Gom fact thành 5–7 nhóm ý — mỗi nhóm sẽ thành 1 beat.

**Ví dụ fact cứng từ project Interstellar (đã kiểm chứng):**

| Fact | Số liệu |
|---|---|
| Phim ra mắt | 2014, đạo diễn Christopher Nolan |
| Hố đen Gargantua | mô phỏng theo phương trình của Kip Thorne |
| Render Gargantua | tối đa ~100 giờ/frame, ~800 TB dữ liệu mô phỏng |
| Giãn thời gian hành tinh Miller | 1 giờ trên Miller = 7 năm trên Trái Đất |
| Oscar | 1 tượng vàng — Hiệu ứng hình ảnh xuất sắc nhất (Oscar 2015) |
| Kinh phí / doanh thu | ~165 triệu USD / hơn 782 triệu USD toàn cầu |

### Bước 3 — Chia kịch bản thành 5–7 beats + viết VO word-timed

- Chia thành **5–7 beats**, mỗi beat 4–8 giây, 1 ý chính duy nhất.
- Viết lời thoại VO (voiceover) ngắn gọn: tốc độ đọc tự nhiên ~160–220 từ/phút (tiếng Việt câu ngắn rõ nhịp). Ví dụ video ~46 giây chuẩn nhịp: ~170 từ (~45 giây giọng đọc). **Đọc thử audio thật trước rồi mới khóa timeline (`PHASE_FRAMES`).**
- Mỗi beat gồm: tiêu đề beat, lời VO, fact hiển thị trên màn hình, component dùng (xem `VOX_COMPONENTS_RECIPES.md`). Nếu biểu đồ có cột so sánh minh họa tương quan (không phải số liệu cứng từ nguồn), ghi chú rõ `(minh họa)` trong code và báo cáo QA.
- Chia VO thành **word cues**: từng từ + thời gian bắt đầu/kết thúc (giây), để phụ đề khớp từng từ. File timeline chuẩn nằm ở `src/timeline.ts` (single source of truth: `PHASE_FRAMES` + `WORD_CUES` + `VOICE_FILE`).
- 7 beats mẫu của project Interstellar (46,67 giây, 2800 frames @ 60fps):
  1. **Bìa báo** — hook: "Một bộ phim khiến cả giới vật lý phải ngả mũ."
  2. **Hồ sơ phim** — 2014, Nolan, Kip Thorne.
  3. **Hố đen Gargantua** — hố đen "đúng vật lý" nhất màn ảnh.
  4. **Số liệu render** — ~100 giờ/frame, ~800 TB dữ liệu.
  5. **Giãn thời gian Miller** — 1 giờ = 7 năm.
  6. **Oscar + doanh thu** — 1 Oscar VFX, ~165M kinh phí / hơn 782M USD doanh thu.
  7. **Tổng kết + CTA** — công thức 2 ô nhập liệu & Follow STK Tech.

### Bước 4 — Chuẩn bị Ảnh Cutout Mixed-Media + Lắp Component VOX (0% VEO 3)

- **Thác nguồn ảnh 4 tầng (không tự bịa, ưu tiên hợp pháp bản quyền):**
  1. Ảnh/tư liệu do người dùng gửi kèm (nếu có).
  2. Ảnh Public Domain / Creative Commons từ **NASA Images API** (`images-api.nasa.gov`) & **Wikimedia Commons API** (`commons.wikimedia.org/w/api.php`) qua script `tools/fetch_real_assets.py` (tự xuất `SOURCES.json` lưu bản quyền).
  3. Tạo đạo cụ minh họa tĩnh sạch trên nền trắng `#FFFFFF` (như đồng hồ cổ, cuộn băng từ, cúp vòng nguyệt quế — **không tạo chữ trên ảnh AI**) bằng `media.generate_image` (tuyệt đối **không** dùng `VEO 3` tạo video).
  4. Xử lý tất cả bằng `tools/cutout_maker.py` (`Pillow` + `numpy`) để tạo **PNG nền trong suốt, ảnh báo halftone B&W, khung Polaroid có băng keo và viền giấy xé trắng/đỏ (`#F4EFE6` + `#C9573C`)**. Chữ tiêu đề/báo luôn dàn bằng HTML/CSS.
- **Bố cục & Animation Mixed-Media (`VOX_COMPONENTS_RECIPES.md` 11 recipes):**
  - **Nền tràn khung từ `local frame 0`** (`BgGrid`, `BgManila`, `BgBlueprint`, báo nhiều cột): không để nửa màn hình trống trơn chờ tới trigger VO.
  - **3 lớp Parallax + Stop-Motion 12fps:** `sm(f) = Math.floor(f / 5) * 5` tại `60fps`, kết hợp `RedThread`, `Pin`, `Stamp` (micro-shake), và wipe giấy chuyển beat (`@remotion/transitions` hoặc `PaperWipe`).
  - **Perf Guard:** không dùng SVG `filter="url(#torn)"` (`feTurbulence`) lên ảnh/thẻ lớn (dùng `clipPath` / PNG xé sẵn).
- **Bài học xương máu (đã gặp thật):**
  - `useCurrentFrame()` bên trong `<Sequence>` đã là frame tương đối của Sequence — **không trừ thêm điểm bắt đầu**, nếu không scene lật ngược/biến mất.
  - Component cần frame tuyệt đối (vd `WordTagCaptions`) đặt **ngoài** `<Sequence>`.
  - Kẹp 2 đầu mọi `interpolate` chuyển cảnh: `extrapolateLeft: "clamp", extrapolateRight: "clamp"`, nếu không scale âm gây lật hình.
  - Không dùng `backfaceVisibility: hidden` chung với `rotateY > 90°` — element tàng hình.

### Bước 5 — Voice miễn phí + phụ đề word-timed + SFX giấy + QA stills

- **Voice miễn phí — edge-tts** (giọng Việt `vi-VN-HoaiMyNeural` / `vi-VN-NamMinhNeural`, hoặc giọng ElevenLabs nếu người dùng đã có sẵn file mp3 + timestamps JSON):
  - Tốc độ: đo thực tế trên kịch bản mẫu 87 từ — NamMinh mặc định 38,3s; **NamMinh +10% = 34,8s** (khuyên dùng khi cần khớp 35s).
  - Xuất MP3 + VTT + words JSON. Script regenerate timeline CLI: `python3 tools/update-timeline.py --input <words.json> --out src/timeline.ts --voice-file audio/voiceover.mp3 --fps 60 --enable-voice` (hỗ trợ cả format ElevenLabs `{t,s,e,sf,ef}` lẫn Whisper/edge-tts `{word,start,end}`).
  - **Lưu ý môi trường sandbox Muse AI:** Nếu proxy egress chặn TLS của `edge-tts` CLI mặc định, dùng biến môi trường `SSL_CERT_FILE` trỏ vào CA bundle hệ thống hoặc viết WebSocket client ngắn bằng Python kết nối trực tiếp tới edge-tts (hoặc dùng file giọng thu sẵn / ElevenLabs do người dùng đính kèm).
  - Đổi giọng chỉ cần: file mp3 mới vào `public/audio/` + timestamps JSON + chạy lại `tools/update-timeline.py` — **không sửa component**, vì mọi mốc thời gian đã tách ra `src/timeline.ts`.
- **Phụ đề word-timed — `WordTagCaptions`:** thẻ giấy rách 1–3 từ/trang, vùng đáy 1530..1690px (khổ 1080x1920). **Chống mất chữ:** khi 2 trang phụ đề kề nhau < 0,23s, chọn trang có **opacity cao nhất** trong các trang khớp (không dùng `find()` lấy trang đầu — trang cũ đang fade-out có opacity 0 sẽ làm caption biến mất ~11 frame).
- **SFX giấy tự tổng hợp (0 đồng):** whoosh (giấy lướt), click, pop, chime, type — chạy `python3 tools/make-sfx.py` (Python/numpy) hoặc lấy từ Openverse (CC0/CC-BY). Freesound CDN thường bị chặn tải trực tiếp trên sandbox Muse AI — ưu tiên chạy `tools/make-sfx.py` ngay.
- **QA stills (bắt buộc):** render still frame kiểm chứng **mỗi beat** (tối thiểu 7 frame), xem trực tiếp bằng mắt, sửa lỗi thật rồi mới render MP4. `tsc --noEmit` sạch **không đủ** — tsc không bắt được lỗi layout / frame-timing.

### Bước 6 — Render MP4 + đóng gói

- Render: `npx remotion render <CompositionId> out/<ten-file>.mp4` — 1080x1920, 60fps, H.264 + AAC.
- Kiểm tra file MP4 thật: `ffprobe` (độ dài, fps, codec) + trích xuất vài frame từ file MP4 để xem lại, không chỉ tin frame preview.
- Đóng gói bàn giao: `src/` + `package.json` + skill + MP4 (zip). Ghi rõ CompositionId, độ dài, số frames, dung lượng file.

---

## Quy chuẩn bắt buộc

| Hạng mục | Quy chuẩn |
|---|---|
| Video AI | **0% VEO 3** — thuần code Remotion 100% |
| Khổ hình | 1080x1920 dọc (9:16), 60fps. Ngang: 1920x1080 |
| Font | `'Segoe UI'`, Roboto, Arial — **không dùng Inter đứng đầu** |
| Màu | Nền giấy kem `#F2ECE1` / `#E6DEC8`, bảng tối `#132124`, băng keo `#C3B284`, dạ quang `#F5C542`, đỏ đất `#C9573C`, xanh STK `#0098F8` |
| Safe Area | Chừa vùng trên/dưới/phải — không để UI TikTok/Reels che chữ |
| Chống đè dấu tiếng Việt | Chữ tiêu đề/hook in hoa cỡ lớn 120–180px: `marginTop >= 48px`, gạch chân hiệu ứng đặt `bottom <= -56px` |
| Bố cục | Tối đa 3 lớp/cảnh: tiêu đề 2 dòng trên + 1 hero visual giữa + phụ đề 1–4 từ dưới |
| Giá tiền | Zero-Price Mode cho video Ads B2C chạy tin nhắn — không hiện giá trừ khi user yêu cầu |
| Môi trường đích | Remotion 4.x + React 19 + TypeScript (thư mục `src/` trong project Remotion mới) |
| Thư viện có sẵn | `remotion`, `@remotion/transitions`, `@remotion/three`, `@remotion/lottie`, `motion`, `gsap`, `three`, `@react-three/fiber`, `@react-three/drei`, `lottie-web` |

---

## File trong skill này

| File | Nội dung |
|---|---|
| `SKILL.md` | Quy trình 6 bước + thác nguồn ảnh 4 tầng (file này) |
| `VOX_COMPONENTS_RECIPES.md` | 11 recipe TSX (Paper, StopMotion 12fps, Backdrops, RedThread, Stamp...) |
| `tools/fetch_real_assets.py` | Tải ảnh PD/CC thật từ NASA Images & Wikimedia Commons API |
| `tools/cutout_maker.py` | Pillow + numpy tách nền trắng, halftone báo B&W, Polaroid & viền giấy xé |
| `tools/make-sfx.py` | Tổng hợp 6+ SFX giấy miễn phí bằng numpy (không cần Freesound) |
| `tools/update-timeline.py` | Sinh `src/timeline.ts` tự động từ JSON timestamps |
| `VOX_GITHUB_REPOS.md` / `.json` | Bảng repo tham chiếu + trạng thái HTTP 200 OK |
| `README_CONG_DONG.md` | Cài skill trong 1 phút + ví dụ mẫu đầy đủ |

---

## Checklist trước khi bàn giao

- [ ] Đủ 2 ô Nguồn + Ý tưởng, link nguồn còn sống
- [ ] Mọi fact trên màn hình đều có nguồn, số liệu không bịa
- [ ] Audio thật đã render trước khi khóa timeline, word cues khớp từng nhịp
- [ ] Nếu biểu đồ có cột so sánh minh họa tương quan, phải ghi chú rõ `(minh họa)`
- [ ] `tsc --noEmit` (strict) = 0 lỗi
- [ ] QA stills đủ 7 beats, đã xem bằng mắt, đã sửa lỗi
- [ ] MP4 render thật đã kiểm tra bằng ffprobe + trích frame
- [ ] Không có chữ nào bị Safe Area / UI TikTok che, không đè dấu tiếng Việt
