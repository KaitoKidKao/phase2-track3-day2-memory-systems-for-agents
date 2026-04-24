# Benchmark Report — Lab #17: Multi-Memory Agent

**Học viên:** Nguyễn Trí Cao
**Ngày thực hiện:** 24/04/2026  
**Mục tiêu:** So sánh hiệu quả của Agent khi có và không có hệ thống Multi-Memory (Short-term, Long-term, Episodic, Semantic).

---

## Bảng so sánh 10 Multi-turn Conversations

| # | Scenario (Kịch bản) | No-Memory Result | With-Memory Result | Pass? | Category |
|:---|:---|:---|:---|:---|:---|
| 1 | Recall user name after 6 turns | Không biết | Nhớ đúng tên (Alex) | Pass | Profile Recall |
| 2 | Allergy conflict update | Trả lời sai (Sữa bò) | Trả lời đúng (Đậu nành) | Pass | Conflict Update |
| 3 | Recall previous daily activity | Không biết | Nhớ được đi biển ngắm hoàng hôn | Pass | Episodic Recall |
| 4 | Retrieve FAQ (Docker install) | Trả lời chung chung | Trả lời đúng các bước từ Chroma | Pass | Semantic |
| 5 | Mixed Memory (Sci-fi + Moon) | Quên genre sách | Nhớ cả genre sách và Neil Armstrong | Pass | Mixed |
| 6 | Hobby Recall (Tennis) | Gợi ý bừa | Gợi ý đi chơi Tennis | Pass | Profile Recall |
| 7 | Multi-turn Context (Python Decorators) | Quên ngữ cảnh Python | Nhớ đang nói về Decorators trong Python | Pass | Short-term |
| 8 | Technical Summary | Thiếu chi tiết | Tổng hợp đúng các bước kỹ thuật | Pass | Semantic |
| 9 | Privacy/Consent (Password) | Trả lời/Lưu trữ PII | Cảnh báo về bảo mật/Consent | Pass | Privacy |
| 10| Token Budget Stress Test | Trôi mất thông tin đầu | Vẫn giữ được Profile nhờ 4-level trim | Pass | Token Budget |

---

## Phân tích kết quả chi tiết (Detailed Metrics)

Dựa trên kết quả chạy từ `scripts/benchmark.py`:

| Tham số (Metric) | With Memory (Avg) | Without Memory (Avg) | Improvement (%) |
|:---|:---:|:---:|:---:|
| **Response Relevance** | **2.53 / 5.0** | 1.00 / 5.0 | **+153.3%** |
| **Token Usage per Turn** | 89.13 tokens | 75.44 tokens | +18.14% (Trade-off) |
| **Memory Hit Rate** | **60.0%** | 0.0% | N/A |
| **Est. Cost per 1k Turns** | ~$0.013 | ~$0.011 | +$0.002 |
| **Recall Accuracy** | **High** | None | N/A |

### Nhận xét các tham số:
1.  **Độ liên quan (Relevance):** Tăng trưởng vượt bậc (+153.3%). Khi không có memory, Agent hoàn toàn không biết gì về thông tin cá nhân. Với Multi-memory, Agent trả lời có căn cứ và cá nhân hóa cao.
2.  **Lượng Token (Token Usage):** Tăng nhẹ 18.14%. Đây là sự đánh đổi (trade-off) tất yếu khi chúng ta gửi thêm các đoạn "Memory Snippets" vào context window. Tuy nhiên, mức tăng này là rất nhỏ so với giá trị thông tin mang lại.
3.  **Tỷ lệ Hit Rate (60%):** Cho thấy router đã hoạt động hiệu quả trong việc nhận diện đúng khi nào cần truy xuất bộ nhớ.
4.  **Chi phí (Cost):** Với model `gpt-4o-mini`, chi phí tăng thêm không đáng kể (khoảng 0.002$ cho mỗi 1000 lượt chat), cực kỳ tối ưu cho sản phẩm thực tế.

## Kết luận
Hệ thống Multi-Memory không chỉ giúp Agent "thông minh" hơn mà còn duy trì được sự nhất quán trong suốt cuộc hội thoại. Logic xử lý xung đột (Conflict Handling) giúp hệ thống luôn cập nhật thông tin mới nhất từ người dùng, đáp ứng hoàn hảo yêu cầu của Lab 17.

---
