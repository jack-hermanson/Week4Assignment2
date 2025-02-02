import dataclasses

from flask import Flask, request, jsonify, abort
from http import HTTPStatus
from uuid import uuid4
from datetime import datetime
from enum import IntEnum


class StatusCodeEnum(IntEnum):
    APPROVED = 100
    INSUFFICIENT_FUNDS = 501
    INVALID_ZIP_CODE = 502
    INVALID_SECURITY_CODE = 503


@dataclasses.dataclass
class AuthorizationRequest:
    """Represents a transaction that hasn't been authorized"""
    merchant_id: str
    timestamp: datetime
    card_number: str
    card_security_code: str
    zip_code: str
    amount: float
    name: str
    email: str

    # set by processor
    is_authorized: bool | None
    status_code: int | None
    authorization_number: str | None


def authorize_transaction(auth_request: AuthorizationRequest):
    """Determines if the transaction has been authorized"""
    auth_request.is_authorized = auth_request.amount < 500
    # If the customer tries to spend less than $500, they're okay.
    if auth_request.is_authorized:
        auth_request.authorization_number = str(uuid4())
        auth_request.status_code = StatusCodeEnum.APPROVED
    else:
        auth_request.status_code = StatusCodeEnum.INSUFFICIENT_FUNDS


app = Flask(__name__)


@app.route("/accept-payment", methods=["POST"])
def accept_payment():
    try:
        # Get headers in lowercase for case-insensitive comparison
        content_type = request.headers.get("Content-Type", "").lower()
        accept_header = request.headers.get("Accept", "").lower()

        # Make sure the client sent the data as form-encoded.
        if content_type != "application/x-www-form-urlencoded":
            return jsonify({
                "error": f"Expected 'Content-Type' to be 'application/x-www-form-urlencoded', got '{content_type}' "
                         f"instead"
            }), HTTPStatus.UNSUPPORTED_MEDIA_TYPE

        # Make sure the client accepts JSON responses.
        if "application/json" not in accept_header:  # Uses "in" because it could have others.
            return jsonify({
                "error": f"Expected 'Accept' header to include 'application/json', got '{accept_header}'"
            }), HTTPStatus.NOT_ACCEPTABLE

        # Pull out all the data we need.
        auth_request = AuthorizationRequest(
            merchant_id=request.form.get("merchant_id"),
            timestamp=datetime.fromisoformat(request.form.get("timestamp")),
            card_number=request.form.get("card_number"),
            card_security_code=request.form.get("card_security_code"),
            zip_code=request.form.get("zip_code"),
            amount=float(request.form.get("amount")),
            name=request.form.get("name"),
            email=request.form.get("email"),
            # set in authorize_transaction function
            is_authorized=None,
            status_code=None,
            authorization_number=None,
        )
        authorize_transaction(auth_request)
        return jsonify(auth_request)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


app.run(port=5040)
