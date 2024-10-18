from flask import Flask, render_template
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.route('/')
def show_layout():
    return render_template('HomePage.html')
if __name__ == '__app__':
    app.run(debug=True, port=5000)