# ConnectDB: Kết nối LM Studio với MySQL và truy xuất thông tin từ tài liệu

Dự án này kết nối LM Studio với cơ sở dữ liệu MySQL và cung cấp khả năng truy xuất thông tin từ các tài liệu văn bản. Nó cho phép người dùng đặt câu hỏi bằng tiếng Việt tự nhiên và nhận về kết quả từ cả cơ sở dữ liệu hoặc tài liệu văn bản.

## Tính năng chính

- **Kết nối với MySQL**: Tạo truy vấn SQL dựa trên câu hỏi tiếng Việt tự nhiên
- **Truy xuất thông tin từ tài liệu**: Tìm kiếm và truy xuất thông tin từ các tài liệu văn bản
- **Truy vấn thông minh**: Phân biệt giữa câu hỏi liên quan đến cơ sở dữ liệu và câu hỏi liên quan đến tài liệu
- **Hiển thị kết quả đẹp mắt**: Hiển thị kết quả dưới dạng bảng có định dạng đẹp

![Ví dụ chức năng](https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-6/499861063_713027097778633_9008190704226737270_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=127cfc&_nc_ohc=kbcNWi2A3toQ7kNvwHPN3rS&_nc_oc=AdkI_XUGP01qDL8ECkXYM0yvVEcBasFla0hmLlvrorqR1F6-08pUVhNR1fDUb7jjL-QVlfdSzMQPmfyXDcS_AV3m&_nc_zt=23&_nc_ht=scontent.fsgn5-10.fna&_nc_gid=rKj5Gp6Ekf2AXS0lUSsVrA&oh=00_AfJhjSW8KIFL21S6w5wZFQe0b6UADWxRwrgmelCsCWj12w&oe=68337770)

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```
pip install mysql-connector-python pandas tabulate
```

2. Cài đặt và cấu hình LM Studio (http://lmstudio.ai)
   - Tải và cài đặt LM Studio
   - Tải model (Gemma-3-12B-it hoặc tương tự)
   - Khởi động máy chủ API ở cổng 1234

3. Cấu hình kết nối MySQL:
   - Chỉnh sửa thông tin kết nối trong file main.py

## Cách sử dụng

1. Chạy chương trình:
```
python main.py
```

2. Chương trình sẽ hiển thị:
   - Thông tin cấu trúc cơ sở dữ liệu
   - Danh sách các tài liệu có sẵn

3. Nhập câu hỏi của bạn, ví dụ:
   - "Hiển thị danh sách sinh viên ở khoa CNTT" (truy vấn cơ sở dữ liệu)
   - "Quy định về bảo mật thông tin là gì?" (truy vấn tài liệu)
   - "Thời gian đào tạo nhân viên mới là bao lâu?" (truy vấn tài liệu)

## Cấu trúc dự án

- `main.py`: Chương trình chính, xử lý tương tác người dùng và hiển thị kết quả
- `generate_sql_local.py`: Tạo truy vấn SQL từ câu hỏi tiếng Việt
- `document_processor.py`: Xử lý đọc và tìm kiếm trong tài liệu văn bản
- `document_query.py`: Xử lý truy vấn tài liệu bằng LLM
- `docs/`: Thư mục chứa các tài liệu văn bản

## Thêm tài liệu mới

Để thêm tài liệu mới, chỉ cần thêm file .txt vào thư mục `docs/`. Định dạng khuyến nghị:
- Tên file: sử dụng gạch dưới để ngăn cách các từ (ví dụ: `quy_dinh_dao_tao.txt`)
- Sử dụng markdown cho định dạng (tiêu đề, danh sách, vv)

## Lưu ý

- Hệ thống phân biệt câu hỏi liên quan đến cơ sở dữ liệu và tài liệu dựa trên từ khóa
- Khi câu hỏi liên quan đến tài liệu, hệ thống sẽ tìm kiếm trong tất cả các tài liệu
- Có thể chỉ định tên tài liệu trong câu hỏi để tìm kiếm trong một tài liệu cụ thể

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Máy chủ MySQL/MariaDB
- LLM Studio local hoặc API khác để tạo truy vấn SQL

## Cấu hình

Mở file `main.py` và chỉnh sửa thông tin kết nối MySQL:

```python
config = {
    'host': '127.0.0.1',  # Địa chỉ máy chủ MySQL
    'user': 'root',       # Tên đăng nhập
    'password': '',       # Mật khẩu
    'port': 3306,         # Cổng (mặc định: 3306)
    'database': 'kt_ai'   # Tên cơ sở dữ liệu
}
```

## Sử dụng

### Chạy ứng dụng

```bash
python main.py
```

### Quy trình sử dụng

1. Khi khởi động, chương trình sẽ kết nối tới cơ sở dữ liệu và hiển thị cấu trúc các bảng
2. Nhập câu hỏi của bạn bằng ngôn ngữ tự nhiên, ví dụ: "Cho tôi danh sách 10 sản phẩm có giá cao nhất"
3. Hệ thống sẽ tự động tạo truy vấn SQL phù hợp và thực thi nó
4. Kết quả truy vấn sẽ được hiển thị dưới dạng bảng

![Ví dụ truy vấn](https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-6/500226969_711488811265795_2256049907301810830_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=127cfc&_nc_ohc=YcxE-SX8JFAQ7kNvwFn4U7v&_nc_oc=AdkwTij-hKGibjO56hEPvUR4s6OllKRb7QiWMPXomisF6DqnPANxzJ640Hq1n9FTp8_Mxs_zO1fz7txECPf7DYY2&_nc_zt=23&_nc_ht=scontent.fsgn5-10.fna&_nc_gid=J4JBaCNBsicVDU5I0ZcFMg&oh=00_AfII5qjFC-ZEqbL6fkvPXj2pjeV6wMKCKHJE_SwrAfnxbA&oe=6830AF7E)

### Thoát chương trình

Gõ `exit` để thoát khỏi chương trình.

## Cấu trúc mã nguồn

- `main.py`: File chính chứa giao diện người dùng và xử lý kết nối cơ sở dữ liệu
- `generate_sql_local.py`: Xử lý việc chuyển đổi câu hỏi thành truy vấn SQL sử dụng LLM

## Hiệu chỉnh nâng cao

### Thay đổi mô hình LLM

Nếu bạn muốn sử dụng một API LLM khác, hãy chỉnh sửa hàm `generate_sql_local()` trong file `generate_sql_local.py`.

### Tùy chỉnh hiển thị kết quả

Để thay đổi cách hiển thị kết quả, chỉnh sửa hàm `display_results()` trong file `main.py`.

## Xử lý sự cố

### Lỗi kết nối cơ sở dữ liệu
- Kiểm tra thông tin kết nối trong biến `config`
- Đảm bảo MySQL/MariaDB đã được khởi động
- Kiểm tra quyền truy cập của người dùng MySQL

### Lỗi tạo truy vấn SQL
- Đảm bảo LLM Studio đang chạy và truy cập được qua http://127.0.0.1:1234
- Kiểm tra log để xem thông báo lỗi chi tiết

### Truy vấn không chính xác
- Cung cấp câu hỏi cụ thể và rõ ràng hơn
- Kiểm tra xem cấu trúc cơ sở dữ liệu đã được hiển thị đúng chưa

## Đóng góp

Nếu bạn muốn đóng góp cho dự án, vui lòng fork repository và tạo Pull Request.

## Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng liên hệ qua [hoangkhoi230@gmail.com]. 