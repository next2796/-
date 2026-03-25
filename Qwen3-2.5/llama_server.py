"""
使用llama-cpp-python创建HTTP服务运行本地Qwen2.5 GGUF模型
"""
from flask import Flask, request, jsonify, render_template_string
from llama_cpp import Llama
import time
import os

app = Flask(__name__)

# 模型配置
MODEL_PATH = "./local_model/qwen2.5-0.5b-instruct-q5_0.gguf"
N_CTX = 2048
N_THREADS = 4

# 加载模型
print("Loading GGUF model with llama_cpp...")
llm = None
try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        verbose=False
    )
    print("✓ GGUF model loaded successfully!")
    print(f"  Context length: {N_CTX}")
    print(f"  Threads: {N_THREADS}")
except Exception as e:
    print(f"✗ Failed to load model: {e}")
    import traceback
    traceback.print_exc()

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qwen2.5 - llama.cpp Server</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 800px;
            height: 80vh;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 { font-size: 1.5rem; margin-bottom: 5px; }
        .header p { font-size: 0.9rem; opacity: 0.9; }
        .chat-body {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: fadeIn 0.3s ease-in;
        }
        .user-message { justify-content: flex-end; }
        .bot-message { justify-content: flex-start; }
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 20px;
            word-wrap: break-word;
            line-height: 1.4;
        }
        .user-message .message-content {
            background: #667eea;
            color: white;
            border-bottom-right-radius: 5px;
        }
        .bot-message .message-content {
            background: white;
            color: #333;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
        }
        .chat-input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }
        .chat-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .send-btn {
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        .typing {
            display: inline-flex;
            gap: 5px;
            padding: 10px;
        }
        .typing span {
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out both;
        }
        .typing span:nth-child(1) { animation-delay: -0.32s; }
        .typing span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Qwen2.5 Chatbot</h1>
            <p>Powered by llama.cpp - Local GGUF Model</p>
        </div>
        <div class="chat-body" id="chatBody">
            <div class="message bot-message">
                <div class="message-content">
                    Hello! I'm Qwen2.5-0.5B running locally with llama.cpp. How can I help you today?
                </div>
            </div>
        </div>
        <div class="input-area">
            <input type="text" class="chat-input" id="chatInput" placeholder="Type your message..." autofocus>
            <button class="send-btn" id="sendBtn">➤</button>
        </div>
    </div>
    
    <script>
        const chatBody = document.getElementById('chatBody');
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');
        let history = [];
        
        function addMessage(type, content) {
            const div = document.createElement('div');
            div.className = `message ${type}-message`;
            div.innerHTML = `<div class="message-content">${content}</div>`;
            chatBody.appendChild(div);
            chatBody.scrollTop = chatBody.scrollHeight;
        }
        
        function addTyping() {
            const id = 'typing-' + Date.now();
            const div = document.createElement('div');
            div.id = id;
            div.className = 'message bot-message';
            div.innerHTML = `<div class="message-content"><div class="typing"><span></span><span></span><span></span></div></div>`;
            chatBody.appendChild(div);
            chatBody.scrollTop = chatBody.scrollHeight;
            return id;
        }
        
        function removeTyping(id) {
            const el = document.getElementById(id);
            if (el) el.remove();
        }
        
        async function sendMessage() {
            const text = chatInput.value.trim();
            if (!text) return;
            
            addMessage('user', text);
            chatInput.value = '';
            const typingId = addTyping();
            
            try {
                const res = await fetch('/v1/chat/completions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        messages: [{role: 'user', content: text}],
                        temperature: 0.7,
                        max_tokens: 512
                    })
                });
                const data = await res.json();
                removeTyping(typingId);
                const reply = data.choices?.[0]?.message?.content || 'Error';
                addMessage('bot', reply);
                history.push([text, reply]);
            } catch (e) {
                removeTyping(typingId);
                addMessage('bot', 'Error: ' + e.message);
            }
        }
        
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', e => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Web界面"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """OpenAI兼容的聊天API"""
    if not llm:
        return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.json
    messages = data.get('messages', [])
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 512)
    
    # 构建prompt
    prompt = ""
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role == 'system':
            prompt += f"<|im_start|>system\n{content}<|im_end|>\n"
        elif role == 'user':
            prompt += f"<|im_start|>user\n{content}<|im_end|>\n"
        elif role == 'assistant':
            prompt += f"<|im_start|>assistant\n{content}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"
    
    # 生成
    start_time = time.time()
    try:
        output = llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["<|im_end|>", "<|im_start|>"]
        )
        response_text = output['choices'][0]['text'].strip()
        elapsed = time.time() - start_time
        print(f"Generated in {elapsed:.2f}s: {response_text[:50]}...")
        
        return jsonify({
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': response_text
                },
                'finish_reason': 'stop'
            }],
            'usage': {
                'prompt_tokens': len(prompt),
                'completion_tokens': len(response_text),
                'total_tokens': len(prompt) + len(response_text)
            }
        })
    except Exception as e:
        print(f"Generation error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy' if llm else 'unhealthy',
        'model': 'Qwen2.5-0.5B-Instruct-GGUF',
        'backend': 'llama.cpp'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Qwen2.5 GGUF Model - llama.cpp Server")
    print("=" * 60)
    
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found: {MODEL_PATH}")
        exit(1)
    
    if llm:
        print("\n✓ Server ready!")
        print(f"Web UI: http://localhost:8080/")
        print(f"API: http://localhost:8080/v1/chat/completions")
        print("\nPress Ctrl+C to stop\n")
        app.run(host='0.0.0.0', port=8080, debug=False)
    else:
        print("\n✗ Failed to start server")
        exit(1)
