from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app import db
from app.models import Usuario, Producto

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor complete todos los campos', 'error')
            return render_template('login.html')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and check_password_hash(usuario.password, password):
            session['user_id'] = usuario.id
            session['username'] = usuario.username
            flash(f'Bienvenido {usuario.username}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Credenciales inválidas', 'error')
            return render_template('login.html')
    
    return render_template('login.html')


@main.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('main.login'))


@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    total_productos = Producto.query.count()
    return render_template('dashboard.html', 
                         username=session.get('username'),
                         total_productos=total_productos)


@main.route('/productos')
def listar_productos():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)


@main.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        cantidad = request.form.get('cantidad')
        
        if not nombre or not precio or not cantidad:
            flash('Todos los campos son obligatorios', 'error')
            return render_template('crear_producto.html')
        
        try:
            precio = float(precio)
            cantidad = int(cantidad)
            
            if precio < 0:
                flash('El precio no puede ser negativo', 'error')
                return render_template('crear_producto.html')
            
            if cantidad < 0:
                flash('La cantidad no puede ser negativa', 'error')
                return render_template('crear_producto.html')
            
            if Producto.query.filter_by(nombre=nombre).first():
                flash('Ya existe un producto con ese nombre', 'error')
                return render_template('crear_producto.html')
            
            producto = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
            db.session.add(producto)
            db.session.commit()
            
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('main.listar_productos'))
            
        except ValueError:
            flash('Precio y cantidad deben ser valores numéricos', 'error')
            return render_template('crear_producto.html')
    
    return render_template('crear_producto.html')


@main.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    producto = Producto.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        cantidad = request.form.get('cantidad')
        
        if not nombre or not precio or not cantidad:
            flash('Todos los campos son obligatorios', 'error')
            return render_template('editar_producto.html', producto=producto)
        
        try:
            precio = float(precio)
            cantidad = int(cantidad)
            
            if precio < 0 or cantidad < 0:
                flash('Precio y cantidad deben ser positivos', 'error')
                return render_template('editar_producto.html', producto=producto)
            
            producto_existente = Producto.query.filter_by(nombre=nombre).first()
            if producto_existente and producto_existente.id != id:
                flash('Ya existe otro producto con ese nombre', 'error')
                return render_template('editar_producto.html', producto=producto)
            
            producto.nombre = nombre
            producto.precio = precio
            producto.cantidad = cantidad
            db.session.commit()
            
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('main.listar_productos'))
            
        except ValueError:
            flash('Precio y cantidad deben ser valores numéricos', 'error')
            return render_template('editar_producto.html', producto=producto)
    
    return render_template('editar_producto.html', producto=producto)


@main.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('main.listar_productos'))