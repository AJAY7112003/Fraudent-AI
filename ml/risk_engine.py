def calculate_risk(
    fraud_probability,
    is_anomaly
):

    score = fraud_probability * 70

    if is_anomaly:
        score += 30

    score = min(
        score,
        100
    )

    return score


def get_risk_level(score):

    if score < 40:
        return "LOW"

    elif score < 70:
        return "MEDIUM"

    else:
        return "HIGH"


def classify_transaction(
    fraud_probability,
    is_anomaly,
    risk_score
):

    if fraud_probability >= 0.80:

        return "FRAUDULENT"

    if (
        is_anomaly
        or risk_score >= 40
    ):

        return "SUSPICIOUS"

    return "NORMAL"