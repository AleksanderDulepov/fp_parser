import os
from flask_restx import Api, Resource
from flask import Flask, request
from config import Config
from service import Service

app = Flask(__name__)
app.config.from_object(Config())
app.app_context().push()

api = Api(app)
query_ns = api.namespace("perform_query")

@query_ns.route("/")
class QueryView(Resource):
    def post(self):
        input_dict = request.json
        file_name = input_dict.get("file_name")

        if file_name is None or not os.path.exists(os.path.join(app.config["DATA_DIR"], file_name)):
            return "Reading file error", 400

        #количество переданных команд query запросов
        count_comands = int((len(input_dict) - 1) / 2)

        def generator(file_name):
            with open(os.path.join(app.config["DATA_DIR"], file_name), "r", encoding="utf-8") as file:
                for line in file:
                    yield line

        result = generator(file_name)

        #цикл по всем переданным командам
        for i in range(1, count_comands + 1):
            cmd_name = input_dict.get(f"cmd{i}", "")
            cmd_value = input_dict.get(f"value{i}", "")
            if cmd_name == "filter":
                result = Service.get_filter(result, cmd_value)
            if cmd_name == "map":
                result = Service.get_map(result, cmd_value)
            if cmd_name == "unique":
                result = Service.get_unique(result)
            if cmd_name == "sort":
                result = Service.get_sort(result, cmd_value)
            if cmd_name == "limit":
                result = Service.get_limit(result, cmd_value)

        return app.response_class("\n".join(list(result)), content_type="text/plain")


if __name__ == "__main__":
    app.run()
