import google.generativeai as genai
import os
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class GeminiJobGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    async def generate_job_listing(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete job listing from minimal inputs using Gemini AI
        
        Args:
            prompt_data: Dict containing job_title, company, location, job_type
        
        Returns:
            Dict with complete job details
        """
        try:
            job_title = prompt_data.get('job_title', '')
            company = prompt_data.get('company', '')
            location = prompt_data.get('location', '')
            job_type = prompt_data.get('job_type', 'full-time')
            category = prompt_data.get('category', 'technology')
            experience_level = prompt_data.get('experience_level', 'mid')
            
            prompt = f"""
            Generate a detailed job listing in JSON format for the following position:
            
            Job Title: {job_title}
            Company: {company}
            Location: {location}
            Job Type: {job_type}
            Category: {category}
            Experience Level: {experience_level}
            
            Please provide a realistic and detailed job listing with:
            1. A comprehensive job description (3-4 paragraphs)
            2. 5-8 key responsibilities
            3. 5-7 required skills
            4. 3-5 qualifications
            5. 3-5 benefits
            6. Realistic salary range for this position
            
            Return ONLY a valid JSON object with this exact structure:
            {{
                "description": "detailed job description",
                "responsibilities": ["responsibility 1", "responsibility 2", ...],
                "skills_required": ["skill 1", "skill 2", ...],
                "qualifications": ["qualification 1", "qualification 2", ...],
                "benefits": ["benefit 1", "benefit 2", ...],
                "salary_min": 50000,
                "salary_max": 80000
            }}
            
            Important: Return ONLY the JSON object, no additional text or markdown formatting.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse the JSON response
            generated_data = json.loads(response_text)
            
            # Combine with original data
            result = {
                "title": job_title,
                "company": company,
                "location": location,
                "job_type": job_type,
                "category": category,
                "experience_level": experience_level,
                "description": generated_data.get('description', ''),
                "responsibilities": generated_data.get('responsibilities', []),
                "skills_required": generated_data.get('skills_required', []),
                "qualifications": generated_data.get('qualifications', []),
                "benefits": generated_data.get('benefits', []),
                "salary_min": generated_data.get('salary_min'),
                "salary_max": generated_data.get('salary_max'),
                "currency": "USD",
                "is_active": True
            }
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.error(f"Response text: {response_text}")
            raise Exception(f"Failed to parse AI response: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating job listing with Gemini: {e}")
            raise Exception(f"AI generation failed: {str(e)}")
    
    async def generate_internship_listing(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete internship listing from minimal inputs
        """
        try:
            title = prompt_data.get('title', '')
            company = prompt_data.get('company', '')
            location = prompt_data.get('location', '')
            duration = prompt_data.get('duration', '3 months')
            category = prompt_data.get('category', 'technology')
            
            prompt = f"""
            Generate a detailed internship listing in JSON format:
            
            Title: {title}
            Company: {company}
            Location: {location}
            Duration: {duration}
            Category: {category}
            
            Return ONLY a valid JSON object:
            {{
                "description": "detailed description",
                "responsibilities": ["responsibility 1", ...],
                "skills_required": ["skill 1", ...],
                "qualifications": ["qualification 1", ...],
                "learning_outcomes": ["outcome 1", ...],
                "stipend_amount": 1000
            }}
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            generated_data = json.loads(response_text)
            
            result = {
                "title": title,
                "company": company,
                "location": location,
                "duration": duration,
                "category": category,
                "internship_type": "stipend",
                "description": generated_data.get('description', ''),
                "responsibilities": generated_data.get('responsibilities', []),
                "skills_required": generated_data.get('skills_required', []),
                "qualifications": generated_data.get('qualifications', []),
                "learning_outcomes": generated_data.get('learning_outcomes', []),
                "stipend_amount": generated_data.get('stipend_amount'),
                "currency": "USD",
                "is_active": True
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating internship listing: {e}")
            raise Exception(f"AI generation failed: {str(e)}")
    
    async def generate_scholarship_listing(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete scholarship listing from minimal inputs
        """
        try:
            title = prompt_data.get('title', '')
            provider = prompt_data.get('provider', '')
            country = prompt_data.get('country', '')
            education_level = prompt_data.get('education_level', 'undergraduate')
            
            prompt = f"""
            Generate a detailed scholarship listing in JSON format:
            
            Title: {title}
            Provider: {provider}
            Country: {country}
            Education Level: {education_level}
            
            Return ONLY a valid JSON object:
            {{
                "description": "detailed description",
                "eligibility_criteria": ["criteria 1", ...],
                "benefits": ["benefit 1", ...],
                "application_process": "process description",
                "amount": 10000,
                "field_of_study": ["field 1", ...]
            }}
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            generated_data = json.loads(response_text)
            
            result = {
                "title": title,
                "provider": provider,
                "country": country,
                "education_level": education_level,
                "scholarship_type": "merit-based",
                "description": generated_data.get('description', ''),
                "eligibility_criteria": generated_data.get('eligibility_criteria', []),
                "benefits": generated_data.get('benefits', []),
                "application_process": generated_data.get('application_process', ''),
                "amount": generated_data.get('amount'),
                "field_of_study": generated_data.get('field_of_study', []),
                "currency": "USD",
                "is_active": True
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating scholarship listing: {e}")
            raise Exception(f"AI generation failed: {str(e)}")
