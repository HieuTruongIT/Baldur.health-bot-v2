# RAG Chatbot - Hỏi đáp dựa trên tài liệu cá nhân

Một chatbot RAG (Retrieval-Augmented Generation) đơn giản, chạy local hoặc deploy trên Streamlit Cloud, cho phép bạn chat hỏi đáp dựa trên các tài liệu của mình (PDF, TXT, DOCX, Markdown...).

Hiện tại hỗ trợ:
- Chạy hoàn toàn local với **Ollama** (miễn phí, offline)
- Dễ dàng chuyển sang dùng API nhanh như **Groq**, **Gemini**, **Together AI**... để deploy cloud
- Giao diện chat thân thiện bằng **Streamlit**
- Tự động build vector index từ thư mục `data/`

## Demo (nếu đã deploy)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

*(Thay link trên bằng URL thật sau khi deploy)*

## Tính năng chính
- Không cần train/fine-tune mô hình
- Hỗ trợ tốt tiếng Việt (dùng embedding BkAI + model tiếng Việt nếu cần)
- Lưu lịch sử chat trong session
- Tự động rebuild index khi thêm tài liệu mới
- Dễ mở rộng: thêm reranker, conversational memory, multi-file upload...

## Cài đặt nhanh (Local)

### Yêu cầu
- Python 3.10+
- [Ollama](https://ollama.com/) đã cài và chạy (tải model ví dụ: `ollama pull llama3.2`)
- (Tùy chọn) GPU nếu muốn embedding/model nhanh hơn

### Các bước
1. Clone repo
   ```bash
   git clone https://github.com/<username>/rag-chatbot.git
   cd rag-chatbot"# Baldur.health-V2" 
"# Baldur.health-bot-v2" 
