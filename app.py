from flask import Flask, render_template
from routes.upload_api import upload_bp

app = Flask(__name__)

# Mount the blueprint under the /api prefix
app.register_blueprint(upload_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
