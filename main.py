import mysql.connector
import pandas as pd
from tabulate import tabulate
from generate_sql_local import generate_sql_local
from document_processor import DocumentProcessor

# Thông tin kết nối MySQL
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'port': 3306,
    'database': 'kt_ai'
}

def get_table_schema(connection):
    """Lấy thông tin schema của tất cả các bảng trong database"""
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    schema_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        schema_info[table_name] = columns
    
    cursor.close()
    return schema_info

def print_schema_info(schema_info):
    """In thông tin schema để người dùng tham khảo"""
    print("\n=== THÔNG TIN CẤU TRÚC CƠ SỞ DỮ LIỆU ===")
    for table_name, columns in schema_info.items():
        print(f"\nBảng: {table_name}")
        print("-" * 60)
        print(f"{'Tên cột':<20}{'Kiểu dữ liệu':<15}{'Null':<10}{'Khóa':<10}{'Mặc định':<15}{'Extra':<15}")
        print("-" * 60)
        for column in columns:
            print(f"{column[0]:<20}{column[1]:<15}{column[2]:<10}{column[3]:<10}{str(column[4]):<15}{column[5]:<15}")

def execute_query(connection, sql_query):
    """Thực thi truy vấn SQL và trả về kết quả"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_query)
        
        # Kiểm tra loại truy vấn
        if sql_query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE')):
            results = cursor.fetchall()
            cursor.close()
            return True, results
        else:
            connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return True, f"Truy vấn thực thi thành công. Số dòng bị ảnh hưởng: {affected_rows}"
    except mysql.connector.Error as err:
        return False, f"Lỗi khi thực thi truy vấn: {err}"

def display_results(results, column_names=None):
    """Hiển thị kết quả truy vấn dưới dạng bảng đẹp"""
    if isinstance(results, list) and len(results) > 0:
        df = pd.DataFrame(results, columns=column_names)
        print("\n=== KẾT QUẢ TRUY VẤN ===\n")
        print(tabulate(df, headers="keys", tablefmt="rounded_grid", showindex=False))
        print(f"\n🔹 Tổng số bản ghi: {len(results)}\n")
    elif isinstance(results, str):
        print(f"\n{results}")
    else:
        print("\n⚠️ Không có kết quả nào được trả về.")

def display_document_results(sql_query):
    """Hiển thị kết quả truy vấn từ tài liệu"""
    # Kiểm tra xem có phải là kết quả từ tài liệu không
    if sql_query.startswith("SELECT * FROM document_results WHERE content = '"):
        # Trích xuất nội dung từ câu truy vấn giả
        content_start = sql_query.find("'") + 1
        content_end = sql_query.rfind("'")
        content = sql_query[content_start:content_end]
        
        print("\n=== KẾT QUẢ TỪ TÀI LIỆU ===\n")
        print(content)
        return True
    
    return False

def print_document_info():
    """In thông tin về các tài liệu có sẵn"""
    doc_processor = DocumentProcessor()
    doc_names = doc_processor.get_document_names()
    
    print("\n=== THÔNG TIN TÀI LIỆU CÓ SẴN ===")
    for i, name in enumerate(doc_names, 1):
        print(f"{i}. {name}")

def main():
    try:
        # Tạo kết nối đến MySQL
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("Kết nối đến MySQL thành công!")
            
            # Lấy thông tin schema
            schema_info = get_table_schema(connection)
            print_schema_info(schema_info)
            
            # In thông tin về tài liệu có sẵn
            print_document_info()
            
            while True:
                print("\n" + "-"*60)
                user_question = input("Nhập câu hỏi của bạn (hoặc 'exit' để thoát): ")
                
                if user_question.lower() == 'exit':
                    break
                
                # Tạo truy vấn SQL từ câu hỏi bằng LLM
                print("\nĐang xử lý câu hỏi...")
                sql_query = generate_sql_local(user_question, schema_info)
                
                # Kiểm tra và hiển thị kết quả từ tài liệu nếu có
                if display_document_results(sql_query):
                    continue
                    
                print(f"\nTruy vấn SQL được tạo: {sql_query}")
                
                # Thực thi truy vấn
                print("\nĐang thực thi truy vấn...")
                success, results = execute_query(connection, sql_query)
                
                # Hiển thị kết quả
                if success:
                    display_results(results)
                else:
                    print(f"\nLỗi: {results}")
            
            # Đóng kết nối
            connection.close()
            print("\nĐã đóng kết nối MySQL.")
            
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối: {err}")

if __name__ == "__main__":
    main()