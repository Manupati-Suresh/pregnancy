import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import os

st.set_page_config(
    page_title="Model Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Model Analytics & Dataset Insights")

# Load data and model
@st.cache_data
def load_data():
    """Load the diabetes dataset"""
    return pd.read_csv("diabetes.csv")

@st.cache_data
def load_model_info():
    """Load model performance metrics"""
    if os.path.exists("logistic_model.pkl"):
        model = pickle.load(open("logistic_model.pkl", "rb"))
        return model
    return None

# Load data
df = load_data()
model = load_model_info()

# Dataset Overview
st.header("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Samples", len(df))
with col2:
    st.metric("Features", len(df.columns) - 1)
with col3:
    st.metric("Diabetic Cases", df['Outcome'].sum())
with col4:
    st.metric("Diabetes Rate", f"{df['Outcome'].mean():.1%}")

# Feature Distributions
st.header("📈 Feature Distributions")

# Select feature to analyze
feature_options = [col for col in df.columns if col != 'Outcome']
selected_feature = st.selectbox("Select feature to analyze:", feature_options)

col1, col2 = st.columns(2)

with col1:
    # Histogram
    fig_hist = px.histogram(
        df, x=selected_feature, color='Outcome',
        title=f"Distribution of {selected_feature}",
        nbins=30, opacity=0.7
    )
    fig_hist.update_layout(barmode='overlay')
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # Box plot
    fig_box = px.box(
        df, x='Outcome', y=selected_feature,
        title=f"{selected_feature} by Diabetes Status",
        color='Outcome'
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Correlation Analysis
st.header("🔗 Feature Correlations")

# Correlation matrix
corr_matrix = df.corr()
fig_corr = px.imshow(
    corr_matrix,
    title="Feature Correlation Matrix",
    color_continuous_scale="RdBu_r",
    aspect="auto"
)
fig_corr.update_layout(height=600)
st.plotly_chart(fig_corr, use_container_width=True)

# Feature Statistics
st.header("📊 Feature Statistics")

# Summary statistics by outcome
stats_diabetic = df[df['Outcome'] == 1].describe()
stats_non_diabetic = df[df['Outcome'] == 0].describe()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Diabetic Patients")
    st.dataframe(stats_diabetic.round(2))

with col2:
    st.subheader("Non-Diabetic Patients")
    st.dataframe(stats_non_diabetic.round(2))

# Age Analysis
st.header("👥 Age Group Analysis")

# Create age groups
df_age = df.copy()
df_age['AgeGroup'] = pd.cut(df_age['Age'], 
                           bins=[0, 30, 40, 50, 60, 100], 
                           labels=['<30', '30-39', '40-49', '50-59', '60+'])

age_analysis = df_age.groupby('AgeGroup')['Outcome'].agg(['count', 'sum', 'mean']).reset_index()
age_analysis.columns = ['AgeGroup', 'Total', 'Diabetic', 'DiabetesRate']

fig_age = px.bar(
    age_analysis, x='AgeGroup', y=['Total', 'Diabetic'],
    title="Diabetes Cases by Age Group",
    barmode='group'
)
st.plotly_chart(fig_age, use_container_width=True)

# Risk Factors Analysis
st.header("⚠️ Risk Factors Analysis")

# Define risk thresholds
risk_factors = {
    'High Glucose': df['Glucose'] > 140,
    'High BMI': df['BMI'] > 30,
    'High Blood Pressure': df['BloodPressure'] > 90,
    'Advanced Age': df['Age'] > 50,
    'Multiple Pregnancies': df['Pregnancies'] > 3
}

risk_analysis = []
for factor, condition in risk_factors.items():
    total_with_factor = condition.sum()
    diabetic_with_factor = df[condition]['Outcome'].sum()
    risk_rate = diabetic_with_factor / total_with_factor if total_with_factor > 0 else 0
    
    risk_analysis.append({
        'Risk Factor': factor,
        'Population with Factor': total_with_factor,
        'Diabetic with Factor': diabetic_with_factor,
        'Risk Rate': risk_rate
    })

risk_df = pd.DataFrame(risk_analysis)

fig_risk = px.bar(
    risk_df, x='Risk Factor', y='Risk Rate',
    title="Diabetes Risk Rate by Risk Factor",
    color='Risk Rate',
    color_continuous_scale='Reds'
)
fig_risk.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_risk, use_container_width=True)

# Model Performance (if available)
if model is not None:
    st.header("🤖 Model Performance")
    
    # Feature importance (coefficients)
    feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    if hasattr(model, 'coef_'):
        coefficients = model.coef_[0]
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': coefficients,
            'Abs_Coefficient': np.abs(coefficients)
        }).sort_values('Abs_Coefficient', ascending=True)
        
        fig_importance = px.bar(
            importance_df, x='Abs_Coefficient', y='Feature',
            title="Feature Importance (Absolute Coefficients)",
            orientation='h',
            color='Coefficient',
            color_continuous_scale='RdBu_r'
        )
        st.plotly_chart(fig_importance, use_container_width=True)

# Data Quality Report
st.header("🔍 Data Quality Report")

quality_report = []
for col in df.columns:
    if col != 'Outcome':
        zero_count = (df[col] == 0).sum()
        zero_pct = zero_count / len(df) * 100
        
        quality_report.append({
            'Feature': col,
            'Zero Values': zero_count,
            'Zero Percentage': f"{zero_pct:.1f}%",
            'Min': df[col].min(),
            'Max': df[col].max(),
            'Mean': df[col].mean(),
            'Std': df[col].std()
        })

quality_df = pd.DataFrame(quality_report)
st.dataframe(quality_df.round(2), use_container_width=True)

# Download section
st.header("💾 Download Data")

col1, col2 = st.columns(2)

with col1:
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Dataset as CSV",
        data=csv,
        file_name="diabetes_dataset.csv",
        mime="text/csv"
    )

with col2:
    if not risk_df.empty:
        risk_csv = risk_df.to_csv(index=False)
        st.download_button(
            label="Download Risk Analysis as CSV",
            data=risk_csv,
            file_name="risk_analysis.csv",
            mime="text/csv"
        )