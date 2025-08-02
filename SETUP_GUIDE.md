# ClauseWise Setup Guide

## Step-by-Step Implementation Guide

### 1. Project Structure Overview

The ClauseWise project has been implemented with the following structure:

```
clausewise/
├── app.py                 # Main Streamlit application
├── test_app.py           # Test application (no API credentials needed)
├── requirements.txt      # Python dependencies
├── env_example.txt      # Example environment variables
├── README.md            # Project documentation
├── SETUP_GUIDE.md      # This setup guide
├── utils/
│   ├── __init__.py
│   ├── document_processor.py  # Document processing utilities
│   ├── watson_client.py       # IBM Watson API client
│   └── granite_client.py      # IBM Granite API client
└── components/
    ├── __init__.py
    ├── sidebar.py             # Sidebar components
    └── document_upload.py     # Document upload interface
```

### 2. Installation Steps

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Set Up Environment Variables
1. Copy `env_example.txt` to `.env`
2. Add your IBM Watson API credentials:
   ```
   IBM_API_KEY=your_actual_api_key_here
   IBM_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/your_instance_id
   ```

#### Step 3: Get IBM Watson API Credentials
1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Create a Natural Language Understanding service
3. Get your API key and service URL
4. Add them to your `.env` file

### 3. Running the Application

#### Option 1: Run with API Credentials (Full Functionality)
```bash
streamlit run app.py
```

#### Option 2: Run Test Version (No API Credentials Needed)
```bash
streamlit run test_app.py
```

### 4. Features Implemented

#### ✅ Core Features
1. **Document Upload & Processing**
   - Support for PDF, DOCX, and TXT files
   - Text extraction and processing
   - Document statistics calculation

2. **Clause Analysis**
   - Automatic clause extraction
   - Document simplification using AI
   - Structure analysis

3. **Entity Recognition**
   - Named Entity Recognition (NER)
   - Legal entity extraction
   - Parties, dates, amounts, locations identification

4. **Document Classification**
   - Automatic document type classification
   - Support for NDA, employment contracts, leases, etc.
   - Confidence scoring

5. **User Interface**
   - Streamlit-based web interface
   - Tabbed navigation
   - Real-time analysis results

#### 🔧 Technical Implementation

1. **Document Processing Pipeline**
   ```
   Upload → Extract Text → Split Clauses → AI Analysis → Results
   ```

2. **AI Integration**
   - IBM Watson Natural Language Understanding
   - IBM Granite for advanced processing
   - Mock implementations for testing

3. **Error Handling**
   - Graceful API error handling
   - User-friendly error messages
   - Fallback to mock functionality

### 5. API Integration Details

#### IBM Watson Integration
- **Natural Language Understanding**: Entity extraction, sentiment analysis
- **Document Classification**: Automatic categorization
- **Entity Recognition**: Legal-specific entity identification

#### IBM Granite Integration
- **Advanced Text Processing**: Complex legal text simplification
- **Document Classification**: Enhanced classification capabilities
- **Clause Structure Analysis**: Deep analysis of legal clause structure

### 6. Testing and Validation

#### Test Without API Credentials
Run `test_app.py` to test:
- Document processing
- Clause extraction
- Mock AI analysis
- File upload functionality

#### Test with API Credentials
Run `app.py` to test:
- Full AI-powered analysis
- Real entity recognition
- Live document classification
- Advanced simplification

### 7. Customization Options

#### Model Selection
- Choose between Watson, Granite, or both
- Configure analysis parameters
- Set confidence thresholds

#### Processing Options
- Adjust clause length limits
- Configure entity extraction settings
- Set document processing preferences

### 8. Deployment Considerations

#### Local Development
- Use `streamlit run app.py` for local testing
- Set up virtual environment
- Configure environment variables

#### Production Deployment
- Deploy to Streamlit Cloud, Heroku, or similar
- Set up proper environment variables
- Configure API rate limits
- Implement proper error handling

### 9. Troubleshooting

#### Common Issues
1. **API Connection Errors**
   - Verify API credentials in `.env`
   - Check network connectivity
   - Ensure service is active

2. **Document Processing Errors**
   - Check file format support
   - Verify file size limits
   - Ensure proper file encoding

3. **Import Errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Verify file paths

### 10. Next Steps

#### Immediate Enhancements
1. Add more document formats (RTF, HTML)
2. Implement batch processing
3. Add export functionality (PDF, DOCX)
4. Enhance visualization components

#### Advanced Features
1. Multi-language support
2. Advanced analytics dashboard
3. User authentication
4. Document comparison tools
5. Template generation

### 11. Performance Optimization

#### Current Optimizations
- Efficient document processing
- Cached AI responses
- Optimized text extraction

#### Future Optimizations
- Implement caching layer
- Add background processing
- Optimize API calls
- Add result persistence

### 12. Security Considerations

#### Data Privacy
- No document storage on server
- Temporary processing only
- Secure API communication

#### API Security
- Environment variable protection
- Rate limiting implementation
- Error message sanitization

## Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment (copy and edit)
cp env_example.txt .env
# Edit .env with your API credentials

# 3. Test without API credentials
streamlit run test_app.py

# 4. Run full application
streamlit run app.py
```

## Support and Documentation

- **README.md**: Complete project documentation
- **Test App**: Use `test_app.py` for testing without credentials
- **Error Logs**: Check Streamlit console for detailed error messages
- **API Documentation**: Refer to IBM Watson and Granite documentation

The ClauseWise application is now ready for use! Start with the test application to verify functionality, then configure your API credentials for full AI-powered analysis. 