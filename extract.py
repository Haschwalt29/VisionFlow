import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
else:
    model = None

def fetch_webpage_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(url, headers=headers, timeout=15, verify=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text_content = soup.get_text()
        
        lines = (line.strip() for line in text_content.splitlines())
        text_content = ' '.join(line for line in lines if line)
        
        return text_content[:8000]
        
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"Network connection failed. Unable to reach the website. This might be due to DNS issues or network connectivity problems. Error: {str(e)}")
    except requests.exceptions.Timeout as e:
        raise Exception(f"Request timed out. The website took too long to respond. Try again later or check if the URL is accessible.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch webpage: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error while fetching webpage: {str(e)}")

def extract_data_with_gemini(content):
    try:
        if not model:
            raise Exception("Google AI API key not configured. Please set GOOGLE_AI_API_KEY environment variable.")
        prompt = """
        Extract the following details from the provided webpage content:
        - Name or Title of the product/service/company
        - Description (brief summary of what it offers)
        - Key Features (list key features or points)
        - Pricing information (if any)

        Return the result strictly as valid JSON with keys: name, description, features, pricing.
        If any field is not available or unclear, use null for that field.
        
        Example format:
        {
            "name": "OpenAI",
            "description": "AI research and deployment company",
            "features": ["GPT models", "ChatGPT API", "DALL-E"],
            "pricing": "Freemium model"
        }
        
        Webpage content:
        """ + content

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=1000,
            )
        )
        
        extracted_text = response.text.strip()
        
        try:
            if extracted_text.startswith('```json'):
                extracted_text = extracted_text[7:]
            if extracted_text.endswith('```'):
                extracted_text = extracted_text[:-3]
            
            extracted_data = json.loads(extracted_text)
            return extracted_data
            
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', extracted_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            
            return {
                "name": "Unknown",
                "description": extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text,
                "features": [],
                "pricing": "Not available"
            }
            
    except Exception as e:
        raise Exception(f"Gemini extraction failed: {str(e)}")

def process_url(url):
    try:
        content = fetch_webpage_content(url)
        
        if not content:
            return {"error": "No content found on webpage"}
        
        extracted_data = extract_data_with_gemini(content)
        
        required_fields = ['name', 'description', 'features', 'pricing']
        for field in required_fields:
            if field not in extracted_data:
                extracted_data[field] = "Not available"
        
        if isinstance(extracted_data.get('features'), list):
            extracted_data['features'] = ', '.join(extracted_data['features'])
        
        return {
            "success": True,
            "data": extracted_data,
            "raw_content_length": len(content)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }