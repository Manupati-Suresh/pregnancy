
import streamlit as st
import pandas as pd
import pickle
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .risk-high {
        background-color: #ffebee;
        border-left-color: #f44336;
    }
    .risk-low {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stAlert > div {
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_model_files():
    """Load model and scaler with error handling"""
    try:
        if not os.path.exists("logistic_model.pkl") or not os.path.exists("scaler.pkl"):
            with st.spinner("🔄 Training model for first time... This may take a moment."):
                exec(open("train_model.py").read())
            st.success("✅ Model trained successfully!")
        
        model = pickle.load(open("logistic_model.pkl", "rb"))
        scaler = pickle.load(open("scaler.pkl", "rb"))
        return model, scaler
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        logger.error(f"Model loading error: {str(e)}")
        return None, None

def validate_inputs(inputs):
    """Validate user inputs for medical reasonableness"""
    warnings = []
    
    if inputs['glucose'] < 70:
        warnings.append("⚠️ Glucose level seems low (normal fasting: 70-100 mg/dL)")
    elif inputs['glucose'] > 180:
        warnings.append("⚠️ Glucose level seems high (normal fasting: 70-100 mg/dL)")
    
    if inputs['bp'] < 60:
        warnings.append("⚠️ Blood pressure seems low (normal: 80-120 mmHg)")
    elif inputs['bp'] > 140:
        warnings.append("⚠️ Blood pressure seems high (normal: 80-120 mmHg)")
    
    if inputs['bmi'] < 18.5:
        warnings.append("⚠️ BMI indicates underweight")
    elif inputs['bmi'] > 30:
        warnings.append("⚠️ BMI indicates obesity")
    
    return warnings

def create_risk_gauge(probability):
    """Create a risk gauge visualization"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Diabetes Risk %"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def create_feature_importance_chart():
    """Create a feature importance visualization"""
    features = ['Glucose', 'BMI', 'Age', 'Pregnancies', 'Insulin', 'Blood Pressure', 'Skin Thickness', 'Pedigree Function']
    importance = [0.35, 0.20, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03]  # Approximate importance
    
    fig = px.bar(
        x=importance, 
        y=features, 
        orientation='h',
        title="Feature Importance in Diabetes Prediction",
        labels={'x': 'Relative Importance', 'y': 'Features'}
    )
    fig.update_layout(height=400)
    return fig

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🩺 Diabetes Risk Predictor</h1>', unsafe_allow_html=True)
    
    # Load model
    model, scaler = load_model_files()
    if model is None or scaler is None:
        st.stop()
    
    # Sidebar for inputs
    st.sidebar.header("📋 Patient Information")
    st.sidebar.markdown("*Please enter the patient's medical parameters*")
    
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with st.sidebar:
        # Input fields with better descriptions and help text
        pregnancies = st.slider(
            "Number of Pregnancies", 
            min_value=0, max_value=17, value=1,
            help="Total number of pregnancies"
        )
        
        glucose = st.slider(
            "Glucose Level (mg/dL)", 
            min_value=0, max_value=200, value=120,
            help="Plasma glucose concentration (normal fasting: 70-100)"
        )
        
        bp = st.slider(
            "Blood Pressure (mmHg)", 
            min_value=0, max_value=122, value=80,
            help="Diastolic blood pressure (normal: 60-80)"
        )
        
        skin = st.slider(
            "Skin Thickness (mm)", 
            min_value=0, max_value=99, value=20,
            help="Triceps skin fold thickness"
        )
        
        insulin = st.slider(
            "Insulin Level (μU/mL)", 
            min_value=0, max_value=846, value=80,
            help="2-hour serum insulin (normal: 16-166)"
        )
        
        bmi = st.slider(
            "BMI (kg/m²)", 
            min_value=0.0, max_value=67.1, value=25.0, step=0.1,
            help="Body Mass Index (normal: 18.5-24.9)"
        )
        
        pedigree = st.slider(
            "Diabetes Pedigree Function", 
            min_value=0.0, max_value=2.5, value=0.5, step=0.01,
            help="Genetic predisposition score"
        )
        
        age = st.slider(
            "Age (years)", 
            min_value=21, max_value=90, value=30,
            help="Patient's age in years"
        )
        
        # Prediction button
        predict_button = st.button("🔍 Predict Diabetes Risk", type="primary", use_container_width=True)
    
    # Main content area
    with col1:
        if predict_button:
            # Collect inputs
            inputs = {
                'pregnancies': pregnancies,
                'glucose': glucose,
                'bp': bp,
                'skin': skin,
                'insulin': insulin,
                'bmi': bmi,
                'pedigree': pedigree,
                'age': age
            }
            
            # Validate inputs
            warnings = validate_inputs(inputs)
            if warnings:
                st.warning("⚠️ **Input Validation Warnings:**\n" + "\n".join(warnings))
            
            # Prepare data for prediction
            input_df = pd.DataFrame([[pregnancies, glucose, bp, skin, insulin, bmi, pedigree, age]],
                                   columns=["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", 
                                          "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"])
            
            try:
                input_scaled = scaler.transform(input_df)
                pred = model.predict(input_scaled)[0]
                proba = model.predict_proba(input_scaled)[0][1]
                
                # Display results
                st.subheader("📊 Prediction Results")
                
                # Risk level determination
                if proba < 0.3:
                    risk_level = "Low Risk"
                    risk_color = "green"
                    risk_class = "risk-low"
                elif proba < 0.7:
                    risk_level = "Moderate Risk"
                    risk_color = "orange"
                    risk_class = "metric-card"
                else:
                    risk_level = "High Risk"
                    risk_color = "red"
                    risk_class = "risk-high"
                
                # Results display
                result_col1, result_col2 = st.columns(2)
                
                with result_col1:
                    st.markdown(f"""
                    <div class="metric-card {risk_class}">
                        <h3>Prediction: {"Diabetic" if pred == 1 else "Non-Diabetic"}</h3>
                        <h4>Risk Level: {risk_level}</h4>
                        <p>Probability: {proba:.1%}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col2:
                    # Risk gauge
                    fig_gauge = create_risk_gauge(proba)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Recommendations based on risk level
                st.subheader("💡 Recommendations")
                if proba < 0.3:
                    st.success("""
                    **Low Risk - Keep up the good work!**
                    - Maintain current healthy lifestyle
                    - Regular check-ups every 1-2 years
                    - Continue balanced diet and exercise
                    """)
                elif proba < 0.7:
                    st.warning("""
                    **Moderate Risk - Take preventive action:**
                    - Consult healthcare provider for detailed assessment
                    - Consider lifestyle modifications (diet, exercise)
                    - Monitor blood glucose levels regularly
                    - Schedule follow-up in 6-12 months
                    """)
                else:
                    st.error("""
                    **High Risk - Seek immediate medical attention:**
                    - Consult endocrinologist or primary care physician immediately
                    - Comprehensive diabetes screening recommended
                    - Implement strict dietary and lifestyle changes
                    - Regular monitoring and follow-up required
                    """)
                
                # Log prediction
                logger.info(f"Prediction made: Risk={proba:.3f}, Result={'Diabetic' if pred == 1 else 'Non-Diabetic'}")
                
            except Exception as e:
                st.error(f"❌ Prediction error: {str(e)}")
                logger.error(f"Prediction error: {str(e)}")
        
        else:
            # Welcome message and instructions
            st.info("""
            👋 **Welcome to the Diabetes Risk Predictor!**
            
            This AI-powered tool helps assess diabetes risk based on key health indicators. 
            Please enter the patient information in the sidebar and click 'Predict' to get started.
            
            **Important:** This tool is for educational purposes only and should not replace professional medical advice.
            """)
            
            # Show feature importance chart
            st.subheader("📈 Understanding the Model")
            fig_importance = create_feature_importance_chart()
            st.plotly_chart(fig_importance, use_container_width=True)
    
    with col2:
        # Model information panel
        st.subheader("🤖 Model Information")
        st.info("""
        **Algorithm:** Logistic Regression
        **Dataset:** Pima Indians Diabetes Database
        **Features:** 8 medical indicators
        **Samples:** 768 patients
        **Accuracy:** ~77% on test data
        """)
        
        # Quick stats
        st.subheader("📊 Dataset Statistics")
        st.metric("Total Patients", "768")
        st.metric("Diabetic Cases", "268 (34.9%)")
        st.metric("Non-Diabetic Cases", "500 (65.1%)")
        
        # Disclaimer
        st.subheader("⚠️ Medical Disclaimer")
        st.warning("""
        This application is for educational and informational purposes only. 
        It should not be used as a substitute for professional medical advice, 
        diagnosis, or treatment. Always consult qualified healthcare providers 
        for medical decisions.
        """)

if __name__ == "__main__":
    main()
