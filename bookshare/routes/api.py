from datetime import date
from flask import Blueprint, current_app, jsonify, request
from bookshare.services.api_client import ApiClient
from bookshare.services.memory_store import store

api_bp = Blueprint('api', __name__)
def client(): return ApiClient(current_app.config['API_BASE_URL'], current_app.config['USE_MOCKS'])
def body(): return request.get_json(silent=True) or {}

@api_bp.post('/usuarios/login')
def login(): return jsonify(client().login(body().get('correo', 'ana@correo.edu'), body().get('contrasena', '')))
@api_bp.get('/usuarios/<int:user_id>')
def profile(user_id):
    user = store.user(user_id); return (jsonify(user), 200) if user else (jsonify({'error': 'Usuario no encontrado'}), 404)
@api_bp.get('/busqueda')
def search():
    result = client().search_books(request.args.get('titulo', ''), request.args.get('categoria', '')); return jsonify({'resultados': result, 'total': len(result)})
@api_bp.get('/catalogo/<int:book_id>')
def detail(book_id):
    book = client().book_detail(book_id); return (jsonify(book), 200) if book else (jsonify({'error': 'Libro no encontrado'}), 404)
@api_bp.get('/catalogo')
def catalog(): return jsonify({'resultados': store.books, 'total': len(store.books)})
@api_bp.post('/solicitudes')
def create_request():
    result = client().create_request(body().get('usuario_id', 25), body().get('libro_id')); return (jsonify(result), 201) if result else (jsonify({'error': 'Libro no encontrado'}), 404)
@api_bp.get('/solicitudes')
def requests():
    uid = request.args.get('usuario_id', type=int); rows = [r for r in store.requests if not uid or r['usuario_id'] == uid]; return jsonify({'resultados': store.enrich(rows), 'total': len(rows)})
@api_bp.post('/prestamos')
def create_loan():
    data = body(); req = next((r for r in store.requests if r['solicitud_id'] == data.get('solicitud_id')), None)
    if not req or req['estado'] != 'aceptada': return jsonify({'error': 'La solicitud debe estar aceptada'}), 400
    loan = {'prestamo_id': store.next_id('loan'), 'solicitud_id': req['solicitud_id'], 'usuario_id': req['usuario_id'], 'libro_id': req['libro_id'], 'estado': 'activo', 'fecha_inicio': str(date.today()), 'fecha_devolucion': None}; store.loans.append(loan); return jsonify(loan), 201
@api_bp.get('/prestamos')
def loans():
    uid = request.args.get('usuario_id', type=int); rows = [r for r in store.loans if not uid or r['usuario_id'] == uid]; return jsonify({'resultados': store.enrich(rows), 'total': len(rows)})
@api_bp.post('/prestamos/<int:loan_id>/devolucion')
def return_loan(loan_id):
    loan = next((r for r in store.loans if r['prestamo_id'] == loan_id), None)
    if not loan: return jsonify({'error': 'Préstamo no encontrado'}), 404
    loan.update(estado='devuelto', fecha_devolucion=str(date.today())); return jsonify(loan)
@api_bp.get('/valoraciones')
def ratings():
    bid = request.args.get('libro_id', type=int); return jsonify({'resultados': [r for r in store.ratings if not bid or r['libro_id'] == bid]})
@api_bp.post('/valoraciones')
def create_rating():
    data = body(); row = {'valoracion_id': store.next_id('rating'), **{k: data.get(k) for k in ('usuario_id', 'libro_id', 'calificacion', 'comentario')}}; store.ratings.append(row); return jsonify(row), 201
@api_bp.get('/chat/conversaciones/<int:conversation_id>/mensajes')
def messages(conversation_id): return jsonify({'resultados': store.conversations.get(conversation_id, [])})
@api_bp.post('/chat/conversaciones/<int:conversation_id>/mensajes')
def send_message(conversation_id):
    data = body(); row = {'mensaje_id': store.next_id('message'), 'conversacion_id': conversation_id, 'usuario_id': data.get('usuario_id', 25), 'texto': data.get('texto', ''), 'fecha': str(date.today())}; store.conversations.setdefault(conversation_id, []).append(row); return jsonify(row), 201
@api_bp.get('/health')
def health(): return jsonify(client().health())
