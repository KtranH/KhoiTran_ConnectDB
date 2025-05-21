import requests
from document_processor import DocumentProcessor

def query_document_llm(question, context):
    """
    Gửi câu hỏi và nội dung tài liệu đến LLM để xử lý
    """
    url = "http://127.0.0.1:1234/v1/completions"
    
    prompt = (
        f"Dựa trên thông tin tài liệu sau đây, hãy trả lời câu hỏi của người dùng.\n\n"
        f"### THÔNG TIN TÀI LIỆU ###\n"
        f"{context}\n\n"
        f"### CÂU HỎI ###\n"
        f"{question}\n\n"
        f"### TRẢ LỜI ###\n"
        f"(Hãy trả lời ngắn gọn, rõ ràng dựa trên thông tin từ tài liệu. Nếu không có thông tin liên quan, "
        f"hãy trả lời rằng 'Không tìm thấy thông tin liên quan trong tài liệu.')"
    )
    
    payload = {
        "model": "gemma-3-12b-it",
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.3,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        answer = response.json().get("choices", [{}])[0].get("text", "").strip()
        return answer
    
    except requests.exceptions.RequestException as e:
        return f"Lỗi kết nối đến LLM Studio: {e}"
    except Exception as e:
        return f"Lỗi khi xử lý câu hỏi: {e}"

def process_document_query(question):
    """
    Xử lý câu hỏi liên quan đến tài liệu bằng LLM
    """
    doc_processor = DocumentProcessor()
    
    # Kiểm tra xem câu hỏi liên quan đến tài liệu cụ thể nào không
    doc_names = doc_processor.get_document_names()
    target_doc = None
    
    for doc_name in doc_names:
        if doc_name.lower() in question.lower():
            target_doc = doc_name
            break
    
    # Nếu câu hỏi chỉ định tài liệu cụ thể
    if target_doc:
        context = doc_processor.get_document_content(target_doc)
        if context:
            return query_document_llm(question, context)
        else:
            return "Không tìm thấy tài liệu được yêu cầu."
    
    # Tìm kiếm trong tất cả tài liệu
    doc_results = doc_processor.search_in_documents(question)
    
    if doc_results:
        # Tạo context từ các phần liên quan
        context_parts = []
        for doc_name, sections in doc_results.items():
            for section in sections:
                context_parts.append(f"--- Từ {doc_name} ---\n{section}")
        
        context = "\n\n".join(context_parts)
        return query_document_llm(question, context)
    else:
        # Không tìm thấy nội dung liên quan, sử dụng toàn bộ tài liệu làm context
        context = doc_processor.get_all_documents_content()
        return query_document_llm(question, context) 