"""
ClauseWise - AI-Powered Legal Document Analyzer
Enhanced Streamlit application for long legal documents
"""

import streamlit as st
import os
from dotenv import load_dotenv
from utils.document_processor import DocumentProcessor
from utils.huggingface_client import HuggingFaceClient
import pandas as pd
import io

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ClauseWise - AI Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
if 'document_text' not in st.session_state:
    st.session_state.document_text = ""
if 'filename' not in st.session_state:
    st.session_state.filename = ""
if 'clauses' not in st.session_state:
    st.session_state.clauses = []
if 'simplified_text' not in st.session_state:
    st.session_state.simplified_text = ""
if 'document_summary' not in st.session_state:
    st.session_state.document_summary = ""
if 'clause_analysis' not in st.session_state:
    st.session_state.clause_analysis = []
if 'document_type' not in st.session_state:
    st.session_state.document_type = ""

# Initialize AI clients
@st.cache_resource
def get_ai_clients():
    """Initialize AI clients with caching"""
    return {
        'huggingface': HuggingFaceClient()
    }

def main():
    # Header
    st.title("⚖️ ClauseWise")
    st.subheader("AI-Powered Legal Document Analyzer")
    st.markdown("**Powered by IBM Granite Model - Upload any legal document and get a comprehensive analysis with simplified explanations**")
    
    # Initialize AI clients
    ai_clients = get_ai_clients()
    
    # Document upload section
    st.header("📄 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=['txt', 'pdf', 'docx', 'doc', 'rtf', 'odt'],
        help="Upload any legal document (PDF, DOCX, TXT, DOC, RTF, ODT)"
    )
    
    if uploaded_file is not None:
        # Process the uploaded file
        doc_processor = DocumentProcessor()
        result = doc_processor.process_uploaded_file(uploaded_file)
        
        if result.get("success"):
            st.session_state.document_text = result.get("text", "")
            st.session_state.filename = uploaded_file.name
            
            st.success(f"✅ Document '{uploaded_file.name}' uploaded successfully!")
            
            # Document statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Document Length", f"{len(st.session_state.document_text)} characters")
            with col2:
                st.metric("Word Count", f"{len(st.session_state.document_text.split())} words")
            with col3:
                st.metric("Line Count", f"{len(st.session_state.document_text.splitlines())} lines")
            with col4:
                file_size = len(uploaded_file.getvalue()) / 1024
                st.metric("File Size", f"{file_size:.1f} KB")
            
            # Show document preview
            with st.expander("📄 Document Preview"):
                st.text(st.session_state.document_text[:2000] + "..." if len(st.session_state.document_text) > 2000 else st.session_state.document_text)
        else:
            st.error(f"❌ Error processing file: {result.get('error', 'Unknown error')}")
    
    # Analysis section
    if st.session_state.document_text:
        st.header("🔍 Document Analysis")
        
        # Analysis options
        analysis_type = st.selectbox(
            "Select Analysis Type:",
            ["Comprehensive Analysis", "Document Summarization", "Clause-by-Clause Analysis", "Document Simplification", "Legal Entity Extraction"]
        )
        
        if st.button("🔍 Analyze Document", type="primary"):
            with st.spinner("Analyzing document..."):
                if analysis_type == "Comprehensive Analysis":
                    comprehensive_analysis(ai_clients['huggingface'])
                elif analysis_type == "Document Summarization":
                    analyze_document_summarization(ai_clients['huggingface'])
                elif analysis_type == "Clause-by-Clause Analysis":
                    analyze_clause_extraction(ai_clients['huggingface'])
                elif analysis_type == "Document Simplification":
                    analyze_document_simplification(ai_clients['huggingface'])
                elif analysis_type == "Legal Entity Extraction":
                    analyze_legal_entities(ai_clients['huggingface'])
    else:
        st.info("Please upload a document to begin analysis.")

def comprehensive_analysis(hf_client):
    """Perform comprehensive analysis of the document"""
    st.subheader("🔍 Comprehensive Document Analysis")
    
    # Step 1: Document classification
    st.write("**Step 1: Document Classification**")
    doc_type_result = hf_client.classify_document_type(st.session_state.document_text)
    if doc_type_result.get("success"):
        st.session_state.document_type = doc_type_result.get("document_type", "Legal Document")
        st.success(f"📋 Document Type: {st.session_state.document_type}")
        st.info(f"Confidence: {doc_type_result.get('confidence', 0):.2f}")
    
    # Step 2: Generate summary
    st.write("**Step 2: Document Summary**")
    summary_result = hf_client.generate_summary(st.session_state.document_text)
    if summary_result.get("success"):
        st.session_state.document_summary = summary_result.get("summary", "")
        st.write("**Executive Summary:**")
        st.write(st.session_state.document_summary)
    
    # Step 3: Extract and analyze clauses
    st.write("**Step 3: Clause Analysis**")
    doc_processor = DocumentProcessor()
    clauses = doc_processor.split_into_clauses(st.session_state.document_text)
    
    if clauses:
        st.session_state.clauses = clauses
        st.success(f"📋 Found {len(clauses)} clauses")
        
        # Analyze each clause
        clause_analysis = []
        for i, clause in enumerate(clauses[:20], 1):  # Limit to first 20 clauses for performance
            with st.spinner(f"Analyzing clause {i}..."):
                # Simplify clause
                simplify_result = hf_client.simplify_clause(clause)
                simplified = simplify_result.get("simplified", clause) if simplify_result.get("success") else clause
                
                # Extract key information
                key_info = extract_clause_key_info(clause)
                
                clause_analysis.append({
                    "clause_number": i,
                    "original": clause,
                    "simplified": simplified,
                    "type": classify_clause_type(clause),
                    "key_points": key_info
                })
        
        st.session_state.clause_analysis = clause_analysis
        
        # Display clause analysis
        for analysis in clause_analysis[:10]:  # Show first 10
            with st.expander(f"Clause {analysis['clause_number']} - {analysis['type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Original:**")
                    st.write(analysis['original'])
                with col2:
                    st.write("**Simplified:**")
                    st.write(analysis['simplified'])
                
                st.write("**Key Points:**")
                for point in analysis['key_points']:
                    st.write(f"• {point}")
    
    # Step 4: Generate simplified version
    st.write("**Step 4: Simplified Document**")
    simplify_result = hf_client.simplify_clause(st.session_state.document_text)
    if simplify_result.get("success"):
        st.session_state.simplified_text = simplify_result.get("simplified", "")
        st.write("**Simplified Version:**")
        st.write(st.session_state.simplified_text)
    
    # Step 5: Download options
    st.write("**Step 5: Download Results**")
    render_download_options()

def extract_clause_key_info(clause):
    """Extract key information from a clause"""
    key_points = []
    
    # Look for common legal terms and their implications
    legal_terms = {
        "confidential": "Contains confidentiality obligations",
        "termination": "Specifies termination conditions",
        "liability": "Defines liability and responsibility",
        "payment": "Outlines payment terms and conditions",
        "breach": "Defines what constitutes a breach",
        "governing law": "Specifies which law applies",
        "dispute": "Outlines dispute resolution process",
        "amendment": "Specifies how changes can be made",
        "force majeure": "Covers unforeseen circumstances",
        "indemnification": "Defines protection against losses"
    }
    
    clause_lower = clause.lower()
    for term, explanation in legal_terms.items():
        if term in clause_lower:
            key_points.append(explanation)
    
    if not key_points:
        key_points.append("Standard legal clause")
    
    return key_points

def classify_clause_type(clause):
    """Classify the type of clause"""
    clause_lower = clause.lower()
    
    if any(word in clause_lower for word in ["confidential", "non-disclosure"]):
        return "Confidentiality"
    elif any(word in clause_lower for word in ["termination", "terminate"]):
        return "Termination"
    elif any(word in clause_lower for word in ["payment", "pay", "fee"]):
        return "Payment"
    elif any(word in clause_lower for word in ["liability", "responsible"]):
        return "Liability"
    elif any(word in clause_lower for word in ["breach", "default"]):
        return "Breach"
    elif any(word in clause_lower for word in ["governing law", "jurisdiction"]):
        return "Governing Law"
    elif any(word in clause_lower for word in ["dispute", "arbitration"]):
        return "Dispute Resolution"
    else:
        return "General"

def analyze_document_summarization(hf_client):
    """Analyze document summarization"""
    st.subheader("📝 Document Summary")
    
    result = hf_client.generate_summary(st.session_state.document_text)
    
    if result.get("success"):
        summary = result.get("summary", "")
        st.session_state.document_summary = summary
        
        st.write("**Generated Summary:**")
        st.write(summary)
        
        # Display summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Length", f"{len(st.session_state.document_text)} characters")
        with col2:
            st.metric("Summary Length", f"{len(summary)} characters")
        with col3:
            compression_ratio = len(summary) / len(st.session_state.document_text) * 100
            st.metric("Compression Ratio", f"{compression_ratio:.1f}%")
    else:
        st.error("Failed to generate summary.")

def analyze_document_simplification(hf_client):
    """Analyze document simplification"""
    st.subheader("📝 Document Simplification")
    
    result = hf_client.simplify_clause(st.session_state.document_text)
    
    if result.get("success"):
        simplified = result.get("simplified", "")
        st.session_state.simplified_text = simplified
        
        st.write("**Simplified Document:**")
        st.write(simplified)
        
        # Display simplification statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Length", f"{len(st.session_state.document_text)} characters")
        with col2:
            st.metric("Simplified Length", f"{len(simplified)} characters")
        with col3:
            readability_improvement = (len(st.session_state.document_text) - len(simplified)) / len(st.session_state.document_text) * 100
            st.metric("Readability Improvement", f"{readability_improvement:.1f}%")
    else:
        st.error("Failed to simplify document.")

def analyze_clause_extraction(hf_client):
    """Analyze clause extraction"""
    st.subheader("📋 Clause-by-Clause Analysis")
    
    # Extract clauses using document processor
    doc_processor = DocumentProcessor()
    clauses = doc_processor.split_into_clauses(st.session_state.document_text)
    
    if clauses:
        st.write(f"**Found {len(clauses)} clauses:**")
        
        clause_analysis = []
        for i, clause in enumerate(clauses[:15], 1):  # Limit to first 15 clauses
            with st.spinner(f"Analyzing clause {i}..."):
                # Simplify this clause
                result = hf_client.simplify_clause(clause)
                simplified = result.get("simplified", clause) if result.get("success") else clause
                
                # Extract key information
                key_info = extract_clause_key_info(clause)
                
                clause_analysis.append({
                    "clause_number": i,
                    "original": clause,
                    "simplified": simplified,
                    "type": classify_clause_type(clause),
                    "key_points": key_info
                })
        
        st.session_state.clause_analysis = clause_analysis
        
        # Display clause analysis
        for analysis in clause_analysis:
            with st.expander(f"Clause {analysis['clause_number']} - {analysis['type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Original:**")
                    st.write(analysis['original'])
                with col2:
                    st.write("**Simplified:**")
                    st.write(analysis['simplified'])
                
                st.write("**Key Points:**")
                for point in analysis['key_points']:
                    st.write(f"• {point}")
    else:
        st.warning("No clauses found in the document.")

def analyze_legal_entities(hf_client):
    """Analyze legal entities"""
    st.subheader("🏷️ Legal Entity Recognition")
    
    result = hf_client.extract_legal_entities(st.session_state.document_text)
    
    if result.get("success"):
        entities = result.get("entities", [])
        
        if entities:
            # Group entities by type
            entity_types = {}
            for entity in entities:
                entity_type = entity.get("type", "OTHER")
                if entity_type not in entity_types:
                    entity_types[entity_type] = []
                entity_types[entity_type].append(entity)
            
            # Display entities by type
            for entity_type, type_entities in entity_types.items():
                with st.expander(f"{entity_type} ({len(type_entities)} entities)"):
                    for entity in type_entities:
                        confidence = entity.get("confidence", 0.0)
                        st.write(f"**{entity.get('text', '')}** (confidence: {confidence:.2f})")
        else:
            st.info("No entities found in the document.")
    else:
        st.error("Failed to extract entities.")

def render_download_options():
    """Render download options for analysis results"""
    st.subheader("💾 Download Results")
    
    doc_processor = DocumentProcessor()
    
    # Create download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📝 Simplified Document**")
        if st.session_state.simplified_text:
            txt_download = doc_processor.create_download_link(
                st.session_state.simplified_text, 
                f"simplified_{st.session_state.filename}.txt", 
                "txt"
            )
            st.download_button("📄 Download TXT", txt_download, file_name=f"simplified_{st.session_state.filename}.txt")
        else:
            st.info("No simplified document available.")
    
    with col2:
        st.write("**📝 Document Summary**")
        if st.session_state.document_summary:
            txt_download = doc_processor.create_download_link(
                st.session_state.document_summary, 
                f"summary_{st.session_state.filename}.txt", 
                "txt"
            )
            st.download_button("📄 Download TXT", txt_download, file_name=f"summary_{st.session_state.filename}.txt")
        else:
            st.info("No document summary available.")
    
    with col3:
        st.write("**📋 Clause Analysis**")
        if st.session_state.clause_analysis:
            # Create CSV of clause analysis
            clause_data = []
            for analysis in st.session_state.clause_analysis:
                clause_data.append({
                    "Clause Number": analysis['clause_number'],
                    "Type": analysis['type'],
                    "Original": analysis['original'][:200] + "..." if len(analysis['original']) > 200 else analysis['original'],
                    "Simplified": analysis['simplified'][:200] + "..." if len(analysis['simplified']) > 200 else analysis['simplified']
                })
            
            df = pd.DataFrame(clause_data)
            csv = df.to_csv(index=False)
            st.download_button(
                "📊 Download CSV",
                csv,
                file_name=f"clause_analysis_{st.session_state.filename}.csv",
                mime="text/csv"
            )
        else:
            st.info("No clause analysis available.")

if __name__ == "__main__":
    main() 