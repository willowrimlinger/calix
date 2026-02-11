from flask import Blueprint
from flask_parameter_validation import ValidateParameters
from flask_parameter_validation.parameter_types import Json, Route

from calix.api.utils import resp_bad_request, resp_id_not_found, resp_success
from calix.models.label import Label, is_valid_hex_alpha

label_api = Blueprint("label", __name__, url_prefix="/label")


@label_api.post("/")
@ValidateParameters()
def create(
    name: str = Json(),
    color: str = Json(),
):
    if not is_valid_hex_alpha(color):
        return resp_bad_request(
            f"{color} is not a valid hex with alpha color (#RRGGBBAA)"
        )

    label = Label(name, color)

    return resp_success(label)


@label_api.get("/<int:id>")
@ValidateParameters()
def get(id: int = Route()):
    label = Label.get_by_id(id)
    if not label:
        return resp_id_not_found("Label", id)

    return label.to_dict()


@label_api.put("/<int:id>")
@ValidateParameters()
def update(id: int = Route(), name: str = Json(), color: str = Json()):
    label = Label.get_by_id(id)
    if not label:
        return resp_id_not_found("Label", id)

    label.update(name, color)

    return label.to_dict()


@label_api.delete("/<int:id>")
@ValidateParameters()
def delete(id: int = Route()):
    label = Label.get_by_id(id)
    if not label:
        return resp_id_not_found("Label", id)

    label.delete()

    return resp_success()
