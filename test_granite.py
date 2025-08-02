"""
Test script for IBM Granite model integration
"""

import os
from dotenv import load_dotenv
from utils.huggingface_client import HuggingFaceClient

# Load environment variables
load_dotenv()

def test_granite_model():
    """Test the IBM Granite model integration"""
    print("Testing IBM Granite model integration...")
    
    # Initialize client
    client = HuggingFaceClient()
    
    if not client.api_available:
        print("❌ HUGGINGFACE_API_KEY not found in environment variables")
        return
    
    print("✅ API key found")
    
    # Test document classification
    test_text = """
    NON-DISCLOSURE AGREEMENT
    
    This Non-Disclosure Agreement (the "Agreement") is entered into as of [Date] by and between:
    
    [Company Name], a corporation organized under the laws of [State] ("Disclosing Party")
    and
    [Recipient Name], an individual ("Receiving Party")
    
    WHEREAS, the parties wish to explore a potential business relationship;
    WHEREAS, in connection with such exploration, the Disclosing Party may disclose to the Receiving Party certain confidential and proprietary information;
    
    NOW, THEREFORE, in consideration of the mutual promises and covenants contained herein, the parties agree as follows:
    
    1. CONFIDENTIAL INFORMATION. "Confidential Information" means any information disclosed by the Disclosing Party to the Receiving Party, either directly or indirectly, in writing, orally or by inspection of tangible objects.
    
    2. NON-USE AND NON-DISCLOSURE. The Receiving Party agrees not to use the Confidential Information for any purpose other than to evaluate the potential business relationship.
    
    3. MAINTENANCE OF CONFIDENTIALITY. The Receiving Party agrees that it shall take reasonable measures to protect the secrecy of and avoid disclosure and unauthorized use of the Confidential Information.
    """
    
    print("\n🔍 Testing Document Classification...")
    result = client.classify_document_type(test_text)
    if result.get("success"):
        print(f"✅ Document Type: {result.get('document_type')}")
        print(f"✅ Model Used: {result.get('model_used')}")
    else:
        print("❌ Classification failed")
    
    print("\n📝 Testing Document Summarization...")
    result = client.generate_summary(test_text)
    if result.get("success"):
        print(f"✅ Summary generated successfully")
        print(f"✅ Model Used: {result.get('model_used')}")
        print(f"📄 Summary: {result.get('summary')[:200]}...")
    else:
        print("❌ Summarization failed")
    
    print("\n🔧 Testing Clause Simplification...")
    test_clause = "The Receiving Party agrees that it shall take reasonable measures to protect the secrecy of and avoid disclosure and unauthorized use of the Confidential Information."
    result = client.simplify_clause(test_clause)
    if result.get("success"):
        print(f"✅ Clause simplified successfully")
        print(f"✅ Model Used: {result.get('model_used')}")
        print(f"📄 Original: {result.get('original')}")
        print(f"📄 Simplified: {result.get('simplified')}")
    else:
        print("❌ Simplification failed")
    
    print("\n🏷️ Testing Entity Extraction...")
    result = client.extract_legal_entities(test_text)
    if result.get("success"):
        print(f"✅ Entities extracted successfully")
        print(f"✅ Model Used: {result.get('model_used')}")
        entities = result.get("entities", [])
        print(f"📄 Found {len(entities)} entities")
        for entity in entities[:3]:  # Show first 3
            print(f"   - {entity.get('text', '')} ({entity.get('type', '')})")
    else:
        print("❌ Entity extraction failed")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_granite_model() 