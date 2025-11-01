import google.generativeai as genai
import json
import re

class GeminiArticleGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    async def generate_article(self, prompt_data: dict) -> dict:
        """
        Generate a comprehensive article using Gemini AI
        
        Args:
            prompt_data: dict with keys:
                - title: Article title
                - category: Category (technology, career-advice, interview-tips, etc.)
                - author: Author name
                - target_audience: Target audience description (optional)
                - key_points: List of key points to cover (optional)
        """
        title = prompt_data.get("title", "")
        category = prompt_data.get("category", "technology")
        author = prompt_data.get("author", "Admin")
        target_audience = prompt_data.get("target_audience", "professionals and students")
        key_points = prompt_data.get("key_points", [])
        
        key_points_text = ""
        if key_points:
            key_points_text = f"\n\nKey points to cover:\n" + "\n".join([f"- {point}" for point in key_points])
        
        prompt = f"""
You are an expert content writer for a career guidance platform. Generate a comprehensive, well-structured article.

Article Title: {title}
Category: {category}
Target Audience: {target_audience}
{key_points_text}

Generate a complete article with the following structure in JSON format:

{{
    "title": "{title}",
    "content": "Full article content in Markdown format with proper headings, paragraphs, lists, and formatting. Minimum 1500 words. Use ##, ###, **, *, bullet points, numbered lists, etc.",
    "excerpt": "Compelling 150-200 character summary that hooks the reader",
    "author": "{author}",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "category": "{category}",
    "read_time": 8
}}

Requirements:
1. Content should be engaging, informative, and actionable
2. Use proper Markdown formatting with headings (##, ###), bold (**text**), italics (*text*), lists
3. Include real-world examples and practical tips
4. Add 5-7 relevant tags
5. Calculate read_time based on word count (average 200 words per minute)
6. Make excerpt compelling and SEO-friendly
7. Content should be at least 1500 words
8. Include sections like: Introduction, Main Content (multiple sections), Key Takeaways, Conclusion

Respond ONLY with valid JSON, no additional text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                article_data = json.loads(json_match.group())
            else:
                article_data = json.loads(response_text)
            
            # Ensure all required fields are present
            article_data.setdefault("title", title)
            article_data.setdefault("author", author)
            article_data.setdefault("category", category)
            article_data.setdefault("tags", [])
            article_data.setdefault("read_time", 8)
            article_data.setdefault("is_published", True)
            
            return article_data
            
        except json.JSONDecodeError as e:
            # Fallback: create article from raw response
            return self._create_fallback_article(title, response_text, category, author)
        except Exception as e:
            raise Exception(f"Error generating article with Gemini: {str(e)}")
    
    def _create_fallback_article(self, title: str, content: str, category: str, author: str) -> dict:
        """Create article from raw content if JSON parsing fails"""
        # Clean content
        content = content.replace("```json", "").replace("```", "").strip()
        
        # Extract excerpt (first 200 chars)
        excerpt = content[:200] + "..." if len(content) > 200 else content
        
        # Calculate read time
        word_count = len(content.split())
        read_time = max(1, word_count // 200)
        
        # Generate basic tags from title and category
        tags = [category, "career", "guide"]
        
        return {
            "title": title,
            "content": content,
            "excerpt": excerpt,
            "author": author,
            "tags": tags,
            "category": category,
            "read_time": read_time,
            "is_published": True
        }
