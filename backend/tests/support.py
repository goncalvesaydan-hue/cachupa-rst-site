"""Shared helpers for backend tests (standard library only)."""
import copy
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
ROOT = BACKEND.parent
SRC = BACKEND / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

PAGE_KEYS = ('home', 'house', 'gallery', 'reservations', 'contacts', 'privacy', 'notFound')


def page(title='Página', **extra):
    data = {'title': title, 'description': 'Descrição.', 'heading': 'Cabeçalho.',
            'intro': None, 'heroImageId': None, 'sections': []}
    data.update(extra)
    return data


def complete_source():
    """Editorial source (legacy format) with every production field filled.
    Example values only; never published."""
    return copy.deepcopy({
        'name': 'Cachupa Rst',
        'preview': True,
        'restaurant': {
            'city': 'Cidade Exemplo',
            'address': 'Rua Exemplo, 1',
            'phone': '+351 210 000 000',
            'whatsappNumber': '+351 910 000 000',
            'whatsappMessage': 'Olá! Mesa para 2 & café?',
            'email': 'reservas@example.com',
            'emailSubject': 'Pedido de reserva',
            'directionsUrl': 'https://maps.example.com/cachupa',
            'hours': [
                {'day': 1, 'closed': True, 'intervals': [], 'note': None},
                {'day': 5, 'closed': False, 'note': 'Cozinha fecha mais cedo',
                 'intervals': [{'opens': '19:00', 'closes': '01:00', 'closesNextDay': True}]},
            ],
        },
        'artist': {'name': None, 'bio': None},
        'artworks': [],
        'pages': {key: page(key.capitalize()) for key in PAGE_KEYS},
    })

