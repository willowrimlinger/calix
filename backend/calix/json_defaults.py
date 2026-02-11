import datetime
from decimal import Decimal
from typing import Any
import uuid


def json_defaults(obj: Any):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, Exception):
        return str(obj)
    raise TypeError("Type %s not serializable" % type(obj))
