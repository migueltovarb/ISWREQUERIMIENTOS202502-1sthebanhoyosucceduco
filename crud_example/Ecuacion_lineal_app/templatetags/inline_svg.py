from django import template
from django.contrib.staticfiles.finders import find
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def inline_svg(path):
    """Busca un archivo estático por su ruta relativa y devuelve su contenido SVG embebido.

    `path` debe ser la ruta relativa dentro de `static/`, por ejemplo
    `Ecuacion_lineal_app/img/productos/cafe.svg`.
    """
    if not path:
        return ''

    # find() buscará el archivo en los staticfiles dirs
    filepath = find(path)
    if not filepath:
        return ''

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return mark_safe(content)
    except Exception:
        return ''
