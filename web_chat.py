"""
PULSE UK Agent Web Chat Interface
A Flask-based chat interface for the PULSE agent
"""

import os
import json
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
from pulse_agent import PulseUKAgent

# Load environment
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize agent
agent = None

# HTML template for chat interface
CHAT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PULSE UK Cultural Intelligence Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 700px;
            height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            text-align: center;
        }

        .chat-header h1 {
            font-size: 28px;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .chat-header p {
            opacity: 0.95;
            font-size: 15px;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 25px;
            background: #f8f9fa;
        }

        .message {
            margin-bottom: 20px;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            text-align: right;
        }

        .message-content {
            display: inline-block;
            padding: 14px 18px;
            border-radius: 20px;
            max-width: 75%;
            word-wrap: break-word;
            line-height: 1.5;
        }

        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .message.agent .message-content {
            background: white;
            color: #333;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .message-label {
            font-size: 13px;
            color: #666;
            margin-bottom: 6px;
            font-weight: 500;
        }

        .chat-input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }

        .quick-queries {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .quick-query {
            padding: 8px 14px;
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.3s;
            font-weight: 500;
        }

        .quick-query:hover {
            background: #667eea;
            color: white;
        }

        .chat-input-wrapper {
            display: flex;
            gap: 12px;
        }

        .chat-input {
            flex: 1;
            padding: 14px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 15px;
            transition: border-color 0.3s;
        }

        .chat-input:focus {
            border-color: #667eea;
        }

        .send-button {
            padding: 14px 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            font-size: 15px;
            transition: transform 0.2s;
        }

        .send-button:hover {
            transform: scale(1.05);
        }

        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .loading {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            animation: pulse 1s infinite;
            margin: 0 3px;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.2); }
        }

        .loading:nth-child(2) { animation-delay: 0.2s; }
        .loading:nth-child(3) { animation-delay: 0.4s; }

        pre {
            background: #f5f5f5;
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>PULSE UK Cultural Intelligence</h1>
            <p>AI-powered UK trend analysis and content generation</p>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message agent">
                <div class="message-label">PULSE Agent</div>
                <div class="message-content">
                    Hello! I'm PULSE, your UK cultural intelligence agent. I can help you:
                    <br><br>
                    • Analyze UK cultural trends<br>
                    • Generate British-style content<br>
                    • Assess brand safety for UK market<br>
                    • Understand regional variations<br>
                    <br>
                    What would you like to know about UK culture today?
                </div>
            </div>
        </div>

        <div class="chat-input-container">
            <div class="quick-queries">
                <button class="quick-query" onclick="sendQuickQuery('What UK trends are happening today?')">
                    Today's Trends
                </button>
                <button class="quick-query" onclick="sendQuickQuery('Generate Twitter content for UK audience')">
                    Twitter Content
                </button>
                <button class="quick-query" onclick="sendQuickQuery('Analyze UK regional differences')">
                    Regional Analysis
                </button>
                <button class="quick-query" onclick="sendQuickQuery('Check brand safety for UK market')">
                    Brand Safety
                </button>
            </div>

            <div class="chat-input-wrapper">
                <input
                    type="text"
                    class="chat-input"
                    id="chatInput"
                    placeholder="Ask about UK trends, content ideas, or brand safety..."
                    onkeypress="if(event.key === 'Enter' && !event.shiftKey) sendMessage()"
                >
                <button class="send-button" id="sendButton" onclick="sendMessage()">
                    Send
                </button>
            </div>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();

            if (!message) return;

            // Add user message to chat
            addMessage(message, 'user');

            // Clear input and disable send button
            input.value = '';
            const sendButton = document.getElementById('sendButton');
            sendButton.disabled = true;

            // Show loading indicator
            const loadingId = addLoadingMessage();

            try {
                // Call the API
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: message })
                });

                const data = await response.json();

                // Remove loading indicator
                removeMessage(loadingId);

                // Add agent response
                if (data.status === 'success') {
                    addMessage(data.response, 'agent');
                } else {
                    addMessage('Sorry, I encountered an error: ' + (data.error || 'Unknown error'), 'agent');
                }

            } catch (error) {
                console.error('Error:', error);
                removeMessage(loadingId);
                addMessage('Sorry, I couldn\'t connect to the server. Please try again.', 'agent');
            } finally {
                sendButton.disabled = false;
                input.focus();
            }
        }

        function sendQuickQuery(query) {
            document.getElementById('chatInput').value = query;
            sendMessage();
        }

        function addMessage(content, sender) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;

            const labelDiv = document.createElement('div');
            labelDiv.className = 'message-label';
            labelDiv.textContent = sender === 'user' ? 'You' : 'PULSE Agent';

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';

            // Format the content
            if (content.includes('{') || content.includes('[')) {
                try {
                    // Try to parse as JSON for better formatting
                    const parsed = JSON.parse(content);
                    contentDiv.innerHTML = `<pre>${JSON.stringify(parsed, null, 2)}</pre>`;
                } catch {
                    // Not JSON, just format normally
                    contentDiv.innerHTML = content.replace(/\\n/g, '<br>');
                }
            } else {
                contentDiv.innerHTML = content.replace(/\\n/g, '<br>');
            }

            messageDiv.appendChild(labelDiv);
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);

            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;

            return messageDiv.id = Date.now();
        }

        function addLoadingMessage() {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message agent';
            messageDiv.id = `loading-${Date.now()}`;

            const labelDiv = document.createElement('div');
            labelDiv.className = 'message-label';
            labelDiv.textContent = 'PULSE Agent';

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = `
                <span class="loading"></span>
                <span class="loading"></span>
                <span class="loading"></span>
            `;

            messageDiv.appendChild(labelDiv);
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);

            chatMessages.scrollTop = chatMessages.scrollHeight;

            return messageDiv.id;
        }

        function removeMessage(messageId) {
            const message = document.getElementById(messageId);
            if (message) {
                message.remove();
            }
        }

        // Focus input on load
        window.onload = () => {
            document.getElementById('chatInput').focus();
        };
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    """Serve the chat interface"""
    return render_template_string(CHAT_TEMPLATE)


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    global agent

    try:
        data = request.json
        query = data.get('query', '')

        if not query:
            return jsonify({'status': 'error', 'error': 'No query provided'}), 400

        # Process the query based on keywords
        response = ""

        if 'trend' in query.lower():
            result = agent.analyze_uk_trends(query)
            response = json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
        elif 'content' in query.lower() or 'generate' in query.lower():
            # Extract trend from query
            trend = query.replace('generate', '').replace('content', '').strip()
            response = agent.generate_uk_content(trend)
        elif 'safety' in query.lower() or 'safe' in query.lower():
            content = query.replace('brand safety', '').replace('safety', '').strip()
            result = agent.assess_brand_safety(content)
            response = json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
        elif 'region' in query.lower():
            trend = query.replace('regional', '').replace('region', '').strip()
            result = agent.analyze_regional_variations(trend)
            response = json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
        else:
            # General query
            response = agent.process_query(query)

        return jsonify({
            'status': 'success',
            'response': response
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


def initialize():
    """Initialize the agent"""
    global agent

    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("[ERROR] GEMINI_API_KEY not found in environment")
        print("Please set it in your .env file")
        return False

    try:
        agent = PulseUKAgent()
        print("[OK] Agent initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize agent: {e}")
        return False


if __name__ == '__main__':
    print("\n" + "="*60)
    print("PULSE UK Cultural Intelligence Web Chat")
    print("="*60)

    if initialize():
        print("\n[LAUNCH] Starting web server...")
        print("   Open your browser to: http://localhost:8080")
        print("   Press Ctrl+C to stop the server")
        print("="*60 + "\n")

        app.run(host='localhost', port=8080, debug=False)
    else:
        print("\n[ERROR] Failed to start server")
        print("Please check your .env file and ensure GEMINI_API_KEY is set")