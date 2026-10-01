import streamlit as st

from security.otp import verify_otp

st.title("🔐 Transaction Verification")

transaction_id = st.text_input(
    "Transaction ID"
)

entered_otp = st.text_input(
    "Enter OTP",
    type="password"
)

if st.button("Verify OTP"):

    result = verify_otp(
        transaction_id,
        entered_otp
    )

    if result:

        st.success(
            "OTP verified successfully."
        )

        st.info(
            "Proceed to iris authentication."
        )

    else:

        st.error(
            "OTP verification failed."
        )

        st.warning(
            "Transaction should be blocked."
        )