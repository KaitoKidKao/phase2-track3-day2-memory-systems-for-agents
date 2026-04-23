# Ngày 17 — Memory Systems for Agents

> Tại sao agent của bạn quên mọi thứ sau mỗi conversation — và làm sao fix nó đúng cách với Cognitive Memory Model.

**Đối tượng:** Tài liệu nội bộ dành cho giảng viên, lab coach, và TA.

---

## Tổng quan buổi học

```text
SÁNG — Lecture (4h)                     CHIỀU — Lab (4h)
┌──────────────────────────┐            ┌──────────────────────────┐
│ Context Engineering      │            │ Implement Memory Backend │
│ Cognitive Memory Model   │     →      │ Build Memory Router      │
│ LangGraph Code Deep-Dive │            │ Context Trim Strategies  │
│ Privacy (GDPR/Mem0/Zep)  │            │ Benchmark & Evaluation   │
└──────────────────────────┘            └──────────────────────────┘
```

**Lecture** đi sâu vào lý do Agent bị giới hạn bởi context window và cách giải quyết bằng kiến trúc Cognitive Memory Model (Short-term, Long-term, Episodic, Semantic). Giới thiệu cách setup LangGraph Memory State và vấn đề thiết kế privacy-by-design.

**Lab** yêu cầu học viên tự tay code hệ thống Multi-Memory Agent kết hợp giữa Redis (Long-term) và ChromaDB (Semantic). Sau đó đo lường hiệu năng bằng tập dữ liệu conversation mẫu.

---

## Nguyên tắc chung (Trọng tâm Giai đoạn 2)

1. **Hiểu rõ giới hạn Token Limit** — Token = Tiền và Tốc độ. Đẩy quá nhiều data vào Context Window gây nhiễu và đắt đỏ.
2. **Memory phải lấy đúng lúc** — Lưu vào Database không quan trọng bằng việc Retrieval đúng fact khi nào cần.
3. **Phân loại vai trò DB** — Không dùng Vector DB lưu Preference, không dùng SQL lưu Trajectory.
4. **Viết code có kiến trúc (Clean Code/LangGraph)** — Bài thực hành code phức tạp hơn giai đoạn 1, đòi hỏi logic route chặt chẽ.

---

## Tài liệu

### Giảng viên → [`instructor/`](instructor/)

| File | Mô tả |
|------|-------|
| [day02-memory-systems-for-agents.tex](instructor/day02-memory-systems-for-agents.tex) | Nguồn file slide (LaTeX Beamer) |
| [day02-memory-systems-for-agents.pdf](instructor/day02-memory-systems-for-agents.pdf) | Bản trình chiếu Slide (dùng khi lên lớp) |
| [day02-instructor-notes.md](instructor/day02-instructor-notes.md) | Talking script guide — nội dung nói từng block, case study, Q&A thường gặp |
| [day02-reference-document.md](instructor/day02-reference-document.md) | Tài liệu đọc thêm (Deep dive: Token Math, Zep/Mem0 architecture) |

### Lab Coach / TA → [`lab-coach/`](lab-coach/)

| File | Mô tả |
|------|-------|
| [day02-lab-01-coach-guide.md](lab-coach/day02-lab-01-coach-guide.md) | Guide chính — Mốc code check, lỗi hay gặp với LangGraph/Redis, stress-test questions |

### Chấm điểm → [`assessment/`](assessment/)

| File | Mô tả |
|------|-------|
| [day02-assess-01-rubric-guidance.md](assessment/day02-assess-01-rubric-guidance.md) | Tiêu chí chấm mã nguồn Lab và Benchmark Report |

---

## Flow buổi lab (4h)

```text
Phase 0  WORKED EXAMPLE         30 min   GV chạy thử Code mẫu — Học viên review logic architecture
Phase 1  MOCK DATA SETUP        30 min   Cá nhân: Lên nội dung test (Fake user history, FAQ doc)
Phase 2  MEMORY BACKEND         60 min   Nhóm: Khởi tạo Storage Connections (Buffer, Redis, Chroma)
         ─── Break ───          10 min
Phase 3  MEMORY ROUTER          60 min   Nhóm: Viết điều phối logic retrieve() để gom context
Phase 4  BENCHMARK & METRICS    40 min   Nhóm: Chạy script so sánh Token/Thời gian (No-Memory vs Full-Memory)
Phase 5  REFLECTION             10 min   Thu bài + Wrap up
```

---

## Mục tiêu học viên

Cuối buổi, mỗi nhóm/cá nhân phải:
- [ ] Cấu hình thành công 2 dạng Storage (Redis cho profile, Chroma cho external knowledge).
- [ ] Implement hàm Router với chức năng Auto-trim tự giới hạn (Token limit cap).
- [ ] Chạy thành công chuỗi >50 multi-turn chat mà Agent vẫn trả lời đúng Context cá nhân (không hit context limit văng lỗi).
- [ ] Có bảng so sánh Metrics và đưa ra Report.
