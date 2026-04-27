from flask import Flask
app = Flask(__name__)

@app.route('/chat')
def chat():
    return nano_ai.think(request.args['q'])

# ngrok tunnel → Web access