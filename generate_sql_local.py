import requests
import re
from document_processor import DocumentProcessor
from document_query import process_document_query

def generate_sql_local(question, schema_info=None):
    # Kiểm tra xem câu hỏi có liên quan đến tài liệu không
    doc_keywords = ["quy định", "quy chế", "nội quy", "chính sách", "hướng dẫn", 
                   "đào tạo", "bảo mật", "làm việc", "nhân sự", "văn bản"]
    
    is_doc_related = any(keyword.lower() in question.lower() for keyword in doc_keywords)
    
    if is_doc_related:
        # Xử lý câu hỏi về tài liệu bằng mô-đun mới
        answer = process_document_query(question)
        
        if answer:
            # Tạo câu truy vấn giả để hiển thị kết quả từ tài liệu
            sql_like_response = "SELECT * FROM document_results WHERE content = '"
            sql_like_response += answer.replace("'", "''")  # Escape dấu nháy đơn trong SQL
            sql_like_response += "';"
            return sql_like_response
    
    # Tạo thông tin về schema để cung cấp cho LLM
    schema_context = ""
    if schema_info:
        schema_context = "Thông tin về cấu trúc cơ sở dữ liệu:\n"
        for table_name, columns in schema_info.items():
            schema_context += f"Bảng {table_name}: "
            column_info = []
            for column in columns:
                column_info.append(f"{column[0]} ({column[1]})")
            schema_context += ", ".join(column_info) + "\n"
    
    url = "http://127.0.0.1:1234/v1/completions"  
    payload = {
        "model": "gemma-3-12b-it",
        "prompt": (
            f"Bạn là một chuyên gia SQL giỏi. Hãy viết một truy vấn SQL hợp lệ dựa trên yêu cầu sau.\n\n"
            f"{schema_context}\n"
            f"HƯỚNG DẪN QUAN TRỌNG:\n"
            f"1. CHỈ trả về câu lệnh SQL thuần túy, KHÔNG có giải thích, KHÔNG có bình luận, KHÔNG có markdown.\n"
            f"2. KHÔNG bao gồm bất kỳ ký tự đặc biệt nào ngoài cú pháp SQL tiêu chuẩn.\n"
            f"3. KHÔNG sử dụng ký tự Unicode đặc biệt trong truy vấn.\n"
            f"4. Đảm bảo cú pháp SQL chuẩn và tương thích với MariaDB/MySQL.\n"
            f"5. Sử dụng tên bảng và cột chính xác như đã cung cấp.\n"
            f"6. Truy vấn phải kết thúc bằng dấu chấm phẩy (;).\n\n"
            f"Yêu cầu: {question}\n\n"
            f"Truy vấn SQL (CHỈ trả về SQL thuần túy, không có giải thích):"
        ),
        "max_tokens": 512,
        "temperature": 0.7,
        "stream": False,
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        
        sql_query = response.json().get("choices", [{}])[0].get("text", "").strip()
        
        # Làm sạch truy vấn SQL
        # Loại bỏ các dòng bắt đầu bằng -- (comment trong SQL)
        sql_query = re.sub(r'--.*?\n', '', sql_query)
        
        # Loại bỏ các khối comment /* ... */
        sql_query = re.sub(r'/\*.*?\*/', '', sql_query, flags=re.DOTALL)
        
        # Loại bỏ các dòng trống và khoảng trắng thừa
        sql_query = '\n'.join([line.strip() for line in sql_query.split('\n') if line.strip()])
        
        # Loại bỏ các phần không phải SQL như "```sql" và "```"
        sql_query = re.sub(r'```sql|```', '', sql_query)
        
        # Loại bỏ các từ khóa không phải SQL
        non_sql_patterns = [
            r'^SQL:', r'^Truy vấn SQL:', r'^Câu lệnh SQL:',
            r'Đây là truy vấn SQL', r'Kết quả:', r'Giải thích:'
        ]
        for pattern in non_sql_patterns:
            sql_query = re.sub(pattern, '', sql_query, flags=re.IGNORECASE)
        
        # Loại bỏ phần giải thích sau truy vấn
        if ';' in sql_query:
            sql_query = sql_query.split(';')[0] + ';'
        
        # Loại bỏ các ký tự Unicode đặc biệt
        sql_query = re.sub(r'[^\x00-\x7F]+', '', sql_query)
        
        # Đảm bảo truy vấn kết thúc bằng dấu chấm phẩy
        sql_query = sql_query.strip()
        if sql_query and not sql_query.endswith(";"):
            sql_query += ";"
        
        # Kiểm tra xem truy vấn có hợp lệ không
        if not is_valid_sql(sql_query):
            return "SELECT 'Không thể tạo truy vấn SQL hợp lệ' AS error;"
        
        return sql_query
    
    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối đến LLM Studio: {e}")
        return "SELECT 'Lỗi kết nối đến LLM Studio' AS error;"
    
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return "SELECT 'Lỗi xử lý truy vấn' AS error;"

def is_valid_sql(sql_query):
    """Kiểm tra xem truy vấn SQL có hợp lệ không"""
    # Kiểm tra cơ bản
    if not sql_query or len(sql_query) < 5:
        return False
    
    # Kiểm tra xem có chứa các từ khóa SQL cơ bản không
    basic_keywords = ['SELECT', 'FROM', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'SHOW']
    has_keyword = False
    for keyword in basic_keywords:
        if keyword in sql_query.upper():
            has_keyword = True
            break
    
    if not has_keyword:
        return False
    
    # Kiểm tra xem có chứa các ký tự không hợp lệ không
    invalid_chars = ['用户名', '？', '…']
    for char in invalid_chars:
        if char in sql_query:
            return False
    
    return True

def get_document_response(question, doc_results):
    """Tạo câu trả lời dựa vào kết quả tìm kiếm từ tài liệu"""
    # Format kết quả từ tài liệu thành câu truy vấn giả SQL để hiển thị
    sql_like_response = "SELECT * FROM document_results WHERE content = '"
    
    # Thêm nội dung tài liệu vào câu trả lời
    content_parts = []
    for doc_name, sections in doc_results.items():
        for section in sections:
            clean_section = section.replace("'", "''")  # Escape dấu nháy đơn trong SQL
            content_parts.append(f"--- Từ {doc_name} ---\n{clean_section}")
    
    sql_like_response += " | ".join(content_parts)
    sql_like_response += "';"
    
    return sql_like_response
