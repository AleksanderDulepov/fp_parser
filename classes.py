import re
from dataclasses import dataclass, field
from typing import Iterable, List, Callable
from marshmallow import validate


class CMD_available_storage():
    cmd_list:List = ["regex", "filter", "map", "unique", "sort", "limit"]

    @staticmethod
    def get_reg_exp(iter_object: Iterable[str], value: str) -> Iterable[str]:
        regexp = re.compile(value)
        for i in iter_object:
            if regexp.match(i) is not None:
                yield i

    @staticmethod
    def get_filter(iter_object: Iterable[str], value: str) -> Iterable[str]:
        return filter(lambda x: value in x, iter_object)

    @staticmethod
    def get_map(iter_object: Iterable[str], value: str) -> Iterable[str]:
        return map(lambda x: x.split()[int(value)], iter_object)

    @staticmethod
    def get_unique(iter_object: Iterable[str]) -> Iterable[str]:
        return set(iter_object)

    @staticmethod
    def get_sort(iter_object: Iterable[str], value: str) -> Iterable[str]:
        return sorted(iter_object, reverse=True if value == "desc" else False)

    @staticmethod
    def get_limit(iter_object: Iterable[str], value: str) -> Iterable[str]:
        counter: int = 0
        for i in iter_object:
            if counter < int(value):
                counter += 1
                yield i

    regex: Callable[[Iterable[str], str], Iterable[str]] = get_reg_exp
    filter: Callable[[Iterable[str], str], Iterable[str]] = get_filter
    map: Callable[[Iterable[str], str], Iterable[str]] = get_map
    unique: Callable[[Iterable[str]], Iterable[str]] = get_unique
    sort: Callable[[Iterable[str], str], Iterable[str]] = get_sort
    limit: Callable[[Iterable[str], str], Iterable[str]] = get_limit


@dataclass
class Query_item:
    cmd: str =field(metadata=dict(required=True, validate=validate.OneOf(CMD_available_storage.cmd_list)))
    value: str = field(metadata=dict(required=True))

@dataclass
class Query:
    query: List[Query_item]
    file_name: str
