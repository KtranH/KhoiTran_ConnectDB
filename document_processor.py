import os
import re

class DocumentProcessor:
    def __init__(self, docs_folder="docs"):
        """Khởi tạo processor với đường dẫn đến thư mục tài liệu"""
        self.docs_folder = docs_folder
        self.documents = {}
        self.load_all_documents()

    def load_all_documents(self):
        """Đọc tất cả các tài liệu từ thư mục"""
        if not os.path.exists(self.docs_folder):
            print(f"Thư mục {self.docs_folder} không tồn tại!")
            return

        for file_name in os.listdir(self.docs_folder):
            if file_name.endswith('.txt'):
                file_path = os.path.join(self.docs_folder, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # Tách tên tài liệu từ tên file (bỏ đuôi .txt và thay gạch dưới bằng khoảng trắng)
                        doc_name = file_name[:-4].replace('_', ' ')
                        self.documents[doc_name] = content
                except Exception as e:
                    print(f"Không thể đọc file {file_name}: {e}")
    
    def get_document_names(self):
        """Trả về danh sách tên các tài liệu"""
        return list(self.documents.keys())
    
    def get_document_content(self, doc_name):
        """Trả về nội dung của một tài liệu dựa vào tên"""
        # Tìm tên tài liệu không phân biệt hoa thường và ký tự đặc biệt
        normalized_name = doc_name.lower()
        
        for name in self.documents:
            if name.lower() == normalized_name:
                return self.documents[name]
        
        # Nếu không tìm thấy chính xác, thử tìm tên gần đúng
        for name in self.documents:
            if normalized_name in name.lower() or name.lower() in normalized_name:
                return self.documents[name]
                
        return None
    
    def search_in_documents(self, query):
        """Tìm kiếm một chuỗi trong tất cả các tài liệu"""
        results = {}
        
        for doc_name, content in self.documents.items():
            # Tìm tất cả các đoạn chứa từ khóa (phân biệt hoa thường)
            matches = self._find_relevant_sections(content, query)
            if matches:
                results[doc_name] = matches
        
        return results
    
    def _find_relevant_sections(self, content, query):
        """Tìm các đoạn văn liên quan đến truy vấn"""
        # Chia tài liệu thành các đoạn (sections) theo dấu ##
        sections = re.split(r'(?=## )', content)
        
        relevant_sections = []
        for section in sections:
            if query.lower() in section.lower():
                # Làm sạch section, loại bỏ khoảng trắng thừa
                clean_section = section.strip()
                relevant_sections.append(clean_section)
        
        return relevant_sections

    def get_all_documents_content(self):
        """Lấy nội dung tất cả các tài liệu dưới dạng một chuỗi"""
        all_content = ""
        
        for doc_name, content in self.documents.items():
            all_content += f"\n=== {doc_name.upper()} ===\n\n"
            all_content += content
            all_content += "\n\n"
            
        return all_content 