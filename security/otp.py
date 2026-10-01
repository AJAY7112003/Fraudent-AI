import secrets
import time


otp_store = {}


def generate_otp(transaction_id):

    otp = str(
        secrets.randbelow(900000) + 100000
    )

    otp_store[transaction_id] = {
        "otp": otp,
        "created_at": time.time(),
        "attempts": 0
    }

    return otp


def verify_otp(
    transaction_id,
    entered_otp
):

    data = otp_store.get(
        transaction_id
    )

    if not data:
        return False

    # OTP expires after 5 minutes

    if time.time() - data["created_at"] > 300:

        del otp_store[transaction_id]

        return False

    if data["attempts"] >= 3:
        return False

    data["attempts"] += 1

    if data["otp"] == entered_otp:

        del otp_store[transaction_id]

        return True

    return False