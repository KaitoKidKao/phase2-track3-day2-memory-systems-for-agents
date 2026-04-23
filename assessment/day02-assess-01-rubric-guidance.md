# Tiêu Chí Đánh Giá (Rubric) — Lab 17: Agent Memory
*Tài liệu nội bộ dành cho Giảng Viên và TA sử dụng để chấm điểm Deliverable.*

**Tổng Điểm:** 100 điểm.
**Hình Thức Nộp:** Nhóm nén Tệp Source Code (File Script/Jupyter Notebook Python) + Benchmark Report (`BENCHMARK.md`).

---

## Gate 1: Thiết Kế Storage System (20 điểm)
- **10đ:** Hoàn thành logic thiết lập In-Memory Buffer để lưu trữ 1 cửa sổ giới hạn N tin nhắn (Short-term).
- **10đ:** Tạo được hệ thống giả lập Database Key-Value độc lập (như Class Redis Fake/Dictionary) và có các Interface cơ bản `Read()` và `Update()` để cất giữ Profile User (Long-term).
- *(Không chấm điểm kĩ thuật DB gốc là Docker/Cloud hay gì, vì trọng tâm là thiết kế cấu trúc AI, xài Dict Python cũng cho full điểm)*.

## Gate 2: LangGraph Memory Router (30 điểm)
- **10đ:** Định nghĩa đúng `Graph State` trong LangChain/LangGraph, thể hiện được các luồng thuộc tính: Tin nhắn, Hồ sơ, Truy xuất thông tin phụ.
- **10đ:** Node Retrieve (Nạp bộ nhớ) - Hoạt động và tự động chèn Fact từ Database lên Header hệ thống trước khi API Call tới LLM Core được thực thi.
- **10đ:** Trimming Logic (Ngữ Cảnh Cắt Gọt) - Viết được hàm tự động tóm tắt tin nhắn cũ đi (hoặc thẳng tay cắt bỏ tin nhắn cũ) khi biến lưu độ dài Conversation String vượt quá con số Token Limit ấn định `mem_budget`.
- *Nguy cơ (-15đ):* Code chạy một mạch và rơi vào vòng lặp đồ thị vô hạn do định tuyến nhánh sai (Edges conditional).

## Gate 3: Auto-Extraction Process (Logic Lọc Thông Tin) (20 điểm)
- **10đ:** Lập trình để Agent (hoặc một LLM phụ thu nhỏ) đóng vai trò "Kẻ nghe lén". Sau mỗi nhánh phản hồi của Client, System sẽ soi xem có Fact mới nào không để tự tạo Lệnh bóc tách và Add vào Long-term Profile. VD: (Client: "Mình bị dị ứng sữa bò"). Hàm Extract tự động bổ sung `"dị_ứng": "sữa_bò"` vào Storage của `user_id_x`.
- **10đ:** Khả năng Overwrite Conflict. Khi đối mặt với thay đổi trạng thái (Client: "À nhầm, mình dị ứng đậu nành chứ không phải bò"), Agent Update được Fact cũ thay vì Append chồng chất fact đối lập lên vào DB gây rối loạn LLM.

## Gate 4: Benchmark & Reflection Report (30 điểm)
- **10đ (Độ tin cậy của Test):** Chứng minh Output bằng File Script: Đã đẩy vô nghĩa > 20 Turn Chat rác, LLM vẫn trả lời đúng câu hỏi thử thách kiểm tra sự ghi nhớ của Long-term profile do Router đã hoàn thành xuất sắc nhiệm vụ.
- **10đ (Bóc tách Metric):** Tính được sự khác biệt độ trễ phản hồi (Latency) hay số Token (Cost budget) ở thời điểm chat thứ 20 (khi dùng Full History vs Buffer Trimmer Router). Bảng số rõ ràng.
- **10đ (Tư Duy Suy Ngẫm):** Trình bày sâu sắc 1 điểm hạn chế của kiến trúc Memory Router đang được code trong phiên này. Ví dụ: Rủi ro lỗi bảo mật PII, Rủi ro lỗi Format Parse khi hàm extraction xài Model cùi bị liệt...
