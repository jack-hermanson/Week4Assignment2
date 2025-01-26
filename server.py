import dataclasses

from flask import Flask, request, jsonify, abort
from http import HTTPStatus
from uuid import uuid4
from datetime import datetime


@dataclasses.dataclass
class AuthorizationRequest:
    """Represents a transaction that hasn't been authorized"""
    timestamp: datetime
    card_number: str
    card_security_code: str
    zip_code: str
    amount: float
    name: str
    email: str

    # set by processor
    is_authorized: bool
    authorization_code: str | None


def authorize_transaction(auth_request: AuthorizationRequest):
    """Determines if the transaction has been authorized"""
    auth_request.is_authorized = auth_request.amount < 500
    # If the customer tries to spend less than $500, they're okay.
    if auth_request.is_authorized:
        auth_request.authorization_code = str(uuid4())


app = Flask(__name__)


@app.route("/accept-payment", methods=["POST"])
def accept_payment():
    try:
        # Make sure the client is okay with JSON responses.
        if not request.headers.get("Accept") == "application/json":
            return jsonify({
                "error": f"Expected 'Accept' header to be application/json, "
                         f"got {request.headers.get('Accept')}"
            }), HTTPStatus.NOT_ACCEPTABLE

        # Pull out all the data we need.
        auth_request = AuthorizationRequest(
            timestamp=datetime.fromisoformat(request.form.get("timestamp")),
            card_number=request.form.get("card_number"),
            card_security_code=request.form.get("card_security_code"),
            zip_code=request.form.get("zip_code"),
            amount=float(request.form.get("amount")),
            name=request.form.get("name"),
            email=request.form.get("email"),
            is_authorized=False,
            authorization_code=None
        )
        authorize_transaction(auth_request)
        return jsonify(auth_request)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


app.run(port=5040)
