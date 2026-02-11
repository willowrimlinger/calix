from datetime import date, datetime
from typing import TypedDict
from flask import Blueprint
from flask_parameter_validation import ValidateParameters
from flask_parameter_validation.parameter_types import Json, Route

from calix.api.utils import (
    resp_bad_request,
    resp_id_not_found,
    resp_not_found,
    resp_success,
)
from calix.models.event import Event
from calix.models.label import Label
from calix.models.recurrence import Recurrence, RecurrenceType

event_api = Blueprint("event", __name__, url_prefix="/event")


class RecurrenceIn(TypedDict):
    n: int
    type: RecurrenceType
    start_date: date
    end_date: date


@event_api.post("/")
@ValidateParameters()
def create(
    start: datetime = Json(),
    end: datetime = Json(),
    description: str = Json(),
    location: str = Json(),
    recurrence: RecurrenceIn | None = Json(),
    label_id: int = Json(),
):
    if start > end:
        return resp_bad_request("Start time cannot be after end time")
    label = Label.get_by_id(label_id)
    if not label:
        return resp_id_not_found("Label", label_id)

    recurrence_obj = None
    if recurrence:
        recurrence_obj = Recurrence(
            recurrence["n"],
            recurrence["type"],
            recurrence["start_date"],
            recurrence["end_date"],
        )

    event = Event(
        start,
        end,
        description,
        location,
        recurrence_obj,
        label,
    )

    return event.to_dict()


@event_api.get("/<int:id>")
@ValidateParameters()
def get(
    id: int = Route(),
):
    event = Event.get_by_id(id)
    if not event:
        return resp_id_not_found("Event", id)

    return event.to_dict()


@event_api.delete("/<int:id>")
@ValidateParameters()
def delete(
    id: int = Route(),
):
    event = Event.get_by_id(id)
    if not event:
        return resp_id_not_found("Event", id)

    event.delete()

    return resp_success()
