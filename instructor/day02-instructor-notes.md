# Ngày 17 — Instructor Notes

**Chương trình:** VinUni A20 — AI Thực Chiến (Phase 2 - Track 3)
**Chủ đề:** Memory Systems for Agents
**Thời lượng:** 4h lecture (sáng) + 4h lab (chiều)
**Slide tham chiếu:** `day02-memory-systems-for-agents.pdf` (Chuyển đổi từ `.tex`)

---

## Phân đoạn bài giảng (Lecture Flow - 4h Sáng)

### Block A: Tại sao Agent "quên"? (~30 min)
*Slides: 1-5 (Phân tích Limitation của LLM API)*

**Key Talking Points:**
- **Slide 2 (Stateless by default):** Nhấn mạnh: Mỗi API call gửi đến OpenAI là một phiên giao dịch hoàn toàn trắng. Không có phép màu nào tự nhớ context cũ cả.
- **Slide 3 (Não bộ người vs Agent):** Dùng phép ẩn dụ (Analogy). "Working Memory" ở người có thể nhớ 7 ± 2 thông tin tương đương "Context Window" của AI. "Long-term Memory" tương đương External Store (DB). Khẳng định Agent Production cần cả 2.
- **Insight:** Nếu nhét mọi thứ vào Context Window (kiểu nhét toàn bộ lịch sử chat 1 năm vào lệnh gọi API), mô hình sẽ bị "Lost in the Middle" và chậm, siêu tốn tiền (Token rate xé túi).

### Block B: Context Engineering Framework (~40 min)
*Slides: 6-8 (Chiến lược kiến trúc thông tin cho Agent)*

**Key Talking Points:**
- **Slide 7 (7 Context Layers):** Đây là Framework tư duy cực quan trọng. Phải giải thích theo trình tự Trim từ trên xuống:
  - Policy (Luật an toàn) luôn nằm layer dưới cùng. Không bao giờ được Trim.
  - Khi token chạm mức limit trần, phải lập trigger cho agent vứt "System Context" trước, rồi tóm tắt lại "User Context" ... v.v.
- **Slide 8 (Token Budget 20%):** Quy tắc vàng. Mọi Memory chỉ được dùng tối đa 20% tổng dung lượng Context Window. Nếu context của GPT-4 là 128k, anh em chỉ được xài tối đa khoảng 25k token cho việc Load Memory Context. Phần còn lại phải nhường cho Document (Retrieved) và đầu ra.

### Block C: Cognitive Memory Model (4 Loại Memory) (~60 min)
*Slides: 9-14 (Short-term, Long-term, Episodic, Semantic)*

**Key Talking Points:**
- **Slide 10 (Memory Taxonomy):** Bức tranh 2x2. Cá nhân (Cột trái) vs Tri thức (Cột phải). Tạm thời (Hàng trên) vs Bền vững (Hàng dưới). Trả bài kiểm tra nhanh trên lớp: *"Hồ sơ bệnh án là loại bộ nhớ nào?"* (=> Long-term profile)
- **Slide 11 (Short-term strategies):** So sánh Buffer vs Summary vs Sliding Window. Phải kết luận Sliding Window là top tier approach cho production.
- **Slide 12 (Redis):** Cách Extract Facts từ đoạn chat cũ để cất vào Redis. Giải thích tại sao lại là Redis? Vì Read/Write đạt tốc độ O(1), ngay lúc user kết nối vào session, context đã fetch xong.
- **Slide 13 (Mem Management Flow):** Sơ đồ quan trọng. Khẳng định nguyên tắc sống còn: "Chỉ write-back (persist) Memory sau khi task/session hoàn tất". Ghi db liên tục ở giữa luồng chat sẽ gây ra Race Condition.

### Block D: Implementation Deep-Dive (~40 min)
*Slides: 15-18 (LangGraph và Episodic/Semantic)*

**Key Talking Points:**
- **Slide 16 (LangGraph State):** Mở Slide xem source Python. Phân tích `MemoryState`. Route logic trả Context về dựa theo Priority Order (Short -> Long -> Episodic -> Semantic).
- **Slide 17 (Episodic - Ký ức bài học):** Kỹ thuật *Smart Forgetting*. Một Agent quá "nhớ dai" dễ bị hoang tưởng (Overfitting với lịch sử). Phải thiết lập cơ chế quên dần (Forget mechanism theo Importance Decay).
- **Slide 18 (Semantic vs Chroma):** RAG không phải là Memory. RAG chỉ phục vụ Semantic Context tĩnh bên ngoài.

### Block E: Frameworks & Privacy (~30 min)
*Slides: 19-21 (Zep, Mem0 và GDPR)*

**Key Talking Points:**
- **Slide 20 (Build vs Buy cho Memory):** Giới thiệu kiến trúc Mem0 / Zep. Giải thích: Tận dụng SaaS Memory có ưu/nhược gì so với tự code LangGraph. Lời khuyên chốt: MVP/PoC dùng Mem0. Scale/Sản phẩm cốt lõi dùng custom build.
- **Slide 21 (GDPR Policy):** Tôn chỉ Quyền được lãng quên (Right to be Forgotten). "Nếu khách hàng yêu cầu xóa data, Agent trong mạng Multi-Agent có đồng loạt xóa hay không?". Chặn rủi ro tuân thủ pháp lý khi AI lưu user preference.

### Block F: Demo & Transition to Lab (~20 min)
*Slides: 22-25*

**Key Talking Points:**
- **Demo:** Trực tiếp đóng vai user với 2 session cách biệt. VD: 
  - Session 1 (Trên terminal): Nhập "Tôi là dân Vegan, dị ứng đậu nành". System load vào DB. Đóng app.
  - Session 2 (Mở terminal lại trắng trơn): "Gợi ý tôi món canh hôm nay." 
  - Kết quả: Agent trả ra món chay (đã loại đậu nành). Sự kì diệu nằm ở độ tự nhiên!
- **Transition Script:** 
  > *"Sáng nay chúng ta biết vì sao DB Redis kết hợp Chroma là thứ bắt buộc để có AI thông minh 'ngoài luồng' (Cross-session). Chiều nay, các bạn sẽ không cần phải nghe lý thuyết nữa. Các bạn phải viết cho được một Router Code (Python+LangChain) có phép thuật tự trim Memory để không bị sập ngân sách Token. Mở hướng dẫn lab-guide và chia máy ra!"*
