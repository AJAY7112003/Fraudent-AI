def suspicious_alert(
    amount,
    transaction_id
):

    return (
        f"FraudNet Alert: "
        f"Suspicious transaction of "
        f"Rs.{amount} detected. "
        f"Transaction ID: {transaction_id}. "
        f"Please verify."
    )


def hold_alert(
    amount,
    transaction_id
):

    return (
        f"FraudNet Alert: "
        f"High-risk transaction of "
        f"Rs.{amount} has been placed "
        f"on hold. "
        f"Transaction ID: {transaction_id}."
    )


def blocked_alert(
    amount,
    transaction_id
):

    return (
        f"FraudNet Alert: "
        f"Transaction of Rs.{amount} "
        f"has been blocked because "
        f"verification failed."
    )