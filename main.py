import functions_framework
import google.generativeai as genai
import json
import os

# Configure Gemini
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

@functions_framework.http
def pulse_agent(request):
    """PULSE UK Cultural Intelligence Agent Cloud Function"""

    # Parse request
    request_json = request.get_json(silent=True)
    if not request_json or 'query' not in request_json:
        return json.dumps({'error': 'No query provided'}), 400

    query = request_json['query']

    # Initialize model
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction="""You are PULSE, a UK cultural intelligence agent.
        Analyze UK trends, generate content, assess brand safety.
        Focus on British culture, humor, and regional variations."""
    )

    try:
        # Generate response
        response = model.generate_content(query)

        return json.dumps({
            'status': 'success',
            'response': response.text,
            'query': query
        })

    except Exception as e:
        return json.dumps({
            'status': 'error',
            'error': str(e)
        }), 500
