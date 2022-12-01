from config.app import create_app

if __name__ == "__main__":
    server = create_app()

    server.run(host="0.0.0.0")
