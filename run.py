from app import create_app

app = create_app()

if __name__ == "__main__":
    from app.config import HOST, PORT, DEBUG
    app.run(host=HOST, port=PORT, debug=DEBUG)
