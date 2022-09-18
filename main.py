from flask_restx import Api
from flask import Flask
from config import Config
from view import query_ns


def create_app(config: Config) -> Flask:
    appliction = Flask(__name__)
    appliction.config.from_object(config)
    appliction.app_context().push()

    return appliction


def configure_app(application_: Flask) -> None:
    api = Api(application_)
    api.add_namespace(query_ns)


if __name__ == "__main__":
    app_config: Config = Config()
    app = create_app(app_config)
    configure_app(app)
    app.run()
