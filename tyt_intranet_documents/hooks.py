
import logging 

_logger = logging.getLogger(__name__)

def post_init_hook(env):
    
    folders = env['documents.document'].search([
        ('type', '=', 'folder'),
        ('name', 'in', [
            'Documentos Intranet',
            'Vida y Estilo',
            'Revistas',
            'Libros',
            'Autocuidado',
            'Cine Y Espectáculos',
            'Tecnología',
            'Salud mental',
            'Nutrición',
            'Mindfulness',
            'IDEAS QUE INSPIRAN',
            'LECTURA LIGERA',
            'Deportes',
            'Moda',
            'Negocios',
            'CREATIVIDAD Y CULTURA',
            'TENDENCIAS Y FUTURO',
            'Desarrollo profesional',
            'Liderazgo',
            'Idiomas',
            'Finanzas',
            'Desarrollo personal',
            'Ciencia',
            'LITERATURA',
            'BIENESTAR Y SALUD MENTAL',
            'Ficción',
            'Poemas',
            'Novelas',
            'Historia y cultura',
            'Innovación',
            'Arte',
            'COMICS',
        ])
    ])
    _logger.info(f"Updating {len(folders)} folders intranet")
    folders.write({'is_intranet_folder': True})
