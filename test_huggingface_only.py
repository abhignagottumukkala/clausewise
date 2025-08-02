#!/usr/bin/env python3
"""
Test script for Hugging Face only version of ClauseWise
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from utils.document_processor import DocumentProcessor
        print("✅ DocumentProcessor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DocumentProcessor: {e}")
        return False
    
    try:
        from utils.huggingface_client import HuggingFaceClient
        print("✅ HuggingFaceClient imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import HuggingFaceClient: {e}")
        return False
    
    try:
        from components.sidebar import render_sidebar
        print("✅ Sidebar component imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import sidebar component: {e}")
        return False
    
    try:
        from components.document_upload import render_document_upload
        print("✅ Document upload component imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import document upload component: {e}")
        return False
    
    return True

def test_huggingface_client():
    """Test Hugging Face client functionality"""
    print("\n🤖 Testing Hugging Face client...")
    
    try:
        from utils.huggingface_client import HuggingFaceClient
        
        client = HuggingFaceClient()
        print(f"✅ HuggingFaceClient initialized")
        print(f"   API Available: {client.api_available}")
        
        # Test with sample text
        sample_text = "This is a confidentiality agreement between ABC Corp and XYZ Inc."
        
        # Test document classification
        result = client.classify_document_type(sample_text)
        print(f"✅ Document classification: {result.get('document_type', 'Unknown')}")
        
        # Test entity extraction
        result = client.extract_legal_entities(sample_text)
        print(f"✅ Entity extraction: {len(result.get('entities', []))} entities found")
        
        # Test text simplification
        result = client.simplify_clause(sample_text)
        print(f"✅ Text simplification: {len(result.get('simplified', ''))} characters")
        
        # Test sentiment analysis
        result = client.analyze_sentiment(sample_text)
        print(f"✅ Sentiment analysis: {result.get('sentiment', 'Unknown')}")
        
        # Test key phrase extraction
        result = client.extract_key_phrases(sample_text)
        print(f"✅ Key phrase extraction: {len(result.get('key_phrases', []))} phrases found")
        
        # Test summary generation
        result = client.generate_summary(sample_text)
        print(f"✅ Summary generation: {len(result.get('summary', ''))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Hugging Face client test failed: {e}")
        return False

def test_document_processor():
    """Test document processor functionality"""
    print("\n📄 Testing document processor...")
    
    try:
        from utils.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        print("✅ DocumentProcessor initialized")
        
        # Test supported formats
        formats = processor.get_supported_formats_display()
        print(f"✅ Supported formats: {formats}")
        
        # Test document statistics
        sample_text = "This is a test document. It has multiple sentences. We can analyze it."
        stats = processor.get_document_stats(sample_text)
        print(f"✅ Document stats: {stats['word_count']} words, {stats['sentence_count']} sentences")
        
        # Test clause splitting
        clauses = processor.split_into_clauses(sample_text)
        print(f"✅ Clause splitting: {len(clauses)} clauses found")
        
        # Test download link creation
        download_link = processor.create_download_link(sample_text, "test.txt", "txt")
        print(f"✅ Download link creation: {len(download_link)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Document processor test failed: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment configuration...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found (will use default settings)")
    
    # Check Hugging Face API key
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if api_key:
        print("✅ Hugging Face API key found")
    else:
        print("⚠️  Hugging Face API key not found (will use local fallbacks)")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting ClauseWise Hugging Face Only Tests")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Document Processor", test_document_processor),
        ("Hugging Face Client", test_huggingface_client),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo run the application:")
        print("1. streamlit run app.py")
        print("2. Open http://localhost:8501 in your browser")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 