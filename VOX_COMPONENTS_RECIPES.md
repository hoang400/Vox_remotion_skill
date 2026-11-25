# VOX Components Recipes — 7 hiệu ứng giấy cắt tái sử dụng (Remotion + TSX)

> Mỗi recipe gồm: mô tả ngắn + code TSX chạy được + cách dùng. Copy vào `src/components/` là dùng ngay. Khổ chuẩn 1080x1920, 60fps. Palette: giấy kem `#F2ECE1`/`#E6DEC8`, bảng tối `#132124`, băng keo `#C3B284`, dạ quang `#F5C542`, đỏ đất `#C9573C`, xanh STK `#0098F8`. Font: `'Segoe UI', Roboto, Arial`.
>
> Quy ước chung: mọi recipe dùng `useCurrentFrame()` + `spring()` của Remotion, kẹp 2 đầu mọi `interpolate` bằng `extrapolateLeft: "clamp", extrapolateRight: "clamp"`. Component cần frame tuyệt đối (như `WordTagCaptions`) đặt **ngoài** `<Sequence>`.

---

## 1. PaperDefs — hạt giấy + mép rách (SVG filter)

**Mô tả:** Định nghĩa 2 SVG filter dùng chung cho toàn bộ video: `#paper` (hạt giấy fractalNoise) và `#torn` (mép rách displacement). Render 1 lần ở gốc composition, mọi component khác chỉ việc gọi `filter: url(#paper)` / `clipPath` mép rách. Không có filter này thì "giấy" trông như hình chữ nhật phẳng.

```tsx
import React from "react";

/** Đặt 1 lần ở đầu Composition, bên trong <AbsoluteFill>. */
export const PaperDefs: React.FC = () => (
  <svg width="0" height="0" style={{ position: "absolute" }} aria-hidden>
    <defs>
      {/* Hạt giấy: nhiễu fractal nhẹ, phủ lên nền/mảng giấy */}
      <filter id="paper" x="0%" y="0%" width="100%" height="100%">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.9"
          numOctaves="2"
          result="noise"
        />
        <feColorMatrix
          in="noise"
          type="matrix"
          values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.06 0"
        />
        <feComposite operator="over" in2="SourceGraphic" />
      </filter>
      {/* Mép rách: bóp méo viền bằng turbulence tần số thấp */}
      <filter id="torn" x="-5%" y="-5%" width="110%" height="110%">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.015 0.09"
          numOctaves="3"
          seed="7"
          result="warp"
        />
        <feDisplacementMap in="SourceGraphic" in2="warp" scale="14" />
      </filter>
    </defs>
  </svg>
);
```

**Cách dùng:**

```tsx
<AbsoluteFill style={{ background: "#F2ECE1", filter: "url(#paper)" }}>
  <PaperDefs />
  {/* ...các scene... */}
</AbsoluteFill>
```

---

## 2. TapeBanner — dải băng keo dán chéo

**Mô tả:** Dải băng keo mờ `#C3B284` dán chéo 1 góc của thẻ giấy, xoay nhẹ và "dán xuống" bằng spring khi scene vào. Hiệu ứng giấy thật nằm ở độ trong suốt + viền rách nhẹ.

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const TapeBanner: React.FC<{
  width?: number;
  rotate?: number;
  top?: number;
  left?: number;
}> = ({ width = 220, rotate = -8, top = -18, left = 40 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const drop = spring({ frame, fps, config: { damping: 14, stiffness: 120 } });
  const opacity = interpolate(drop, [0, 1], [0, 0.85], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        position: "absolute",
        top,
        left,
        width,
        height: 56,
        background: "rgba(195, 178, 132, 0.75)",
        transform: `rotate(${rotate}deg) translateY(${(1 - drop) * -30}px)`,
        opacity,
        boxShadow: "0 2px 6px rgba(0,0,0,0.18)",
        filter: "url(#torn)",
      }}
    />
  );
};
```

**Cách dùng:** đặt bên trong thẻ giấy (`position: relative`), chỉnh `top/left/rotate` để băng keo đè lên mép thẻ.

---

## 3. ChapterBar — thanh chương 5 chương

**Mô tả:** Thanh chương ở đầu mỗi beat: số chương lớn + tên chương + vạch tiến độ chạy theo frame. Giúp người xem biết mình đang ở đâu trong video (đặc trưng phong cách VOX explainer).

```tsx
import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const CHAPTERS = [
  "Bìa báo",
  "Hồ sơ phim",
  "Gargantua",
  "Số liệu",
  "Miller",
  "Oscar",
  "Tổng kết",
];

export const ChapterBar: React.FC<{
  chapterIndex: number; // 0-based
  from: number; // frame bắt đầu beat
  durationInFrames: number;
}> = ({ chapterIndex, from, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = interpolate(
    frame,
    [from, from + durationInFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return (
    <div style={{ position: "absolute", top: 150, left: 72, right: 72 }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
        <span
          style={{
            fontFamily: "'Segoe UI', Roboto, Arial, sans-serif",
            fontSize: 64,
            fontWeight: 900,
            color: "#C9573C",
          }}
        >
          {String(chapterIndex + 1).padStart(2, "0")}
        </span>
        <span
          style={{
            fontFamily: "'Segoe UI', Roboto, Arial, sans-serif",
            fontSize: 34,
            fontWeight: 700,
            color: "#132124",
            textTransform: "uppercase",
            letterSpacing: 2,
          }}
        >
          {CHAPTERS[chapterIndex]}
        </span>
        <span style={{ marginLeft: "auto", fontSize: 28, color: "#13212499" }}>
          {chapterIndex + 1} / {CHAPTERS.length}
        </span>
      </div>
      <div
        style={{
          height: 6,
          background: "#13212422",
          marginTop: 12,
          borderRadius: 3,
        }}
      >
        <div
          style={{
            width: `${progress * 100}%`,
            height: "100%",
            background: "#0098F8",
            borderRadius: 3,
          }}
        />
      </div>
    </div>
  );
};
```

**Cách dùng:** 1 `<ChapterBar>` mỗi beat, truyền `chapterIndex` (0–6) và khung frame của beat. Đặt trong `Sequence` của beat, hoặc truyền `from` tuyệt đối khi đặt ngoài Sequence.

---

## 4. WordTagCaptions — phụ đề thẻ giấy rách, khớp từng từ

**Mô tả:** Phụ đề word-timed: mỗi "trang" 1–3 từ hiện trên thẻ giấy rách ở vùng đáy (1530..1690px), từ nổi bật highlight màu `#0098F8` + scale 1.04. **Bắt buộc đặt ngoài `<Sequence>`** (cần frame tuyệt đối). **Chống mất chữ:** khi 2 trang kề nhau < 0,23s, chọn trang có opacity cao nhất trong các trang khớp — không dùng `find()` lấy trang đầu tiên (trang cũ đang fade-out có opacity 0 sẽ làm caption biến mất ~11 frame).

```tsx
import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type WordCue = {
  word: string;
  start: number; // giây
  end: number; // giây
  highlight?: boolean;
};

/** Gom các từ liên tiếp thành trang 1-3 từ (đã làm sẵn trong timeline.ts). */
export type CaptionPage = {
  words: WordCue[];
  start: number;
  end: number;
};

export const WordTagCaptions: React.FC<{ pages: CaptionPage[] }> = ({
  pages,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // Tìm TẤT CẢ trang đang khớp tại thời điểm t, tính opacity từng trang,
  // rồi chọn trang có opacity cao nhất (chống mất chữ khi 2 trang kề < 0.23s).
  let best: { page: CaptionPage; opacity: number } | null = null;
  for (const page of pages) {
    if (t < page.start || t > page.end) continue;
    const fadeIn = interpolate(t, [page.start, page.start + 0.08], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const fadeOut = interpolate(t, [page.end - 0.08, page.end], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const opacity = Math.min(fadeIn, fadeOut);
    if (!best || opacity > best.opacity) best = { page, opacity };
  }
  if (!best) return null;

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: 1530,
        height: 160,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        opacity: best.opacity,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          background: "#F2ECE1",
          filter: "url(#torn)",
          padding: "18px 34px",
          display: "flex",
          gap: 14,
          boxShadow: "0 4px 14px rgba(0,0,0,0.18)",
        }}
      >
        {best.page.words.map((w, i) => (
          <span
            key={i}
            style={{
              fontFamily: "'Segoe UI', Roboto, Arial, sans-serif",
              fontSize: 56,
              fontWeight: 900,
              color: w.highlight ? "#0098F8" : "#081D31",
              transform: w.highlight ? "scale(1.04)" : undefined,
              display: "inline-block",
            }}
          >
            {w.word}
          </span>
        ))}
      </div>
    </div>
  );
};
```

**Cách dùng:**

```tsx
// Trong Root/Composition — NGOÀI mọi <Sequence>:
<WordTagCaptions pages={CAPTION_PAGES} />
```

---

## 5. HighlighterSweep — vệt dạ quang quét qua từ khóa

**Mô tả:** Vệt dạ quang `#F5C542` quét ngang qua một từ/cụm từ (kiểu bút highlight), chạy theo frame bằng `interpolate` trên `scaleX` với `transformOrigin: left`. Dùng để nhấn fact quan trọng trong beat.

```tsx
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const HighlighterSweep: React.FC<{
  children: React.ReactNode;
  /** frame bắt đầu quét (tương đối trong Sequence) */
  startFrame?: number;
  /** số frame để quét xong */
  sweepFrames?: number;
  fontSize?: number;
}> = ({ children, startFrame = 10, sweepFrames = 25, fontSize = 64 }) => {
  const frame = useCurrentFrame();
  const sweep = interpolate(
    frame,
    [startFrame, startFrame + sweepFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return (
    <span
      style={{
        position: "relative",
        display: "inline-block",
        fontFamily: "'Segoe UI', Roboto, Arial, sans-serif",
        fontSize,
        fontWeight: 900,
        color: "#081D31",
        padding: "0 10px",
      }}
    >
      <span
        style={{
          position: "absolute",
          inset: "12% -4%",
          background: "rgba(245, 197, 66, 0.65)",
          transform: `scaleX(${sweep})`,
          transformOrigin: "left center",
          zIndex: 0,
        }}
      />
      <span style={{ position: "relative", zIndex: 1 }}>{children}</span>
    </span>
  );
};
```

**Cách dùng:** bọc quanh cụm từ cần nhấn, vd `<HighlighterSweep>1 giờ = 7 năm</HighlighterSweep>`.

---

## 6. PaperBarChart — biểu đồ cột cắt giấy + số đếm nhảy

**Mô tả:** Biểu đồ cột phong cách giấy cắt: mỗi cột là mảnh giấy rách (`filter: url(#torn)`) mọc lên bằng spring, số liệu trên đầu cột đếm nhảy từ 0 tới giá trị thật theo frame. Dùng cho beat số liệu (doanh thu, kinh phí, lượt render...).

```tsx
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export type BarDatum = {
  label: string;
  value: number;
  unit?: string;
  color?: string;
};

export const PaperBarChart: React.FC<{
  data: BarDatum[];
  maxValue: number;
  height?: number;
}> = ({ data, maxValue, height = 520 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        gap: 36,
        height,
        padding: "0 72px",
      }}
    >
      {data.map((d, i) => {
        const grow = spring({
          frame: frame - i * 8,
          fps,
          config: { damping: 16, stiffness: 90 },
        });
        const shown = Math.round(
          interpolate(grow, [0, 1], [0, d.value], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        );
        return (
          <div
            key={d.label}
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 12,
            }}
          >
            <span
              style={{
                fontFamily: "'Segoe UI', Roboto, Arial, sans-serif",
                fontSize: 52,
                fontWeight: 900,
                color: "#081D31",
              }}
            >
              {shown}
              {d.unit ?? ""}
            </span>
            <div
              style={{
                width: "100%",
                height: Math.max(8, (d.value / maxValue) * (height - 140) * grow),
                background: d.color ?? "#0098F8",
                clipPath:
                  "polygon(0% 1%, 24% 0%, 50% 2%, 78% 0%, 100% 1%, 99% 34%, 100% 68%, 99% 100%, 72% 99%, 44% 100%, 16% 99%, 0% 100%, 1% 65%, 0% 30%)",
              }}
            />
            <span
              style={{
                fontFamily: "'Segoe UI', Roboto, Arial, sans-serif",
                fontSize: 30,
                fontWeight: 700,
                color: "#132124",
              }}
            >
              {d.label}
            </span>
          </div>
        );
      })}
    </div>
  );
};
```

**Cách dùng (beat Oscar + doanh thu):**

```tsx
<PaperBarChart
  maxValue={800}
  data={[
    { label: "Kinh phí", value: 165, unit: "M$", color: "#C3B284" },
    { label: "Doanh thu", value: 782, unit: "M$", color: "#0098F8" },
  ]}
/>
```

---

## 7. BlackHoleRings — vòng sáng Gargantua nhiều lớp

**Mô tả:** Hố đen Gargantua phong cách giấy cắt: đĩa đen ở giữa + nhiều vòng sáng đồng tâm (`#F5C542` trong, `#0098F8` ngoài) xoay chậm ngược chiều nhau, kèm quầng sáng mờ. Thuần CSS/SVG, không cần Three.js. Vòng xoay bằng `interpolate` tuyến tính theo frame — càng nhiều lớp, càng có chiều sâu.

```tsx
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const BlackHoleRings: React.FC<{ size?: number }> = ({
  size = 560,
}) => {
  const frame = useCurrentFrame();
  const slow = interpolate(frame, [0, 3600], [0, 360], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ring = (r: number, color: string, width: number, reverse = false) => ({
    position: "absolute" as const,
    width: r,
    height: r,
    borderRadius: "50%",
    border: `${width}px solid ${color}`,
    transform: `rotate(${reverse ? -slow : slow}deg)`,
  });
  return (
    <div
      style={{
        position: "relative",
        width: size,
        height: size,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* Quầng sáng ngoài */}
      <div
        style={{
          position: "absolute",
          width: size,
          height: size,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(245,197,66,0.35) 0%, rgba(0,152,248,0.12) 55%, transparent 70%)",
        }}
      />
      {/* Vòng sáng nhiều lớp, xoay ngược chiều */}
      <div style={ring(size * 0.92, "#0098F8", 10)} />
      <div style={ring(size * 0.78, "#F5C542", 16)} />
      <div style={ring(size * 0.66, "#C9573C", 6, true)} />
      {/* Đĩa đen Gargantua + viền sáng mỏng */}
      <div
        style={{
          width: size * 0.52,
          height: size * 0.52,
          borderRadius: "50%",
          background: "#0B0F14",
          border: "6px solid #F5C542",
          boxShadow: "0 0 60px rgba(245,197,66,0.55)",
          zIndex: 2,
        }}
      />
    </div>
  );
};
```

**Cách dùng:** đặt làm hero visual giữa beat Gargantua, kèm `TapeBanner` + tiêu đề "HỐ ĐEN ĐÚNG VẬT LÝ NHẤT MÀN ẢNH". Có thể bọc trong `<div style={{ transform: "perspective(1400px) rotateX(12deg)" }}>` để tạo chiều sâu.

---

## 8. StopMotion & Parallax (`sm`, `drift`) — rung giấy 12fps + chiều sâu 3 lớp

**Mô tả:** Tạo cảm giác "giấy sống" chuẩn VOX TikTok: rung vi mô bậc thang `12fps` (`Math.floor(frame / 5) * 5` trên timeline `60fps`) và trượt 3 lớp chiều sâu (`0.25x` nền / `0.7x` ảnh giữa / `1.0x` tem & dây chỉ).

```tsx
import { interpolate } from "remotion";

export const sm = (f: number): number => Math.floor(f / 5) * 5;

export const drift = (f: number, amp: number, speed = 0.02): number =>
  Math.sin(sm(f) * speed) * amp;

export const enter = (f: number, start: number, dur = 12): number =>
  interpolate(f, [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
```

---

## 9. StageBackdrops (`BgGrid`, `BgManila`, `BgBlueprint`) — nền tràn khung từ frame 0

**Mô tả:** Phủ kín 100% khung hình ngay từ `local frame 0` (không bao giờ để nền trống chờ VO). Tránh dùng SVG `feTurbulence` lên nền lớn — dùng CSS grid/gradient hoặc ảnh `newspaper_bg.jpg` kèm lớp chữ HTML sắc nét.

```tsx
export const BgGrid: React.FC<{ frame: number }> = ({ frame }) => (
  <div
    style={{
      position: "absolute",
      inset: -30,
      background: "#F2ECE1",
      transform: `translate(${drift(frame, 8)}px, ${drift(frame, 5, 0.013)}px)`,
    }}
  >
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundImage:
          "linear-gradient(rgba(0,152,248,0.13) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(0,152,248,0.13) 1.5px, transparent 1.5px), linear-gradient(rgba(201,87,60,0.35) 2px, transparent 2px)",
        backgroundSize: "54px 54px, 54px 54px, 100% 270px",
        backgroundPosition: "0 0, 0 0, 0 120px",
      }}
    />
  </div>
);
```

---

## 10. PushPin & RedThread — đinh ghim 3D & dây chỉ đỏ nối chứng cứ

**Mô tả:** Tự vẽ đường dây chỉ đỏ SVG nối giữa các ảnh Polaroid / chứng cứ bằng `pathLength={1000}` + `strokeDashoffset` kẹp 2 đầu.

```tsx
export const Pin: React.FC<{ style?: React.CSSProperties }> = ({ style }) => (
  <div
    style={{
      position: "absolute",
      width: 30,
      height: 30,
      borderRadius: "50%",
      background: "radial-gradient(circle at 35% 30%, #E87A5F, #C9573C 55%, #8E3323)",
      boxShadow: "0 4px 8px rgba(8,29,49,0.45)",
      zIndex: 5,
      ...style,
    }}
  />
);

export const RedThread: React.FC<{
  frame: number;
  start: number;
  points: string;
  width?: number;
  height?: number;
  style?: React.CSSProperties;
}> = ({ frame, start, points, width = 600, height = 300, style }) => {
  const p = enter(frame, start, 22);
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      style={{ position: "absolute", overflow: "visible", zIndex: 4, ...style }}
    >
      <polyline
        points={points}
        fill="none"
        stroke="#C9573C"
        strokeWidth={5}
        strokeLinecap="round"
        strokeLinejoin="round"
        pathLength={1000}
        strokeDasharray={1000}
        strokeDashoffset={1000 * (1 - p)}
        opacity={0.9}
      />
    </svg>
  );
};
```

---

## 11. RubberStamp — con dấu mực đỏ kèm micro-shake

**Mô tả:** Dập con dấu nghiêng `-8deg` đúng từ khóa VO, rung nhẹ `12fps` khi vừa chạm mặt giấy.

```tsx
export const Stamp: React.FC<{
  frame: number;
  start: number;
  label: string;
  style?: React.CSSProperties;
}> = ({ frame, start, label, style }) => {
  if (frame < start) return null;
  const p = enter(frame, start, 6);
  const shake = frame < start + 12 ? Math.sin(sm(frame) * 1.7) * 2.5 * (1 - p) : 0;
  return (
    <div
      style={{
        position: "absolute",
        border: "5px solid #C9573C",
        borderRadius: 10,
        color: "#C9573C",
        fontWeight: 900,
        fontSize: 44,
        letterSpacing: 2,
        padding: "10px 22px",
        transform: `rotate(-8deg) scale(${interpolate(p, [0, 1], [1.7, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}) translateX(${shake}px)`,
        background: "rgba(242,236,225,0.35)",
        whiteSpace: "nowrap",
        zIndex: 6,
        ...style,
      }}
    >
      {label}
    </div>
  );
};
```

---

## Ghi chú lắp ráp & Quy tắc hiệu năng

- **Perf Guard bắt buộc:** Tuyệt đối **không** gắn SVG `filter: "url(#torn)"` (`feTurbulence` / `feDisplacementMap`) lên ảnh PNG, thẻ lớn hoặc nền — chỉ dùng cho tag nhỏ. Dùng CSS `clipPath` polygon hoặc ảnh PNG cắt sẵn từ `tools/cutout_maker.py`.
- Thứ tự render trong 1 beat: `PaperDefs` (gốc) → Backdrop `0.25x` (`BgGrid`/`BgManila`/`BgBlueprint`/`BgNewspaper`) → Cutouts & Polaroid `0.7x` → `RedThread` / `Pin` / `Stamp` `1.0x` → `ChapterBar` + `TapeBanner` → `WordTagCaptions` (ngoài Sequence, cấp composition).
- Font chữ: khai báo 1 lần ở root — `fontFamily: "'Segoe UI', Roboto, Arial, sans-serif"`, không dùng Inter đứng đầu.
- Kiểm chứng sau khi lắp: render still từng beat, xem trực tiếp — đặc biệt kiểm tra `backfaceVisibility` (không dùng chung với `rotateY > 90°`) và caption không biến mất ở chỗ 2 trang kề nhau.
