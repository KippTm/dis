from flask import Flask, render_template, abort

app = Flask(__name__, template_folder='views')

def render_temp(temp):
    try:
        return render_template(f'{temp}.html')
    except:
        abort(404)

@app.route('/')
def main():
    return render_temp("index")
