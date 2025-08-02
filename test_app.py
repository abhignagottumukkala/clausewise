"""
Test script for ClauseWise
Tests the application without requiring API credentials
"""

import streamlit as st
from utils.document_processor import DocumentProcessor
import os

def test_document_processing():
    """Test document processing functionality"""
    
    st.title("🧪 ClauseWise Test")
    st.markdown("Testing document processing without API credentials")
    
    # Test document processor
    processor = DocumentProcessor()
    
    # Show supported formats
    supported_formats = processor.get_supported_formats_display()
    st.info(f"**Supported Formats:** {supported_formats}")
    
    # File upload section
    st.subheader("📤 Upload Your Document")
    
    uploaded_file = st.file_uploader(
        "Upload a legal document to test processing",
        type=['pdf', 'docx', 'txt', 'rtf', 'doc', 'odt'],
        help=f"Supported formats: {supported_formats}"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Process the uploaded file
        result = processor.process_document(uploaded_file)
        
        if result["success"]:
            st.success("✅ Document processed successfully!")
            
            # Document stats
            stats = processor.get_document_stats(result["text"])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Words", f"{stats['word_count']:,}")
            with col2:
                st.metric("Sentences", f"{stats['sentence_count']:,}")
            with col3:
                st.metric("Paragraphs", f"{stats['paragraph_count']:,}")
            with col4:
                st.metric("Reading Time", f"~{stats['estimated_reading_time']} min")
            
            # Document preview
            with st.expander("View Processed Document"):
                st.text_area(
                    "Document Content", 
                    value=result["text"][:2000] + "..." if len(result["text"]) > 2000 else result["text"], 
                    height=300
                )
            
            # Analysis options
            st.subheader("🔍 Analysis Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📋 Generate Summary"):
                    summary = processor.summarize_document(result["text"])
                    st.session_state['document_summary'] = summary
                    st.session_state['processed_text'] = result["text"]
                    st.session_state['filename'] = result["filename"]
                    
                    st.subheader("📋 Document Summary")
                    st.text_area("Summary", value=summary, height=300)
                    st.success("✅ Summary generated! Check download options below.")
            
            with col2:
                if st.button("🔍 Extract Clauses"):
                    clauses = processor.split_into_clauses(result["text"])
                    
                    if clauses:
                        st.success(f"✅ Extracted {len(clauses)} clauses")
                        
                        for i, clause in enumerate(clauses[:3]):  # Show first 3 clauses
                            with st.expander(f"Clause {i+1}"):
                                st.text_area(f"Clause {i+1}", value=clause, height=150)
                        
                        if len(clauses) > 3:
                            st.info(f"Showing first 3 clauses. Total: {len(clauses)}")
                    else:
                        st.warning("⚠️ No clauses detected")
            
            # Download functionality
            if st.session_state.get('document_summary'):
                st.subheader("💾 Download Options")
                
                base_filename = os.path.splitext(st.session_state.get('filename', 'document'))[0]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📝 Summary as TXT**")
                    if st.button("Download Summary TXT", key="test_summary_txt"):
                        download_link = processor.create_download_link(
                            st.session_state['document_summary'], 
                            f"{base_filename}_summary.txt", 
                            "txt"
                        )
                        st.markdown(download_link, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**📄 Summary as DOCX**")
                    if st.button("Download Summary DOCX", key="test_summary_docx"):
                        download_link = processor.create_download_link(
                            st.session_state['document_summary'], 
                            f"{base_filename}_summary.docx", 
                            "docx"
                        )
                        st.markdown(download_link, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("**📊 Summary as PDF**")
                    if st.button("Download Summary PDF", key="test_summary_pdf"):
                        download_link = processor.create_download_link(
                            st.session_state['document_summary'], 
                            f"{base_filename}_summary.pdf", 
                            "pdf"
                        )
                        st.markdown(download_link, unsafe_allow_html=True)
                
                # Also offer original document download
                st.subheader("📄 Download Original Document")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📝 Original as TXT**")
                    if st.button("Download Original TXT", key="test_original_txt"):
                        download_link = processor.create_download_link(
                            st.session_state['processed_text'], 
                            f"{base_filename}_original.txt", 
                            "txt"
                        )
                        st.markdown(download_link, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**📄 Original as DOCX**")
                    if st.button("Download Original DOCX", key="test_original_docx"):
                        download_link = processor.create_download_link(
                            st.session_state['processed_text'], 
                            f"{base_filename}_original.docx", 
                            "docx"
                        )
                        st.markdown(download_link, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("**📊 Original as PDF**")
                    if st.button("Download Original PDF", key="test_original_pdf"):
                        download_link = processor.create_download_link(
                            st.session_state['processed_text'], 
                            f"{base_filename}_original.pdf", 
                            "pdf"
                        )
                        st.markdown(download_link, unsafe_allow_html=True)
            
        else:
            st.error(f"❌ Error processing file: {result['error']}")
    
    else:
        # Show sample document for testing
        st.subheader("📄 Sample Document (for testing without upload)")
        
        sample_text = """
        CONFIDENTIALITY AGREEMENT
        
        This Confidentiality Agreement (the "Agreement") is entered into as of January 1, 2024, 
        by and between ABC Corporation, a Delaware corporation ("Company"), and John Doe 
        ("Recipient"), collectively referred to as the "Parties."
        
        WHEREAS, the Parties wish to establish a confidential relationship for the purpose of 
        discussing potential business opportunities;
        
        NOW, THEREFORE, in consideration of the mutual promises and covenants contained herein, 
        the Parties agree as follows:
        
        1. CONFIDENTIAL INFORMATION. "Confidential Information" means any information disclosed 
        by Company to Recipient, either directly or indirectly, in writing, orally or by 
        inspection of tangible objects, which is designated as "Confidential," "Proprietary" 
        or some similar designation.
        
        2. NON-DISCLOSURE. Recipient agrees not to use any Confidential Information for any 
        purpose except to evaluate and engage in discussions concerning a potential business 
        relationship between the Parties.
        
        3. TERM. This Agreement shall remain in effect for a period of two (2) years from 
        the date of this Agreement.
        
        IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first 
        written above.
        """
        
        st.text_area("Sample Legal Document", value=sample_text, height=300)
        
        # Test document statistics
        st.subheader("📊 Document Statistics")
        stats = processor.get_document_stats(sample_text)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Words", f"{stats['word_count']:,}")
        with col2:
            st.metric("Sentences", f"{stats['sentence_count']:,}")
        with col3:
            st.metric("Paragraphs", f"{stats['paragraph_count']:,}")
        with col4:
            st.metric("Reading Time", f"~{stats['estimated_reading_time']} min")
        
        # Test clause extraction
        st.subheader("🔍 Clause Extraction")
        clauses = processor.split_into_clauses(sample_text)
        
        if clauses:
            st.success(f"✅ Extracted {len(clauses)} clauses from document")
            
            for i, clause in enumerate(clauses):
                with st.expander(f"Clause {i+1}"):
                    st.text_area(f"Clause {i+1}", value=clause, height=150)
        else:
            st.warning("⚠️ No clauses detected in document")
        
        # Test mock AI functionality
        st.subheader("🤖 Mock AI Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Test Document Classification"):
                # Mock classification
                st.info("Mock Document Classification Results:")
                st.markdown("- **Document Type:** NDA (Non-Disclosure Agreement)")
                st.markdown("- **Confidence:** 85%")
                st.markdown("- **Key Terms:** confidentiality, non-disclosure, proprietary")
                
                # Mock entity extraction
                st.markdown("**Extracted Entities:**")
                st.markdown("- **Parties:** ABC Corporation, John Doe")
                st.markdown("- **Dates:** January 1, 2024")
                st.markdown("- **Legal Terms:** Confidentiality Agreement, Confidential Information")
        
        with col2:
            if st.button("📝 Test Document Summarization"):
                # Generate summary
                summary = processor.summarize_document(sample_text)
                st.text_area("Document Summary", value=summary, height=200)
                
                # Test download functionality
                if st.button("💾 Test Download Summary"):
                    download_link = processor.create_download_link(
                        summary, 
                        "sample_summary.txt", 
                        "txt"
                    )
                    st.markdown(download_link, unsafe_allow_html=True)
        
        # Test download functionality
        st.subheader("💾 Download Functionality Test")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Download as TXT"):
                download_link = processor.create_download_link(
                    sample_text, 
                    "sample_document.txt", 
                    "txt"
                )
                st.markdown(download_link, unsafe_allow_html=True)
        
        with col2:
            if st.button("📄 Download as DOCX"):
                download_link = processor.create_download_link(
                    sample_text, 
                    "sample_document.docx", 
                    "docx"
                )
                st.markdown(download_link, unsafe_allow_html=True)
        
        with col3:
            if st.button("📊 Download as PDF"):
                download_link = processor.create_download_link(
                    sample_text, 
                    "sample_document.pdf", 
                    "pdf"
                )
                st.markdown(download_link, unsafe_allow_html=True)


if __name__ == "__main__":
    test_document_processing() 