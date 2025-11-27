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
usuarios_registrados = {
    
}

lista_recetas = [
    {
        "nombre": "Bowl de Quinoa y Pollo",
        "tiempo": 25,
        "dificultad": "Fácil",
        "dieta": "Mediterránea",
        "calorias": 420,
        "ingrediente": "pollo",
        "carbohidratos": "45 g",
        "saludabilidad": "5/5",
        "ingredientes": [
            "1 taza de quinoa cocida",
            "150 g pechuga de pollo a la plancha en cubos",
            "1/2 pepino picado",
            "1/2 aguacate en láminas",
            "1 zanahoria rallada",
            "1 cda aceite de oliva",
            "Jugo de 1 limón",
            "Sal y pimienta al gusto"
        ],
        "preparacion": [
            "1) Lava la quinoa en un colador fino bajo agua fría hasta que el agua salga clara.",
            "2) Cocina 1 taza de quinoa con 2 tazas de agua o caldo, lleva a ebullición, baja el fuego y cocina 12–15 minutos hasta que esté tierna. Deja reposar 5 min y esponja con un tenedor.",
            "3) Mientras la quinoa se cocina, sazona la pechuga de pollo con sal y pimienta. Calienta una sartén con 1 cucharadita de aceite y cocina el pollo 4–5 minutos por lado hasta que esté dorado y cocido por dentro. Corta en cubos.",
            "4) Lava y corta el pepino, ralla la zanahoria y corta el aguacate en láminas.",
            "5) En un bowl grande coloca la quinoa como base. Dispón el pollo, pepino, zanahoria y aguacate en secciones sobre la quinoa.",
            "6) Prepara el aliño mezclando el jugo de limón, el aceite de oliva, sal y pimienta. Prueba y ajusta.",
            "7) Vierte el aliño sobre el bowl justo antes de servir y mezcla ligeramente para integrar sabores.",
            "8) Sirve inmediatamente para aprovechar la textura del aguacate y la quinoa tibia."
        ]
    },
    {
        "nombre": "Meal Prep de Pollo Asado",
        "tiempo": 40,
        "dificultad": "Intermedia",
        "dieta": "Keto",
        "calorias": 510,
        "ingrediente": "pollo",
        "carbohidratos": "10 g",
        "saludabilidad": "4/5",
        "ingredientes": [
            "2 pechugas de pollo",
            "2 cdas aceite de oliva",
            "1 cda pimentón dulce",
            "1 cda ajo en polvo",
            "Sal y pimienta",
            "Verduras para acompañar (brócoli, pimientos)"
        ],
        "preparacion": [
            "1) Precalienta el horno a 200°C. Mezcla aceite, pimentón, ajo en polvo, sal y pimienta.",
            "2) Unta las pechugas con la mezcla por ambos lados y colócalas en una bandeja para horno.",
            "3) Hornea 20–25 minutos hasta que el interior marque 75°C o no esté rosado.",
            "4) Mientras tanto, lava y corta las verduras. Saltea el brócoli y pimientos 5–7 minutos con una cucharadita de aceite hasta que estén al dente.",
            "5) Retira el pollo, deja reposar 5 minutos y filetea o corta en cubos para el meal prep.",
            "6) Divide en recipientes: pollo + verduras. Guarda en fría (4°C) hasta 4 días.",
            "7) Para recalentar, usa microondas o sartén 2–3 minutos hasta que esté caliente por completo."
        ]
    },
    {
        "nombre": "Wrap Vegano de Garbanzos",
        "tiempo": 15,
        "dificultad": "Fácil",
        "dieta": "Vegana",
        "calorias": 320,
        "ingrediente": "garbanzos",
        "carbohidratos": "40 g",
        "saludabilidad": "5/5",
        "ingredientes": [
            "1 tortilla integral o de tu preferencia",
            "1/2 taza garbanzos cocidos",
            "1/4 taza col morada rallada",
            "1/4 aguacate en láminas",
            "1 cda hummus",
            "Limón, sal y pimienta"
        ],
        "preparacion": [
            "1) Calienta la tortilla en una sartén 30 segundos por lado para que sea fácil de doblar.",
            "2) Machaca ligeramente los garbanzos con un tenedor, sazona con sal, pimienta y unas gotas de limón.",
            "3) Unta hummus en el centro de la tortilla como base (esto ayuda a mantener húmedo el wrap).",
            "4) Coloca los garbanzos, la col morada y las láminas de aguacate sobre el hummus.",
            "5) Dobla los extremos y enrolla firmemente para formar el wrap. Si deseas, corta por la mitad.",
            "6) Sirve inmediatamente o envuelve en papel film para llevar."
        ]
    },
    {
        "nombre": "Salteado Keto de Res y Brócoli",
        "tiempo": 30,
        "dificultad": "Intermedia",
        "dieta": "Keto",
        "calorias": 480,
        "ingrediente": "res",
        "carbohidratos": "8 g",
        "saludabilidad": "4/5",
        "ingredientes": [
            "200 g filete de res en tiras",
            "1 taza brócoli en floretes",
            "2 cdas salsa de soja baja en sodio",
            "1 cda aceite de sésamo o oliva",
            "1 diente ajo picado",
            "Jengibre al gusto"
        ],
        "preparacion": [
            "1) Corta la res en tiras finas y sécalas con papel para que se doren mejor.",
            "2) Calienta una sartén grande a fuego alto con 1 cda de aceite. Añade la res y saltea 2–3 minutos hasta dorar. Retira y reserva.",
            "3) En la misma sartén añade un poco más de aceite si hace falta y saltea el ajo y jengibre 30 segundos hasta aromatizar.",
            "4) Agrega el brócoli y saltea 4–5 minutos hasta que esté tierno pero crujiente.",
            "5) Vuelve a incorporar la res, añade la salsa de soja y mezcla 1–2 minutos para integrar sabores.",
            "6) Rectifica sal y sirve inmediatamente."
        ]
    },
    {
        "nombre": "Paella Vegetariana Integral",
        "tiempo": 55,
        "dificultad": "Difícil",
        "dieta": "Vegetariana",
        "calorias": 520,
        "ingrediente": "arroz integral",
        "carbohidratos": "60 g",
        "saludabilidad": "4/5",
        "ingredientes": [
            "1 taza arroz integral",
            "1 pimiento rojo",
            "1 cebolla",
            "1 taza alcachofas",
            "1 taza chícharos (guisantes)",
            "1 tomate rallado",
            "3 tazas caldo de verduras caliente",
            "1 cdta cúrcuma o hebras de azafrán",
            "Aceite de oliva",
            "Sal y pimienta"
        ],
        "preparacion": [
            "1) Limpia y corta el pimiento y la cebolla en cubos pequeños. Ralla el tomate.",
            "2) Calienta una paellera o sartén amplia con 2 cdas de aceite de oliva a fuego medio.",
            "3) Sofríe la cebolla 4–5 minutos hasta que esté translúcida; añade el pimiento y cocina 5 minutos más hasta que empiece a ablandar.",
            "4) Añade las alcachofas y los chícharos; saltea 2–3 minutos para incorporar.",
            "5) Agrega el tomate rallado y cocina 3–4 minutos hasta que el líquido se reduzca ligeramente y concentre sabor.",
            "6) Incorpora el arroz integral y revuelve 1–2 minutos para que los granos se impregnen del sofrito.",
            "7) Añade la cúrcuma o el azafrán y mezcla. Vierte 3 tazas de caldo caliente (la proporción con arroz integral suele ser mayor que con arroz blanco).",
            "8) Distribuye los ingredientes de manera uniforme y ajusta de sal y pimienta. Sube el fuego hasta que rompa hervor.",
            "9) Cuando hierva, reduce el fuego a bajo-medio y cocina sin remover durante 30–35 minutos, hasta que el arroz esté tierno y el líquido se haya absorbido. Si hace falta, agrega un poco más de caldo caliente y continúa la cocción hasta que el arroz esté en su punto.",
            "10) Una vez cocinado, apaga el fuego y deja reposar la paella 5–10 minutos cubierta con un paño limpio para que los aromas se asienten.",
            "11) Sirve caliente, acomodando si quieres unas hebras de perejil o un chorrito de aceite de oliva por encima."
        ]
    }
]


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/plantillas')
def plantillas():
    return render_template('plantillas.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get("correo").lower()
        if correo in usuarios_registrados:
            flash("Este correo ya está registrado", "danger")
            return redirect(url_for('registro'))
        usuarios_registrados[correo] = {key: request.form.get(key) for key in diccionario_datos}
        flash("Registro exitoso, inicia sesión ahora", "exito")
        return redirect(url_for('sesion'))
    return render_template('registro.html')

@app.route("/recetas")
def recetas():

    if not request.args:
        return render_template("recetas.html", recetas=None)

    tiempo = request.args.get("tiempo", type=int)
    dificultad = request.args.get("dificultad")
    dieta = request.args.get("dieta")
    calorias = request.args.get("calorias", type=int)
    ingrediente = request.args.get("ingrediente")

    resultados = lista_recetas

    if tiempo:
        resultados = [r for r in resultados if r["tiempo"] <= tiempo]

    if dificultad and dificultad != "Selecciona":
        resultados = [r for r in resultados if r["dificultad"] == dificultad]

    if dieta and dieta != "Selecciona":
        resultados = [r for r in resultados if r["dieta"] == dieta]

    if calorias:
        resultados = [r for r in resultados if r["calorias"] <= calorias]

    if ingrediente:
        resultados = [
            r for r in resultados
            if ingrediente.lower() in r["ingrediente"].lower()
        ]

    return render_template("recetas.html", recetas=resultados)

@app.route("/receta")
def receta_detalle():

    nombre = request.args.get("nombre")

    if not nombre:
        return "Error: falta el parámetro 'nombre'", 400

    receta = next((r for r in lista_recetas if r["nombre"] == nombre), None)

    if receta is None:
        return "Receta no encontrada", 404

    return render_template("receta_detalle.html", receta=receta)




@app.route('/herramientas')
def herramientas():
    return render_template('herramientas.html')

@app.route('/inicia_sesion', methods=['GET', 'POST'])
def sesion():
    if request.method == 'POST':
        correo = request.form.get("correo").lower()  
        contraseña = request.form.get("contraseña") 
        usuario = usuarios_registrados.get(correo)  
        
        if usuario and usuario.get("contraseña") == contraseña:
            session["correo"] = correo 
            flash(f"Bienvenido {usuario.get('nombre')}!", "exito")  
            return redirect(url_for('inicio')) 
        else:
            flash("Correo o contraseña incorrectos", "danger")  
            return redirect(url_for('sesion'))  
    
    return render_template('login.html') 


@app.route('/logout')
def logout():
    session.pop("usuario", None)
    flash("Has cerrado sesión correctamente.", "exito")
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
    datos_finales = []
    totales = {
        "calorias": 0,
        "proteina": 0,
        "carbohidratos": 0,
        "grasas": 0
    }

    if request.method == 'POST':
        receta = request.form.get('receta', '').strip()

        if not receta:
            flash("Ingresa una receta válida.", "warning")
            return render_template('analizador.html')

        ingredientes = receta.split("\n")

        for ing in ingredientes:
            ing = ing.strip()
            if not ing:
                continue

            params = {"query": ing, "api_key": API_KEY}

            try:
                response = requests.get(USDA_SEARCH_URL, params=params)

                if response.status_code != 200:
                    continue

                datos = response.json()
                foods = datos.get("foods", [])

                if not foods:
                    datos_finales.append({
                        "nombre": ing,
                        "calorias": "No encontrado",
                        "proteina": "No encontrado",
                        "carbohidratos": "No encontrado",
                        "grasas": "No encontrado",
                    })
                    continue

                alimento = foods[0]
                nutrientes = alimento.get("foodNutrients", [])

                cal = pro = carb = fat = 0

                for n in nutrientes:
                    nombre = n.get("nutrientName", "").lower()
                    valor = n.get("value", 0)

                    if "energy" in nombre:
                        cal = valor
                    if "protein" in nombre:
                        pro = valor
                    if "carbohydrate" in nombre:
                        carb = valor
                    if "total lipid" in nombre or "fat" in nombre:
                        fat = valor

                datos_finales.append({
                    "nombre": ing,
                    "calorias": cal,
                    "proteina": pro,
                    "carbohidratos": carb,
                    "grasas": fat
                })

                totales["calorias"] += cal
                totales["proteina"] += pro
                totales["carbohidratos"] += carb
                totales["grasas"] += fat

            except Exception:
                continue

        resultado = "Análisis completado"

    return render_template(
        'analizador.html',
        resultado=resultado,
        datos_finales=datos_finales,
        totales=totales
    )


if __name__ == '__main__':
    app.run(debug=True)


