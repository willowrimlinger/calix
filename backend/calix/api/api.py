from flask import Blueprint, request
from flask_parameter_validation import ValidateParameters, Route

from calix.api.utils import resp_not_found


api = Blueprint("api", __name__, url_prefix="/api")

# api.register_blueprint(api_v1)

@api.route("/<path:path>", methods=["GET", "POST", "DELETE"])
@ValidateParameters()
def api_not_found(path: str = Route(comment="Any /api route that is not defined")):
    """API Catch-all for undefined routes, returns status code 404"""
    return resp_not_found(f"Invalid Route: {request.method} /api/{path}")
