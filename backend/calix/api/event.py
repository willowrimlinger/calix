from datetime import date, datetime
from typing import NotRequired, TypedDict
from flask import Blueprint
from flask_parameter_validation import ValidateParameters
from flask_parameter_validation.parameter_types import Json, Query, Route

from calix.api.utils import (
    resp_bad_request,
    resp_id_not_found,
    resp_success,
)
from calix.models.event import Event
from calix.models.label import Label
from calix.models.recurrence import Recurrence, RecurrenceType

event_api = Blueprint("event", __name__, url_prefix="/event")


class RecurrenceIn(TypedDict):
    id: NotRequired[int]
    n: int
    type: RecurrenceType
    start_date: date
    end_date: date


@event_api.post("/")
@ValidateParameters()
def create(
    start: datetime = Json(comment="UTC"),
    end: datetime = Json(comment="UTC"),
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

    return resp_success(event.to_dict())


@event_api.get("/<int:id>")
@ValidateParameters()
def get(
    id: int = Route(),
):
    event = Event.get_by_id(id)
    if not event:
        return resp_id_not_found("Event", id)

    return resp_success(event.to_dict())


@event_api.get("/")
@ValidateParameters()
def get_range(
    start: datetime = Query(comment="UTC"), end: datetime = Query(comment="UTC")
):
    return resp_success(
        [event.to_dict() for event in Event.get_range(start, end)]
    )


@event_api.put("/<int:id>")
@ValidateParameters()
def update(
    start: datetime = Json(comment="UTC"),
    end: datetime = Json(comment="UTC"),
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
        if "id" in recurrence:
            recurrence_obj = Recurrence.get_by_id(recurrence["id"])
            if not recurrence_obj:
                return resp_id_not_found("Recurrence", recurrence["id"])
            recurrence_obj.update(
                recurrence["n"],
                recurrence["type"],
                recurrence["start_date"],
                recurrence["end_date"],
            )
        else:
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

    return resp_success(event.to_dict())


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
