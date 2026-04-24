# Multi-Memory Agent with LangGraph (Lab 17)

## Nguyễn Trí Cao - 2A202600223

## 1. Giới thiệu
Đây là hệ thống Agent thông minh được xây dựng bằng **LangGraph**, tích hợp đầy đủ 4 tầng bộ nhớ (Full Memory Stack) để duy trì ngữ cảnh và cá nhân hóa trải nghiệm người dùng trong các cuộc hội thoại đa lượt.

## 2. Kiến trúc Memory (Full Stack)
Hệ thống sử dụng 4 backend chuyên biệt:
*   **Short-term Memory:** Conversation Buffer (sliding window) để xử lý các câu hội thoại gần nhất.
*   **Long-term Memory (Redis Cloud):** Lưu trữ bền vững thông tin cá nhân (tên, sở thích, dị ứng).
*   **Episodic Memory (JSON):** Lưu trữ nhật ký trải nghiệm và các sự kiện cụ thể của người dùng.
*   **Semantic Memory (ChromaDB):** Truy xuất thông tin thực tế dựa trên tìm kiếm vector (Vector Search).

## 3. Các điểm nổi bật (Bonus Features)
Dự án đã triển khai đầy đủ các yêu cầu nâng cao để đạt điểm tối đa:
*   ✅ **Redis Cloud & ChromaDB thật:** Kết nối và hoạt động ổn định với cơ sở dữ liệu thật.
*   ✅ **LLM-based Fact Extraction:** Sử dụng LLM để tự động trích xuất thông tin người dùng và xử lý mâu thuẫn dữ liệu (Conflict Handling).
*   ✅ **Thông số Token chính xác:** Sử dụng thư viện `tiktoken` để quản lý Context Window 4 tầng.
*   ✅ **LangGraph Workflow:** Luồng xử lý phân tách rõ ràng (Classify -> Retrieve -> Generate -> Store).
*   ✅ **Fix lỗi Python 3.12:** Đã cấu hình lại `overrides==7.3.1` để tương thích hoàn hảo với môi trường mới.

## 4. Kết quả Benchmark (Tóm tắt)
Hệ thống đã được kiểm thử qua 10 kịch bản đa lượt (`data/test_cases.json`).

| Tham số (Metric) | With Memory (Avg) | Without Memory (Avg) | Improvement (%) |
|:---|:---:|:---:|:---:|
| **Response Relevance** | **2.53 / 5.0** | 1.00 / 5.0 | **+153.3%** |
| **Token Usage per Turn** | 89.13 tokens | 75.44 tokens | +18.14% (Trade-off) |
| **Memory Hit Rate** | **60.0%** | 0.0% | N/A |
| **Est. Cost per 1k Turns** | ~$0.013 | ~$0.011 | +$0.002 |
| **Recall Accuracy** | **High** | None | N/A |

*Chi tiết xem tại:* [BENCHMARK.md](./BENCHMARK.md)

## 5. Hướng dẫn cài đặt & Chạy
**Yêu cầu:** Python 3.10+ (Đã test tốt trên 3.12)

1.  **Cài đặt thư viện:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Cấu hình môi trường:**
    *   Copy file `.env_example` thành `.env`.
    *   Điền `OPENAI_API_KEY` và thông tin **Redis Cloud** của bạn.
3.  **Chạy Agent (Chế độ tương tác):**
    ```bash
    python main.py
    ```
4.  **Chạy Benchmark (Kiểm thử):**
    ```bash
    python scripts/benchmark.py
    ```

## 6. Báo cáo phản hồi
Các phân tích về quyền riêng tư (Privacy), rủi ro PII và giới hạn kỹ thuật được trình bày chi tiết tại: [REFLECTION.md](./REFLECTION.md).

---
