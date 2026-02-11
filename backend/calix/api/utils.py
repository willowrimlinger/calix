from flask import jsonify


def resp_success(data: str | None = None, status: int = 200):
    if data is None:
        response = jsonify({"success": True})
        response.status_code = status
        return response
    response = jsonify({"success": True, "data": data})
    response.status_code = status
    return response


def resp_error(
    error_message: str | None = None, error_detail: str | None = None, status: int = 400
):
    result = {"success": False, "error": error_message, "error_detail": error_detail}
    response = jsonify(result)
    response.status_code = status
    return response


def resp_bad_request(error_detail: str | None = None):
    return resp_error("Bad request", error_detail, 400)


def resp_not_authorized(error_detail: str | None = None):
    return resp_error("Not Authorized", error_detail, 401)


def resp_forbidden(error_detail: str | None = None):
    return resp_error("Forbidden", error_detail, 403)


def resp_not_found(error_detail: str | None = None):
    return resp_error("Not Found", error_detail, 404)


def resp_internal_server_error(error_detail: str | None = None):
    return resp_error("Internal Server Error", error_detail, 500)
