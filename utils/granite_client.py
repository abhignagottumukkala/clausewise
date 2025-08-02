"""
IBM Granite client for ClauseWise
Handles advanced text processing and classification using IBM Granite models
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional
import streamlit as st


class GraniteClient:
    """IBM Granite client for advanced document analysis"""
    
    def __init__(self):
        self.api_key = os.getenv('IBM_API_KEY')
        self.granite_url = os.getenv('GRANITE_URL', 'https://api.ibm.com/granite/v1')
        
        if not self.api_key:
            st.warning("IBM API key not found. Using enhanced local processing instead.")
            self.api_available = False
        else:
            self.api_available = True
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def classify_document_advanced(self, text: str) -> Dict[str, Any]:
        """Advanced document classification using Granite"""
        try:
            if self.api_available:
                # Real Granite API call
                payload = {
                    "text": text[:2000],  # Limit text for API
                    "task": "document_classification",
                    "model": "granite-13b-chat-v2"
                }
                
                response = requests.post(
                    f"{self.granite_url}/classify",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "classification": result.get("classification", "Unknown"),
                        "confidence": result.get("confidence", 0.0),
                        "model_used": "granite-13b-chat-v2"
                    }
                else:
                    st.warning(f"Granite API error: {response.status_code}. Using enhanced local classification.")
                    return self._enhanced_local_classification(text)
            else:
                return self._enhanced_local_classification(text)
            
        except Exception as e:
            st.warning(f"Granite API unavailable: {str(e)}. Using enhanced local classification.")
            return self._enhanced_local_classification(text)
    
    def _enhanced_local_classification(self, text: str) -> Dict[str, Any]:
        """Enhanced local document classification"""
        text_lower = text.lower()
        
        # Enhanced keyword-based classification with confidence scoring
        doc_patterns = {
            "NDA": {
                "keywords": ["confidential", "non-disclosure", "proprietary", "trade secret", "nda"],
                "weight": 1.0
            },
            "Employment Contract": {
                "keywords": ["employment", "employee", "hire", "termination", "salary", "compensation", "work"],
                "weight": 1.0
            },
            "Lease Agreement": {
                "keywords": ["lease", "rent", "tenant", "landlord", "property", "premises", "rental"],
                "weight": 1.0
            },
            "Service Agreement": {
                "keywords": ["service", "vendor", "provider", "deliverable", "scope", "consulting"],
                "weight": 1.0
            },
            "Purchase Agreement": {
                "keywords": ["purchase", "buy", "sale", "payment", "delivery", "goods", "product"],
                "weight": 1.0
            },
            "Partnership Agreement": {
                "keywords": ["partnership", "partner", "joint venture", "collaboration", "cooperation"],
                "weight": 1.0
            }
        }
        
        scores = {}
        for doc_type, pattern in doc_patterns.items():
            score = 0
            for keyword in pattern["keywords"]:
                if keyword in text_lower:
                    score += pattern["weight"]
            scores[doc_type] = score
        
        if scores:
            best_match = max(scores.items(), key=lambda x: x[1])
            confidence = min(best_match[1] / 3.0, 1.0)  # Normalize confidence
            return {
                "success": True,
                "classification": best_match[0],
                "confidence": confidence,
                "model_used": "enhanced-local-classification"
            }
        else:
            return {
                "success": True,
                "classification": "General Contract",
                "confidence": 0.3,
                "model_used": "enhanced-local-classification"
            }
    
    def generate_simplified_text(self, complex_text: str) -> Dict[str, Any]:
        """Generate simplified text using Granite or enhanced local processing"""
        try:
            if self.api_available:
                # Real Granite API call for text simplification
                payload = {
                    "text": complex_text[:3000],  # Limit text for API
                    "task": "text_simplification",
                    "model": "granite-13b-chat-v2",
                    "parameters": {
                        "style": "legal_to_plain",
                        "preserve_meaning": True
                    }
                }
                
                response = requests.post(
                    f"{self.granite_url}/simplify",
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "original": complex_text,
                        "simplified": result.get("simplified_text", complex_text),
                        "model_used": "granite-13b-chat-v2"
                    }
                else:
                    st.warning(f"Granite API error: {response.status_code}. Using enhanced local simplification.")
                    return self._enhanced_local_simplification(complex_text)
            else:
                return self._enhanced_local_simplification(complex_text)
            
        except Exception as e:
            st.warning(f"Granite API unavailable: {str(e)}. Using enhanced local simplification.")
            return self._enhanced_local_simplification(complex_text)
    
    def _enhanced_local_simplification(self, text: str) -> Dict[str, Any]:
        """Enhanced local text simplification"""
        # Advanced legal term replacement
        legal_replacements = {
            "hereinafter": "from now on",
            "whereas": "since",
            "aforesaid": "mentioned above",
            "pursuant to": "according to",
            "notwithstanding": "despite",
            "in witness whereof": "to confirm this",
            "party of the first part": "first party",
            "party of the second part": "second party",
            "hereby": "by this",
            "herein": "in this document",
            "hereto": "to this",
            "hereof": "of this",
            "thereof": "of that",
            "therein": "in that",
            "thereto": "to that",
            "subject to": "depending on",
            "in accordance with": "following",
            "for the avoidance of doubt": "to be clear",
            "save and except": "except",
            "mutatis mutandis": "with necessary changes",
            "inter alia": "among other things",
            "prima facie": "at first glance",
            "de facto": "in fact",
            "de jure": "by law",
            "ex parte": "from one side",
            "in camera": "in private",
            "sub judice": "under consideration",
            "ultra vires": "beyond authority",
            "bona fide": "in good faith",
            "mala fide": "in bad faith",
            "force majeure": "unforeseen circumstances",
            "ipso facto": "by that very fact",
            "per se": "by itself",
            "ad hoc": "for this specific purpose",
            "pro rata": "proportionally",
            "quid pro quo": "something for something",
            "status quo": "current situation",
            "vice versa": "the other way around",
            "et al": "and others",
            "i.e.": "that is",
            "e.g.": "for example",
            "viz.": "namely",
            "cf.": "compare",
            "ibid": "same source",
            "op. cit.": "work cited",
            "loc. cit.": "place cited",
            "supra": "above",
            "infra": "below",
            "ante": "before",
            "post": "after"
        }
        
        simplified = text
        
        # Replace complex legal terms
        for legal_term, simple_term in legal_replacements.items():
            simplified = simplified.replace(legal_term, simple_term)
            simplified = simplified.replace(legal_term.title(), simple_term.title())
        
        # Break down long sentences
        sentences = simplified.split('.')
        simplified_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 100:  # Long sentence
                # Split on common legal connectors
                connectors = [' and ', ' or ', ' but ', ' however ', ' furthermore ', ' moreover ', ' additionally ']
                for connector in connectors:
                    if connector in sentence:
                        parts = sentence.split(connector)
                        simplified_sentences.extend(parts)
                        break
                else:
                    simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        simplified = '. '.join(simplified_sentences)
        
        # Add explanations for complex terms
        complex_terms = [
            "liability", "indemnification", "breach", "termination", 
            "jurisdiction", "arbitration", "governing law", "force majeure"
        ]
        
        explanations = []
        for term in complex_terms:
            if term in simplified.lower():
                if term == "liability":
                    explanations.append(f"'{term}' means legal responsibility for damages")
                elif term == "indemnification":
                    explanations.append(f"'{term}' means protection against legal claims")
                elif term == "breach":
                    explanations.append(f"'{term}' means violation of the agreement")
                elif term == "termination":
                    explanations.append(f"'{term}' means ending the agreement")
                elif term == "jurisdiction":
                    explanations.append(f"'{term}' means which court system applies")
                elif term == "arbitration":
                    explanations.append(f"'{term}' means dispute resolution outside of court")
                elif term == "governing law":
                    explanations.append(f"'{term}' means which state's laws apply")
                elif term == "force majeure":
                    explanations.append(f"'{term}' means unforeseeable circumstances that prevent performance")
        
        if explanations:
            simplified += f"\n\nKey terms explained: {'; '.join(explanations)}"
        
        # Add a summary section
        simplified += "\n\nSUMMARY:\n"
        simplified += "This document has been simplified to make it easier to understand. "
        simplified += "The key points are:\n"
        
        # Extract key points
        key_points = []
        if "shall" in simplified.lower() or "must" in simplified.lower():
            key_points.append("- Contains obligations that must be followed")
        if "liability" in simplified.lower():
            key_points.append("- Discusses legal responsibility")
        if "termination" in simplified.lower():
            key_points.append("- Explains how the agreement can end")
        if "payment" in simplified.lower() or "compensation" in simplified.lower():
            key_points.append("- Contains payment terms")
        
        if key_points:
            simplified += '\n'.join(key_points)
        else:
            simplified += "- Review all terms carefully before signing"
        
        return {
            "success": True,
            "original": text,
            "simplified": simplified,
            "model_used": "enhanced-local-simplification"
        }
    
    def extract_advanced_entities(self, text: str) -> Dict[str, Any]:
        """Extract advanced entities using Granite or enhanced local processing"""
        try:
            if self.api_available:
                # Real Granite API call for entity extraction
                payload = {
                    "text": text[:2000],
                    "task": "entity_extraction",
                    "model": "granite-13b-chat-v2",
                    "entity_types": ["PERSON", "ORGANIZATION", "DATE", "MONEY", "LOCATION", "LEGAL_TERM"]
                }
                
                response = requests.post(
                    f"{self.granite_url}/extract_entities",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "entities": result.get("entities", {}),
                        "model_used": "granite-13b-chat-v2"
                    }
                else:
                    st.warning(f"Granite API error: {response.status_code}. Using enhanced local extraction.")
                    return self._enhanced_local_entity_extraction(text)
            else:
                return self._enhanced_local_entity_extraction(text)
            
        except Exception as e:
            st.warning(f"Granite API unavailable: {str(e)}. Using enhanced local extraction.")
            return self._enhanced_local_entity_extraction(text)
    
    def _enhanced_local_entity_extraction(self, text: str) -> Dict[str, Any]:
        """Enhanced local entity extraction"""
        entities = {
            "parties": [],
            "dates": [],
            "amounts": [],
            "locations": [],
            "legal_terms": [],
            "obligations": [],
            "penalties": [],
            "conditions": []
        }
        
        # Enhanced regex-based extraction
        import re
        
        # Extract monetary amounts
        amount_pattern = r'\$[\d,]+(?:\.\d{2})?|\d+\s*(?:dollars?|USD|euros?|pounds?)'
        amounts = re.findall(amount_pattern, text)
        entities["amounts"] = [{"text": amount, "type": "MonetaryAmount"} for amount in amounts]
        
        # Extract dates
        date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        dates = re.findall(date_pattern, text)
        entities["dates"] = [{"text": date, "type": "Date"} for date in dates]
        
        # Extract legal terms
        legal_terms = [
            "confidentiality", "non-disclosure", "proprietary", "trade secret",
            "liability", "indemnification", "breach", "termination",
            "jurisdiction", "arbitration", "governing law", "force majeure",
            "intellectual property", "copyright", "trademark", "patent",
            "warranty", "representation", "covenant", "condition"
        ]
        
        for term in legal_terms:
            if term in text.lower():
                entities["legal_terms"].append({"text": term, "type": "LegalTerm"})
        
        # Extract obligations
        obligation_indicators = ["shall", "must", "will", "agree to", "obligated to", "required to"]
        for indicator in obligation_indicators:
            if indicator in text.lower():
                entities["obligations"].append({"text": indicator, "type": "Obligation"})
        
        # Extract parties (organizations and people)
        org_pattern = r'\b[A-Z][a-zA-Z\s&.,]+(?:Corporation|Corp|Inc|LLC|Ltd|Company|Co|Partners|Associates)\b'
        organizations = re.findall(org_pattern, text)
        entities["parties"].extend([{"text": org, "type": "Organization"} for org in organizations])
        
        return {
            "success": True,
            "entities": entities,
            "model_used": "enhanced-local-extraction"
        }
    
    def analyze_clause_structure(self, text: str) -> Dict[str, Any]:
        """Analyze the structure of legal clauses"""
        try:
            if self.api_available:
                # Real Granite API call for clause analysis
                payload = {
                    "text": text[:2000],
                    "task": "clause_analysis",
                    "model": "granite-13b-chat-v2"
                }
                
                response = requests.post(
                    f"{self.granite_url}/analyze_clause",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "structure": result.get("structure", {}),
                        "model_used": "granite-13b-chat-v2"
                    }
                else:
                    st.warning(f"Granite API error: {response.status_code}. Using enhanced local analysis.")
                    return self._enhanced_local_clause_analysis(text)
            else:
                return self._enhanced_local_clause_analysis(text)
            
        except Exception as e:
            st.warning(f"Granite API unavailable: {str(e)}. Using enhanced local analysis.")
            return self._enhanced_local_clause_analysis(text)
    
    def _enhanced_local_clause_analysis(self, text: str) -> Dict[str, Any]:
        """Enhanced local clause structure analysis"""
        structure = {
            "clause_type": "Unknown",
            "key_elements": [],
            "conditions": [],
            "exceptions": [],
            "timeframes": [],
            "parties_involved": []
        }
        
        text_lower = text.lower()
        
        # Determine clause type
        if "confidential" in text_lower or "non-disclosure" in text_lower:
            structure["clause_type"] = "Confidentiality"
        elif "payment" in text_lower or "compensation" in text_lower:
            structure["clause_type"] = "Payment"
        elif "termination" in text_lower:
            structure["clause_type"] = "Termination"
        elif "liability" in text_lower or "indemnification" in text_lower:
            structure["clause_type"] = "Liability"
        elif "governing law" in text_lower or "jurisdiction" in text_lower:
            structure["clause_type"] = "Governing Law"
        elif "force majeure" in text_lower:
            structure["clause_type"] = "Force Majeure"
        elif "intellectual property" in text_lower:
            structure["clause_type"] = "Intellectual Property"
        
        # Extract key elements
        key_phrases = [
            "subject to", "provided that", "except as", "unless otherwise",
            "in the event", "upon", "within", "prior to", "subsequent to",
            "notwithstanding", "pursuant to", "in accordance with"
        ]
        
        for phrase in key_phrases:
            if phrase in text_lower:
                structure["key_elements"].append(phrase)
        
        # Extract conditions
        condition_indicators = ["if", "when", "provided", "subject to", "conditional upon"]
        for indicator in condition_indicators:
            if indicator in text_lower:
                structure["conditions"].append(indicator)
        
        # Extract exceptions
        exception_indicators = ["except", "excluding", "notwithstanding", "save for"]
        for indicator in exception_indicators:
            if indicator in text_lower:
                structure["exceptions"].append(indicator)
        
        return {
            "success": True,
            "structure": structure,
            "model_used": "enhanced-local-analysis"
        } 