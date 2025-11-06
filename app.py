from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('base2.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)