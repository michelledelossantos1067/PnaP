import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app import db
from app.models import Usuario, Producto

@click.command('init-db')
@with_appcontext
def init_db():
    db.create_all()
    
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        
        productos_prueba = [
            Producto(nombre='Laptop HP', precio=899.99, cantidad=10),
            Producto(nombre='Mouse Logitech', precio=25.50, cantidad=50),
            Producto(nombre='Teclado Mecánico', precio=75.00, cantidad=30),
        ]
        
        for producto in productos_prueba:
            db.session.add(producto)
        
        db.session.commit()
        click.echo('Base de datos inicializada con éxito!')
        click.echo('Usuario creado: admin / admin123')
        click.echo(f'{len(productos_prueba)} productos de prueba agregados')
    else:
        click.echo('La base de datos ya está inicializada.')
        click.echo('Si deseas reiniciarla, elimina el archivo productos.db')