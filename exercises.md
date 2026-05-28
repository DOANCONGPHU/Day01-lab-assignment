# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *tem thấp ổn định ngắn gọn, temp cao output có sự sáng tạo. Temperature ảnh hưởng trực tiếp đến mức độ ngẫu nhiên và sáng tạo của mô hình.*

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Khoảng 0.2 -0.5 cho chatbot hỗ trợ khách hàng, giúp chatbot trả lời ổn định, nhất quán và chính xác hơn*

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> **~16.67 lần đắt hơn**
> 


**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> **GPT-4o xứng đáng:** *Ứng dụng chẩn đoán y tế hoặc phân tích pháp lý, nơi độ chính xác cao là tối quan trọng. Một lỗi có thể gây thiệt hại lớn về tài chính hoặc sức khỏe. GPT-4o có khả năng lý luận và hiểu ngữ cảnh tốt hơn, giúp giảm sai lầm quan trọng.*
>
> **GPT-4o-mini tốt hơn:** *Ứng dụng chatbot hỗ trợ khách hàng, tóm tắt tin tức, hoặc gợi ý sản phẩm đơn giản. Những tác vụ này không yêu cầu lý luận phức tạp, và Mini đủ khả năng xử lý với chi phí rẻ hơn 94% (tiết kiệm ~$100k/tháng cho 1M users).*

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming là cực kỳ quan trọng cho các ứng dụng tương tác trực tiếp với người dùng như chatbot, trợ lý ảo, hoặc giao diện web, vì nó cho phép người dùng thấy phản hồi dần dần thay vì phải chờ toàn bộ thời gian xử lý (cải thiện UX và giảm cảm giác "hung")—đây là lý do ChatGPT sử dụng streaming. Ngược lại, non-streaming phù hợp hơn cho batch processing, công việc background như tạo báo cáo hoặc xử lý dữ liệu quy mô lớn, nơi không có người dùng chờ đợi trực tiếp, hoặc khi ứng dụng cần toàn bộ phản hồi trước khi xử lý tiếp (ví dụ: lưu vào database hoặc thực hiện phân tích). Streaming cũng tiêu thụ nhiều tài nguyên hơn, nên cho các API calls từ máy chủ sang máy chủ với frequency cao, non-streaming thường hiệu quả chi phí hơn.*


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
