from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/analysis.html')
def analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)