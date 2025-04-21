from flask import Flask, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Attach rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per 10 seconds"]
)

# Custom 429 error handler
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template_string(f'''
        <html>
        <head><title>Rate Limit Exceeded</title></head>
        <body style="text-align:center; font-family:sans-serif;">
            <h1 style="color:orange;">429 - Too Many Requests 🚫</h1>
            <p>{e.description}</p>
            <img src="https://media.giphy.com/media/xT9DPpf0zTqRASyzTi/giphy.gif" alt="Too Many Requests" width="300"/>
        </body>
        </html>
    '''), 429

# Test route with custom rate limit
@app.route('/test')
@limiter.limit("10 per minute")
def test():
    try:
        # Uncomment to simulate a crash:
        # 1 / 0  
        return render_template_string('''
            <html>
            <head><title>API Status</title></head>
            <body style="text-align:center; font-family:sans-serif;">
                <h1 style="color:green;">API is Running Smoothly ✅</h1>
                <img src="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif" alt="Running" width="300"/>
            </body>
            </html>
        ''')
    except Exception as e:
        return render_template_string(f'''
            <html>
            <head><title>API Crashed</title></head>
            <body style="text-align:center; font-family:sans-serif;">
                <h1 style="color:red;">API Crashed! ❌</h1>
                <p>{str(e)}</p>
                <img src="https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif" alt="Crash" width="300"/>
            </body>
            </html>
        ''')

# Run server
app.run(host="0.0.0.0", port=5000, debug=True)

