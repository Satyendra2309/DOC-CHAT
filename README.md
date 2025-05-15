# AI Document Chat

A powerful document chat application that allows you to upload documents and interact with them using natural language. The application uses advanced text processing and AI to provide intelligent responses based on your documents.

## Features

- 📄 Support for PDF and DOCX documents
- 🤖 AI-powered document understanding
- 💬 Natural language interaction
- 🔍 Smart document search and retrieval
- 📱 Modern, user-friendly interface
- 🔒 Secure document processing

## Prerequisites

- Python 3.8 or higher
- OpenRouter API key (for AI responses)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/docchat.git
cd docchat
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API key:
```
DEEPSEEK_API_KEY=your_openrouter_api_key_here
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Usage

1. Start the application:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload a document (PDF or DOCX)

4. Start chatting with your document!

## Project Structure

```
docchat/
├── src/
│   ├── app.py                 # Main Streamlit application
│   └── utils/
│       ├── chat_manager.py    # Handles chat interactions
│       └── document_processor.py  # Processes documents
├── data/                      # Directory for uploaded documents
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (not tracked by git)
└── README.md                 # This file
```

## Technical Details

- **Document Processing**: Uses TF-IDF vectorization and cosine similarity for efficient document search
- **Chat Interface**: Built with Streamlit for a modern, responsive UI
- **AI Integration**: Uses OpenRouter API with Mistral 7B model for intelligent responses
- **Text Processing**: Implements chunking and semantic search for better context understanding

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web framework
- OpenRouter for AI capabilities
- The open-source community for various libraries and tools

## Support

If you encounter any issues or have questions, please:
1. Check the existing issues
2. Create a new issue with a detailed description
3. Include any relevant error messages or screenshots 