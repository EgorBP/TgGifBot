from dataclasses import dataclass


@dataclass()
class ResponseModel:
    data: dict
    code: int
