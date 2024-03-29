from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import numpy as np
from utils.python_utils import readEDF
import os
import tempfile

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

save_path = tempfile.gettempdir() + '/uploaded_file.edf'
print(save_path)

@app.route('/analysis.html', methods=['GET', 'POST'])
def analysis():
    final_avg1 = final_avg2 = []
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename

        if file and filename.rsplit('.', 1)[1].lower() == 'edf':
            file.save(save_path)
            print(file)
            try:
                final_avg1, final_avg2 = readEDF(save_path)
                os.remove(save_path)
            except Exception as e:
                print(f"Error occurred while reading EDF file: {e}")
                # Remove the file if the readEDF function fails
                os.remove(save_path)
        else:
            return 'Invalid file format. Only .edf files are allowed.'
            
    return render_template('analysis.html', final_avg1=final_avg1.tolist(), final_avg2=final_avg2.tolist())

if __name__ == '__main__':
    app.run(debug=True)