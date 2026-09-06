import streamlit as st
import pandas as pd
from pathlib import Path
from google import genai


# =========================================================
# 1. LOAD DATA
# =========================================================

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data" / "cleaned"

features = pd.read_csv(
    DATA_PATH / "customer_features.csv"
)

risk = pd.read_csv(
    DATA_PATH / "customer_churn_risk.csv"
)

feedback = pd.read_csv(
    DATA_PATH / "customer_feedback.csv"
)

churn = pd.read_csv(
    DATA_PATH / "churn_labels.csv"
)


# Combine customer features with churn risk
ai_data = features.merge(
    risk,
    on="customer_id",
    how="left"
)


# =========================================================
# 2. GEMINI CONNECTION
# =========================================================

# For the portfolio demo, enter your Gemini API key
# when the application starts.
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    gemini_client = genai.Client(
        api_key=api_key
    )
else:
    gemini_client = None


# =========================================================
# 3. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Netflix Customer Intelligence Copilot",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Netflix Customer Intelligence Copilot")

st.caption(
    "Data-driven customer analytics, churn risk and AI-powered retention insights"
)


# =========================================================
# 4. CUSTOMER SEARCH
# =========================================================

st.sidebar.header("Customer Search")

customer_id = st.sidebar.text_input(
    "Customer ID",
    value="CUST000744"
)


customer = ai_data[
    ai_data["customer_id"] == customer_id
]


if customer.empty:

    st.error(
        "Customer not found. Please enter a valid Customer ID."
    )

    st.stop()


c = customer.iloc[0]


# =========================================================
# 5. CUSTOMER OVERVIEW
# =========================================================

st.header(
    f"Customer Intelligence: {customer_id}"
)

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Plan",
    str(c["current_plan"])
)

col2.metric(
    "Watch Time",
    f"{c['total_watch_time_minutes']:.0f} min"
)

col3.metric(
    "Sessions",
    f"{c['total_viewing_sessions']:.0f}"
)

col4.metric(
    "Churn Risk",
    str(c["risk_level"])
    if pd.notna(c["risk_level"])
    else "Unavailable"
)


# =========================================================
# 6. CUSTOMER DETAILS
# =========================================================

st.subheader("📊 Customer Details")


details = pd.DataFrame({
    "Metric": [
        "Customer Segment",
        "Acquisition Channel",
        "Favorite Genre",
        "Completion Rate",
        "Average Rating",
        "Support Tickets",
        "Failed Payments",
        "Payment Failure Rate",
        "Subscription Count"
    ],

    "Value": [
        c["customer_segment"],
        c["acquisition_channel"],
        c["favorite_genre"],

        f"{c['average_completion_percentage']:.1f}%",

        (
            f"{c['average_rating']:.1f}"
            if pd.notna(c["average_rating"])
            else "No rating"
        ),

        int(c["support_ticket_count"]),
        int(c["failed_payment_count"]),
        f"{c['payment_failure_rate']:.1%}",
        int(c["subscription_count"])
    ]
})


st.dataframe(
    details,
    hide_index=True,
    use_container_width=True
)


# =========================================================
# 7. CHURN RISK
# =========================================================

st.subheader("⚠️ Churn Risk")


if pd.notna(c["churn_probability"]):

    probability = float(
        c["churn_probability"]
    )

    st.progress(
        min(probability, 1.0)
    )

    st.write(
        f"Model churn probability: **{probability:.1%}**"
    )

    st.caption(
        "This is a model risk score, not a certainty of churn."
    )

else:

    st.info(
        "Churn risk is unavailable for this customer."
    )


# =========================================================
# 8. RISK SIGNALS
# =========================================================

st.subheader("🔎 Risk Signals")


signals = []


if c["failed_payment_count"] > 0:

    signals.append(
        "Payment failures detected."
    )


if c["total_viewing_sessions"] < 5:

    signals.append(
        "Low viewing activity."
    )


if c["average_completion_percentage"] < 60:

    signals.append(
        "Low content completion."
    )


if c["support_ticket_count"] >= 2:

    signals.append(
        "Multiple support interactions."
    )


if (
    pd.notna(c["average_support_satisfaction"])
    and c["average_support_satisfaction"] < 3
):

    signals.append(
        "Low support satisfaction."
    )


if not signals:

    signals.append(
        "No major negative signal identified."
    )


for signal in signals:

    st.write(
        "•",
        signal
    )


# =========================================================
# 9. RETENTION RECOMMENDATIONS
# =========================================================

st.subheader("🎯 Retention Recommendations")


actions = []


if c["failed_payment_count"] > 0:

    actions.append(
        "Contact the customer about payment issues."
    )


if c["total_viewing_sessions"] < 5:

    actions.append(
        "Send personalized content recommendations."
    )


if c["average_completion_percentage"] < 60:

    actions.append(
        "Recommend shorter or highly relevant content."
    )


if (
    pd.notna(c["average_support_satisfaction"])
    and c["average_support_satisfaction"] < 3
):

    actions.append(
        "Prioritize a support follow-up."
    )


if not actions:

    actions.append(
        "Continue engagement monitoring and personalized recommendations."
    )


for action in actions:

    st.write(
        "✅",
        action
    )


# =========================================================
# 10. CUSTOMER FEEDBACK
# =========================================================

st.subheader("💬 Customer Feedback")


customer_feedback = feedback[
    feedback["customer_id"] == customer_id
]


if customer_feedback.empty:

    st.info(
        "No feedback available."
    )

else:

    for _, row in customer_feedback.iterrows():

       # Detect the sentiment column used in the cleaned dataset
            sentiment_column = next(
    (
        col for col in [
            "sentiment",
            "sentiment_label",
            "sentiment_score"
        ]
        if col in customer_feedback.columns
    ),
    None
)

for _, row in customer_feedback.iterrows():

    sentiment_value = (
        row[sentiment_column]
        if sentiment_column
        else "Not available"
    )

    st.write(
        f"**Rating:** {row['rating']} | "
        f"**Sentiment:** {sentiment_value}"
    )

    st.write(   
        row["feedback_text"]
    )

    st.divider()





# =========================================================
# 11. GEMINI AI COPILOT
# =========================================================

st.header("🤖 AI Customer Intelligence Copilot")


question = st.text_input(
    "Ask a question about this customer",
    placeholder="Why is this customer at risk?"
)


if st.button("Ask Copilot"):

    if not gemini_client:

        st.warning(
            "Enter your Gemini API key in the sidebar first."
        )

    elif not question:

        st.warning(
            "Please enter a question."
        )

    else:

        customer_context = c.to_dict()

        prompt = f"""
You are a Netflix Customer Intelligence Copilot.

Use ONLY the customer data provided below.

Do not invent facts.

CUSTOMER DATA:
{customer_context}

CUSTOMER FEEDBACK:
{customer_feedback["feedback_text"].tolist()}

USER QUESTION:
{question}
Give a concise, business-focused answer.

Important rules:
- Treat churn probability as a model risk score, NOT a certainty.
- Never say the customer will definitely churn.
- Do not claim that a feature caused churn.
- Clearly distinguish observed customer signals from your interpretation.
- Base explanations only on the provided customer data.
- Do not invent customer history, reasons, or events.
- If the data is insufficient, say so.
- Retention recommendations should be practical and clearly presented as suggestions.
"""

        try:

            response = gemini_client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            st.markdown(
                "### 💡 Copilot Answer"
            )

            st.write(
                response.text
            )

        except Exception as e:

            st.error(
                f"Gemini API error: {e}"
            )


# =========================================================
# 12. BUSINESS ANALYTICS
# =========================================================

st.header("📈 Business Intelligence")


plan_data = features[
    ["customer_id", "current_plan"]
].merge(
    churn[
        ["customer_id", "churn_date"]
    ],
    on="customer_id",
    how="left"
)

# A customer is considered churned when churn_date exists
plan_data["churn_flag"] = (
    plan_data["churn_date"].notna().astype(int)
)


plan_summary = (
    plan_data
    .groupby("current_plan")
    .agg(
        customers=("customer_id", "count"),
        churned_customers=("churn_flag", "sum")
    )
)


plan_summary["churn_rate"] = (
    plan_summary["churned_customers"]
    / plan_summary["customers"]
)


st.subheader("Churn by Plan")


st.dataframe(
    plan_summary.reset_index(),
    hide_index=True,
    use_container_width=True
)


# =========================================================
# 13. HIGH-RISK CUSTOMERS
# =========================================================

st.subheader("🚨 High-Risk Customers")


high_risk = ai_data[
    ai_data["risk_level"] == "High"
].copy()


high_risk = high_risk[
    [
        "customer_id",
        "current_plan",
        "failed_payment_count",
        "payment_failure_rate",
        "churn_probability",
        "risk_level"
    ]
].sort_values(
    "churn_probability",
    ascending=False
)


st.dataframe(
    high_risk.head(20),
    hide_index=True,
    use_container_width=True
)