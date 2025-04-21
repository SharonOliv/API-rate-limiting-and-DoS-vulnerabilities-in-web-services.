from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/test')
def test():
    try:
        # Simulate an error for testing
        # Uncomment the next line to test crash detection
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

app.run(host='0.0.0.0', port=5000, debug=True)

