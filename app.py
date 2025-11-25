from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "LgHJdzvsfDQ0jcffIyAVRLu3hbTg2tpUG7AJ4d3M"

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
    "obligatorio": True},
    "correo": {"tipo": "Texto (string)", "descripcion": "Correo electrónico", "obligatorio": True},
    "contraseña": {"tipo": "Texto (string)", "descripcion": "Contraseña de usuario", "obligatorio": True},
    "objetivo": {"tipo": "Texto (string)", "descripcion": "Objetivo principal", "obligatorio": True},
    "alergias": {"tipo": "Texto (string)", "descripcion": "Alergias o intolerancias", "obligatorio": False},
    "dieta": {"tipo": "Texto (string)", "descripcion": "Dieta o preferencia", "obligatorio": False},
    "disgustos": {"tipo": "Texto (string)", "descripcion": "Alimentos que no gustan", "obligatorio": False},
    "cocina": {"tipo": "Texto (string)", "descripcion": "Nivel de experiencia en cocina", "obligatorio": True}
}
usuarios_registrados = {}

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/inicio')
def inicio():
    if not session.get("usuario"):
        flash("Debes iniciar sesión primero.", "warning")
        return redirect(url_for('sesion'))
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get("correo").lower()
        if correo in usuarios_registrados:
            flash("Este correo ya está registrado", "danger")
            return redirect(url_for('registro'))
        usuarios_registrados[correo] = {key: request.form.get(key) for key in diccionario_datos}
        flash("Registro exitoso, inicia sesión ahora", "success")
        return redirect(url_for('sesion'))
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
        correo = request.form.get("correo").lower()
        contraseña = request.form.get("contraseña")
        usuario = usuarios_registrados.get(correo)
        if usuario and usuario.get("contraseña") == contraseña:
            session["usuario"] = correo
            flash(f"Bienvenido {usuario.get('nombre')}!", "success")
            return redirect(url_for('inicio'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('sesion'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("usuario", None)
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for('sesion'))

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
    datos_api = None
    if request.method == 'POST':
        receta = request.form.get('receta', '').strip()
        if receta:
            params = {"query": receta, "api_key": API_KEY}
            try:
                response = requests.get(USDA_SEARCH_URL, params=params)
                if response.status_code == 200:
                    datos_api = response.json()
                    resultado = f"Resultados obtenidos para la receta '{receta}'"
                else:
                    flash("No se pudieron obtener datos de la API.", "danger")
            except Exception as e:
                flash(f"Error al consultar la API: {e}", "danger")
        else:
            flash("Por favor, ingresa una receta válida.", "warning")
    return render_template('analizador.html', resultado=resultado, datos_api=datos_api)

if __name__ == '__main__':
    app.run(debug=True)


