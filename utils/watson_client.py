"""
IBM Watson client for ClauseWise
Handles Natural Language Understanding, Discovery, and other Watson services
"""

import os
import json
from typing import Dict, Any, List, Optional
import streamlit as st
from ibm_watson import NaturalLanguageUnderstandingV1, DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions


class WatsonClient:
    """IBM Watson client for document analysis"""
    
    def __init__(self):
        self.api_key = os.getenv('IBM_API_KEY')
        self.url = os.getenv('IBM_URL')
        
        if not self.api_key or not self.url:
            st.error("IBM Watson credentials not found. Please set IBM_API_KEY and IBM_URL in your .env file.")
            return
        
        try:
            # Initialize Watson services
            authenticator = IAMAuthenticator(self.api_key)
            
            # Natural Language Understanding
            self.nlu = NaturalLanguageUnderstandingV1(
                version='2022-04-07',
                authenticator=authenticator
            )
            self.nlu.set_service_url(self.url)
            
            # Discovery (if available)
            try:
                self.discovery = DiscoveryV1(
                    version='2019-04-30',
                    authenticator=authenticator
                )
                self.discovery.set_service_url(self.url)
            except Exception as e:
                st.warning(f"Discovery service not available: {str(e)}")
                self.discovery = None
                
        except Exception as e:
            st.error(f"Error initializing Watson services: {str(e)}")
    
    def analyze_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities from legal text"""
        try:
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    entities=EntitiesOptions(emotion=True, sentiment=True, limit=50),
                    keywords=KeywordsOptions(emotion=True, sentiment=True, limit=50),
                    sentiment=SentimentOptions()
                )
            ).get_result()
            
            return {
                "success": True,
                "entities": response.get('entities', []),
                "keywords": response.get('keywords', []),
                "sentiment": response.get('sentiment', {}),
                "usage": response.get('usage', {})
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "entities": [],
                "keywords": [],
                "sentiment": {},
                "usage": {}
            }
    
    def classify_document_type(self, text: str) -> Dict[str, Any]:
        """Classify document type using Watson NLU"""
        try:
            # Use keywords and entities to classify document type
            response = self.nlu.analyze(
                text=text[:1000],  # Use first 1000 characters for classification
                features=Features(
                    keywords=KeywordsOptions(limit=20),
                    entities=EntitiesOptions(limit=20)
                )
            ).get_result()
            
            # Define document type patterns
            doc_patterns = {
                "NDA": ["confidential", "non-disclosure", "proprietary", "trade secret"],
                "Employment Contract": ["employment", "employee", "hire", "termination", "salary"],
                "Lease Agreement": ["lease", "rent", "tenant", "landlord", "property", "premises"],
                "Service Agreement": ["service", "vendor", "provider", "deliverable", "scope"],
                "Purchase Agreement": ["purchase", "buy", "sale", "payment", "delivery"],
                "Partnership Agreement": ["partnership", "partner", "joint venture", "collaboration"]
            }
            
            keywords = [kw['text'].lower() for kw in response.get('keywords', [])]
            entities = [ent['text'].lower() for ent in response.get('entities', [])]
            
            all_text = ' '.join(keywords + entities)
            
            # Score each document type
            scores = {}
            for doc_type, patterns in doc_patterns.items():
                score = sum(1 for pattern in patterns if pattern in all_text)
                scores[doc_type] = score
            
            # Get the document type with highest score
            if scores:
                best_match = max(scores.items(), key=lambda x: x[1])
                confidence = min(best_match[1] / len(doc_patterns[best_match[0]]), 1.0)
            else:
                best_match = ("Unknown", 0)
                confidence = 0.0
            
            return {
                "success": True,
                "document_type": best_match[0],
                "confidence": confidence,
                "scores": scores,
                "keywords": keywords,
                "entities": entities
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "document_type": "Unknown",
                "confidence": 0.0,
                "scores": {},
                "keywords": [],
                "entities": []
            }
    
    def simplify_clause(self, clause_text: str) -> Dict[str, Any]:
        """Simplify complex legal clause using Watson NLU"""
        try:
            # Analyze the clause for entities and keywords
            response = self.nlu.analyze(
                text=clause_text,
                features=Features(
                    entities=EntitiesOptions(emotion=True, sentiment=True, limit=20),
                    keywords=KeywordsOptions(emotion=True, sentiment=True, limit=20),
                    sentiment=SentimentOptions()
                )
            ).get_result()
            
            # Extract key information
            entities = response.get('entities', [])
            keywords = response.get('keywords', [])
            
            # Create simplified version
            simplified = self._create_simplified_text(clause_text, entities, keywords)
            
            return {
                "success": True,
                "original": clause_text,
                "simplified": simplified,
                "entities": entities,
                "keywords": keywords,
                "sentiment": response.get('sentiment', {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": clause_text,
                "simplified": "",
                "entities": [],
                "keywords": [],
                "sentiment": {}
            }
    
    def _create_simplified_text(self, original_text: str, entities: List[Dict], keywords: List[Dict]) -> str:
        """Create simplified version of legal text"""
        # This is a basic simplification - in production, you'd use more sophisticated NLP
        simplified = original_text
        
        # Replace complex legal terms with simpler equivalents
        legal_terms = {
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
            "thereto": "to that"
        }
        
        for legal_term, simple_term in legal_terms.items():
            simplified = simplified.replace(legal_term, simple_term)
            simplified = simplified.replace(legal_term.title(), simple_term.title())
        
        # Add entity explanations
        entity_explanations = []
        for entity in entities:
            if entity.get('type') in ['Person', 'Organization', 'Location', 'Date']:
                entity_explanations.append(f"{entity['text']} ({entity['type']})")
        
        if entity_explanations:
            simplified += f"\n\nKey entities: {', '.join(entity_explanations)}"
        
        return simplified
    
    def extract_legal_entities(self, text: str) -> Dict[str, Any]:
        """Extract legal-specific entities"""
        try:
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    entities=EntitiesOptions(emotion=True, sentiment=True, limit=100),
                    keywords=KeywordsOptions(emotion=True, sentiment=True, limit=100)
                )
            ).get_result()
            
            # Categorize entities by legal relevance
            legal_entities = {
                "parties": [],
                "dates": [],
                "amounts": [],
                "locations": [],
                "legal_terms": [],
                "other": []
            }
            
            for entity in response.get('entities', []):
                entity_text = entity['text']
                entity_type = entity.get('type', '')
                
                if entity_type == 'Person' or entity_type == 'Organization':
                    legal_entities['parties'].append(entity)
                elif entity_type == 'Date':
                    legal_entities['dates'].append(entity)
                elif entity_type == 'Location':
                    legal_entities['locations'].append(entity)
                elif any(term in entity_text.lower() for term in ['contract', 'agreement', 'clause', 'section']):
                    legal_entities['legal_terms'].append(entity)
                elif any(char.isdigit() for char in entity_text):
                    legal_entities['amounts'].append(entity)
                else:
                    legal_entities['other'].append(entity)
            
            return {
                "success": True,
                "legal_entities": legal_entities,
                "all_entities": response.get('entities', []),
                "keywords": response.get('keywords', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "legal_entities": {},
                "all_entities": [],
                "keywords": []
            } 