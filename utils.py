"""
Utility functions for the diabetes prediction app
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import logging

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def get_bmi_category(bmi):
    """Categorize BMI values"""
    if bmi < 18.5:
        return "Underweight", "blue"
    elif bmi < 25:
        return "Normal", "green"
    elif bmi < 30:
        return "Overweight", "orange"
    else:
        return "Obese", "red"

def get_glucose_category(glucose):
    """Categorize glucose levels"""
    if glucose < 70:
        return "Low", "blue"
    elif glucose < 100:
        return "Normal", "green"
    elif glucose < 126:
        return "Pre-diabetic", "orange"
    else:
        return "Diabetic", "red"

def get_bp_category(bp):
    """Categorize blood pressure"""
    if bp < 80:
        return "Normal", "green"
    elif bp < 90:
        return "High Normal", "orange"
    else:
        return "High", "red"

def validate_medical_ranges(inputs):
    """Comprehensive medical validation"""
    issues = []
    
    # Glucose validation
    if inputs['glucose'] < 50 or inputs['glucose'] > 300:
        issues.append("Glucose level outside typical range (50-300 mg/dL)")
    
    # Blood pressure validation
    if inputs['bp'] < 40 or inputs['bp'] > 150:
        issues.append("Blood pressure outside typical range (40-150 mmHg)")
    
    # BMI validation
    if inputs['bmi'] < 10 or inputs['bmi'] > 70:
        issues.append("BMI outside typical range (10-70 kg/m²)")
    
    # Age validation
    if inputs['age'] < 18 or inputs['age'] > 120:
        issues.append("Age outside typical range (18-120 years)")
    
    # Insulin validation
    if inputs['insulin'] > 1000:
        issues.append("Insulin level seems unusually high")
    
    return issues

def format_prediction_confidence(probability):
    """Format prediction confidence with descriptive text"""
    if probability < 0.2:
        return "Very Low", "🟢"
    elif probability < 0.4:
        return "Low", "🟡"
    elif probability < 0.6:
        return "Moderate", "🟠"
    elif probability < 0.8:
        return "High", "🔴"
    else:
        return "Very High", "🚨"

def generate_health_tips(inputs, prediction_prob):
    """Generate personalized health tips based on inputs"""
    tips = []
    
    # BMI-based tips
    bmi_category, _ = get_bmi_category(inputs['bmi'])
    if bmi_category == "Overweight" or bmi_category == "Obese":
        tips.append("💪 Consider a balanced diet and regular exercise to achieve healthy weight")
    
    # Glucose-based tips
    glucose_category, _ = get_glucose_category(inputs['glucose'])
    if glucose_category in ["Pre-diabetic", "Diabetic"]:
        tips.append("🍎 Monitor carbohydrate intake and consider consulting a nutritionist")
    
    # Age-based tips
    if inputs['age'] > 45:
        tips.append("👩‍⚕️ Regular health screenings become more important with age")
    
    # General tips based on risk level
    if prediction_prob > 0.5:
        tips.extend([
            "🏃‍♀️ Aim for at least 150 minutes of moderate exercise per week",
            "🥗 Focus on a diet rich in vegetables, whole grains, and lean proteins",
            "💧 Stay well hydrated and limit sugary beverages"
        ])
    
    return tips

@st.cache_data
def load_reference_data():
    """Load reference ranges for medical parameters"""
    return {
        'glucose': {'normal': (70, 100), 'prediabetic': (100, 126), 'diabetic': (126, float('inf'))},
        'bp': {'normal': (60, 80), 'elevated': (80, 90), 'high': (90, float('inf'))},
        'bmi': {'underweight': (0, 18.5), 'normal': (18.5, 25), 'overweight': (25, 30), 'obese': (30, float('inf'))},
        'insulin': {'normal': (16, 166), 'high': (166, float('inf'))}
    }

def create_patient_summary(inputs):
    """Create a formatted patient summary"""
    bmi_cat, _ = get_bmi_category(inputs['bmi'])
    glucose_cat, _ = get_glucose_category(inputs['glucose'])
    bp_cat, _ = get_bp_category(inputs['bp'])
    
    summary = f"""
    **Patient Summary:**
    - Age: {inputs['age']} years
    - BMI: {inputs['bmi']:.1f} kg/m² ({bmi_cat})
    - Glucose: {inputs['glucose']} mg/dL ({glucose_cat})
    - Blood Pressure: {inputs['bp']} mmHg ({bp_cat})
    - Pregnancies: {inputs['pregnancies']}
    """
    
    return summary

def log_prediction(inputs, prediction, probability):
    """Log prediction for monitoring purposes"""
    logger = logging.getLogger(__name__)
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'inputs': inputs,
        'prediction': int(prediction),
        'probability': float(probability)
    }
    
    logger.info(f"Prediction logged: {log_entry}")
    return log_entry