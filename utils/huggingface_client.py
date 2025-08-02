"""
Hugging Face client for ClauseWise
Uses IBM Granite model for legal document analysis
"""

import os
import requests
import json
from typing import Dict, List, Any, Optional
import re

class HuggingFaceClient:
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.api_url = "https://api-inference.huggingface.co/models"
        self.api_available = bool(self.api_key)
        # IBM Granite model
        self.granite_model = "ibm-granite/granite-13b-chat-v2"
        
    def _make_api_call(self, model_name: str, inputs: Any) -> Optional[Dict]:
        """Make API call to Hugging Face Inference API"""
        if not self.api_available:
            return None
            
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.api_url}/{model_name}"
        
        try:
            response = requests.post(url, headers=headers, json=inputs, timeout=60)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API call failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"API call error: {e}")
            return None
    
    def _make_granite_call(self, prompt: str) -> Optional[Dict]:
        """Make API call to IBM Granite model"""
        if not self.api_available:
            return None
            
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.api_url}/{self.granite_model}"
        
        # Format for Granite model
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Granite API call failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Granite API call error: {e}")
            return None
    
    def classify_document_type(self, text: str) -> Dict[str, Any]:
        """Classify the type of legal document using IBM Granite model"""
        prompt = f"""Analyze this legal document and classify its type. Return only the document type name.

Document text:
{text[:1000]}

Document type:"""

        if self.api_available:
            result = self._make_granite_call(prompt)
            if result and len(result) > 0:
                response_text = result[0].get("generated_text", "").strip()
                # Extract the document type from the response
                doc_type = self._extract_document_type(response_text)
                return {
                    "success": True,
                    "document_type": doc_type,
                    "confidence": 0.9,
                    "model_used": self.granite_model,
                    "details": "Classified using IBM Granite model"
                }
        
        # Fallback to local classification
        return self._local_document_classification(text)
    
    def _extract_document_type(self, response_text: str) -> str:
        """Extract document type from Granite response"""
        response_lower = response_text.lower()
        
        # Map common terms to document types
        type_mapping = {
            "nda": "Non-Disclosure Agreement (NDA)",
            "non-disclosure": "Non-Disclosure Agreement (NDA)",
            "confidential": "Non-Disclosure Agreement (NDA)",
            "employment": "Employment Contract",
            "employee": "Employment Contract",
            "hire": "Employment Contract",
            "lease": "Lease Agreement",
            "rent": "Lease Agreement",
            "tenant": "Lease Agreement",
            "service": "Service Agreement",
            "vendor": "Service Agreement",
            "purchase": "Purchase Agreement",
            "sale": "Purchase Agreement",
            "contract": "Legal Contract",
            "agreement": "Legal Contract"
        }
        
        for term, doc_type in type_mapping.items():
            if term in response_lower:
                return doc_type
        
        return "Legal Document"
    
    def _local_document_classification(self, text: str) -> Dict[str, Any]:
        """Local document classification using keyword matching"""
        text_lower = text.lower()
        
        # Define document types and their keywords
        doc_types = {
            "Non-Disclosure Agreement (NDA)": ["confidential", "non-disclosure", "nda", "trade secret", "proprietary"],
            "Employment Contract": ["employment", "employee", "salary", "benefits", "termination", "work"],
            "Lease Agreement": ["lease", "rent", "tenant", "landlord", "property", "premises"],
            "Service Agreement": ["service", "provider", "client", "scope of work", "deliverables"],
            "Purchase Agreement": ["purchase", "buy", "seller", "buyer", "payment", "delivery"]
        }
        
        scores = {}
        for doc_type, keywords in doc_types.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[doc_type] = score
        
        best_type = max(scores, key=scores.get) if scores else "Legal Document"
        confidence = min(0.95, max(0.6, scores[best_type] / 5))
        
        return {
            "success": True,
            "document_type": best_type,
            "confidence": confidence,
            "model_used": "Local Keyword Matching",
            "details": f"Classified using keyword analysis with {confidence:.2f} confidence"
        }
    
    def simplify_clause(self, clause: str) -> Dict[str, Any]:
        """Simplify complex legal clauses using IBM Granite model"""
        prompt = f"""Simplify this legal clause in plain English that a non-lawyer can understand. Keep it concise and clear.

Original clause:
{clause}

Simplified version:"""

        if self.api_available:
            result = self._make_granite_call(prompt)
            if result and len(result) > 0:
                simplified = result[0].get("generated_text", "").strip()
                return {
                    "success": True,
                    "original": clause,
                    "simplified": simplified,
                    "model_used": self.granite_model
                }
        
        # Fallback to local simplification
        return self._local_clause_simplification(clause)
    
    def _local_clause_simplification(self, clause: str) -> Dict[str, Any]:
        """Local clause simplification using rule-based approach"""
        simplified = clause
        
        # Replace complex legal terms with simpler equivalents
        replacements = {
            r'\bhereinafter\b': 'from now on',
            r'\bwhereas\b': 'since',
            r'\bhereby\b': 'by this',
            r'\bthereof\b': 'of this',
            r'\btherein\b': 'in this',
            r'\bthereto\b': 'to this',
            r'\baforesaid\b': 'mentioned above',
            r'\bsubject to\b': 'depending on',
            r'\bprovided that\b': 'but only if',
            r'\bin accordance with\b': 'following',
            r'\bnotwithstanding\b': 'despite',
            r'\bfor the avoidance of doubt\b': 'to be clear',
            r'\bwithout prejudice to\b': 'without affecting',
            r'\bsave and except\b': 'except for',
            r'\bnull and void\b': 'completely invalid'
        }
        
        for legal_term, simple_term in replacements.items():
            simplified = re.sub(legal_term, simple_term, simplified, flags=re.IGNORECASE)
        
        # Break down long sentences
        sentences = simplified.split('. ')
        simplified_sentences = []
        for sentence in sentences:
            if len(sentence) > 100:
                # Split long sentences at conjunctions
                parts = re.split(r'\s+(and|or|but)\s+', sentence)
                if len(parts) > 1:
                    simplified_sentences.extend(parts)
                else:
                    simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        simplified = '. '.join(simplified_sentences)
        
        return {
            "success": True,
            "original": clause,
            "simplified": simplified,
            "model_used": "Local Rule-based Simplification"
        }
    
    def extract_legal_entities(self, text: str) -> Dict[str, Any]:
        """Extract legal entities using IBM Granite model"""
        prompt = f"""Extract all legal entities, parties, dates, amounts, and important terms from this legal document. Return them in a structured format.

Document text:
{text[:2000]}

Extract and list:
1. Company names and parties
2. Dates and time periods
3. Monetary amounts
4. Legal terms and conditions
5. Key obligations and rights

Entities found:"""

        if self.api_available:
            result = self._make_granite_call(prompt)
            if result and len(result) > 0:
                response_text = result[0].get("generated_text", "").strip()
                entities = self._parse_entities_from_response(response_text)
                
                return {
                    "success": True,
                    "entities": entities,
                    "model_used": self.granite_model
                }
        
        # Local entity extraction
        return self._local_entity_extraction(text)
    
    def _parse_entities_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse entities from Granite model response"""
        entities = []
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and any(keyword in line.lower() for keyword in ['company', 'party', 'date', 'amount', 'term', 'obligation']):
                # Extract entity type and text
                if 'company' in line.lower() or 'party' in line.lower():
                    entity_type = "ORGANIZATION"
                elif 'date' in line.lower():
                    entity_type = "DATE"
                elif 'amount' in line.lower() or '$' in line:
                    entity_type = "MONEY"
                else:
                    entity_type = "LEGAL_TERM"
                
                entities.append({
                    "text": line,
                    "type": entity_type,
                    "confidence": 0.8
                })
        
        return entities
    
    def _local_entity_extraction(self, text: str) -> Dict[str, Any]:
        """Local entity extraction using regex patterns"""
        entities = []
        
        # Extract company names
        company_pattern = r'\b[A-Z][a-zA-Z\s&.,]+(?:Inc|Corp|LLC|Ltd|Company|Corporation)\b'
        companies = re.findall(company_pattern, text)
        for company in companies:
            entities.append({
                "text": company.strip(),
                "type": "ORGANIZATION",
                "confidence": 0.7
            })
        
        # Extract dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        dates = re.findall(date_pattern, text)
        for date in dates:
            entities.append({
                "text": date,
                "type": "DATE",
                "confidence": 0.8
            })
        
        # Extract monetary amounts
        money_pattern = r'\$\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars|USD)'
        amounts = re.findall(money_pattern, text)
        for amount in amounts:
            entities.append({
                "text": amount,
                "type": "MONEY",
                "confidence": 0.9
            })
        
        return {
            "success": True,
            "entities": entities,
            "model_used": "Local Regex Extraction"
        }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of legal document using IBM Granite model"""
        prompt = f"""Analyze the sentiment and tone of this legal document. Determine if it's neutral, positive, negative, or formal.

Document text:
{text[:1000]}

Analysis:"""

        if self.api_available:
            result = self._make_granite_call(prompt)
            if result and len(result) > 0:
                response_text = result[0].get("generated_text", "").strip()
                sentiment = self._extract_sentiment_from_response(response_text)
                
                return {
                    "success": True,
                    "sentiment": sentiment,
                    "model_used": self.granite_model
                }
        
        # Local sentiment analysis
        return self._local_sentiment_analysis(text)
    
    def _extract_sentiment_from_response(self, response_text: str) -> str:
        """Extract sentiment from Granite response"""
        response_lower = response_text.lower()
        
        if any(word in response_lower for word in ['positive', 'favorable', 'beneficial']):
            return "positive"
        elif any(word in response_lower for word in ['negative', 'unfavorable', 'restrictive']):
            return "negative"
        elif any(word in response_lower for word in ['formal', 'legal', 'professional']):
            return "formal"
        else:
            return "neutral"
    
    def _local_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """Local sentiment analysis using keyword matching"""
        text_lower = text.lower()
        
        # Count positive and negative legal terms
        positive_terms = ['benefit', 'right', 'entitle', 'protect', 'secure', 'guarantee']
        negative_terms = ['penalty', 'breach', 'violation', 'terminate', 'forfeit', 'damage']
        
        positive_count = sum(1 for term in positive_terms if term in text_lower)
        negative_count = sum(1 for term in negative_terms if term in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "success": True,
            "sentiment": sentiment,
            "model_used": "Local Keyword Analysis"
        }
    
    def extract_key_phrases(self, text: str) -> Dict[str, Any]:
        """Extract key phrases using IBM Granite model"""
        prompt = f"""Extract the most important key phrases and terms from this legal document. Focus on obligations, rights, conditions, and critical terms.

Document text:
{text[:1500]}

Key phrases:"""

        if self.api_available:
            result = self._make_granite_call(prompt)
            if result and len(result) > 0:
                response_text = result[0].get("generated_text", "").strip()
                phrases = self._parse_phrases_from_response(response_text)
                
                return {
                    "success": True,
                    "phrases": phrases,
                    "model_used": self.granite_model
                }
        
        # Local key phrase extraction
        return self._local_key_phrase_extraction(text)
    
    def _parse_phrases_from_response(self, response_text: str) -> List[str]:
        """Parse key phrases from Granite model response"""
        phrases = []
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:  # Filter out very short lines
                phrases.append(line)
        
        return phrases[:10]  # Limit to top 10 phrases
    
    def _local_key_phrase_extraction(self, text: str) -> Dict[str, Any]:
        """Local key phrase extraction using frequency analysis"""
        # Extract sentences containing important legal terms
        important_terms = ['shall', 'must', 'agree', 'obligated', 'liable', 'terminate', 'breach', 'damages']
        
        sentences = text.split('.')
        key_phrases = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(term in sentence.lower() for term in important_terms):
                key_phrases.append(sentence)
        
        return {
            "success": True,
            "phrases": key_phrases[:10],
            "model_used": "Local Frequency Analysis"
        }
    
    def generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate document summary using IBM Granite model"""
        prompt = f"""Create a comprehensive summary of this legal document. Include the main purpose, key parties, important terms, and critical obligations. Make it easy for a non-lawyer to understand.

Document text:
{text[:2000]}

Summary:"""

        if self.api_available:
            result = self._make_granite_call(prompt)
            if result and len(result) > 0:
                summary = result[0].get("generated_text", "").strip()
                return {
                    "success": True,
                    "summary": summary,
                    "model_used": self.granite_model
                }
        
        # Local summarization
        return self._local_summarization(text)
    
    def _local_summarization(self, text: str) -> Dict[str, Any]:
        """Local document summarization using extractive approach"""
        # Split into sentences
        sentences = text.split('.')
        
        # Score sentences based on legal importance
        sentence_scores = []
        for sentence in sentences:
            score = 0
            sentence_lower = sentence.lower()
            
            # Score based on legal terms
            legal_terms = ['shall', 'must', 'agree', 'obligated', 'liable', 'terminate', 'breach', 'damages', 'confidential', 'non-disclosure']
            score += sum(2 for term in legal_terms if term in sentence_lower)
            
            # Score based on length (prefer medium-length sentences)
            if 20 < len(sentence) < 100:
                score += 1
            
            sentence_scores.append((sentence, score))
        
        # Get top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [sentence for sentence, score in sentence_scores[:5]]
        
        summary = '. '.join(top_sentences) + '.'
        
        return {
            "success": True,
            "summary": summary,
            "model_used": "Local Extractive Summarization"
        } 