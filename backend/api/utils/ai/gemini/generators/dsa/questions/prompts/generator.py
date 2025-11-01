import google.generativeai as genai
import json
import re

class GeminiDSAGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def generate_dsa_question(self, prompt_data: dict):
        """Generate a complete DSA question using Gemini AI"""
        
        topic = prompt_data.get('topic', 'Arrays')
        difficulty = prompt_data.get('difficulty', 'medium')
        company = prompt_data.get('company', '')
        
        prompt = f"""Generate a complete Data Structures and Algorithms coding question with the following specifications:

Topic: {topic}
Difficulty: {difficulty}
{f"Company Context: This question is similar to those asked at {company}" if company else ""}

Please provide a comprehensive DSA question in the following JSON format:
{{
    "title": "Clear, specific problem title",
    "description": "Detailed problem description (200-500 words) explaining the problem, what needs to be solved, and any important context",
    "difficulty": "{difficulty}",
    "topics": ["{topic}", "related_topic1", "related_topic2"],
    "companies": ["{company if company else 'Google'}", "similar_company1", "similar_company2"],
    "input_format": "Detailed description of input format with examples",
    "output_format": "Detailed description of expected output format",
    "constraints": "All constraints like array size, value ranges, time limits, etc.",
    "examples": [
        {{
            "input": "Example input",
            "output": "Example output",
            "explanation": "Step by step explanation of how we get from input to output"
        }},
        {{
            "input": "Another example input",
            "output": "Another example output",
            "explanation": "Detailed explanation"
        }}
    ],
    "solution_approach": "Detailed explanation of the optimal solution approach (300-500 words). Explain the intuition, algorithm steps, and why this approach works",
    "time_complexity": "O(n log n) or appropriate complexity with brief explanation",
    "space_complexity": "O(n) or appropriate complexity with brief explanation",
    "code_solutions": [
        {{
            "language": "python",
            "code": "Complete, working Python solution with comments"
        }},
        {{
            "language": "javascript",
            "code": "Complete, working JavaScript solution with comments"
        }},
        {{
            "language": "java",
            "code": "Complete, working Java solution with comments"
        }}
    ],
    "hints": [
        "Hint 1 - subtle clue",
        "Hint 2 - more direct",
        "Hint 3 - very direct"
    ],
    "acceptance_rate": 45.5,
    "is_active": true,
    "is_premium": false
}}

Make sure the question is:
1. Original and interesting
2. Has clear problem statement
3. Includes multiple examples with explanations
4. Provides complete working code solutions in multiple languages
5. Includes helpful hints that progressively reveal the solution
6. Has realistic acceptance rate based on difficulty

Return ONLY the JSON object, no additional text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from markdown code blocks if present
            if '```json' in result_text:
                result_text = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL).group(1)
            elif '```' in result_text:
                result_text = re.search(r'```\s*(.*?)\s*```', result_text, re.DOTALL).group(1)
            
            question_data = json.loads(result_text)
            return question_data
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {result_text}")
            # Return a basic structure if JSON parsing fails
            return {
                "title": f"{difficulty.capitalize()} {topic} Problem",
                "description": "Error generating question. Please try again.",
                "difficulty": difficulty,
                "topics": [topic],
                "companies": [company] if company else [],
                "examples": [],
                "solution_approach": "Error generating solution",
                "time_complexity": "N/A",
                "space_complexity": "N/A",
                "code_solutions": [],
                "hints": [],
                "is_active": True,
                "is_premium": False
            }
        except Exception as e:
            print(f"Error generating DSA question: {e}")
            raise
    
    async def generate_dsa_sheet(self, prompt_data: dict):
        """Generate a complete DSA practice sheet"""
        
        sheet_name = prompt_data.get('sheet_name', 'DSA Practice Sheet')
        level = prompt_data.get('level', 'intermediate')
        focus_topics = prompt_data.get('focus_topics', ['Arrays', 'Strings', 'Trees'])
        
        prompt = f"""Generate a complete DSA practice sheet with the following specifications:

Sheet Name: {sheet_name}
Level: {level}
Focus Topics: {', '.join(focus_topics)}

Create a curated list of 20-30 problems organized by topic and difficulty. Provide in JSON format:
{{
    "name": "{sheet_name}",
    "description": "Comprehensive description of the sheet (200-300 words) - what it covers, who it's for, what skills will be gained",
    "author": "CareerGuide Team",
    "level": "{level}",
    "estimated_time": "Realistic time estimate like '4 weeks' or '2 months'",
    "tags": ["relevant", "tags", "for", "sheet"],
    "difficulty_breakdown": {{
        "easy": 8,
        "medium": 12,
        "hard": 5
    }},
    "topics_covered": {json.dumps(focus_topics)},
    "questions": [
        {{
            "question_title": "Problem name",
            "topic": "Topic name",
            "difficulty": "easy/medium/hard",
            "order": 1,
            "is_completed": false
        }},
        // ... more questions organized logically
    ],
    "is_published": true,
    "is_featured": false,
    "is_premium": false
}}

Make sure:
1. Problems progress logically from easy to hard within each topic
2. Good mix of fundamental and advanced problems
3. Problems build on each other
4. Include variety across different topics
5. Realistic difficulty distribution

Return ONLY the JSON object."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from markdown code blocks if present
            if '```json' in result_text:
                result_text = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL).group(1)
            elif '```' in result_text:
                result_text = re.search(r'```\s*(.*?)\s*```', result_text, re.DOTALL).group(1)
            
            sheet_data = json.loads(result_text)
            return sheet_data
            
        except Exception as e:
            print(f"Error generating DSA sheet: {e}")
            raise
