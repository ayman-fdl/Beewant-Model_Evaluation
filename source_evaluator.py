import csv
import json
import re
import requests
from typing import List, Dict, Tuple
from config import API_TOKEN, API_URL, CHAT_MODEL, EVALUATOIN_MODEL
import time

def read_questions_from_csv(file_path: str) -> List[Dict[str, str]]:
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            questions.append({
                'thematic': row['thematic'],
                'question': row['question']
            })
    return questions

def get_web_search_results(question: str):
    headers = {
        'Authorization': f'Token {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "prompt": question,
        "chat_model": CHAT_MODEL,
        "web": True,
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        results = response.json()
        
        links = []
        sources = re.search(r'\[\{.*?\}\]', results['answer'][0], re.DOTALL)
        raw_answer = (results['answer'][0]).split("}]")[1]
        if sources:
            result = json.loads(sources.group(0))
            for citation in result:
                links.append(citation['url'])
        return links, raw_answer
    except Exception as e:
        print(f"Error getting web search results: {e}")
        return [], None

def evaluate_sources(sources: List[str], question: str) -> Dict:
    headers = {
        'Authorization': f'Token {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Create evaluation prompt using the exact format
    evaluation_prompt = f"""Evaluate the following sources for the question: "{question}"

Sources:
{json.dumps(sources, indent=2)}

Evaluate each source based on:
- The domain name (e.g., .org, .gov, known institutions, major news outlets),
- The structure and keywords in the URL (e.g., presence of date or topic),
- Any general knowledge you have about the source.

For each link, assign a **total score out of 25** based on the following 4 criteria (each scored from 0 to 5):
1. **relevance** to the user question  
2. **credibility** of the domain  
3. **freshness** (based on year or indicators in the URL)  
4. **coverage** or depth based on the URL context

Add the scores for each URL and return the result as a JSON list with this structure:

[
    {{
    "url": "https://example.com/article-sahel-water-2023",
    "score": 22
    }},
    {{
    "url": "https://oldnews.net/blog123",
    "score": 9
    }},
    {{
    "url": "https://un.org/sahel-water-report",
    "score": 24
    }}
]
Return only the raw JSON array. Do not include any explanation, commentary, or text outside the JSON. Do not wrap it in code blocks."""
    
    data = {
        "prompt": evaluation_prompt,
        "chat_model": EVALUATOIN_MODEL,
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Parse the evaluation result
        # Note: You'll need to adjust this based on the actual response structure
        return result
        # evaluation = result.get('response', {})
        # return evaluation
    except Exception as e:
        print(f"Error evaluating sources: {e}")
        return {"sources": []}

def main():
    # Read API token from environment or config file
    
    # Read questions from CSV
    questions = read_questions_from_csv('thematic_subjects.csv')
    
    # Process each question
    for question_data in questions:
        print(f"\nProcessing question: ({question_data['thematic']}) {question_data['question']}")
        
        # Get web search results
        sources, raw_answers = get_web_search_results(question_data['question'])
        
        if sources:
            evaluation = evaluate_sources(sources, question_data['question'])
            
            print(json.dumps(evaluation['answer'], indent=2))
            with open("result.json", 'w') as f:
                json.dump(evaluation['answer'], f, indent=2)
            
            time.sleep(1)
        else:
            print("No sources found for this question")
        break

if __name__ == "__main__":
    main() 