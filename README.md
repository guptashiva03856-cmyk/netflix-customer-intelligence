# 🎬 Netflix Customer Intelligence Copilot

A data-driven customer intelligence platform that combines customer analytics, churn-risk prediction, customer feedback analysis, and Gemini-powered AI insights through an interactive Streamlit dashboard.

---

## 📌 Project Overview

The Netflix Customer Intelligence Copilot is designed to help a streaming business understand customer behavior, identify customers who may be at risk of churn, and provide actionable retention recommendations.

The system combines multiple customer data sources such as:

- Customer profiles
- Subscription history
- Viewing activity
- Payment history
- Support tickets
- Customer feedback
- Content information
- Churn labels

Machine learning is used to generate churn-risk scores, while Gemini provides natural-language explanations and business recommendations based on the available customer intelligence.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Analyze customer behavior and engagement.
2. Clean and prepare customer-related datasets.
3. Engineer customer-level features.
4. Analyze churn patterns.
5. Build a machine learning model for future churn-risk estimation.
6. Identify high-risk customers.
7. Analyze customer feedback and payment issues.
8. Generate retention recommendations.
9. Build an AI-powered customer intelligence copilot.
10. Provide an interactive Streamlit dashboard for business users.

---

## 🏗️ System Architecture

```text
                    Customer Data
                         │
                         ▼
               Data Quality Analysis
                         │
                         ▼
                   Data Cleaning
                         │
                         ▼
                Feature Engineering
                         │
                         ▼
                Customer Analytics
                         │
                         ▼
             Point-in-Time Churn Model
                         │
                         ▼
                Churn Risk Scoring
                         │
                         ▼
             Customer Intelligence Data
                    ┌────┴────┐
                    │         │
                    ▼         ▼
              Business     Gemini AI
              Analytics     Copilot
                    │         │
                    └────┬────┘
                         ▼
                Streamlit Dashboard
📁 Project Structure
 netflix-customer-intelligence/
│
├── app/
│   ├── components/
│   ├── pages/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── docs/
│   ├── Netflix_Database_Schema.docx
│   ├── Netflix_Dataset_Dictionary.docx
│   ├── Netflix_SQL_Business_Questions.docx
│   └── PRD_Netflix_Customer_Intelligence_Copilot.docx
│
├── models/
│   ├── churn_preprocessor.pkl
│   └── churn_random_forest.pkl
│
├── notebooks/
│   ├── 01_data_quality.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_customer_analytics.ipynb
│   ├── 05_churn_model.ipynb
│   └── 06_ai_copilot.ipynb
│
├── sql/
│
├── src/
│   ├── ai/
│   ├── analytics/
│   ├── data/
│   ├── database/
│   ├── models/
│   └── utils/
│
├── tests/
│
├── vector_store/
│
├── .gitignore
├── README.md
├── requirements.txt
└── run_app.py
📊 Datasets

The project uses nine datasets.

Dataset	Purpose
customers.csv	Customer demographic and acquisition information
subscriptions.csv	Customer subscription history
subscription_plans.csv	Subscription plan details
payments.csv	Payment transactions and payment status
viewing_activity.csv	Customer viewing behavior
content.csv	Content metadata such as genre
customer_feedback.csv	Customer ratings, feedback and sentiment
support_tickets.csv	Customer support interactions
churn_labels.csv	Historical churn information

The raw datasets are stored in:

data/raw/

Cleaned datasets are stored in:

data/cleaned/
🧹 Data Quality & Cleaning

Data quality was analyzed before performing feature engineering and modeling.

The cleaning process included:

Missing-value analysis
Duplicate detection
Data type validation
Date conversion
Categorical value normalization
Invalid date detection
Payment anomaly checks
Viewing activity validation
Customer ID validation
Structural missingness analysis
Important cleaning decisions

Not every missing value was automatically replaced.

For example, some subscription fields are naturally missing because a customer may still have an active subscription.

Similarly, support satisfaction can be missing when a customer has no resolved support interaction.

This prevents artificial information from being introduced into the dataset.

⚙️ Feature Engineering

Customer-level features were created by combining information from multiple datasets.

Important engineered features include:

Engagement
total_watch_time_minutes
total_viewing_sessions
average_completion_percentage
average_watch_time_per_session
unique_titles_watched
active_viewing_days
Feedback
average_rating
feedback_count
Support
support_ticket_count
average_support_satisfaction
has_support_satisfaction
Payments
successful_payment_count
total_successful_payment_amount
failed_payment_count
payment_failure_rate
has_failed_payment
Subscription
subscription_count
current_subscription_tenure_days
current_plan
has_plan_change
is_active_subscription
Content
favorite_genre
unique_genres_watched

These features were combined into a customer-level intelligence dataset.

📈 Customer Analytics

The analytics stage was used to understand customer behavior and churn patterns.

Subscription Plan Distribution

The customer base contains:

Basic: 42.10%
Standard: 37.73%
Premium: 20.18%
Overall Engagement

Average customer engagement:

Average watch time: 408.01 minutes
Average viewing sessions: 8.30
Average completion: 70.22%
Overall Churn

Historical churn rate:

24.89%

Churn by Plan
Plan	Churn Rate
Basic	26.31%
Standard	24.59%
Premium	22.49%
Churned vs Retained Customers

Churned customers showed:

Lower average watch time
Fewer viewing sessions
Higher payment failure rates
Lower average support satisfaction

These findings represent associations in the dataset and should not be interpreted as proof of causation.

🤖 Churn Prediction

A Random Forest model was developed to estimate future churn risk.

Instead of using information from the entire customer history, the model follows a point-in-time prediction approach.

Prediction Setup

Prediction cutoff:

2026-03-31

Future churn window:

2026-04-01 → 2026-06-30

Customers who had already churned before the cutoff were excluded.

Only information available on or before the prediction cutoff was used as model input.

This helps reduce data leakage.

📊 Churn Model Performance

The Random Forest model achieved:

Metric	Score
Accuracy	56.58%
Precision	12.84%
Recall	54.74%
F1 Score	20.80%
ROC-AUC	0.581

A probability threshold of 0.20 was selected to improve recall for retention use cases.

Why threshold 0.20?

The default threshold of 0.50 produced very low recall.

Because the business objective is to identify more potentially at-risk customers for retention campaigns, a lower threshold was evaluated.

The threshold of 0.20 provided the best F1 score among the tested thresholds.

Model Limitation

The ROC-AUC of 0.581 indicates that the model has limited predictive discrimination.

Therefore, the model should be treated as a churn-risk ranking and retention-support tool, not as a highly accurate standalone churn predictor.

🎯 Churn Risk Scoring

The trained model generates a churn probability for eligible customers.

Customers are categorized into:

Low Risk
Medium Risk
High Risk

The generated customer risk dataset is:

data/cleaned/customer_churn_risk.csv

It contains:

customer_id
churn_probability
risk_level

The risk score can then be combined with customer behavior and feedback to support retention decisions.

🧠 AI Customer Intelligence Copilot

The project includes a Generative AI Copilot powered by Gemini.

The Copilot receives structured customer intelligence such as:

Customer profile
Current subscription plan
Watch time
Viewing sessions
Completion rate
Favorite genre
Customer ratings
Support interactions
Payment failures
Subscription history
Churn probability
Churn risk level

The AI then converts these structured signals into natural-language business insights.

Example

Instead of manually checking multiple tables, a business user can ask:

Why is this customer at risk?

The Copilot can summarize the customer's important risk signals and provide possible retention actions.

💬 Example Copilot Questions

The dashboard supports questions such as:

Why is this customer at risk?

Show me high-risk customers with payment failures.

What are the main negative complaints?

Which plan has the highest churn?

What retention action should we take?

Give me a summary of this customer.

What are the main engagement problems for this customer?

Does this customer have payment issues?

What customer behavior may indicate churn risk?
🎯 Retention Recommendations

The system uses customer signals to generate practical retention recommendations.

Examples include:

Payment Problems

If payment failures are detected:

Contact the customer about payment issues and provide a payment-method update option.
Low Engagement

If viewing sessions are low:

Send personalized content recommendations to increase engagement.
Low Completion

If completion rate is low:

Recommend shorter or highly relevant content to improve completion.
Low Support Satisfaction

If support satisfaction is low:

Prioritize a support follow-up because satisfaction is low.

The recommendations are intended as decision-support suggestions, not automatic business actions.

🖥️ Streamlit Dashboard

The project includes an interactive Streamlit dashboard.

The dashboard provides:

Customer search
Customer profile
Subscription information
Engagement metrics
Churn risk
Payment information
Support information
Customer feedback
AI Copilot
Retention recommendations
Business analytics

Users can enter a customer ID and ask the Copilot questions about that customer.

🔐 API Key Security

The Gemini API key is not stored directly inside the Python source code.

The project uses Streamlit secrets:

.streamlit/secrets.toml

This file is excluded from Git using .gitignore.

Example:

GEMINI_API_KEY = "your-api-key"

Never commit a real API key to GitHub.

🛠️ Technologies Used
Programming
Python
Data Analysis
Pandas
NumPy
Machine Learning
Scikit-learn
Random Forest
Logistic Regression
Feature preprocessing
Threshold optimization
Generative AI
Google Gemini API
Dashboard
Streamlit
Development
VS Code
Jupyter Notebook
Git
GitHub
📓 Notebook Workflow

The project is organized into six main notebooks.

01 — Data Quality
01_data_quality.ipynb

Performs initial dataset inspection, missing-value analysis, duplicate detection and validation.

02 — Data Cleaning
02_data_cleaning.ipynb

Cleans and validates the raw datasets.

03 — Feature Engineering
03_feature_engineering.ipynb

Creates customer-level behavioral, payment, subscription and engagement features.

04 — Customer Analytics
04_customer_analytics.ipynb

Analyzes customer segments, engagement, churn, payments and support.

05 — Churn Model
05_churn_model.ipynb

Builds and evaluates the point-in-time churn prediction model and generates churn-risk scores.

06 — AI Copilot
06_ai_copilot.ipynb

Builds the customer intelligence context and connects it to the Generative AI layer.

🚀 Installation

Clone the repository:

git clone https://github.com/guptashiva03856-cmyk/netflix-customer-intelligence.git

Move into the project:

cd netflix-customer-intelligence

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
▶️ Run the Application

Run:

streamlit run app/app.py

The application will open in the browser.

📂 Data Flow
Raw CSV Files
      ↓
Data Quality
      ↓
Cleaned CSV Files
      ↓
Customer Feature Engineering
      ↓
Customer Analytics
      ↓
Point-in-Time Churn Model
      ↓
Customer Churn Risk
      ↓
AI Customer Context
      ↓
Gemini AI Copilot
      ↓
Streamlit Dashboard
⚠️ Limitations

This project has several limitations:

The churn model has limited predictive performance.
The dataset is a project dataset rather than live Netflix production data.
Churn relationships represent associations and not guaranteed causal relationships.
AI-generated recommendations should be reviewed by business users.
Gemini API usage may be subject to API quotas and pricing policies.
Customer risk scores should be used as decision-support signals rather than absolute predictions.
🔮 Future Improvements

Possible future improvements include:

Improve churn model performance with additional behavioral features.
Experiment with XGBoost or other boosting models.
Perform model calibration.
Add explainable AI using SHAP.
Add semantic search over customer feedback.
Build a proper vector database for feedback retrieval.
Implement Retrieval-Augmented Generation (RAG).
Add automated retention campaign tracking.
Add real-time customer event processing.
Add model monitoring and drift detection.
Deploy the application to a cloud platform.
Add authentication and role-based access.
💡 Business Value

The project demonstrates how multiple data sources can be transformed into actionable customer intelligence.

Instead of only showing dashboards and charts, the system combines:

Data
 ↓
Analytics
 ↓
Machine Learning
 ↓
Customer Risk
 ↓
Generative AI
 ↓
Business Recommendations

This allows business users to move from:

"What happened?"

to:

"Why did it happen?"

and finally:

"What should we do?"

👨‍💻 Author

Shiva Gupta

GitHub:

https://github.com/guptashiva03856-cmyk

LinkedIn:

https://www.linkedin.com/in/shiva-gupta-b8603a324/
⭐ Project Summary

Netflix Customer Intelligence Copilot is an end-to-end data and AI project combining:

Data Quality
Data Cleaning
Feature Engineering
Customer Analytics
Churn Prediction
Risk Scoring
Generative AI
Retention Recommendations
Streamlit Dashboard