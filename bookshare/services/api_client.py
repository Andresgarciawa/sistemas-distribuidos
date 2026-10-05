"""Cliente del API Gateway.

Por ahora devuelve datos de demostración. Cuando exista el Gateway, este es el
único módulo que debe cambiarse para usar requests/httpx y Authorization Bearer.
"""
from datetime import date
from bookshare.models import Book


class ApiClient:
    def __init__(self, base_url: str, use_mocks: bool = True):
        self.base_url = base_url.rstrip('/')
        self.use_mocks = use_mocks
        self._books = [
            Book(87, 'Sistemas Distribuidos', 'A. Tanenbaum', True, 'Ingeniería'),
            Book(88, 'Clean Code', 'Robert C. Martin', True, 'Programación'),
            Book(89, 'El principito', 'Antoine de Saint-Exupéry', False, 'Literatura'),
            Book(90, 'Inteligencia emocional', 'Daniel Goleman', True, 'Humanidades'),
        ]

    def search_books(self, title='', category=''):
        query = f'{title} {category}'.strip().lower()
        return [b.to_dict() for b in self._books if not query or query in f'{b.titulo} {b.autor} {b.categoria}'.lower()]

    def book_detail(self, book_id):
        return next((b.to_dict() for b in self._books if b.libro_id == book_id), None)

    def create_request(self, user_id, book_id):
        return {'solicitud_id': 340, 'usuario_id': user_id, 'libro_id': book_id, 'estado': 'pendiente', 'fecha_solicitud': str(date.today())}

    def health(self):
        return {'status': 'ok', 'mode': 'mock' if self.use_mocks else 'gateway'}
