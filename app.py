from flask import Flask, render_template

app = Flask(__name__)

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


diccionario_datos = {
    "nombre": {
        "tipo": "Texto (string)",
        "descripcion": "Nombre del usuario",
        "obligatorio": True
    },
    "apellidos": {
        "tipo": "Texto (string)",
        "descripcion": "Apellidos del usuario",
        "obligatorio": True
    },
    "edad": {
        "tipo": "Entero (int)",
        "descripcion": "Edad del usuario en años",
        "obligatorio": True
    },
    "sexo": {
        "tipo": "Texto (string)",
        "descripcion": "Sexo o identidad de género",
        "valores_permitidos": ["Femenino", "Masculino", "Otro"],
        "obligatorio": True
    },
    "peso": {
        "tipo": "Decimal (float)",
        "descripcion": "Peso corporal en kilogramos",
        "obligatorio": True
    },
    "altura": {
        "tipo": "Entero (int)",
        "descripcion": "Altura del usuario en centímetros",
        "obligatorio": True
    },
    "nivel_actividad": {
        "tipo": "Texto (string)",
        "descripcion": "Nivel de actividad física diaria",
        "valores_permitidos": ["Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"],
        "obligatorio": True
    },
    "email": {
        "tipo": "Texto (string)",
        "descripcion": "Correo electrónico del usuario",
        "obligatorio": True
    },
    "password": {
        "tipo": "Texto (string, encriptado)",
        "descripcion": "Contraseña del usuario",
        "obligatorio": True
    },
    "objetivo": {
        "tipo": "Texto (string)",
        "descripcion": "Meta nutricional principal",
        "valores_permitidos": [
            "Bajar de peso",
            "Ganar masa muscular",
            "Mantener peso",
            "Mejorar digestión",
            "Controlar una condición"
        ],
        "obligatorio": True
    },
    "alergias": {
        "tipo": "Texto (string)",
        "descripcion": "Alergias o intolerancias alimentarias",
        "obligatorio": False
    },
    "dieta_preferencia": {
        "tipo": "Texto (string)",
        "descripcion": "Tipo de dieta o preferencia alimentaria",
        "valores_permitidos": [
            "Sin preferencia",
            "Vegana",
            "Vegetariana",
            "Keto",
            "Mediterránea"
        ],
        "obligatorio": False
    },
    "alimentos_no_gustan": {
        "tipo": "Texto (string)",
        "descripcion": "Lista de alimentos que no le gustan al usuario",
        "obligatorio": False
    },
    "nivel_experiencia": {
        "tipo": "Texto (string)",
        "descripcion": "Nivel de habilidad culinaria del usuario",
        "valores_permitidos": ["Principiante", "Intermedio", "Chef aficionado"],
        "obligatorio": True
    }
}

if __name__ == '__main__':
    app.run(debug=True)