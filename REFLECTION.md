# Báo cáo Phản hồi: Multi-Memory Agent (Lab 17)

## 1. Rủi ro về Quyền riêng tư & PII (Thông tin định danh cá nhân)
- **Lưu trữ dữ liệu nhạy cảm**: Các module `LongTermMemory` (Redis) và `EpisodicMemory` (JSON) ghi lại các sự thật cá nhân như tên, dị ứng và thói quen. Nếu người dùng vô tình chia sẻ mật khẩu hoặc mã số sức khỏe, chúng sẽ bị lưu dưới dạng văn bản thuần túy (plain text).
- **Bộ nhớ nhạy cảm nhất**: **Long-term profile (Redis)** là nơi nhạy cảm nhất vì nó chứa dữ liệu cá nhân có cấu trúc, giá trị cao và có thể được sử dụng để định danh người dùng.
- **Rủi ro truy xuất sai**: Nếu bộ nhớ ngữ nghĩa (Chroma) truy xuất một sự thật thuộc về người dùng khác (trong thiết lập đa người dùng), nó có thể dẫn đến rò rỉ dữ liệu chéo.

## 2. Xóa dữ liệu & TTL (Thời gian tồn tại)
- Hiện tại, hệ thống chưa triển khai **TTL (Time-To-Live)** cho các nhật ký sự kiện. Trong một hệ thống thực tế, các nhật ký cũ nên được lưu trữ hoặc xóa sau X tháng để tuân thủ các quy định như GDPR/CCPA.
- **Sự đồng ý (Consent)**: Người dùng cần được thông báo rằng sở thích của họ đang được lưu lại. Cần triển khai lệnh như `/forget_me` để xóa sạch các mục nhập trong Redis và JSON cho một `user_id` cụ thể.

## 3. Giới hạn kỹ thuật & Khả năng mở rộng
- **JSON cho Episodic Logs**: Việc sử dụng một file JSON duy nhất cho tất cả người dùng sẽ trở thành nút thắt cổ chai. Khi file lớn dần, thời gian đọc/ghi sẽ tăng theo hàm tuyến tính (O(n)). Cần một cơ sở dữ liệu thực sự như PostgreSQL hoặc MongoDB để thay thế.
- **Cắt tỉa Token (Trimming)**: Phân cấp 4 tầng hiện tại là một giải pháp tình thế. Trong các cuộc hội thoại phức tạp, Agent vẫn có thể mất đi các sắc thái quan trọng nếu cửa sổ "tin nhắn gần đây" quá nhỏ so với các sự thật ngữ nghĩa được truy xuất.
- **Độ chính xác của Tìm kiếm Vector**: Truy xuất ngữ nghĩa phụ thuộc vào chất lượng của embeddings. Nếu câu truy vấn mơ hồ, Chroma có thể trả về "nhiễu" không liên quan, gây xao nhãng cho LLM.

## 4. Các hiểu biết chính (Key Insights)
- **Bộ nhớ nào giúp ích nhất?**: **Short-term memory** là quan trọng nhất để duy trì sự mạch lạc, tiếp theo là **Long-term profile** để cá nhân hóa trải nghiệm.
- **Rủi ro thất bại**: Hệ thống có khả năng thất bại khi mở rộng quy mô lớn do việc trích xuất thông tin bằng LLM (`store_node`) có thể quá chậm hoặc xảy ra xung đột ghi đồng thời vào file JSON.
