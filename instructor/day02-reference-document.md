# Tài Liệu Tham Khảo Nâng Cao: Agent Memory Systems
*Dành cho Instructor*

## 1. Context Window vs Memory: Khái niệm kỹ thuật chuyên sâu
- **Context Window** (Giới hạn Ngữ Cảnh) là cửa sổ xử lý tạm thời (RAM) của tính toán LLM. OpenAI GPT-4 hỗ trợ 128K Token, Claude 3 Opus/Sonnet cung cấp khoảng 200K, Gemini 1.5 Pro lên tới 1M-2M Token.
- Với sức chứa khổng lồ này, nhiều người lầm tưởng không cần Database, chỉ cần nhồi tất cả lịch sử ứng dụng vào RAM là xong. Nhưng kiến trúc này mang nhiều nhược điểm chí mạng:
  1. **Độ trễ khủng khiếp (High Latency):** Tính toán đọc/hiểu (Attention Matrix) cho 128K token mất nhiều thời gian, đẩy Time-To-First-Token (TTFT) lên 5-15 giây.
  2. **Chi Phí Tài Chính:** Mức phí tính tiền trả dựa trên số token đầu vào của MỖI request. Dù người dùng chỉ nhập chữ "Hi", bạn vẫn phải trả tiền cho quá trình model đọc lại toàn bộ 128K token lịch sử cũ đó để lấy bối cảnh.
  3. **"Lost in the middle":** Logic thống kê chỉ ra rằng LLMs xuất sắc với dữ liệu xuất hiện ở *Đầu* (First) hoặc *Cuối* đoạn prompt (End), nhưng lại gặp chứng hay quên hoặc ảo giác với thông tin nằm chôn ở giữa (Middle). Vậy nên, nhồi nhét là rủi ro cao.

## 2. Phương pháp Cắt Gọt Ngữ Cảnh (Token-Trim Tactics)
Khi sử dụng LangChain hoặc LangGraph, chúng ta truyền một mảng các đối tượng `Message`. Việc giữ Token Budget dưới 20% yêu cầu phải Cắt Gọt.
- **Buffer Retention / Sliding Window:** Cắt vứt giữ đúng N tin nhắn mới nhất. (Nhanh nhưng rủi ro gây mất ý định gốc).
- **Progressive Summarization:** Dùng mô hình cấp thấp chạy cực lẹ với giá siêu rẻ (như GPT-3.5 hoặc Claude Haiku) để liên tục tóm tắt toàn bộ lịch sử trò chuyện phía xa tít tắp, tạo ra một "chuỗi mô tả dài 200 từ" và chèn vô làm tin nhắn hệ thống (System Message). 

## 3. Phân biệt Thiết Kế Redis và VectorDB
- **User Profile Fact (Redis Hash/Key-Value):** 
  - Tại sao dùng KV Store? Vì nó hữu hiệu khi lưu trữ các "Định danh và Thuộc tính tuyệt đối". (VD: Món ăn: Chay, Tên thật: Trần Văn A, Ngôn ngữ lập trình chánh: Python).
  - Tốc độ đọc O(1), tức thì nạp thẳng vào System Prompt trước khi chu trình sinh đoạn Text bắt đầu.
- **Episodic vs Semantic (Vector DB - Chroma/Pinecone):**
  - **Episodic (Hồi ức chặng đường):** Lưu lại nhật ký giải quyết công việc. VD: "Thứ Hai Agent A đã báo lỗi thiếu bộ nhớ khi Compile C++, cách fix là thêm Flag XY." Trải nghiệm này được lưu vết Embeddings, lần sau gặp lỗi tương tự, nó tự lôi sách ra chép cách fix.
  - **Semantic (Tri thức):** Lưu kiến thức ngoài luồng, VD: Các file PDF sổ tay định mức xây dựng do Cục Đăng Kiểm phát hành. Mô hình không nằm lòng, Agent tự Search (RAG thuần thuý).

## 4. Dùng SaaS (Mem0/Zep) lúc nào?
- **Mem0 (Memory for AI):** Là một API SaaS xử lý hộ. Mình gửi message: `mem0.add("Tôi mua Macbook bị ám xanh màn hình", user_id="bob123")`. Xong. Mem0 tự gọi LLM giải nén ý định, tự ghi vào cục DB của nó và tự tìm cách Index. Cực tiện cho Hackathon và làm bản MVP. Nhược điểm: Trả tiền Subcription + Khó debug lộ trình Vectorisation.
- **Zep:** Nền tảng chuyên tập trung xử lý Context/Memory có hỗ trợ Self-hosting cực mạnh. Rất hữu hình khi build App Chat với hàng ngàn user nhắn đồng thời.

## Nguồn Đọc Thêm:
- **Tài liệu nền tảng Cognitive:** "Generative Agents: Interactive Simulacra of Human Behavior" (Park et al., Stanford, 2023). Bản thiết kế cho các NPCS AI tự nhớ nhau, tự tám chuyện ở 1 thị trấn ảo. Khái niệm Ký ức (Memory Stream) bắt đầu từ đây.
- **Anthropic Guidebook:** Bài blog cực xịn "Building Effective Agents - Context Engineering." (Anthropic, 2024). Căn vặn việc khi nào nhồi Prompt khi nào đi Retrieval.
