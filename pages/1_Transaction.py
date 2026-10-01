import streamlit as st
import uuid
from datetime import datetime

from streamlit_geolocation import streamlit_geolocation

from ml.predict import predict_transaction

from ml.risk_engine import (
    calculate_risk,
    get_risk_level,
    classify_transaction
)

from database.database import (
    save_transaction,
    get_mobile_number
)

from security.otp import generate_otp

from notifications.sms_service import send_sms

from location.location_service import (
    validate_location
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("💳 FraudNet AI - Transaction Analysis")


# ============================================================
# USER INPUT
# ============================================================

st.subheader("📝 Transaction Details")


sender_id = st.text_input(
    "Sender Account ID"
)


receiver_id = st.text_input(
    "Receiver Account ID"
)


amount = st.number_input(
    "Transaction Amount (₹)",
    min_value=1.0,
    step=100.0
)


transaction_type = st.selectbox(
    "Transaction Type",
    [
        "UPI",
        "Card",
        "Bank Transfer",
        "Wallet"
    ]
)


device_id = st.text_input(
    "Device ID"
)


# ============================================================
# AUTOMATIC LOCATION
# ============================================================

st.subheader("📍 Automatic Location")


location_data = streamlit_geolocation()


latitude = None
longitude = None
accuracy = None


if location_data:

    latitude = location_data.get("latitude")

    longitude = location_data.get("longitude")

    accuracy = location_data.get("accuracy")


    if latitude is not None and longitude is not None:

        if validate_location(
            latitude,
            longitude
        ):

            st.success(
                "✅ Location detected successfully."
            )

            st.write(
                "Latitude:",
                latitude
            )

            st.write(
                "Longitude:",
                longitude
            )

            st.write(
                "Accuracy:",
                accuracy
            )

        else:

            st.warning(
                "⚠️ Location could not be validated."
            )


# ============================================================
# ANALYZE TRANSACTION
# ============================================================

if st.button(
    "🔍 Analyze Transaction"
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not sender_id:

        st.error(
            "Please enter Sender Account ID."
        )

        st.stop()


    if not receiver_id:

        st.error(
            "Please enter Receiver Account ID."
        )

        st.stop()


    if not device_id:

        st.error(
            "Please enter Device ID."
        )

        st.stop()


    if latitude is None or longitude is None:

        st.warning(
            "Location is unavailable. "
            "Please allow location access."
        )

        st.stop()


    # ========================================================
    # AUTOMATIC TIME
    # ========================================================

    timestamp = datetime.now().isoformat()


    # ========================================================
    # TRANSACTION ID
    # ========================================================

    transaction_id = (
        "TXN-" +
        uuid.uuid4().hex[:8].upper()
    )


    st.info(
        f"🕒 Transaction Time: {timestamp}"
    )

    st.info(
        f"🆔 Transaction ID: {transaction_id}"
    )


    # ========================================================
    # PREPARE FEATURES FOR ML
    # ========================================================

    processed_features = {

        "amount":
            amount,

        "transaction_type":
            transaction_type,

        "device_id":
            device_id,

        "latitude":
            latitude,

        "longitude":
            longitude
    }


    # ========================================================
    # 16. COMPLETE DECISION ENGINE
    # ========================================================

    try:

        prediction = predict_transaction(
            processed_features
        )


        # ----------------------------------------------------
        # RISK SCORE
        # ----------------------------------------------------

        risk_score = calculate_risk(

            prediction[
                "xgb_probability"
            ],

            prediction[
                "is_anomaly"
            ]
        )


        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        risk_level = get_risk_level(
            risk_score
        )


        # ----------------------------------------------------
        # CLASSIFICATION
        # ----------------------------------------------------

        classification = classify_transaction(

            prediction[
                "xgb_probability"
            ],

            prediction[
                "is_anomaly"
            ],

            risk_score
        )


        # ----------------------------------------------------
        # FINAL STATUS
        # ----------------------------------------------------

        if risk_level == "LOW":

            status = "APPROVED"


        elif risk_level == "MEDIUM":

            status = "FLAGGED"


        else:

            status = "HOLD"


        # ====================================================
        # 17. HIGH-RISK SMS + OTP
        # ====================================================

        if risk_level == "HIGH":

            status = "HOLD"


            # ------------------------------------------------
            # GET ACCOUNT HOLDER MOBILE NUMBER
            # ------------------------------------------------

            mobile = get_mobile_number(
                sender_id
            )


            # ------------------------------------------------
            # SMS MESSAGE
            # ------------------------------------------------

            message = (

                f"FraudNet Alert: "

                f"High-risk transaction "

                f"{transaction_id} "

                f"of ₹{amount} detected. "

                f"Transaction is currently "
                f"on HOLD."
            )


            # ------------------------------------------------
            # SEND REAL SMS
            # ------------------------------------------------

            if mobile:

                try:

                    sms_id = send_sms(
                        mobile,
                        message
                    )

                    st.success(
                        "📱 SMS alert sent to "
                        "account holder."
                    )

                except Exception as sms_error:

                    st.error(
                        f"SMS sending failed: "
                        f"{sms_error}"
                    )

            else:

                st.warning(
                    "Mobile number not found "
                    "for this account."
                )


            # ------------------------------------------------
            # GENERATE OTP
            # ------------------------------------------------

            otp = generate_otp(
                transaction_id
            )


            st.warning(
                "⚠️ High-risk transaction "
                "detected."
            )

            st.info(
                "🔐 OTP verification is "
                "required before approval."
            )


            # ------------------------------------------------
            # DEVELOPMENT ONLY
            # ------------------------------------------------

            st.info(
                f"DEMO OTP: {otp}"
            )


        # ====================================================
        # DISPLAY FINAL RESULT
        # ====================================================

        st.subheader(
            "📊 Transaction Analysis Result"
        )


        st.write(
            "Transaction ID:",
            transaction_id
        )


        st.write(
            "XGBoost Fraud Probability:",
            prediction[
                "xgb_probability"
            ]
        )


        st.write(
            "Anomaly Detected:",
            prediction[
                "is_anomaly"
            ]
        )


        st.write(
            "Risk Score:",
            risk_score
        )


        st.write(
            "Risk Level:",
            risk_level
        )


        st.write(
            "Classification:",
            classification
        )


        # ====================================================
        # STATUS DISPLAY
        # ====================================================

        if status == "APPROVED":

            st.success(
                "✅ Transaction APPROVED"
            )


        elif status == "FLAGGED":

            st.warning(
                "⚠️ Transaction FLAGGED "
                "for review"
            )


        else:

            st.error(
                "🚨 Transaction ON HOLD"
            )


        # ====================================================
        # SAVE TRANSACTION
        # ====================================================

        data = {

            "transaction_id":
                transaction_id,

            "sender_id":
                sender_id,

            "receiver_id":
                receiver_id,

            "amount":
                amount,

            "transaction_type":
                transaction_type,

            "device_id":
                device_id,

            "latitude":
                latitude,

            "longitude":
                longitude,

            "location_accuracy":
                accuracy,

            "location_name":
                "Detected Location",

            "timestamp":
                timestamp,

            "xgb_probability":
                prediction[
                    "xgb_probability"
                ],

            "xgb_prediction":
                prediction.get(
                    "xgb_prediction"
                ),

            "anomaly_score":
                prediction.get(
                    "anomaly_score"
                ),

            "anomaly_prediction":
                prediction.get(
                    "anomaly_prediction"
                ),

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "classification":
                classification,

            "status":
                status
        }


        save_transaction(
            data
        )


        st.success(
            f"Transaction {transaction_id} "
            f"saved successfully."
        )


    except Exception as error:

        st.error(
            "Transaction analysis failed."
        )

        st.exception(error)