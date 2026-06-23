import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def train_models():
    data_path = os.path.join(os.path.dirname(__file__), "agricultural_data.csv")
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run generate_data.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Feature Engineering
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['DayOfYear'] = df['Date'].dt.dayofyear
    
    # We will predict the Modal Price.
    # Features will include Commodity, State, District, Temperature, Rainfall, Humidity, Month
    features = ['Commodity', 'State', 'District', 'Temperature', 'Rainfall', 'Humidity', 'Month']
    X = df[features].copy()
    y = df['Modal Price']

    # Encoding categorical variables
    encoders = {}
    categorical_cols = ['Commodity', 'State', 'District']
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
        
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training models...")
    
    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    print(f"Linear Regression R2: {r2_score(y_test, lr_preds):.4f}")
    
    # Random Forest Regression
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    print(f"Random Forest Regressor R2: {r2_score(y_test, rf_preds):.4f}")
    
    # XGBoost Regression
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)
    print(f"XGBoost Regressor R2: {r2_score(y_test, xgb_preds):.4f}")
    
    # Save the XGBoost model (best performing typically for tabular data)
    model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.pkl")
    encoders_path = os.path.join(os.path.dirname(__file__), "label_encoders.pkl")
    
    joblib.dump(xgb_model, model_path)
    joblib.dump(encoders, encoders_path)
    
    print(f"\nSaved best model to {model_path}")
    print(f"Saved label encoders to {encoders_path}")

if __name__ == "__main__":
    train_models()
