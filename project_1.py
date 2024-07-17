from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


OPENAI_API_KEY = 'sk-proj-E5K5P9Bf0MnOORdwZlklT3BlbkFJGc7zUdQ7XFIWZFkzTFoE'

RAPIDAPI_KEY = 'b3bb6a3311mshf6bb8cd52bf24c1p17cb80jsn3913ab9e48dc'
 

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    message = data['message']

    try:
        
        ai_response = call_openai_api(message)

      
        location = extract_location(ai_response)

        if location:
            
            weather_data = call_openweathermap_api(location)
            response = {
                'ai_response': ai_response,
                'weather_data': weather_data
            }
            return jsonify(response)
        else:
            return jsonify({'error': 'Location not found in message'}), 400

    except Exception as e:
        print(f'Error processing message: {e}')
        return jsonify({'error': 'Internal error'}), 500

def call_openai_api(prompt):
    url = 'https://api.openai.com/v1/engines/davinci/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'prompt': prompt,
        'max_tokens': 150
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
    return response.json()['choices'][0]['text'].strip()

def extract_location(text):
    
    if ' in ' in text:
        location = text.split(' in ')[-1].strip('?')
        return location
    return None

def call_openweathermap_api(location):
    url = f'https://community-open-weather-map.p.rapidapi.com/weather?q={location}'
    headers = {
        'x-rapidapi-host': 'community-open-weather-map.p.rapidapi.com',
        'x-rapidapi-key': RAPIDAPI_KEY,
        'useQueryString': 'true'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
#test
{
    "message": "What's the weather like in New York?"
}