# Hướng dẫn Lab 17: Build Multi-Memory Agent

**Vai trò:** Tài liệu điều phối dành cho Lab Coach và TA.
**Mục tiêu:** Giúp học viên nắm rõ và code chạy thực thụ LangGraph Router ứng dụng Memory Management (Stateful).

## Thời hạn: 4 giờ 
*Lưu ý: Học viên đã học xong lý thuyết ở mảng Memory Structure trên lớp Sáng. Kịch bản dưới đây dành cho nhóm Lab từ 3-5 người.*

---

## Các mốc Giám sát & Hướng dẫn (Checkpoints)

### Phase 1: MOCK DATA SETUP (30 phút)
> Trọng tâm: Xây dưng dữ liệu giả (Dummy Behavior Data) đủ phức tạp để Agent có thể bị "ngợp" hoặc bị ép quên.

**Nhiệm vụ Coach:**
- Bắt buộc học viên viết ra một danh sách Fact ở file TXT hoặc JSON nhỏ: `{"tên": "Linh", "loại cà phê": "Decaf sữa yến mạch", "level_kỹ_thuật": "DevOps cứng", "OS": "Linux Ubuntu"}`.
- Viết 1 file Markdown hướng dẫn (Instruction) cực dài tầm 200 dòng chữ (FAQ công ty).
- *Mục đích:* Dữ liệu này sẽ nhồi vào Agent làm tài nguyên ban đầu.

**Dấu hiệu sai sót (Red Flags):**
- Group tạo data quá ít (VD chỉ có hello, tớ tên Linh) => Tý nữa test chừng 5 tin nhắn là hit pass, không tạo ra được bài toán "Thiếu Token", nên test bị vô nghĩa.

### Phase 2: MEMORY BACKEND (60 phút)
> Trọng tâm: Thiết lập các class kết nối (DB Connector) - như Redis/Chroma (hoặc giả lập In-memory Dict/FAISS cho ai máy yếu).

**Nhiệm vụ Coach:**
- Không hỗ trợ cài Docker quá lâu, nếu máy sinh viên lỗi thư viện, cho qua dùng biến Dict global Python làm Fake Redis.
- Quan sát học viên thiết lập 2 Class Interface riêng biệt: Class `ShortTermBuffer` và Class `LongTermProfile`.
- Yêu cầu viết ít nhất 2 hàm thuần `get_facts(user_id)` và `add_fact(user_id, fact)`.

**Dấu hiệu sai sót (Red Flags):**
- Sinh viên gọi thẳng phương thức vào trong vòng lặp vòng lặp Chat (Whilte True), phá vỡ Design Pattern kiến trúc Agent bằng LangGraph.

### Phase 3: MEMORY ROUTER (60 phút)
> Trọng tâm: Code Node Logic trong LangGraph `MemoryState`. Đỉnh điểm của Session Lab.

**Nhiệm vụ Coach:**
- Cấu trúc `TypedDict`: Phải có field `messages` dạng List, field `profile` dạng Dict, field `semantic_context` dạng str.
- Kiểm tra cái nút Hàm `retrieve_memory(state)`: Coach phải nhìn thấy đoạn Code "Móc data từ Biến Profile -> Format lại thành đoạn Text nhỏ -> Nhét lên đầu danh sách Message hệ thống (System Prompt)".
- **Stress-Test tại bàn:** Đi xuống hỏi nhóm: *"Dữ liệu của Group em hiện tại là 3000 Tokens, nếu vượt mức quota em đặt là 1500 Tokens, hàm của em sẽ hi sinh cái gì trước? Semantic Knowledge hay Lịch sử chat?"*

**Troubleshooting (Chữa cháy LangGraph):**
- **Lỗi Infinite Loop**: Chạy code cái Agent nó lặp và nổ limit recursion? Đó là vì quên điều kiện thoát `END` và cơ chế Edge rẽ nhánh khi node trích xuất Fact kết thúc.
- Giúp sinh viên check lại file Python, print output trạng thái của Graph để ngắt sớm.

### Phase 4: BENCHMARK & METRICS (40 phút)
> Trọng tâm: Script cho tự Tự động chạy/đối chiếu (Automation metrics). Chạy xả 30 câu hội thoại và đo.

**Nhiệm vụ Coach:**
- Gợi ý viết 1 script For Loop bơm 30 tin nhắn vô nghĩa (hoặc chitchat) vào, sau đó xen vào 1 tin nhắn "Nhắc lại coi, sáng nay tớ nói cà phê của tớ là nilon hay yến mạch?". Đo xem độ trả lời đúng/sai bằng mắt thường.
- Dạy cách đo lường số ms (milliseconds) mà LLM trả về giữa 2 version: (1) Cầm 3000 Token thô gửi đi vs (2) Gửi System Profile dồn chỉ mất 200 Token do dùng Memory Router tốt. Sẽ thấy độ trễ chênh lệch.
- Đốc thúc viết File `Report.md` kết luận số tiền tiết kiệm được.

---

## Chuẩn Bị Cơ Bản Dành Cho Lab Coach Trước Khi Đứng Bàn
- Load file Source Solution (Nếu có) chạy test thông trên Colab của chính bạn.
- Bố trí cho Sinh viên xài key OpenAI test, hoặc xài local Ollama (Gemma2/Llama3 8B) đều có thể test được Memory Logic. Tuy nhiên model nhỏ đôi khi sẽ parse sai JSON => Dặn dò sinh viên handle ngoại lệ Parse Error.
