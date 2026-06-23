import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_dataset(num_records=7500):
    commodities = [
        "Tomato", "Onion", "Potato", "Banana", "Apple", "Mango", "Cabbage", "Carrot", "Brinjal",
        "Grapes", "Orange", "Papaya", "Pomegranate", "Watermelon", "Spinach", "Cauliflower", "Garlic", "Ginger", "Green Chilli"
    ]
    
    locations = {
        "Andhra Pradesh": ["West Godavari", "East Godavari", "Krishna", "Guntur", "Visakhapatnam"],
        "Telangana": ["Hyderabad", "Ranga Reddy", "Medchal", "Warangal", "Nizamabad"],
        "Karnataka": ["Bangalore Urban", "Mysore", "Hubli", "Mangalore", "Belgaum"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"]
    }
    
    # Base price mapping (average modal price logic) per kg
    base_prices = {
        "Tomato": 25, "Onion": 30, "Potato": 20, "Banana": 40, "Apple": 120, 
        "Mango": 80, "Cabbage": 20, "Carrot": 35, "Brinjal": 30,
        "Grapes": 90, "Orange": 60, "Papaya": 30, "Pomegranate": 150, "Watermelon": 20,
        "Spinach": 15, "Cauliflower": 25, "Garlic": 180, "Ginger": 120, "Green Chilli": 50
    }
    
    data = []
    
    start_date = datetime(2023, 1, 1)
    
    for _ in range(num_records):
        # Date
        days_offset = random.randint(0, 365 * 2) # Over two years
        date = start_date + timedelta(days=days_offset)
        
        commodity = random.choice(commodities)
        state = random.choice(list(locations.keys()))
        district = random.choice(locations[state])
        
        # Determine Market as District + " Main Market"
        market = f"{district} Main Market"
        
        # Weather simulation
        # Temperature roughly based on month
        month = date.month
        if month in [3, 4, 5, 6]:
            temp = random.uniform(28, 42)
            rainfall = random.uniform(0, 50)
            humidity = random.uniform(30, 60)
        elif month in [7, 8, 9, 10]:
            temp = random.uniform(24, 34)
            rainfall = random.uniform(50, 200) # Monsoon
            humidity = random.uniform(60, 95)
        else:
            temp = random.uniform(15, 28)
            rainfall = random.uniform(0, 20)
            humidity = random.uniform(40, 70)
            
        # Price adjustments based on weather and commodity
        base_price = base_prices[commodity]
        
        # Extreme weather increases price
        price_multiplier = 1.0
        if rainfall > 150:
            if commodity in ["Tomato", "Onion", "Spinach", "Green Chilli"]:
                price_multiplier += 0.4 # Heavy rain ruins delicate crops
            else:
                price_multiplier += 0.2
        if temp > 38:
            if commodity in ["Cabbage", "Cauliflower", "Spinach"]:
                price_multiplier += 0.3
            elif commodity in ["Watermelon", "Mango"]:
                price_multiplier -= 0.1 # High temp might be good/reduce price slightly for summer fruits
            else:
                price_multiplier += 0.15
            
        # Random noise
        price_multiplier *= random.uniform(0.8, 1.3)
        
        modal_price = int(base_price * price_multiplier)
        min_price = int(modal_price * random.uniform(0.85, 0.95))
        max_price = int(modal_price * random.uniform(1.05, 1.15))
        
        data.append([
            date.strftime("%Y-%m-%d"), commodity, state, district, market,
            min_price, max_price, modal_price, temp, rainfall, humidity
        ])
        
    df = pd.DataFrame(data, columns=[
        "Date", "Commodity", "State", "District", "Market", 
        "Minimum Price", "Maximum Price", "Modal Price", 
        "Temperature", "Rainfall", "Humidity"
    ])
    
    # Sort by date
    df = df.sort_values(by="Date").reset_index(drop=True)
    import os
    save_path = os.path.join(os.path.dirname(__file__), "agricultural_data.csv")
    df.to_csv(save_path, index=False)
    print(f"Dataset generated successfully: {save_path}")

if __name__ == "__main__":
    generate_dataset()
