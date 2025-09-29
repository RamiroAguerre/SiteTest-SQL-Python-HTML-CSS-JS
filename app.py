from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__)
app.secret_key = "supersecreto"

# ----------------------
# Conexión a SQL Server
# ----------------------
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=localhost\SQLEXPRESS;'
    'DATABASE=MODELO_TRABAJO_PRACTICO;'
    'UID=sa;'
    'PWD=MiContraseña123;'
    'Encrypt=no;'
    'TrustServerCertificate=yes;'
)



cursor = conn.cursor()

# ----------------------
# Usuarios hardcodeados para demo
# ----------------------
usuarios = {
    "admin": {"password": "admin123", "role": "admin"},
    "usuario1": {"password": "pass123", "role": "user"}
}

# ----------------------
# Login
# ----------------------
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

# ----------------------
# Panel Usuario
# ----------------------
@app.route('/usuario')
def usuario_panel():
    if 'user' not in session or session['role'] != 'user':
        return redirect('/')

    # Traer productos con stock y nombre
    cursor.execute("""
        SELECT mp.PRODUCTO, i.CANTIDAD_DISPONIBLE
        FROM INVENTARIO i
        JOIN MAESTRO_PRODUCTO mp ON i.ID_PRODUCTO = mp.ID_PRODUCTO
    """)
    productos = cursor.fetchall()

    # Traer historial de compras del usuario (ejemplo para usuario1)
    cursor.execute("""
        SELECT op.ID_ORDEN_PEDIDO, op.FECHA, mp.PRODUCTO, opd.CANTIDAD, opd.PRECIO_UNIT
        FROM ORDEN_PEDIDO op
        JOIN ORDEN_PEDIDO_DETALLE opd ON op.ID_ORDEN_PEDIDO = opd.ID_ORDEN_PEDIDO
        JOIN MAESTRO_PRODUCTO mp ON opd.ID_PRODUCTO = mp.ID_PRODUCTO
        WHERE op.ID_USER = 1  -- Para demo, usuario1 ID=1
    """)
    historial = cursor.fetchall()

    return render_template('usuario.html', productos=productos, historial=historial)

# ----------------------
# Panel Admin
# ----------------------
@app.route('/admin')
def admin_panel():
    if 'user' not in session or session['role'] != 'admin':
        return redirect('/')

    # Traer clientes
    cursor.execute("SELECT ID_USER, NOMBRE, APELLIDO, CIUDAD FROM USUARIO")
    clientes = cursor.fetchall()

    # Traer stock de productos
    cursor.execute("""
        SELECT mp.PRODUCTO, i.CANTIDAD_DISPONIBLE
        FROM INVENTARIO i
        JOIN MAESTRO_PRODUCTO mp ON i.ID_PRODUCTO = mp.ID_PRODUCTO
    """)
    productos = cursor.fetchall()

    return render_template('admin.html', clientes=clientes, productos=productos)

# ----------------------
# Logout
# ----------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ----------------------
if __name__ == '__main__':
    app.run(debug=True)

