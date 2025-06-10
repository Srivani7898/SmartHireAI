import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import Dict, List, Tuple
import spacy

class JobMatcher:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the job matcher with S-BERT model.
        
        Args:
            model_name (str): Name of the sentence transformer model
        """
        try:
            self.model = SentenceTransformer(model_name)
            print(f"✅ Loaded S-BERT model: {model_name}")
        except Exception as e:
            print(f"❌ Error loading S-BERT model: {str(e)}")
            raise
        
        # Load spaCy model for text processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.nlp = None
            print("Warning: spaCy model not found. Some features may be limited.")
        
        # Define important keywords for different categories
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'django', 'flask', 'spring', 'mysql', 'postgresql', 'mongodb',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'machine learning',
            'data science', 'artificial intelligence', 'deep learning'
        ]
        
        self.experience_keywords = [
            'experience', 'years', 'worked', 'developed', 'managed', 'led',
            'created', 'designed', 'implemented', 'built', 'maintained'
        ]
        
        self.education_keywords = [
            'degree', 'bachelor', 'master', 'phd', 'university', 'college',
            'engineering', 'computer science', 'information technology'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better matching.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\+\#\-]', ' ', text)
        
        # Normalize common variations
        replacements = {
            'c++': 'cpp',
            'c#': 'csharp',
            '.net': 'dotnet',
            'node.js': 'nodejs',
            'react.js': 'react',
            'vue.js': 'vue'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text.strip()
    
    def extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract key phrases from text using spaCy.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of key phrases
        """
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        key_phrases = []
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Keep short phrases
                key_phrases.append(chunk.text.lower())
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'SKILL']:
                key_phrases.append(ent.text.lower())
        
        return list(set(key_phrases))
    
    def calculate_similarity(self, job_description: str, resume_text: str) -> float:
        """
        Calculate semantic similarity between job description and resume.
        
        Args:
            job_description (str): Job description text
            resume_text (str): Resume text
            
        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            # Preprocess texts
            job_desc_clean = self.preprocess_text(job_description)
            resume_clean = self.preprocess_text(resume_text)
            
            # Generate embeddings using S-BERT
            job_embedding = self.model.encode([job_desc_clean])
            resume_embedding = self.model.encode([resume_clean])
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(job_embedding, resume_embedding)
            similarity_score = similarity_matrix[0][0]
            
            # Ensure score is between 0 and 1
            similarity_score = max(0.0, min(1.0, similarity_score))
            
            return float(similarity_score)
            
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def calculate_weighted_similarity(self, job_description: str, resume_text: str) -> Dict[str, float]:
        """
        Calculate weighted similarity considering different aspects.
        
        Args:
            job_description (str): Job description text
            resume_text (str): Resume text
            
        Returns:
            Dict[str, float]: Dictionary with different similarity scores
        """
        try:
            # Overall semantic similarity
            overall_similarity = self.calculate_similarity(job_description, resume_text)
            
            # Skills-based similarity
            skills_similarity = self._calculate_skills_similarity(job_description, resume_text)
            
            # Experience-based similarity
            experience_similarity = self._calculate_experience_similarity(job_description, resume_text)
            
            # Education-based similarity
            education_similarity = self._calculate_education_similarity(job_description, resume_text)
            
            # Calculate weighted average
            weights = {
                'overall': 0.4,
                'skills': 0.3,
                'experience': 0.2,
                'education': 0.1
            }
            
            weighted_score = (
                overall_similarity * weights['overall'] +
                skills_similarity * weights['skills'] +
                experience_similarity * weights['experience'] +
                education_similarity * weights['education']
            )
            
            return {
                'overall_similarity': overall_similarity,
                'skills_similarity': skills_similarity,
                'experience_similarity': experience_similarity,
                'education_similarity': education_similarity,
                'weighted_score': weighted_score
            }
            
        except Exception as e:
            print(f"Error calculating weighted similarity: {str(e)}")
            return {
                'overall_similarity': 0.0,
                'skills_similarity': 0.0,
                'experience_similarity': 0.0,
                'education_similarity': 0.0,
                'weighted_score': 0.0
            }
    
    def _calculate_skills_similarity(self, job_description: str, resume_text: str) -> float:
        """Calculate similarity based on skills mentioned."""
        job_skills = self._extract_skills_from_text(job_description.lower())
        resume_skills = self._extract_skills_from_text(resume_text.lower())
        
        if not job_skills:
            return 0.0
        
        # Calculate Jaccard similarity for skills
        intersection = len(job_skills.intersection(resume_skills))
        union = len(job_skills.union(resume_skills))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _calculate_experience_similarity(self, job_description: str, resume_text: str) -> float:
        """Calculate similarity based on experience keywords."""
        job_exp_keywords = self._extract_keywords(job_description.lower(), self.experience_keywords)
        resume_exp_keywords = self._extract_keywords(resume_text.lower(), self.experience_keywords)
        
        if not job_exp_keywords:
            return 0.0
        
        intersection = len(job_exp_keywords.intersection(resume_exp_keywords))
        return intersection / len(job_exp_keywords)
    
    def _calculate_education_similarity(self, job_description: str, resume_text: str) -> float:
        """Calculate similarity based on education keywords."""
        job_edu_keywords = self._extract_keywords(job_description.lower(), self.education_keywords)
        resume_edu_keywords = self._extract_keywords(resume_text.lower(), self.education_keywords)
        
        if not job_edu_keywords:
            return 0.5  # Neutral score if no education requirements
        
        intersection = len(job_edu_keywords.intersection(resume_edu_keywords))
        return intersection / len(job_edu_keywords)
    
    def _extract_skills_from_text(self, text: str) -> set:
        """Extract technical skills from text."""
        skills = set()
        
        for skill in self.skill_keywords:
            if skill in text:
                skills.add(skill)
        
        # Additional skill patterns
        skill_patterns = [
            r'\b(?:python|java|javascript|c\+\+|c#|php|ruby|go|rust|swift|kotlin)\b',
            r'\b(?:react|angular|vue|node\.?js|django|flask|spring|laravel)\b',
            r'\b(?:mysql|postgresql|mongodb|redis|elasticsearch|oracle)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|jenkins|git|github)\b'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update([match.lower() for match in matches])
        
        return skills
    
    def _extract_keywords(self, text: str, keywords: List[str]) -> set:
        """Extract specific keywords from text."""
        found_keywords = set()
        
        for keyword in keywords:
            if keyword in text:
                found_keywords.add(keyword)
        
        return found_keywords
    
    def analyze_job_description(self, job_description: str) -> Dict[str, any]:
        """
        Analyze job description to extract key information.
        
        Args:
            job_description (str): Job description text
            
        Returns:
            Dict[str, any]: Analysis results
        """
        analysis = {
            'word_count': len(job_description.split()),
            'character_count': len(job_description),
            'skills': list(self._extract_skills_from_text(job_description.lower())),
            'experience': list(self._extract_keywords(job_description.lower(), self.experience_keywords)),
            'education': list(self._extract_keywords(job_description.lower(), self.education_keywords))
        }
        
        # Extract required years of experience
        exp_pattern = r'(\d+)\s*(?:\+)?\s*years?\s+(?:of\s+)?experience'
        exp_matches = re.findall(exp_pattern, job_description, re.IGNORECASE)
        if exp_matches:
            analysis['required_experience_years'] = int(exp_matches[0])
        else:
            analysis['required_experience_years'] = None
        
        # Extract key phrases
        analysis['key_phrases'] = self.extract_key_phrases(job_description)
        
        return analysis
    
    def rank_resumes(self, job_description: str, resumes: List[Dict]) -> List[Dict]:
        """
        Rank multiple resumes against a job description.
        
        Args:
            job_description (str): Job description text
            resumes (List[Dict]): List of resume dictionaries with 'text' and 'filename'
            
        Returns:
            List[Dict]: Ranked list of resumes with similarity scores
        """
        ranked_resumes = []
        
        for resume in resumes:
            similarity_score = self.calculate_similarity(job_description, resume['text'])
            weighted_scores = self.calculate_weighted_similarity(job_description, resume['text'])
            
            ranked_resumes.append({
                'filename': resume['filename'],
                'similarity_score': similarity_score,
                'weighted_scores': weighted_scores,
                'text': resume['text']
            })
        
        # Sort by similarity score in descending order
        ranked_resumes.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return ranked_resumes
    
    def get_matching_explanation(self, job_description: str, resume_text: str) -> Dict[str, any]:
        """
        Provide explanation for the matching score.
        
        Args:
            job_description (str): Job description text
            resume_text (str): Resume text
            
        Returns:
            Dict[str, any]: Explanation of the matching
        """
        job_analysis = self.analyze_job_description(job_description)
        
        job_skills = self._extract_skills_from_text(job_description.lower())
        resume_skills = self._extract_skills_from_text(resume_text.lower())
        
        matching_skills = job_skills.intersection(resume_skills)
        missing_skills = job_skills - resume_skills
        
        similarity_scores = self.calculate_weighted_similarity(job_description, resume_text)
        
        return {
            'overall_score': similarity_scores['weighted_score'],
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'skill_match_percentage': len(matching_skills) / len(job_skills) if job_skills else 0,
            'detailed_scores': similarity_scores,
            'recommendations': self._generate_recommendations(missing_skills, similarity_scores)
        }
    
    def _generate_recommendations(self, missing_skills: set, scores: Dict[str, float]) -> List[str]:
        """Generate recommendations for improving the match."""
        recommendations = []
        
        if missing_skills:
            recommendations.append(f"Consider highlighting these skills: {', '.join(list(missing_skills)[:5])}")
        
        if scores['experience_similarity'] < 0.5:
            recommendations.append("Emphasize relevant work experience and achievements")
        
        if scores['education_similarity'] < 0.5:
            recommendations.append("Highlight relevant educational background and certifications")
        
        if scores['overall_similarity'] < 0.6:
            recommendations.append("Consider tailoring the resume to better match the job requirements")
        
        return recommendations
