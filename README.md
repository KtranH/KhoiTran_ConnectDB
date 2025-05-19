# ConnectDB - Trợ lý truy vấn cơ sở dữ liệu bằng ngôn ngữ tự nhiên

![Banner ConnectDB](https://scontent.fsgn5-9.fna.fbcdn.net/v/t39.30808-6/499525148_711488807932462_1147746514714061202_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=127cfc&_nc_ohc=6s-139BvcRgQ7kNvwFXzDO7&_nc_oc=Adm7YbGRBT8dTogMqrltUmCDleaDg4iSxtLPp_Xgf_R74XgwTkIAuq_neW5wI_AQxfyjhhFv-88183Zx74IBCujh&_nc_zt=23&_nc_ht=scontent.fsgn5-9.fna&_nc_gid=rQrfSzXBlU0gmfmQYIpyEA&oh=00_AfJ2HEBtVRJ2b89FEQUJnQr8XHP3GkcSUcAZjPrwBLctcA&oe=683093FE)

## Giới thiệu

ConnectDB là một công cụ sử dụng AI để chuyển đổi câu hỏi bằng ngôn ngữ tự nhiên thành truy vấn SQL. Cho phép người dùng tương tác với cơ sở dữ liệu MySQL/MariaDB mà không cần biết nhiều về ngôn ngữ truy vấn SQL.

![Giao diện chính](https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-6/500226969_711488811265795_2256049907301810830_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=127cfc&_nc_ohc=YcxE-SX8JFAQ7kNvwFn4U7v&_nc_oc=AdkwTij-hKGibjO56hEPvUR4s6OllKRb7QiWMPXomisF6DqnPANxzJ640Hq1n9FTp8_Mxs_zO1fz7txECPf7DYY2&_nc_zt=23&_nc_ht=scontent.fsgn5-10.fna&_nc_gid=J4JBaCNBsicVDU5I0ZcFMg&oh=00_AfII5qjFC-ZEqbL6fkvPXj2pjeV6wMKCKHJE_SwrAfnxbA&oe=6830AF7E)

### Tính năng chính

- Tự động kết nối đến cơ sở dữ liệu MySQL/MariaDB
- Phân tích cấu trúc cơ sở dữ liệu (schema) để hiểu dữ liệu
- Chuyển đổi câu hỏi tiếng Việt thành truy vấn SQL chính xác
- Thực thi truy vấn và hiển thị kết quả dưới dạng bảng dễ đọc
- Hỗ trợ nhiều loại truy vấn: SELECT, INSERT, UPDATE, DELETE, v.v.

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Máy chủ MySQL/MariaDB
- LLM Studio local hoặc API khác để tạo truy vấn SQL

## Cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/your-username/ConnectDB.git
cd ConnectDB
```

### Bước 2: Cài đặt các thư viện phụ thuộc

```bash
pip install mysql-connector-python pandas tabulate requests
```

### Bước 3: Cài đặt và chạy LLM Studio (hoặc dịch vụ LLM khác)

Để sử dụng đầy đủ chức năng, bạn cần:
1. Cài đặt [LLM Studio](https://lmstudio.ai/) hoặc sử dụng dịch vụ API tương tự
2. Tải mô hình Gemma-3-12B-IT hoặc mô hình tương đương
3. Chạy API local trên cổng 1234 (có thể thay đổi trong mã nguồn)

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

![Ví dụ truy vấn](đường-dẫn-đến-hình-ảnh-ví-dụ)

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

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng liên hệ qua [email/github/website]. 