from datetime import date, datetime
from typing import TypedDict
from flask import Blueprint
from flask_parameter_validation import ValidateParameters
from flask_parameter_validation.parameter_types import Json

from calix.models.recurrence import RecurrenceType


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
        recurrence: RecurrenceIn = Json(),
        label_id: int = Json(),
):
    if start > end:
        return resp_success
