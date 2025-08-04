"""
Health check script for the diabetes prediction app
Validates model files, dependencies, and system readiness
"""

import os
import sys
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import logging

def setup_logging():
    """Setup logging for health check"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    logger = logging.getLogger(__name__)
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'sklearn', 
        'plotly', 'pickle'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"❌ {package} - MISSING")
    
    return len(missing_packages) == 0, missing_packages

def check_data_files():
    """Check if required data files exist"""
    logger = logging.getLogger(__name__)
    required_files = ['diabetes.csv']
    optional_files = ['logistic_model.pkl', 'scaler.pkl']
    
    missing_required = []
    missing_optional = []
    
    # Check required files
    for file in required_files:
        if os.path.exists(file):
            logger.info(f"✅ {file} - OK")
        else:
            missing_required.append(file)
            logger.error(f"❌ {file} - MISSING (REQUIRED)")
    
    # Check optional files
    for file in optional_files:
        if os.path.exists(file):
            logger.info(f"✅ {file} - OK")
        else:
            missing_optional.append(file)
            logger.warning(f"⚠️ {file} - MISSING (will be created)")
    
    return len(missing_required) == 0, missing_required, missing_optional

def validate_dataset():
    """Validate the diabetes dataset"""
    logger = logging.getLogger(__name__)
    
    try:
        df = pd.read_csv('diabetes.csv')
        
        # Check dataset shape
        expected_shape = (768, 9)
        if df.shape == expected_shape:
            logger.info(f"✅ Dataset shape {df.shape} - OK")
        else:
            logger.warning(f"⚠️ Dataset shape {df.shape}, expected {expected_shape}")
        
        # Check required columns
        expected_columns = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'
        ]
        
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if not missing_columns:
            logger.info("✅ All required columns present - OK")
        else:
            logger.error(f"❌ Missing columns: {missing_columns}")
            return False
        
        # Check data types
        numeric_columns = expected_columns[:-1]  # All except 'Outcome'
        for col in numeric_columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                logger.info(f"✅ {col} data type - OK")
            else:
                logger.error(f"❌ {col} should be numeric")
                return False
        
        # Check target variable
        unique_outcomes = df['Outcome'].unique()
        if set(unique_outcomes) == {0, 1}:
            logger.info("✅ Target variable (Outcome) - OK")
        else:
            logger.error(f"❌ Target variable should be 0/1, found: {unique_outcomes}")
            return False
        
        # Check for missing values
        missing_values = df.isnull().sum().sum()
        if missing_values == 0:
            logger.info("✅ No missing values - OK")
        else:
            logger.warning(f"⚠️ Found {missing_values} missing values")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Dataset validation failed: {str(e)}")
        return False

def validate_model_files():
    """Validate model and scaler files if they exist"""
    logger = logging.getLogger(__name__)
    
    model_valid = True
    scaler_valid = True
    
    # Check model file
    if os.path.exists('logistic_model.pkl'):
        try:
            model = pickle.load(open('logistic_model.pkl', 'rb'))
            
            # Check if it has required methods
            if hasattr(model, 'predict') and hasattr(model, 'predict_proba'):
                logger.info("✅ Model file - OK")
            else:
                logger.error("❌ Model missing required methods")
                model_valid = False
                
        except Exception as e:
            logger.error(f"❌ Model file corrupted: {str(e)}")
            model_valid = False
    
    # Check scaler file
    if os.path.exists('scaler.pkl'):
        try:
            scaler = pickle.load(open('scaler.pkl', 'rb'))
            
            # Check if it has required methods
            if hasattr(scaler, 'transform'):
                logger.info("✅ Scaler file - OK")
            else:
                logger.error("❌ Scaler missing required methods")
                scaler_valid = False
                
        except Exception as e:
            logger.error(f"❌ Scaler file corrupted: {str(e)}")
            scaler_valid = False
    
    return model_valid and scaler_valid

def test_model_prediction():
    """Test model prediction with sample data"""
    logger = logging.getLogger(__name__)
    
    if not (os.path.exists('logistic_model.pkl') and os.path.exists('scaler.pkl')):
        logger.warning("⚠️ Model files not found, skipping prediction test")
        return True
    
    try:
        # Load model and scaler
        model = pickle.load(open('logistic_model.pkl', 'rb'))
        scaler = pickle.load(open('scaler.pkl', 'rb'))
        
        # Create sample input
        sample_input = pd.DataFrame([[
            1, 120, 80, 20, 80, 25.0, 0.5, 30
        ]], columns=[
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ])
        
        # Test prediction
        scaled_input = scaler.transform(sample_input)
        prediction = model.predict(scaled_input)[0]
        probability = model.predict_proba(scaled_input)[0]
        
        # Validate outputs
        if prediction in [0, 1] and len(probability) == 2 and abs(sum(probability) - 1.0) < 0.001:
            logger.info(f"✅ Model prediction test - OK (pred: {prediction}, prob: {probability[1]:.3f})")
            return True
        else:
            logger.error("❌ Model prediction test failed - invalid output format")
            return False
            
    except Exception as e:
        logger.error(f"❌ Model prediction test failed: {str(e)}")
        return False

def check_streamlit_config():
    """Check Streamlit configuration"""
    logger = logging.getLogger(__name__)
    
    config_path = '.streamlit/config.toml'
    if os.path.exists(config_path):
        logger.info("✅ Streamlit config file - OK")
        return True
    else:
        logger.warning("⚠️ Streamlit config file not found (optional)")
        return True

def generate_health_report():
    """Generate comprehensive health report"""
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("DIABETES PREDICTION APP - HEALTH CHECK REPORT")
    logger.info("=" * 60)
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Working Directory: {os.getcwd()}")
    logger.info("-" * 60)
    
    all_checks_passed = True
    
    # Check dependencies
    logger.info("1. CHECKING DEPENDENCIES...")
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        logger.error(f"Missing dependencies: {missing_deps}")
        all_checks_passed = False
    
    # Check data files
    logger.info("\n2. CHECKING DATA FILES...")
    files_ok, missing_req, missing_opt = check_data_files()
    if not files_ok:
        logger.error(f"Missing required files: {missing_req}")
        all_checks_passed = False
    
    # Validate dataset
    logger.info("\n3. VALIDATING DATASET...")
    dataset_ok = validate_dataset()
    if not dataset_ok:
        all_checks_passed = False
    
    # Validate model files
    logger.info("\n4. VALIDATING MODEL FILES...")
    model_ok = validate_model_files()
    if not model_ok:
        all_checks_passed = False
    
    # Test model prediction
    logger.info("\n5. TESTING MODEL PREDICTION...")
    prediction_ok = test_model_prediction()
    if not prediction_ok:
        all_checks_passed = False
    
    # Check Streamlit config
    logger.info("\n6. CHECKING STREAMLIT CONFIG...")
    config_ok = check_streamlit_config()
    
    # Final report
    logger.info("\n" + "=" * 60)
    if all_checks_passed:
        logger.info("🎉 ALL HEALTH CHECKS PASSED - APP READY FOR DEPLOYMENT!")
    else:
        logger.error("❌ SOME HEALTH CHECKS FAILED - PLEASE FIX ISSUES BEFORE DEPLOYMENT")
    logger.info("=" * 60)
    
    return all_checks_passed

def main():
    """Main health check function"""
    logger = setup_logging()
    
    try:
        success = generate_health_report()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Health check failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()