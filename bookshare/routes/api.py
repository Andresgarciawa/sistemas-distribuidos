from flask import Blueprint, current_app, jsonify, request
from bookshare.services.api_client import ApiClient

api_bp = Blueprint('api', __name__)


def client():
    return ApiClient(current_app.config['API_BASE_URL'], current_app.config['USE_MOCKS'])


@api_bp.get('/busqueda')
def search():
    return jsonify({'resultados': client().search_books(request.args.get('titulo', ''), request.args.get('categoria', ''))})


@api_bp.get('/catalogo/<int:book_id>')
def detail(book_id):
    book = client().book_detail(book_id)
    return (jsonify(book), 200) if book else (jsonify({'error': 'Libro no encontrado'}), 404)


@api_bp.post('/solicitudes')
def create_request():
    data = request.get_json(silent=True) or {}
    return jsonify(client().create_request(data.get('usuario_id', 25), data.get('libro_id'))), 201


@api_bp.get('/health')
def health():
    return jsonify(client().health())
