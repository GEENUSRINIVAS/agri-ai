# AgriPredict AI - Quick Start & Practical Exploration Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Open PowerShell & Navigate to Project
```powershell
# Open PowerShell and navigate to project directory
cd d:\srinu\mca_project
```

**Expected Output:**
```
PS D:\srinu\mca_project>
```

---

## 📋 Step 2: Check Python Installation

```powershell
python --version
```

**Expected Output:**
```
Python 3.x.x
```

⚠️ **If Python not found:**
- Install from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

---

## 🔧 Step 3: Create Virtual Environment (Optional but Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

**Expected Output:**
```
(venv) PS D:\srinu\mca_project>
```

⚠️ **If activation fails**, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📦 Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

**This will install:**
- Flask (web framework)
- SQLAlchemy (database)
- XGBoost (ML model)
- pandas, numpy (data processing)
- scikit-learn (ML tools)
- And others...

**Expected Output:**
```
Successfully installed Flask-3.x.x Flask-Login-0.x.x Flask-SQLAlchemy-3.x.x ...
```

⏱️ **Takes 2-3 minutes**

---

## 📊 Step 5: Generate Training Data

```powershell
# Navigate to models folder
cd models

# Generate synthetic dataset
python generate_data.py
```

**Expected Output:**
```
Dataset with 7500 records generated successfully!
Saved to: agricultural_data.csv
```

**What it creates:**
- `agricultural_data.csv` (7,500 rows of agricultural data)
- Includes commodity prices, weather data, locations

**File created:** `models\agricultural_data.csv` ✅

---

## 🤖 Step 6: Train Machine Learning Models

```powershell
# Train XGBoost model
python train.py
```

**Expected Output:**
```
Training models...
Linear Regression R2: 0.8234
Random Forest Regressor R2: 0.9123
XGBoost Regressor R2: 0.9456

Saved best model to C:\...\models\xgboost_model.pkl
Saved label encoders to C:\...\models\label_encoders.pkl
```

**Files created:**
- ✅ `models\xgboost_model.pkl` (ML model)
- ✅ `models\label_encoders.pkl` (encoding rules)

⏱️ **Takes 30-60 seconds**

---

## 🗄️ Step 7: Initialize Database

```powershell
# Go back to project root
cd ..

# Open Python shell
python
```

**Inside Python Shell, type:**
```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Database created successfully!")
exit()
```

**Expected Output:**
```
Database created successfully!
>>>
```

**File created:** ✅ `instance\agricultural_db.sqlite3` (SQLite database)

---

## ▶️ Step 8: Start the Application

```powershell
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server. Do not use it in production.
 * Press CTRL+C to quit
```

✅ **Application is now running!**

---

## 🌐 Step 9: Open Website in Browser

**Copy and paste in your browser's address bar:**
```
http://localhost:5000
```

Or click the link shown in terminal.

**You should see:** 
- Red/Pink gradient background
- "AgriPredict AI" logo
- Login form
- Link to register

---

## 👤 Step 10: Create User Account & Login

### Register New Account:
1. Click **"Create an account"** link (bottom of login page)
2. Fill in the form:
   - **Name:** Any name (e.g., "John Farmer")
   - **Email:** Any unique email (e.g., "john@example.com")
   - **Password:** Any password (e.g., "password123")
3. Click **"Sign Up"** button
4. You'll be redirected to login page

### Login:
1. Enter your email and password
2. Click **"Sign In"**
3. You'll be redirected to main dashboard

---

## 🎯 Step 11: Explore the Dashboard

### You should see:
```
LEFT SIDEBAR                    MAIN CONTENT AREA
├─ AgriPredict AI Logo         ├─ Top Bar (with title)
├─ User Profile                ├─ Module Content
├─ Navigation Menu             │  (Changes based on selection)
│  ├─ Overview (default)       │
│  ├─ Prediction               │
│  ├─ Profit Calculator        │
│  ├─ Market Recommendation    │
│  └─ Tools                    │
├─ Language Selector (🌐)      │
└─ Logout Button               └─ Search/Controls
```

---

## 📈 Step 12: Make Your First Price Prediction

### Navigate to Prediction Module:
1. Click **"Prediction"** in the left sidebar (brain icon 🧠)
2. You'll see a form with:
   - **Commodity** (dropdown)
   - **State** (dropdown)
   - **District** (dropdown)
   - **Predict** button

### Fill the Form:
1. **Select Commodity:** "Tomato"
2. **Select State:** "Karnataka"
3. **Select District:** "Bangalore Urban"
4. Click **"Predict Price"** button

### Results Appear (Below the form):
```
📈 PREDICTION RESULTS

Current Price: ₹25.50
Predicted Price: ₹28.75
Trend: Increasing ↗

Price Change: +12.7%

WEATHER INFO
Temperature: 30.2°C
Humidity: 55%
Rainfall: 25mm

ADVISORY
"📈 Tomato prices are expected to increase moderately (by ~12.7%) 
due to monsoon rainfall affecting crop supply. Farmers are advised 
to hold their Tomato stock and sell next week for higher returns..."

MARKET RECOMMENDATIONS
┌─────────────────────────────┐
│ District      │ Price       │
├─────────────────────────────┤
│ Mysore        │ ₹29.50      │ ← BEST
│ Bangalore     │ ₹28.75      │ (Your location)
│ Hubli         │ ₹27.80      │
└─────────────────────────────┘
```

---

## 🌍 Step 13: Try Other Commodities

### Try different predictions:
1. **Apple in Telangana, Hyderabad**
2. **Mango in Maharashtra, Mumbai**
3. **Onion in Andhra Pradesh, Guntur**
4. **Potato in Tamil Nadu, Chennai**

### Observe Patterns:
- Different commodities have different price trends
- Weather affects prices (rain increases perishables, decreases storage crops)
- Different markets have different prices
- Advisory changes based on commodity type

---

## 💰 Step 14: Use Profit Calculator

### Navigate to Profit Calculator:
1. Click **"Profit Calculator"** in sidebar (📊 icon)
2. Fill in:
   - **Quantity (kg):** 1000
   - **Selling Price (₹/kg):** 28.75 (from prediction)
   - **Transport Cost (₹):** 2000
   - **Market Fees (₹):** 500
   - **Other Expenses (₹):** 1000
3. Click **"Calculate"**

### System calculates:
```
Total Revenue: ₹28,750
Total Expenses: ₹3,500
Net Profit: ₹25,250
Profit Margin: 87.8%
```

---

## 🌐 Step 15: Change Language

### Switch to Different Language:
1. Click **Language Selector** (🌐 icon):
   - Top right of navbar OR
   - Left sidebar in "Tools" section
2. Choose language:
   - 🇬🇧 English
   - 🇮🇳 తెలుగు (Telugu)
   - 🇮🇳 हिंदी (Hindi)
   - 🇮🇳 தமிழ் (Tamil)
   - 🇮🇳 ಕನ್ನಡ (Kannada)

### What changes:
- All UI labels update instantly
- Commodity names translated
- State/district names translated
- Button text translated
- Advisory text remains in English (can be extended)

### Language is saved:
- Your choice is remembered even after you close the browser!

---

## 🏡 Step 16: View Overview Module

### Click "Overview" in sidebar:
You'll see:
- **System Statistics:**
  - Total Commodities: 19
  - Available States: 5
  - Total Districts: 25
  - ML Model Accuracy: 94.56% (R² score)
  
- **Quick Start Cards:**
  - About the system
  - How to use guide
  - Key features

- **Recent Predictions** (if any)

---

## 📊 Step 17: Export Results

### Generate PDF Report:
```powershell
python generate_pdf.py
```

**Creates:** Professional PDF with predictions, charts, and recommendations

### Generate PowerPoint:
```powershell
python generate_ppt.py
```

**Creates:** Professional presentation with prediction results

---

## 🧪 Step 18: Test Prediction Engine

### Run test script:
```powershell
python test_predict.py
```

**Output:**
```
Response Data: {...json prediction data...}
```

---

## 🔍 Step 19: Validate Language Files

### Check if all translations are complete:
```powershell
python validate_lang.py
```

**Output:**
```
en.json: OK (150 keys)
te.json: OK (150 keys)
hi.json: OK (150 keys)
ta.json: OK (150 keys)
kn.json: OK (150 keys)
```

---

## 🔴 STOP the Application

When you want to stop the website:
```powershell
# In the terminal where app.py is running, press:
CTRL + C
```

**Expected Output:**
```
Keyboard interrupt received, shutting down.
 * Press CTRL+C again to force quit
```

---

## 🔄 Restart Application

```powershell
python app.py
```

Then go to `http://localhost:5000` again in browser

---

## 📱 Test on Mobile/Different Screen Sizes

1. Open Developer Tools: Press **F12** in browser
2. Click device icon (top-left corner)
3. Select **iPhone**, **iPad**, or **Android**
4. Website should be responsive and work on all sizes

---

## 🐛 Troubleshooting

### Issue 1: "Address already in use"
```powershell
# Kill the process using port 5000
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process
```

### Issue 2: "Module not found" error
```powershell
# Make sure you installed requirements
pip install -r requirements.txt
```

### Issue 3: Database errors
```powershell
# Delete old database and recreate
Remove-Item instance\agricultural_db.sqlite3
python
# Then inside Python:
from app import app, db
with app.app_context():
    db.create_all()
exit()
```

### Issue 4: Models not found
```powershell
# Make sure you trained the models
cd models
python generate_data.py
python train.py
cd ..
```

### Issue 5: Port 5000 is busy
```powershell
# Use different port
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = 1
python -c "from app import app; app.run(port=5001)"
```

Then access: `http://localhost:5001`

---

## 📸 Expected Screenshots

### Login Page
```
────────────────────────────────────────
│        AgriPredict AI  🌿           │
│                                    │
│  Welcome Back                      │
│  Sign in to access price predictions
│                                    │
│  Email: [_______________]          │
│  Password: [_______________]       │
│                                    │
│  [     Sign In     ]               │
│                                    │
│  Don't have account? Create one    │
────────────────────────────────────────
```

### Dashboard
```
┌─────────────────────────────────────┐
│ ☰  ☁️ OVERVIEW                      │
├──────────────┬──────────────────────┤
│ 🌿           │                      │
│ AgriPredict  │   OVERVIEW           │
│ AI           │   ═══════════════    │
│              │                      │
│ Overview 🏠  │   📊 Statistics      │
│ Predict 🧠   │   ├─ 19 Commodities │
│ Profit 📊    │   ├─ 5 States       │
│ Market 🗺️    │   ├─ 25 Districts   │
│ Tools ⚙️     │   └─ 94.56% Accuracy│
│              │                      │
│ 🌐 English   │   🎯 Quick Start    │
│ 🚪 Logout    │   ├─ Select crop    │
└──────────────┴──────────────────────┘
```

### Prediction Results
```
┌─────────────────────────────────────┐
│ PREDICTION RESULTS                 │
│ ═════════════════════════════════   │
│                                    │
│ Commodity: Tomato                  │
│ Location: Bangalore Urban, Karnataka
│                                    │
│ Current Price: ₹25.50              │
│ Predicted Price: ₹28.75 📈         │
│ Trend: INCREASING                  │
│ Change: +12.7%                     │
│                                    │
│ WEATHER                            │
│ Temperature: 30.2°C                │
│ Humidity: 55%                      │
│ Rainfall: 25mm                     │
│                                    │
│ ADVISORY                           │
│ "Tomato prices expected to rise... │
│  Hold stock and sell next week..."  │
│                                    │
│ BEST MARKETS                       │
│ 1. Mysore (₹29.50) ★               │
│ 2. Bangalore (₹28.75) ●            │
│ 3. Hubli (₹27.80)                  │
└─────────────────────────────────────┘
```

---

## 📋 Complete Checklist

- ✅ Navigate to project folder
- ✅ Install dependencies
- ✅ Generate training data
- ✅ Train ML models
- ✅ Initialize database
- ✅ Start Flask app
- ✅ Open browser to localhost:5000
- ✅ Register new account
- ✅ Login
- ✅ Make price prediction
- ✅ View results
- ✅ Check market recommendations
- ✅ Try profit calculator
- ✅ Change language
- ✅ Logout

---

## 🎓 Learning Path

**Beginner:**
1. Just explore the interface
2. Try 2-3 price predictions
3. Compare different commodities
4. Change language

**Intermediate:**
1. Understand the prediction logic
2. Check market comparisons
3. Use profit calculator
4. Export PDF/PPT reports

**Advanced:**
1. Read the code in `app.py`
2. Understand ML model training
3. Modify the advisory messages
4. Add new commodities/states
5. Integrate real weather API

---

## 📞 Quick Commands Reference

```powershell
# Start application
python app.py

# Train models
cd models
python train.py
cd ..

# Generate data
cd models
python generate_data.py
cd ..

# Test prediction
python test_predict.py

# Validate translations
python validate_lang.py

# Generate PDF
python generate_pdf.py

# Generate PowerPoint
python generate_ppt.py

# Stop app (in terminal running app.py)
CTRL + C

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate
```

---

## 🎯 What Each Feature Does

| Feature | What It Does | Location |
|---------|------------|----------|
| **Prediction** | Predicts commodity price for next week | Sidebar → Prediction 🧠 |
| **Advisory** | Gives smart recommendation based on weather & trend | Below prediction results |
| **Market Comparison** | Shows prices in nearby markets | In prediction results |
| **Profit Calculator** | Calculates net profit from sales | Sidebar → Profit 📊 |
| **Language Switcher** | Changes UI language (not advisory yet) | Top-right or sidebar 🌐 |
| **Overview** | Shows system stats and info | Sidebar → Overview 🏠 |
| **PDF Export** | Generates downloadable PDF report | Run generate_pdf.py |
| **PPT Export** | Generates PowerPoint presentation | Run generate_ppt.py |

---

## 🚀 Next Advanced Steps

After you're comfortable with the basics:

1. **Add Real Weather API**
   - Get API key from OpenWeatherMap
   - Replace random weather generation

2. **Enable Password Hashing**
   - Implement security improvements
   - Use werkzeug for password hashing

3. **Add More Commodities/States**
   - Extend the datasets
   - Add new regions

4. **Deploy to Cloud**
   - Use Heroku, AWS, or Azure
   - Make it accessible online

5. **Add User Dashboard History**
   - Show past predictions
   - Track accuracy

---

## 📞 Support Commands

If something goes wrong:

```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Reinstall all packages
pip install -r requirements.txt --force-reinstall

# Check port 5000 status
netstat -ano | findstr :5000

# Kill process on port 5000
taskkill /PID <PID> /F
```

---

## ✅ You're All Set!

Now you have:
- ✅ Running web application
- ✅ User authentication system
- ✅ Working price predictions
- ✅ Market recommendations
- ✅ Multilingual interface
- ✅ Profit calculator
- ✅ Export functionality

**Enjoy exploring AgriPredict AI! 🌾🚀**
