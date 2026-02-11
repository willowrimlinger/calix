from flask import Blueprint

from calix.api.event import event_api

api_v1 = Blueprint("v1", __name__, url_prefix="/v1")

api_v1.register_blueprint(event_api)
