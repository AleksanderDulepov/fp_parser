import json
import os
from typing import Iterable, Dict, Optional, Any, Mapping

import marshmallow_dataclass
from flask import request, current_app, Response
from flask_restx import Namespace
from flask_restx import Resource
from marshmallow import ValidationError

from classes import Query, CMD_available_storage

query_ns = Namespace("perform_query")


@query_ns.route("/")
class QueryView(Resource):

    def post(self) -> Response:
        data:Any = request.json

        # валидация входных параметров
        QuerySchema = marshmallow_dataclass.class_schema(Query)
        try:
            query_instance: Query = QuerySchema().load(data)
        except ValidationError:
            return current_app.response_class(f"There is unknown command", status=400)

        file_name: str = query_instance.file_name
        if file_name is None or not os.path.exists(os.path.join(current_app.config["DATA_DIR"], file_name)):
            return current_app.response_class("Reading file error", status=400)

        def generator(file_name: str) -> Iterable[str]:
            with open(os.path.join(current_app.config["DATA_DIR"], file_name), "r", encoding="utf-8") as file:
                for line in file:
                    yield line

        result: Iterable[str] = generator(file_name)

        # цикл по всем переданным командам
        for query_item in query_instance.query:
            result = getattr(CMD_available_storage, query_item.cmd)(iter_object=result,
                                                                    value=query_item.value)
        try:
            return current_app.response_class("\n".join(list(result)), content_type="text/plain")
        except ValueError:
            return current_app.response_class("There is unexpected value", status=400)
