from django.core.management.base import BaseCommand
from decimal import Decimal

from Ecuacion_lineal_app.models import CategoriaProducto, Producto


class Command(BaseCommand):
    help = 'Crea productos de ejemplo (café, sándwich, torta_chocolate, jugo_naranja, ensalada) si no existen'

    def handle(self, *args, **options):
        categorias = {
            'Bebidas': ['Café', 'Jugo Naranja'],
            'Comidas': ['Sándwich', 'Ensalada'],
            'Postres': ['Torta Chocolate']
        }

        created_count = 0

        for cat_name, productos in categorias.items():
            categoria, _ = CategoriaProducto.objects.get_or_create(nombre=cat_name, defaults={'descripcion': f'Categoría {cat_name}'})

            for nombre in productos:
                # Evitar duplicados por nombre exacto
                prod, created = Producto.objects.get_or_create(
                    nombre=nombre,
                    defaults={
                        'descripcion': f'{nombre} delicioso y fresco.',
                        'precio': Decimal('5.00') if cat_name == 'Bebidas' else Decimal('7.50'),
                        'categoria': categoria,
                        'disponible': True,
                        'stock': 50
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Producto creado: {prod.nombre}'))

        if created_count == 0:
            self.stdout.write('No se crearon productos. Ya existen productos con esos nombres.')
        else:
            self.stdout.write(self.style.SUCCESS(f'{created_count} productos de ejemplo creados.'))
