import os
from typing import List
from pypdf import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DocumentProcessor:
    def __init__(self):
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 200))
        )
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        self.chunks = []
        self.vector_store = None

    def process_document(self, file_path: str) -> None:
        """Process a document and store its chunks."""
        try:
            # Extract text based on file type
            if file_path.endswith('.pdf'):
                text = self._extract_text_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                text = self._extract_text_from_docx(file_path)
            else:
                raise ValueError("Unsupported file format. Please use PDF or DOCX files.")

            # Split text into chunks
            self.chunks = self.text_splitter.split_text(text)
            
            # Create TF-IDF vectors
            if len(self.chunks) > 0:
                self.vector_store = self.vectorizer.fit_transform(self.chunks)
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            raise

    def _extract_text(self, file) -> str:
        """Extract text from different file types."""
        # Get the file extension
        file_extension = os.path.splitext(file.name)[1].lower()
        
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        try:
            if file_extension == '.pdf':
                return self._extract_text_from_pdf(temp_file_path)
            elif file_extension == '.docx':
                return self._extract_text_from_docx(temp_file_path)
            elif file_extension == '.txt':
                with open(temp_file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from a DOCX file."""
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def get_relevant_chunks(self, query: str, k: int = 3) -> List[str]:
        """Get the most relevant chunks for a given query using TF-IDF and cosine similarity."""
        if self.vector_store is None or len(self.chunks) == 0:
            return []
        
        try:
            # Transform query to TF-IDF vector
            query_vector = self.vectorizer.transform([query])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, self.vector_store).flatten()
            
            # Get top k most similar chunks
            top_k_indices = similarities.argsort()[-k:][::-1]
            
            return [self.chunks[i] for i in top_k_indices]
        except Exception as e:
            print(f"Error getting relevant chunks: {str(e)}")
            return []

    def has_documents(self) -> bool:
        """Check if there are any documents processed."""
        return self.vector_store is not None and len(self.chunks) > 0

    def clear_documents(self) -> None:
        """Clear all processed documents."""
        self.vector_store = None
        self.chunks = [] 