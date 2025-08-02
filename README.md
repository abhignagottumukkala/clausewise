# ⚖️ ClauseWise - AI-Powered Legal Document Analyzer

ClauseWise is an intelligent legal document analyzer that simplifies, decodes, and classifies complex legal texts using the IBM Granite model. Built with Streamlit and powered by IBM's advanced language model, it provides comprehensive legal document analysis capabilities.

## 🚀 Features

### 📄 Document Processing
- **Multi-Format Support**: Handle PDF, DOCX, TXT, RTF, DOC, and ODT files
- **Smart Text Extraction**: Extract text from various document formats seamlessly
- **Document Statistics**: Word count, sentence count, paragraphs, and estimated reading time

### 🤖 AI-Powered Analysis (IBM Granite Model)
- **Document Classification**: Automatically categorize legal documents (NDA, Employment Contract, Lease Agreement, etc.)
- **Entity Recognition**: Extract key legal entities (parties, dates, monetary amounts, organizations)
- **Text Simplification**: Convert complex legal language into plain English
- **Document Summarization**: Generate concise summaries of legal documents
- **Sentiment Analysis**: Analyze the tone and sentiment of legal clauses
- **Key Phrase Extraction**: Identify important legal terms and phrases

### 📊 Advanced Features
- **Clause Extraction**: Break down documents into individual clauses for focused analysis
- **Confidence Scoring**: Get confidence levels for all AI predictions
- **Multiple Export Formats**: Download results in TXT, DOCX, and PDF formats
- **Real-time Processing**: Instant analysis with progress indicators

## 🛠️ Technology Stack

### Core Technologies
- **Streamlit**: Modern web interface and user experience
- **IBM Granite Model**: Advanced AI capabilities for text processing
- **Python**: Backend processing and data manipulation

### AI Models Used
- **IBM Granite 13B Chat v2**: Primary model for all analysis tasks
  - Document Classification
  - Entity Recognition
  - Text Simplification
  - Sentiment Analysis
  - Key Phrase Extraction
  - Document Summarization

### Document Processing
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **ReportLab**: PDF generation for downloads

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd clausewise
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Environment Setup
1. Copy the environment example file:
```bash
cp env_example.txt .env
```

2. Edit `.env` and add your Hugging Face API key:
```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

**Note**: You can get a free Hugging Face API key from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🎯 Usage Guide

### 1. Document Upload
- Navigate to the "📄 Upload" tab
- Upload your legal document (PDF, DOCX, TXT, RTF, DOC, ODT)
- View document statistics and extracted text

### 2. Document Analysis
- Go to the "🔍 Analysis" tab
- Choose analysis type:
  - **Document Summarization**: Generate concise summaries
  - **Document Simplification**: Convert complex language to simple terms
  - **Clause Extraction**: Break down into individual clauses
  - **Full Document Analysis**: Comprehensive analysis

### 3. Entity Recognition
- Visit the "🏷️ Entities" tab
- Extract and view legal entities:
  - Parties and organizations
  - Dates and time periods
  - Monetary amounts
  - Legal terms and phrases

### 4. Document Classification
- Use the "📋 Classification" tab
- Automatically categorize your document
- View confidence scores and classification details

### 5. Download Results
- Access the "💾 Download" tab
- Download simplified documents and summaries
- Choose from TXT, DOCX, or PDF formats

## 🏗️ Project Structure

```
clausewise/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
├── env_example.txt            # Environment variables template
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── document_processor.py  # Document processing utilities
│   └── huggingface_client.py  # Hugging Face AI integration
├── components/                # UI components
│   ├── __init__.py
│   ├── sidebar.py             # Sidebar navigation
│   └── document_upload.py     # Document upload interface
└── test_app.py               # Standalone testing script
```

## 🔧 Configuration

### Environment Variables
- `HUGGINGFACE_API_KEY`: Your Hugging Face API token for AI model access

### Model Configuration
The application uses a hybrid approach:
- **API Models**: When Hugging Face API key is provided
- **Local Fallbacks**: Sophisticated local processing when API is unavailable

### Supported Document Types
- **PDF**: Contracts, agreements, legal documents
- **DOCX**: Word documents, legal templates
- **TXT**: Plain text legal documents
- **RTF**: Rich text format documents
- **DOC**: Legacy Word documents
- **ODT**: OpenDocument text files

## 🚀 API Integration

### Hugging Face Models
The application integrates with various Hugging Face models:

- **Document Classification**: Custom keyword-based classification
- **Entity Recognition**: BERT-based NER models
- **Text Simplification**: Rule-based with AI enhancement
- **Sentiment Analysis**: RoBERTa sentiment models
- **Key Phrase Extraction**: Specialized legal phrase models

### Local Processing
When API is unavailable, the application uses sophisticated local processing:
- Keyword-based document classification
- Regex-based entity extraction
- Rule-based text simplification
- TF-IDF key phrase extraction

## 🧪 Testing

### Test Application
Run the standalone test application:
```bash
python test_app.py
```

This provides a simplified interface for testing core functionalities without the full Streamlit interface.

### Sample Documents
The application includes sample documents for testing:
- Confidentiality Agreement
- Employment Contract
- Lease Agreement

## 🔒 Privacy & Security

- **Local Processing**: All document processing happens locally
- **No Data Storage**: Documents are not stored permanently
- **API Security**: Secure API calls with proper authentication
- **Session Management**: Temporary session storage only

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues
1. **API Key Issues**: Ensure your Hugging Face API key is correctly set
2. **Installation Problems**: Try installing packages individually
3. **Document Processing**: Check file format compatibility

### Getting Help
- Check the documentation
- Review the test application
- Examine error messages in the console

## 🎉 Acknowledgments

- **Hugging Face**: For providing free access to state-of-the-art AI models
- **Streamlit**: For the excellent web application framework
- **Open Source Community**: For the various Python libraries used

---

**ClauseWise** - Making legal documents accessible through AI-powered analysis. 