from datetime import date
from bookshare.services.memory_store import store

class ApiClient:
    """Capa reemplazable por un cliente HTTP cuando exista el API Gateway."""
    def __init__(self, base_url='', use_mocks=True): self.base_url, self.use_mocks = base_url, use_mocks
    def login(self, email, password):
        user = next((u for u in store.users.values() if u['correo'] == email), None)
        return {**(user or {'usuario_id': 25, 'nombre': 'Ana García', 'correo': email}), 'token': 'mock-token'}
    def search_books(self, title='', category=''):
        q = f'{title} {category}'.strip().lower()
        return [b for b in store.books if not q or q in f"{b['titulo']} {b['autor']} {b['categoria']}".lower()]
    def book_detail(self, book_id): return store.book(book_id)
    def create_request(self, user_id, book_id):
        if not store.book(book_id): return None
        row = {'solicitud_id': store.next_id('request'), 'usuario_id': user_id, 'libro_id': book_id, 'estado': 'pendiente', 'fecha_solicitud': str(date.today())}
        store.requests.append(row); return row
    def health(self): return {'status': 'ok', 'mode': 'memory' if self.use_mocks else 'gateway'}
