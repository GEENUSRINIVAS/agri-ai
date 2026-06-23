import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mca_project_secret_key_2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///agricultural_db.sqlite3'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load ML Models
model_path = os.path.join(os.path.dirname(__file__), 'models', 'xgboost_model.pkl')
encoders_path = os.path.join(os.path.dirname(__file__), 'models', 'label_encoders.pkl')

try:
    xgb_model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    print("Machine Learning models loaded successfully.")
except Exception as e:
    print(f"Warning: Models not loaded. {e}")
    xgb_model = None
    encoders = {}

# --- Database Models ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Farmer Advisory Engine ---
def generate_advisory(commodity, trend, price_change_pct, rainfall, temp, humidity):
    """
    Generates a detailed, data-driven advisory message for farmers based on:
    - The commodity type and its weather sensitivity
    - The predicted price trend (Increasing / Decreasing)
    - The magnitude of the price change
    - Current weather conditions (rainfall, temperature, humidity)
    """

    # Classify commodity weather sensitivity
    rain_sensitive = ["Tomato", "Onion", "Spinach", "Green Chilli", "Cabbage", "Cauliflower"]
    heat_sensitive = ["Spinach", "Cabbage", "Cauliflower", "Grapes"]
    heat_loving   = ["Watermelon", "Mango", "Banana", "Papaya"]
    storable      = ["Potato", "Onion", "Garlic", "Ginger"]  # can hold stock longer

    severity = "significantly" if price_change_pct >= 15 else "moderately" if price_change_pct >= 7 else "slightly"

    # --- Build weather reason clause ---
    weather_reasons = []
    if rainfall > 120:
        weather_reasons.append("heavy rainfall disrupting transportation and field harvest")
    elif rainfall > 60:
        weather_reasons.append("moderate monsoon rainfall affecting crop supply")
    elif rainfall < 10:
        weather_reasons.append("dry weather conditions boosting outdoor market demand")

    if temp > 38 and commodity in heat_sensitive:
        weather_reasons.append(f"high temperatures ({temp:.1f}°C) stressing {commodity} crops and reducing yield")
    elif temp > 36 and commodity in heat_loving:
        weather_reasons.append(f"warm temperatures ({temp:.1f}°C) favouring {commodity} growth and increasing supply")

    if humidity > 80:
        weather_reasons.append("high humidity increasing post-harvest spoilage risk")

    weather_clause = ""
    if weather_reasons:
        weather_clause = " due to " + " and ".join(weather_reasons)

    # --- Build advisory based on trend ---
    if trend == "Increasing":
        action_advice = (
            f"Farmers are advised to hold their {commodity} stock and sell next week for higher returns."
            if commodity not in storable
            else f"Farmers can safely store {commodity} and wait for the predicted price peak before selling."
        )
        advisory = (
            f"📈 {commodity} prices are expected to increase {severity} (by ~{price_change_pct}%){weather_clause}. "
            f"{action_advice} "
            f"Traders should consider early procurement before prices rise further."
        )
    else:  # Decreasing
        if commodity in rain_sensitive and rainfall > 60:
            supply_reason = f"an oversupply of {commodity} triggered by favourable post-monsoon growing conditions"
        else:
            supply_reason = "increased market supply or reduced seasonal demand"

        action_advice = (
            f"Farmers are strongly advised to sell available {commodity} stock as soon as possible to avoid further losses."
            if price_change_pct >= 10
            else f"Farmers may consider selling current {commodity} stock in batches rather than waiting."
        )
        advisory = (
            f"📉 {commodity} prices are expected to decrease {severity} (by ~{price_change_pct}%) due to {supply_reason}{weather_clause}. "
            f"{action_advice} "
            f"Consider alternative markets or value-added processing if direct sale price is unfavorable."
        )

    return advisory

# --- Routes ---


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.password == password: # In production, use werkzeug.security password hashing
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'warning')
            return redirect(url_for('register'))
            
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Provide necessary data for the dropdowns
    commodities = [
        "Tomato", "Onion", "Potato", "Banana", "Apple", "Mango", "Cabbage", "Carrot", "Brinjal",
        "Grapes", "Orange", "Papaya", "Pomegranate", "Watermelon", "Spinach", "Cauliflower", "Garlic", "Ginger", "Green Chilli"
    ]
    # Sort for UI convenience
    commodities.sort()
    
    locations = {
        "Andhra Pradesh": ["West Godavari", "East Godavari", "Krishna", "Guntur", "Visakhapatnam"],
        "Telangana": ["Hyderabad", "Ranga Reddy", "Medchal", "Warangal", "Nizamabad"],
        "Karnataka": ["Bangalore Urban", "Mysore", "Hubli", "Mangalore", "Belgaum"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"]
    }
    
    return render_template('dashboard.html', 
                          commodities=commodities, 
                          states=list(locations.keys()),
                          locations=locations,
                          user=current_user)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    import random
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not xgb_model:
        if is_ajax:
            return jsonify({'error': 'Prediction model is not available.'}), 503
        flash("Prediction model is not available.", "danger")
        return redirect(url_for('dashboard'))

    commodity = request.form.get('commodity')
    state     = request.form.get('state')
    district  = request.form.get('district')

    temp      = random.uniform(25, 35)
    rainfall  = random.uniform(10, 50)
    humidity  = random.uniform(40, 70)
    current_month = datetime.now().month

    try:
        comm_encoded  = encoders['Commodity'].transform([commodity])[0]
        state_encoded = encoders['State'].transform([state])[0]
        dist_encoded  = encoders['District'].transform([district])[0]

        features        = np.array([[comm_encoded, state_encoded, dist_encoded, temp, rainfall, humidity, current_month]])
        predicted_price = float(xgb_model.predict(features)[0])
        current_price   = float(predicted_price * random.uniform(0.9, 1.1))

        trend            = "Increasing" if predicted_price > current_price else "Decreasing"
        price_change_pct = float(round(abs(predicted_price - current_price) / current_price * 100, 1))

        storable      = ["Potato", "Onion", "Garlic", "Ginger"]
        rain_sensitive = ["Tomato", "Onion", "Spinach", "Green Chilli", "Cabbage", "Cauliflower"]
        severity_key   = "significantly" if price_change_pct >= 15 else "moderately" if price_change_pct >= 7 else "slightly"

        if trend == "Increasing":
            adv_type = "increasing_storable" if commodity in storable else "increasing_perishable"
        else:
            adv_type = "decreasing_heavy" if (commodity in rain_sensitive and rainfall > 60) else "decreasing_normal"

        weather_key = ""
        if rainfall > 120:  weather_key = "heavy_rain"
        elif rainfall > 60: weather_key = "monsoon_rain"
        elif humidity > 80: weather_key = "high_humidity"

        advisory_data = {
            "type": adv_type,
            "severity_key": severity_key,
            "pct": round(price_change_pct, 1),
            "commodity": commodity,
            "weather_key": weather_key,
        }
        advisory_en = generate_advisory(commodity, trend, price_change_pct, rainfall, temp, humidity)

        other_districts  = [d for d in encoders['District'].classes_ if d != district]
        nearby_districts = random.sample(other_districts, min(3, len(other_districts)))
        market_prices    = []
        for d in nearby_districts:
            d_enc = encoders['District'].transform([d])[0]
            f     = np.array([[comm_encoded, state_encoded, d_enc, temp, rainfall, humidity, current_month]])
            p     = xgb_model.predict(f)[0]
            market_prices.append({"district": d, "price": round(float(p), 2), "is_selected": False})

        market_prices.append({"district": district, "price": round(float(predicted_price), 2), "is_selected": True})
        market_prices = sorted(market_prices, key=lambda x: x['price'], reverse=True)
        best_district = market_prices[0]['district']

        results = {
            "commodity": commodity,
            "district": district,
            "state": state,
            "location": f"{district}, {state}",
            "current_price": round(float(current_price), 2),
            "predicted_price": round(float(predicted_price), 2),
            "trend": trend,
            "price_change_pct": round(price_change_pct, 1),
            "temperature": round(temp, 1),
            "humidity": round(humidity, 1),
            "rainfall": round(rainfall, 1),
            "advisory": advisory_en,
            "advisory_data": advisory_data,
            "best_district": best_district,
            "market_comparisons": market_prices
        }

        # AJAX request → return JSON for inline dashboard rendering
        if is_ajax:
            return jsonify(results)

        # Classic full-page fallback
        return render_template('results.html', results=results)

    except Exception as e:
        if is_ajax:
            return jsonify({'error': str(e)}), 500
        flash(f"Error during prediction: {str(e)}", "danger")
        return redirect(url_for('dashboard'))


@app.route('/api/market_recommendation', methods=['POST'])
@login_required
def market_recommendation():
    """Standalone market recommendation API for the dashboard Market module."""
    import random
    if not xgb_model:
        return jsonify({'error': 'Model not available.'}), 503

    commodity = request.form.get('commodity')
    state     = request.form.get('state')
    district  = request.form.get('district')

    if not commodity or not state or not district:
        return jsonify({'error': 'commodity, state and district are required.'}), 400

    temp     = random.uniform(25, 35)
    rainfall = random.uniform(10, 50)
    humidity = random.uniform(40, 70)
    current_month = datetime.now().month

    try:
        comm_encoded  = encoders['Commodity'].transform([commodity])[0]
        state_encoded = encoders['State'].transform([state])[0]

        other_districts  = [d for d in encoders['District'].classes_ if d != district]
        nearby_districts = random.sample(other_districts, min(3, len(other_districts)))
        market_prices    = []

        for d in nearby_districts:
            d_enc = encoders['District'].transform([d])[0]
            f     = np.array([[comm_encoded, state_encoded, d_enc, temp, rainfall, humidity, current_month]])
            p     = xgb_model.predict(f)[0]
            market_prices.append({'district': d, 'state': state, 'price': round(float(p), 2), 'is_selected': False})

        # Add the selected district
        dist_encoded    = encoders['District'].transform([district])[0]
        features        = np.array([[comm_encoded, state_encoded, dist_encoded, temp, rainfall, humidity, current_month]])
        selected_price  = xgb_model.predict(features)[0]
        market_prices.append({'district': district, 'state': state, 'price': round(float(selected_price), 2), 'is_selected': True})

        market_prices = sorted(market_prices, key=lambda x: x['price'], reverse=True)
        return jsonify(market_prices)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug_mode)
