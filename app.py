from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  



@app.route('/')
def base():
    return render_template('base.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')

@app.route('/herramientas')
def herramientas():
    return render_template('herramientas.html')

@app.route('/inicia sesion', methods=['GET', 'POST'])
def sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        if correo == "admin@gmail.com" and contraseña == "1234":
            return redirect(url_for('inicio')) 

        flash("Correo o contraseña incorrectos", "danger")
        return redirect(url_for('login'))

    return render_template('login.html')




@app.route('/imc', methods=['GET', 'POST'])
def imc():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form.get('peso', 0))
            altura = float(request.form.get('altura', 0)) / 100
            if peso <= 0 or altura <= 0:
                raise ValueError("Valores inválidos.")

            imc_valor = peso / (altura ** 2)
            if imc_valor < 18.5:
                estado = "Bajo peso"
            elif imc_valor < 25:
                estado = "Normal"
            elif imc_valor < 30:
                estado = "Sobrepeso"
            else:
                estado = "Obesidad"

            resultado = f"Tu IMC es {imc_valor:.2f} ({estado})"
        except Exception:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('imc.html', resultado=resultado)



@app.route('/tmb', methods=['GET', 'POST'])
def tmb():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form.get('peso', 0))
            altura = float(request.form.get('altura', 0))
            edad = int(request.form.get('edad', 0))
            sexo = request.form.get('sexo')

            if sexo not in ["Masculino", "Femenino"] or peso <= 0 or altura <= 0 or edad <= 0:
                raise ValueError("Datos inválidos.")

            if sexo == "Masculino":
                tmb_valor = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
            else:
                tmb_valor = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)

            resultado = f"Tu TMB es {tmb_valor:.2f} kcal/día"
        except Exception:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('tmb.html', resultado=resultado)



@app.route('/gct', methods=['GET', 'POST'])
def gct():
    resultado = None
    if request.method == 'POST':
        try:
            tmb = float(request.form.get('tmb', 0))
            actividad = float(request.form.get('actividad', 0))
            if tmb <= 0 or actividad <= 0:
                raise ValueError("Datos inválidos.")
            gct_valor = tmb * actividad
            resultado = f"Tu Gasto Calórico Total es {gct_valor:.2f} kcal/día"
        except Exception:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('gct.html', resultado=resultado)



@app.route('/peso_ideal', methods=['GET', 'POST'])
def peso_ideal():
    resultado = None
    if request.method == 'POST':
        try:
            altura = float(request.form.get('altura', 0))
            sexo = request.form.get('sexo')

            if sexo not in ["Masculino", "Femenino"] or altura <= 0:
                raise ValueError("Datos inválidos.")

            if sexo == 'Masculino':
                peso_ideal_valor = 50 + 2.3 * ((altura / 2.54) - 60)
            else:
                peso_ideal_valor = 45.5 + 2.3 * ((altura / 2.54) - 60)

            resultado = f"Tu peso ideal es {peso_ideal_valor:.2f} kg"
        except Exception:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('peso_ideal.html', resultado=resultado)



@app.route('/macronutrientes', methods=['GET', 'POST'])
def macronutrientes():
    resultado = None
    if request.method == 'POST':
        try:
            calorias = float(request.form.get('calorias', 0))
            if calorias <= 0:
                raise ValueError("Valor inválido.")
            proteinas = calorias * 0.3 / 4
            grasas = calorias * 0.25 / 9
            carbohidratos = calorias * 0.45 / 4
            resultado = {
                "proteinas": round(proteinas, 1),
                "grasas": round(grasas, 1),
                "carbohidratos": round(carbohidratos, 1)
            }
        except Exception:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('macronutrientes.html', resultado=resultado)



@app.route('/analizador', methods=['GET', 'POST'])
def analizador():
    resultado = None
    if request.method == 'POST':
        receta = request.form.get('receta', '').strip()
        if receta:
            resultado = f"La receta '{receta}' tiene una estimación de 350 kcal por porción (demo)."
        else:
            flash("Por favor, ingresa una receta válida.", "warning")
    return render_template('analizador.html', resultado=resultado)



diccionario_datos = {
    "nombre": {"tipo": "Texto (string)", "descripcion": "Nombre del usuario", "obligatorio": True},
    "apellidos": {"tipo": "Texto (string)", "descripcion": "Apellidos del usuario", "obligatorio": True},
    "edad": {"tipo": "Entero (int)", "descripcion": "Edad del usuario", "obligatorio": True},
    "sexo": {"tipo": "Texto (string)", "descripcion": "Sexo o identidad de género",
    "valores_permitidos": ["Femenino", "Masculino", "Otro"], "obligatorio": True},
    "peso": {"tipo": "Decimal (float)", "descripcion": "Peso corporal (kg)", "obligatorio": True},
    "altura": {"tipo": "Entero (int)", "descripcion": "Altura (cm)", "obligatorio": True},
    "nivel_actividad": {"tipo": "Texto (string)", "descripcion": "Nivel de actividad física diaria",
    "valores_permitidos": ["Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"],
    "obligatorio": True}
}


if __name__ == '__main__':
    app.run(debug=True)

