from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__)
app.secret_key = "supersecreto"

# Conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=TU_SERVIDOR;'
    'DATABASE=TU_BASE_DE_DATOS;'
    'UID=TU_USUARIO;'
    'PWD=TU_CONTRASEÑA'
)
cursor = conn.cursor()

# Usuarios hardcodeados para demo
usuarios = {
    "admin": {"password": "admin123", "role": "admin"},
    "usuario1": {"password": "pass123", "role": "user"}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and usuarios[username]["password"] == password:
            session['user'] = username
            session['role'] = usuarios[username]["role"]
            if usuarios[username]["role"] == "admin":
                return redirect('/admin')
            else:
                return redirect('/usuario')
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('index.html')

# Panel usuario
@app.route('/usuario')
def usuario_panel():
    if 'user' not in session or session['role'] != 'user':
        return redirect('/')
    # Ejemplo: mostrar stock de productos
    cursor.execute("SELECT * FROM Stock")
    productos = cursor.fetchall()
    return render_template('usuario.html', productos=productos)

# Panel admin
@app.route('/admin')
def admin_panel():
    if 'user' not in session or session['role'] != 'admin':
        return redirect('/')
    # Ejemplo: mostrar clientes
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    return render_template('admin.html', clientes=clientes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
