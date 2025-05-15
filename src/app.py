import os
import streamlit as st
from utils.document_processor import DocumentProcessor
from utils.chat_manager import ChatManager
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify DeepSeek API key
if not os.getenv("DEEPSEEK_API_KEY"):
    st.error("DeepSeek API key not found! Please create a .env file with your DEEPSEEK_API_KEY.")
    st.stop()

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary location and return the file path."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def main():
    st.title("📚 AI Document Chat")
    st.write("Upload your documents and chat with them using AI!")

    # Initialize session state
    if "document_processor" not in st.session_state:
        st.session_state.document_processor = DocumentProcessor()
    if "chat_manager" not in st.session_state:
        st.session_state.chat_manager = ChatManager()

    # File upload
    uploaded_file = st.file_uploader("Upload a document (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file:
        # Save the uploaded file
        file_path = save_uploaded_file(uploaded_file)
        if file_path:
            try:
                # Process the document
                with st.spinner("Processing document..."):
                    st.session_state.document_processor.process_document(file_path)
                st.success("Document processed successfully!")
                
                # Clean up the temporary file
                os.unlink(file_path)
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                if file_path and os.path.exists(file_path):
                    os.unlink(file_path)

    # Chat interface
    if st.session_state.document_processor.has_documents():
        # Display chat history
        for message in st.session_state.chat_manager.get_chat_history():
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask a question about your document"):
            # Add user message to chat
            st.session_state.chat_manager.add_message("user", prompt)
            with st.chat_message("user"):
                st.write(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Get relevant document chunks
                    relevant_chunks = st.session_state.document_processor.get_relevant_chunks(prompt)
                    
                    # Generate response
                    response = st.session_state.chat_manager.get_response(prompt, relevant_chunks)
                    st.write(response)
    else:
        st.info("Please upload a document to start chatting!")

if __name__ == "__main__":
    main() 