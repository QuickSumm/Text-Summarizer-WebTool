from flask import Flask, render_template, request
from QuickSumm import summarize_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarization():
    if request.method == 'POST':
        text = request.form['input_text']
        summary = summarize_text(text)
        return render_template('index.html', input_text=text, summary=summary,text=text)

if __name__ == '__main__':
    app.run(debug=True)
