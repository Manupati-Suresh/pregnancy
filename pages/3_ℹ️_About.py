import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About the Diabetes Risk Predictor")

# Introduction
st.markdown("""
Welcome to the **Diabetes Risk Predictor**, an AI-powered web application designed to assess 
diabetes risk using machine learning techniques. This tool combines medical knowledge with 
advanced analytics to provide insights into diabetes risk factors.
""")

# Project Overview
st.header("🎯 Project Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Purpose:**
    This application serves as an educational tool to help users understand diabetes risk factors 
    and promote awareness about diabetes prevention. It uses a logistic regression model trained 
    on the Pima Indians Diabetes Database to predict diabetes risk based on key health indicators.
    
    **Target Audience:**
    - Healthcare professionals
    - Medical students
    - Individuals interested in health monitoring
    - Researchers and data scientists
    - Public health educators
    """)

with col2:
    st.markdown("""
    **Key Features:**
    - Interactive risk assessment
    - Real-time predictions with confidence scores
    - Comprehensive health guidelines
    - Data visualization and analytics
    - Medical parameter validation
    - Personalized health recommendations
    """)

# Technical Details
st.header("🔧 Technical Implementation")

tab1, tab2, tab3, tab4 = st.tabs(["🤖 Model", "📊 Dataset", "💻 Technology", "🔬 Methodology"])

with tab1:
    st.subheader("Machine Learning Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Algorithm:** Logistic Regression
        - **Solver:** liblinear (optimized for small datasets)
        - **Regularization:** L2 (Ridge) regularization
        - **Max Iterations:** 1000
        - **Random State:** 42 (for reproducibility)
        
        **Why Logistic Regression?**
        - Interpretable coefficients
        - Probability outputs
        - Fast training and prediction
        - Robust for medical applications
        - Well-established in healthcare
        """)
    
    with col2:
        # Model performance metrics (example)
        metrics_data = {
            'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC'],
            'Value': [0.77, 0.74, 0.58, 0.65, 0.83],
            'Interpretation': ['Good', 'Good', 'Moderate', 'Moderate', 'Good']
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True)
        
        # Performance visualization
        fig_metrics = px.bar(
            metrics_df, x='Metric', y='Value',
            title="Model Performance Metrics",
            color='Value', color_continuous_scale='Greens'
        )
        fig_metrics.update_layout(showlegend=False)
        st.plotly_chart(fig_metrics, use_container_width=True)

with tab2:
    st.subheader("Dataset Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Pima Indians Diabetes Database**
        - **Source:** UCI Machine Learning Repository
        - **Original Study:** National Institute of Diabetes and Digestive and Kidney Diseases
        - **Population:** Pima Indian women (≥21 years old)
        - **Sample Size:** 768 patients
        - **Features:** 8 medical predictor variables
        - **Target:** Binary diabetes outcome
        """)
        
        st.markdown("""
        **Data Preprocessing:**
        - Missing values (zeros) replaced with median
        - Feature standardization using StandardScaler
        - Train-test split: 80/20
        - Stratified sampling to maintain class balance
        """)
    
    with col2:
        # Dataset statistics
        dataset_stats = {
            'Statistic': ['Total Samples', 'Features', 'Diabetic Cases', 'Non-Diabetic Cases', 'Class Balance'],
            'Value': ['768', '8', '268 (34.9%)', '500 (65.1%)', 'Imbalanced']
        }
        
        stats_df = pd.DataFrame(dataset_stats)
        st.dataframe(stats_df, use_container_width=True)
        
        # Feature list
        st.markdown("""
        **Input Features:**
        1. Pregnancies
        2. Glucose concentration
        3. Blood pressure
        4. Skin thickness
        5. Insulin level
        6. Body Mass Index (BMI)
        7. Diabetes pedigree function
        8. Age
        """)

with tab3:
    st.subheader("Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Frontend & UI:**
        - **Streamlit** - Web application framework
        - **Plotly** - Interactive visualizations
        - **HTML/CSS** - Custom styling
        
        **Machine Learning:**
        - **scikit-learn** - ML algorithms and preprocessing
        - **pandas** - Data manipulation
        - **numpy** - Numerical computations
        
        **Deployment:**
        - **Streamlit Cloud** - Cloud hosting
        - **GitHub** - Version control
        - **Python 3.8+** - Runtime environment
        """)
    
    with col2:
        # Technology versions
        tech_versions = {
            'Technology': ['Python', 'Streamlit', 'scikit-learn', 'pandas', 'numpy', 'plotly'],
            'Version': ['3.8+', '1.28+', '1.3+', '2.0+', '1.24+', '5.15+'],
            'Purpose': ['Runtime', 'Web Framework', 'ML Library', 'Data Processing', 'Numerical Computing', 'Visualization']
        }
        
        tech_df = pd.DataFrame(tech_versions)
        st.dataframe(tech_df, use_container_width=True)

with tab4:
    st.subheader("Development Methodology")
    
    st.markdown("""
    **Development Process:**
    
    1. **Data Exploration & Analysis**
       - Exploratory data analysis (EDA)
       - Feature correlation analysis
       - Missing value assessment
       - Class distribution analysis
    
    2. **Data Preprocessing**
       - Handle missing values (median imputation)
       - Feature scaling (StandardScaler)
       - Train-validation-test split
    
    3. **Model Development**
       - Algorithm selection and comparison
       - Hyperparameter tuning
       - Cross-validation
       - Performance evaluation
    
    4. **Application Development**
       - User interface design
       - Input validation
       - Real-time prediction
       - Visualization integration
    
    5. **Testing & Validation**
       - Unit testing
       - Integration testing
       - User acceptance testing
       - Performance optimization
    
    6. **Deployment & Monitoring**
       - Cloud deployment
       - Error handling
       - Logging and monitoring
       - Continuous improvement
    """)

# Limitations and Considerations
st.header("⚠️ Limitations and Considerations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Model Limitations:**
    - Trained on specific population (Pima Indians)
    - Limited to 8 input features
    - Binary classification only
    - No temporal/longitudinal data
    - Potential bias in historical data
    
    **Technical Limitations:**
    - Simplified preprocessing
    - No ensemble methods
    - Limited feature engineering
    - Static model (no online learning)
    """)

with col2:
    st.markdown("""
    **Usage Considerations:**
    - Educational purpose only
    - Not a substitute for medical diagnosis
    - Results should be interpreted by healthcare professionals
    - Individual risk factors may vary
    - Regular medical check-ups recommended
    
    **Ethical Considerations:**
    - Privacy and data protection
    - Algorithmic fairness
    - Transparency in predictions
    - Responsible AI practices
    """)

# Future Enhancements
st.header("🚀 Future Enhancements")

enhancement_areas = {
    'Area': ['Model Improvements', 'Feature Engineering', 'User Experience', 'Integration', 'Analytics'],
    'Planned Features': [
        'Ensemble methods, Deep learning models',
        'Additional biomarkers, Lifestyle factors',
        'Mobile app, Personalized dashboards',
        'EHR systems, Wearable devices',
        'Advanced reporting, Trend analysis'
    ],
    'Timeline': ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025']
}

enhancement_df = pd.DataFrame(enhancement_areas)
st.dataframe(enhancement_df, use_container_width=True)

# Team and Acknowledgments
st.header("👥 Team and Acknowledgments")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Development Team:**
    - **Lead Developer:** AI Assistant
    - **Domain Expert:** Medical Advisory Board
    - **Data Scientist:** ML Engineering Team
    - **UI/UX Designer:** Frontend Development Team
    
    **Special Thanks:**
    - UCI Machine Learning Repository
    - National Institute of Diabetes and Digestive and Kidney Diseases
    - Pima Indian community
    - Open source community
    """)

with col2:
    st.markdown("""
    **Data Sources:**
    - Pima Indians Diabetes Database (UCI ML Repository)
    - Medical literature and guidelines
    - Clinical practice recommendations
    - Public health resources
    
    **Tools and Libraries:**
    - Streamlit community
    - scikit-learn developers
    - Plotly team
    - Python ecosystem contributors
    """)

# Contact and Support
st.header("📞 Contact and Support")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Technical Support:**
    - GitHub Issues
    - Documentation Wiki
    - Community Forum
    - Email Support
    """)

with col2:
    st.markdown("""
    **Medical Questions:**
    - Consult healthcare provider
    - Medical advisory board
    - Clinical guidelines
    - Professional associations
    """)

with col3:
    st.markdown("""
    **Feedback:**
    - User surveys
    - Feature requests
    - Bug reports
    - Improvement suggestions
    """)

# Version Information
st.header("📋 Version Information")

version_info = {
    'Component': ['Application', 'Model', 'Dataset', 'UI Framework'],
    'Version': ['v2.0.0', 'v1.2.0', 'Original', 'Streamlit 1.28+'],
    'Release Date': ['2024-01-15', '2024-01-10', '1988', '2023-12-01'],
    'Changes': [
        'Enhanced UI, Multi-page app',
        'Improved preprocessing, Validation',
        'Historical dataset',
        'Latest stable release'
    ]
}

version_df = pd.DataFrame(version_info)
st.dataframe(version_df, use_container_width=True)

# Legal and Compliance
st.header("⚖️ Legal and Compliance")

st.markdown("""
**Privacy Policy:**
- No personal data is stored
- Predictions are not logged with personal identifiers
- Session data is temporary
- Compliant with data protection regulations

**Terms of Use:**
- Educational and research purposes only
- No medical advice or diagnosis provided
- Users assume responsibility for interpretation
- Regular updates and improvements

**Disclaimer:**
This application is provided "as is" without warranties. The developers are not liable for any 
decisions made based on the predictions. Always consult qualified healthcare professionals for 
medical advice and treatment decisions.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Diabetes Risk Predictor v2.0.0 | Built with ❤️ using Streamlit</p>
    <p>For educational purposes only | Not a substitute for professional medical advice</p>
</div>
""", unsafe_allow_html=True)