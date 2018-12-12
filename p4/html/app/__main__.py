# Para ejecutar sin Apache/mod_wsgi, en directorio con .wsgi:
# PYTHONPATH=. python -m app

from app import app

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)

