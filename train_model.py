
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import pickle
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_preprocess_data():
    """Load and preprocess the diabetes dataset"""
    try:
        df = pd.read_csv("diabetes.csv")
        logger.info(f"Dataset loaded successfully. Shape: {df.shape}")
        
        # Data quality checks
        logger.info(f"Missing values: {df.isnull().sum().sum()}")
        logger.info(f"Target distribution:\n{df['Outcome'].value_counts()}")
        
        # Replace 0s with median in important columns (0 is not medically possible)
        cols_to_fix = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
        
        for col in cols_to_fix:
            zero_count = (df[col] == 0).sum()
            if zero_count > 0:
                median_val = df[df[col] != 0][col].median()
                df[col] = df[col].replace(0, median_val)
                logger.info(f"Replaced {zero_count} zeros in {col} with median value {median_val:.2f}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def train_model(df):
    """Train the logistic regression model"""
    try:
        # Separate features and target
        X = df.drop("Outcome", axis=1)
        y = df["Outcome"]
        
        # Feature scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training set size: {X_train.shape[0]}")
        logger.info(f"Test set size: {X_test.shape[0]}")
        
        # Train model with cross-validation
        model = LogisticRegression(solver="liblinear", random_state=42, max_iter=1000)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
        logger.info(f"Cross-validation AUC scores: {cv_scores}")
        logger.info(f"Mean CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Fit the model
        model.fit(X_train, y_train)
        
        # Evaluate on test set
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        test_auc = roc_auc_score(y_test, y_pred_proba)
        logger.info(f"Test AUC: {test_auc:.4f}")
        
        # Classification report
        logger.info("Classification Report:")
        logger.info(f"\n{classification_report(y_test, y_pred)}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"Confusion Matrix:\n{cm}")
        
        # Feature importance (coefficients)
        feature_names = X.columns
        coefficients = model.coef_[0]
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'coefficient': coefficients,
            'abs_coefficient': np.abs(coefficients)
        }).sort_values('abs_coefficient', ascending=False)
        
        logger.info("Feature Importance (by coefficient magnitude):")
        logger.info(f"\n{feature_importance}")
        
        return model, scaler, test_auc
        
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise

def save_model(model, scaler):
    """Save the trained model and scaler"""
    try:
        # Create backup if files exist
        if os.path.exists("logistic_model.pkl"):
            os.rename("logistic_model.pkl", "logistic_model_backup.pkl")
            logger.info("Created backup of existing model")
        
        if os.path.exists("scaler.pkl"):
            os.rename("scaler.pkl", "scaler_backup.pkl")
            logger.info("Created backup of existing scaler")
        
        # Save new model and scaler
        pickle.dump(model, open("logistic_model.pkl", "wb"))
        pickle.dump(scaler, open("scaler.pkl", "wb"))
        
        logger.info("Model and scaler saved successfully")
        
        # Verify saved files
        test_model = pickle.load(open("logistic_model.pkl", "rb"))
        test_scaler = pickle.load(open("scaler.pkl", "rb"))
        logger.info("Model files verified successfully")
        
    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")
        raise

def main():
    """Main training pipeline"""
    logger.info("Starting model training pipeline...")
    
    try:
        # Load and preprocess data
        df = load_and_preprocess_data()
        
        # Train model
        model, scaler, test_auc = train_model(df)
        
        # Save model
        save_model(model, scaler)
        
        logger.info(f"Training completed successfully! Final test AUC: {test_auc:.4f}")
        
        return model, scaler
        
    except Exception as e:
        logger.error(f"Training pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
