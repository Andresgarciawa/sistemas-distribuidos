from datetime import date
from itertools import count

class MemoryStore:
    def __init__(self):
        self.users = {25: {'usuario_id': 25, 'nombre': 'Ana García', 'correo': 'ana@correo.edu', 'calificacion_promedio': 4.8}}
        self.books = [
            {'libro_id': 87, 'titulo': 'Sistemas Distribuidos', 'autor': 'A. Tanenbaum', 'propietario_id': 12, 'disponible': True, 'categoria': 'Ingeniería'},
            {'libro_id': 88, 'titulo': 'Clean Code', 'autor': 'Robert C. Martin', 'propietario_id': 12, 'disponible': True, 'categoria': 'Programación'},
            {'libro_id': 89, 'titulo': 'El principito', 'autor': 'Antoine de Saint-Exupéry', 'propietario_id': 13, 'disponible': False, 'categoria': 'Literatura'},
            {'libro_id': 90, 'titulo': 'Inteligencia emocional', 'autor': 'Daniel Goleman', 'propietario_id': 14, 'disponible': True, 'categoria': 'Humanidades'}]
        self.requests = [{'solicitud_id': 340, 'usuario_id': 25, 'libro_id': 88, 'estado': 'aceptada', 'fecha_solicitud': '2026-09-28'}]
        self.loans = [{'prestamo_id': 88, 'solicitud_id': 340, 'usuario_id': 25, 'libro_id': 88, 'estado': 'activo', 'fecha_inicio': '2026-09-28', 'fecha_devolucion': None}]
        self.ratings = [{'valoracion_id': 1, 'usuario_id': 25, 'libro_id': 88, 'calificacion': 5, 'comentario': 'Excelente estado'}]
        self.conversations = {10: [{'mensaje_id': 512, 'conversacion_id': 10, 'usuario_id': 25, 'texto': '¿A qué hora te queda bien entregar el libro?', 'fecha': '2026-09-21'}]}
        self.ids = {k: count(v) for k, v in [('request', 341), ('loan', 89), ('rating', 2), ('message', 513)]}
    def book(self, book_id): return next((b for b in self.books if b['libro_id'] == book_id), None)
    def user(self, user_id): return self.users.get(user_id)
    def next_id(self, key): return next(self.ids[key])
    def enrich(self, rows): return [{**r, 'libro': self.book(r['libro_id'])} for r in rows]

store = MemoryStore()
