import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Health Guidelines",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Diabetes Prevention & Health Guidelines")

# Introduction
st.markdown("""
This page provides comprehensive information about diabetes prevention, risk factors, 
and healthy lifestyle recommendations based on medical guidelines.
""")

# Risk Factors Section
st.header("⚠️ Diabetes Risk Factors")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Non-Modifiable Risk Factors")
    st.markdown("""
    - **Age**: Risk increases after age 45
    - **Family History**: Having relatives with diabetes
    - **Ethnicity**: Higher risk in certain ethnic groups
    - **Gestational Diabetes**: Previous gestational diabetes
    - **Polycystic Ovary Syndrome (PCOS)**
    """)

with col2:
    st.subheader("🟡 Modifiable Risk Factors")
    st.markdown("""
    - **Overweight/Obesity**: BMI ≥ 25 kg/m²
    - **Physical Inactivity**: Less than 150 min/week exercise
    - **Poor Diet**: High in processed foods, sugar
    - **High Blood Pressure**: ≥ 140/90 mmHg
    - **High Cholesterol**: Abnormal lipid levels
    - **Smoking**: Increases insulin resistance
    """)

# Healthy Ranges
st.header("📊 Healthy Parameter Ranges")

# Create reference ranges table
ranges_data = {
    'Parameter': [
        'Fasting Glucose', 'Random Glucose', 'HbA1c', 'Blood Pressure', 
        'BMI', 'Waist Circumference (Men)', 'Waist Circumference (Women)',
        'Total Cholesterol', 'LDL Cholesterol', 'HDL Cholesterol (Men)', 'HDL Cholesterol (Women)'
    ],
    'Normal Range': [
        '70-100 mg/dL', '<140 mg/dL', '<5.7%', '<120/80 mmHg',
        '18.5-24.9 kg/m²', '<40 inches', '<35 inches',
        '<200 mg/dL', '<100 mg/dL', '>40 mg/dL', '>50 mg/dL'
    ],
    'Pre-diabetic/At Risk': [
        '100-125 mg/dL', '140-199 mg/dL', '5.7-6.4%', '120-139/80-89 mmHg',
        '25-29.9 kg/m²', '40+ inches', '35+ inches',
        '200-239 mg/dL', '100-129 mg/dL', '<40 mg/dL', '<50 mg/dL'
    ],
    'Diabetic/High Risk': [
        '≥126 mg/dL', '≥200 mg/dL', '≥6.5%', '≥140/90 mmHg',
        '≥30 kg/m²', 'N/A', 'N/A',
        '≥240 mg/dL', '≥130 mg/dL', 'N/A', 'N/A'
    ]
}

ranges_df = pd.DataFrame(ranges_data)
st.dataframe(ranges_df, use_container_width=True)

# Prevention Strategies
st.header("🛡️ Diabetes Prevention Strategies")

tab1, tab2, tab3, tab4 = st.tabs(["🍎 Diet", "🏃‍♀️ Exercise", "⚖️ Weight Management", "🧘‍♀️ Lifestyle"])

with tab1:
    st.subheader("Dietary Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Foods to Include:**
        - Whole grains (brown rice, quinoa, oats)
        - Lean proteins (fish, poultry, legumes)
        - Non-starchy vegetables (leafy greens, broccoli)
        - Healthy fats (avocado, nuts, olive oil)
        - Low-fat dairy products
        - Fresh fruits (in moderation)
        """)
    
    with col2:
        st.markdown("""
        **❌ Foods to Limit:**
        - Refined sugars and sweets
        - Processed and packaged foods
        - Sugary beverages
        - White bread and refined grains
        - Fried and high-fat foods
        - Excessive alcohol
        """)
    
    # Plate method visualization
    fig_plate = go.Figure()
    
    # Create pie chart for plate method
    labels = ['Non-starchy Vegetables', 'Lean Protein', 'Whole Grains/Starchy Foods']
    values = [50, 25, 25]
    colors = ['#2E8B57', '#4682B4', '#DAA520']
    
    fig_plate.add_trace(go.Pie(
        labels=labels, values=values, hole=0.3,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='outside'
    ))
    
    fig_plate.update_layout(
        title="The Diabetes Plate Method",
        annotations=[dict(text='Healthy<br>Plate', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    st.plotly_chart(fig_plate, use_container_width=True)

with tab2:
    st.subheader("Exercise Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Weekly Exercise Goals:**
        - **Aerobic Activity**: 150 minutes moderate intensity
        - **Strength Training**: 2+ days per week
        - **Flexibility**: Daily stretching
        - **Balance**: Especially important for older adults
        """)
        
        st.markdown("""
        **💡 Exercise Tips:**
        - Start slowly and gradually increase
        - Choose activities you enjoy
        - Exercise with friends or family
        - Track your progress
        - Consult healthcare provider before starting
        """)
    
    with col2:
        # Exercise benefits chart
        benefits = ['Blood Sugar Control', 'Weight Management', 'Heart Health', 
                   'Stress Reduction', 'Better Sleep', 'Increased Energy']
        impact = [95, 90, 85, 80, 75, 85]
        
        fig_benefits = px.bar(
            x=impact, y=benefits, orientation='h',
            title="Exercise Benefits for Diabetes Prevention",
            color=impact, color_continuous_scale='Greens'
        )
        fig_benefits.update_layout(showlegend=False)
        st.plotly_chart(fig_benefits, use_container_width=True)

with tab3:
    st.subheader("Weight Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Weight Loss Goals:**
        - Aim for 5-10% body weight reduction
        - Lose 1-2 pounds per week
        - Focus on sustainable changes
        - Combine diet and exercise
        """)
        
        # BMI calculator
        st.markdown("**BMI Calculator:**")
        height_ft = st.number_input("Height (feet)", min_value=4, max_value=7, value=5)
        height_in = st.number_input("Height (inches)", min_value=0, max_value=11, value=6)
        weight_lbs = st.number_input("Weight (pounds)", min_value=80, max_value=400, value=150)
        
        if st.button("Calculate BMI"):
            height_total_in = height_ft * 12 + height_in
            bmi = (weight_lbs / (height_total_in ** 2)) * 703
            
            if bmi < 18.5:
                category = "Underweight"
                color = "blue"
            elif bmi < 25:
                category = "Normal"
                color = "green"
            elif bmi < 30:
                category = "Overweight"
                color = "orange"
            else:
                category = "Obese"
                color = "red"
            
            st.markdown(f"**BMI: {bmi:.1f}** - :{color}[{category}]")
    
    with col2:
        # Weight loss timeline
        weeks = list(range(0, 25, 4))
        weight_loss = [0, 2, 4, 7, 10, 14, 18]
        
        fig_weight = px.line(
            x=weeks, y=weight_loss,
            title="Healthy Weight Loss Timeline",
            labels={'x': 'Weeks', 'y': 'Weight Loss (lbs)'}
        )
        fig_weight.update_traces(mode='markers+lines', marker_size=8)
        st.plotly_chart(fig_weight, use_container_width=True)

with tab4:
    st.subheader("Lifestyle Modifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **😴 Sleep Hygiene:**
        - Aim for 7-9 hours per night
        - Maintain consistent sleep schedule
        - Create relaxing bedtime routine
        - Avoid screens before bed
        - Keep bedroom cool and dark
        """)
        
        st.markdown("""
        **🚭 Smoking Cessation:**
        - Increases insulin resistance
        - Worsens circulation
        - Seek professional help
        - Use nicotine replacement therapy
        - Join support groups
        """)
    
    with col2:
        st.markdown("""
        **🧘‍♀️ Stress Management:**
        - Practice meditation or yoga
        - Deep breathing exercises
        - Regular physical activity
        - Maintain social connections
        - Seek professional counseling if needed
        """)
        
        st.markdown("""
        **🩺 Regular Health Monitoring:**
        - Annual physical exams
        - Blood glucose screening
        - Blood pressure checks
        - Cholesterol testing
        - Eye and foot examinations
        """)

# Screening Guidelines
st.header("🔬 Screening Guidelines")

screening_data = {
    'Age Group': ['18-39 years', '40-44 years', '45+ years', 'High Risk (any age)'],
    'Screening Frequency': ['Every 3 years if overweight', 'Every 3 years', 'Every 1-3 years', 'Annually'],
    'Tests': ['Fasting glucose, HbA1c', 'Fasting glucose, HbA1c', 'Fasting glucose, HbA1c', 'Comprehensive screening'],
    'Additional Notes': [
        'Screen if BMI ≥25 + risk factors',
        'Screen all adults',
        'More frequent if pre-diabetic',
        'Include OGTT if indicated'
    ]
}

screening_df = pd.DataFrame(screening_data)
st.dataframe(screening_df, use_container_width=True)

# Emergency Warning Signs
st.header("🚨 When to Seek Immediate Medical Attention")

col1, col2 = st.columns(2)

with col1:
    st.error("""
    **Diabetic Emergency Signs:**
    - Blood glucose >400 mg/dL
    - Severe dehydration
    - Difficulty breathing
    - Fruity breath odor
    - Nausea and vomiting
    - Confusion or unconsciousness
    """)

with col2:
    st.warning("""
    **Contact Healthcare Provider:**
    - Blood glucose consistently >180 mg/dL
    - Frequent urination and thirst
    - Unexplained weight loss
    - Slow-healing wounds
    - Blurred vision
    - Tingling in hands/feet
    """)

# Resources
st.header("📚 Additional Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🏥 Organizations:**
    - American Diabetes Association
    - CDC Diabetes Prevention Program
    - National Institute of Diabetes
    - Academy of Nutrition and Dietetics
    """)

with col2:
    st.markdown("""
    **📱 Mobile Apps:**
    - MyFitnessPal (nutrition tracking)
    - Glucose Buddy (blood sugar log)
    - Diabetes:M (comprehensive management)
    - Fooducate (healthy food choices)
    """)

with col3:
    st.markdown("""
    **📖 Educational Materials:**
    - Diabetes prevention cookbooks
    - Exercise guides for beginners
    - Stress management resources
    - Support group directories
    """)

# Disclaimer
st.markdown("---")
st.info("""
**Medical Disclaimer:** This information is for educational purposes only and should not replace 
professional medical advice. Always consult with qualified healthcare providers for personalized 
medical guidance and treatment decisions.
""")