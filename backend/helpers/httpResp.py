httpResponses = {
    "success-resp": {
        200: "Success",
        201: "Created"
    },
    "error-resp": {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        409: "Conflict",
        500: "Internal Server Error"
    }
}

def success(httpCode, message):
    type = "success-resp"
    return {
        "code": httpCode,
        "response": httpResponses[type][httpCode],
        "message": message
    }

def error(httpCode, message):
    type = "error-resp"
    return {
        "code": httpCode,
        "response": httpResponses[type][httpCode],
        "message": message
    }