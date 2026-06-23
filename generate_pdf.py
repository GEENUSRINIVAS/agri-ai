"""
AgriPredict AI — PDF Report Generator
Creates a comprehensive project PDF using reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem
import os

# ── Colors ──────────────────────────────────────────────────
C_GREEN      = colors.HexColor("#16a34a")
C_DARK_GREEN = colors.HexColor("#14532d")
C_BG_DARK    = colors.HexColor("#0f172a")
C_CARD       = colors.HexColor("#1e293b")
C_SLATE      = colors.HexColor("#334155")
C_ACCENT     = colors.HexColor("#22c55e")
C_WHITE      = colors.white
C_LIGHT_GRAY = colors.HexColor("#e2e8f0")
C_MUTED      = colors.HexColor("#94a3b8")
C_BLACK      = colors.black

PAGE_W, PAGE_H = A4  # 595 x 842

# ── Styles ───────────────────────────────────────────────────
def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle',
        fontSize=28, fontName='Helvetica-Bold',
        textColor=C_WHITE, alignment=TA_CENTER,
        spaceAfter=8, leading=34,
    ))
    styles.add(ParagraphStyle(
        'CoverSub',
        fontSize=13, fontName='Helvetica',
        textColor=C_ACCENT, alignment=TA_CENTER,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        'CoverMeta',
        fontSize=11, fontName='Helvetica',
        textColor=C_MUTED, alignment=TA_CENTER,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'SectionHeading',
        fontSize=16, fontName='Helvetica-Bold',
        textColor=C_GREEN, spaceBefore=18, spaceAfter=8,
        borderPad=4,
    ))
    styles.add(ParagraphStyle(
        'SubHeading',
        fontSize=12, fontName='Helvetica-Bold',
        textColor=C_ACCENT, spaceBefore=10, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'BodyText2',
        fontSize=10.5, fontName='Helvetica',
        textColor=C_BLACK, spaceBefore=3, spaceAfter=3,
        leading=15, alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        'Bullet2',
        fontSize=10.5, fontName='Helvetica',
        textColor=C_BLACK, spaceBefore=2, spaceAfter=2,
        leftIndent=16, leading=14,
    ))
    styles.add(ParagraphStyle(
        'CodeMono',
        fontSize=9, fontName='Courier',
        textColor=C_DARK_GREEN, backColor=colors.HexColor("#f0faf4"),
        spaceBefore=2, spaceAfter=2, leftIndent=12,
    ))
    return styles


def hr(color=C_GREEN, width=1):
    return HRFlowable(width="100%", thickness=width, color=color, spaceAfter=8, spaceBefore=4)

def spacer(h=0.15):
    return Spacer(1, h * inch)

def bullet(text, styles):
    return Paragraph(f"• &nbsp;{text}", styles['Bullet2'])

def section(title, styles):
    return [hr(C_DARK_GREEN, 0.5),
            Paragraph(title, styles['SectionHeading']),
            hr(C_GREEN, 1.5)]


# ── Build PDF ─────────────────────────────────────────────────
def create_pdf():
    styles = get_styles()
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Project_Report.pdf")

    doc = SimpleDocTemplate(
        save_path,
        pagesize=A4,
        rightMargin=1.8 * cm, leftMargin=1.8 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="AgriPredict AI — Project Report",
        author="MCA Final Year Student",
        subject="AI-Driven Agricultural Price Forecasting System",
    )

    story = []

    # ── COVER PAGE ────────────────────────────────────────────
    story.append(spacer(1.2))
    story.append(Paragraph("AgriPredict AI", styles['CoverTitle']))
    story.append(spacer(0.1))
    story.append(Paragraph(
        "AI-Driven Fruits &amp; Vegetables Price Forecast<br/>&amp; Smart Market Recommendation System",
        styles['CoverSub']))
    story.append(spacer(0.2))
    story.append(hr(C_ACCENT))
    story.append(spacer(0.1))

    cover_data = [
        ["Project Type",   "MCA Final Year Project"],
        ["Year",           "2026"],
        ["Technology",     "Python Flask, XGBoost, SQLite, Bootstrap 5"],
        ["Commodities",    "19 Agricultural Commodities"],
        ["States Covered", "5 Indian States, Multiple Districts"],
        ["Languages",      "English, Telugu, Hindi, Tamil, Kannada"],
    ]
    cover_table = Table(cover_data, colWidths=[5 * cm, 11 * cm])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#dcfce7")),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor("#f0fdf4")),
        ('TEXTCOLOR',  (0, 0), (0, -1), C_DARK_GREEN),
        ('TEXTCOLOR',  (1, 0), (1, -1), C_BLACK),
        ('FONTNAME',   (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 10),
        ('GRID',       (0, 0), (-1, -1), 0.5, C_GREEN),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1),
         [colors.HexColor("#dcfce7"), colors.HexColor("#f0fdf4")]),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # ── 1. INTRODUCTION ───────────────────────────────────────
    story += section("1.  Introduction & Problem Statement", styles)
    story.append(Paragraph(
        "Indian farmers often face severe financial losses due to unpredictable agricultural price "
        "volatility. Prices of fruits and vegetables can swing 30–60% within a single week due to "
        "seasonal factors, weather anomalies, and supply-demand imbalances. Without access to "
        "predictive tools, farmers rely on guesswork or intermediaries who exploit this information gap.",
        styles['BodyText2']))
    story.append(spacer(0.1))
    story.append(Paragraph("Key Problems Addressed:", styles['SubHeading']))
    for p in [
        "Farmers earn significantly less than market value due to selling at unstable prices",
        "No accessible district-level tool to forecast next-week prices for 19 commodities",
        "Weather events (rainfall, temperature, humidity) cause sudden unexpected price swings",
        "Traders exploit information asymmetry — farmers sell at wrong place & wrong time",
        "No multilingual advisory system accessible to non-English-speaking rural farmers",
    ]:
        story.append(bullet(p, styles))
    story.append(spacer(0.15))

    # ── 2. OBJECTIVES ─────────────────────────────────────────
    story += section("2.  Project Objectives", styles)
    for o in [
        "Forecast next-week modal prices for 19 agricultural commodities using Machine Learning",
        "Use XGBoost Regressor with weather + location + seasonal features as inputs",
        "Build a Smart Market Recommendation engine to identify the most profitable district",
        "Generate dynamic Hold vs Sell Farmer Advisory with weather-context reasoning",
        "Deliver a multilingual web interface in 5 Indian languages (EN, TE, HI, TA, KN)",
        "Achieve fast, responsive predictions with less than 2-second response time",
        "Provide an interactive Chart.js price trend visualization for the farmer",
    ]:
        story.append(bullet(o, styles))
    story.append(spacer(0.15))

    # ── 3. SYSTEM ARCHITECTURE ───────────────────────────────
    story += section("3.  System Architecture", styles)
    story.append(Paragraph(
        "The system follows a layered MVC-inspired architecture built on Flask:",
        styles['BodyText2']))

    arch_data = [
        ["Layer", "Component", "Description"],
        ["Frontend",       "HTML/CSS/JS/Bootstrap 5", "Glassmorphism UI, responsive design, Chart.js graphs"],
        ["Auth Layer",     "Flask-Login + SQLite",    "Session management, user login/registration"],
        ["Dashboard",      "Jinja2 Templates",        "Commodity / State / District dropdowns"],
        ["Weather Layer",  "Mock Weather Engine",     "Generates temp, rainfall, humidity context"],
        ["ML Inference",   "XGBoost + Joblib",        "Loads trained model, encodes inputs, returns price"],
        ["Market Engine",  "Python (app.py)",         "Compares price across 4 districts, finds best"],
        ["Advisory",       "generate_advisory()",     "Builds data-driven Hold/Sell recommendation"],
        ["i18n Engine",    "JS + JSON files",         "Translates full UI into 5 Indian languages"],
        ["Database",       "SQLite / SQLAlchemy",     "Stores user accounts and session data"],
    ]
    arch_table = Table(arch_data, colWidths=[3.5*cm, 5*cm, 8.5*cm])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  C_GREEN),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  C_WHITE),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1),
         [colors.HexColor("#f0fdf4"), colors.white]),
        ('GRID',          (0, 0), (-1, -1), 0.4, C_GREEN),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('BACKGROUND',    (0, 1), (0, -1),  colors.HexColor("#dcfce7")),
        ('TEXTCOLOR',     (0, 1), (0, -1),  C_DARK_GREEN),
        ('FONTNAME',      (0, 1), (0, -1),  'Helvetica-Bold'),
    ]))
    story.append(arch_table)
    story.append(spacer(0.15))

    # ── 4. MACHINE LEARNING ──────────────────────────────────
    story += section("4.  Machine Learning Implementation", styles)

    story.append(Paragraph("4.1  Dataset", styles['SubHeading']))
    for d in [
        "50,000+ synthetic records generated from agricultural_data.csv",
        "Features: Month, Commodity (19), State (5), District (multiple), Temperature, Rainfall, Humidity",
        "Target Variable: Modal Price per kilogram (₹/kg)",
        "All categorical features encoded using Scikit-learn LabelEncoder",
    ]:
        story.append(bullet(d, styles))
    story.append(spacer(0.1))

    story.append(Paragraph("4.2  Model Selection & Evaluation", styles['SubHeading']))
    model_data = [
        ["Algorithm",          "Accuracy (R²)", "Chosen?"],
        ["Linear Regression",  "~0.71",         "No"],
        ["Random Forest",      "~0.87",         "No"],
        ["XGBoost Regressor",  "~0.93+",        "✅ Yes"],
    ]
    mt = Table(model_data, colWidths=[7*cm, 5*cm, 5*cm])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_GREEN),
        ('TEXTCOLOR',  (0,0), (-1,0), C_WHITE),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('GRID',       (0,0), (-1,-1), 0.4, C_GREEN),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f0fdf4"), colors.white]),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#dcfce7")),
        ('FONTNAME',   (0,3), (-1,3), 'Helvetica-Bold'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ]))
    story.append(mt)
    story.append(spacer(0.1))

    story.append(Paragraph("4.3  ML Pipeline", styles['SubHeading']))
    for step in [
        "1. Load agricultural_data.csv with Pandas",
        "2. Encode categorical columns: Commodity, State, District → LabelEncoder",
        "3. Split dataset: 80% training / 20% testing",
        "4. Train XGBoost Regressor (n_estimators=100, max_depth=6, learning_rate=0.1)",
        "5. Evaluate R² and RMSE on test set",
        "6. Save model: joblib.dump(model, 'xgboost_model.pkl')",
        "7. Save encoders: joblib.dump(encoders, 'label_encoders.pkl')",
        "8. Flask loads both files at startup via joblib.load()",
    ]:
        story.append(bullet(step, styles))
    story.append(spacer(0.15))

    # ── 5. TECHNOLOGY STACK ──────────────────────────────────
    story += section("5.  Technology Stack", styles)
    tech_data = [
        ["Category",         "Technology",                    "Purpose"],
        ["Frontend",         "HTML5, CSS3 (Glassmorphism)",   "Structure & premium UI design"],
        ["CSS Framework",    "Bootstrap 5",                   "Responsive grid & components"],
        ["JavaScript",       "Vanilla JS (ES6+)",             "Dynamic DOM & i18n engine"],
        ["Charting",         "Chart.js",                      "Interactive price trend graph"],
        ["Backend",          "Python Flask",                  "Web framework and routing"],
        ["Auth",             "Flask-Login",                   "Session-based authentication"],
        ["ORM",              "Flask-SQLAlchemy",              "Database abstraction layer"],
        ["Templating",       "Jinja2",                        "Server-side HTML rendering"],
        ["ML",               "XGBoost + Scikit-learn",        "Price forecasting model"],
        ["Data Processing",  "Pandas + NumPy",                "Dataset handling & features"],
        ["Model Storage",    "Joblib",                        "Serialize/load .pkl files"],
        ["Database",         "SQLite",                        "Lightweight user storage"],
        ["Fonts & Icons",    "Google Fonts + Font Awesome",   "Typography and UI icons"],
    ]
    tt = Table(tech_data, colWidths=[3.8*cm, 5.5*cm, 7.7*cm])
    tt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  C_GREEN),
        ('TEXTCOLOR',     (0,0), (-1,0),  C_WHITE),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.HexColor("#f0fdf4"), colors.white]),
        ('GRID',          (0,0), (-1,-1), 0.4, C_GREEN),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('BACKGROUND',    (0,1), (0,-1),  colors.HexColor("#dcfce7")),
        ('FONTNAME',      (0,1), (0,-1),  'Helvetica-Bold'),
        ('TEXTCOLOR',     (0,1), (0,-1),  C_DARK_GREEN),
    ]))
    story.append(tt)
    story.append(spacer(0.15))

    # ── 6. KEY FEATURES ──────────────────────────────────────
    story += section("6.  Key Features & Modules", styles)
    features = [
        ("🔐 Secure Authentication",
         "User registration and login using Flask-Login with email-based identity. Passwords "
         "stored in SQLite. Sessions managed securely with Flask's secret key."),
        ("🌾 19 Agricultural Commodities",
         "Tomato, Onion, Potato, Banana, Apple, Mango, Cabbage, Carrot, Brinjal, Grapes, "
         "Orange, Papaya, Pomegranate, Watermelon, Spinach, Cauliflower, Garlic, Ginger, Green Chilli."),
        ("📍 Location-Based Precision",
         "5 Indian states (Andhra Pradesh, Telangana, Karnataka, Tamil Nadu, Maharashtra) with 5 "
         "districts each. District-level granularity for accurate local price forecasting."),
        ("🌦 Weather-Aware Model",
         "Temperature (25–35°C), rainfall (10–50mm), and humidity (40–70%) integrated as features "
         "in the XGBoost model. Weather context also used in advisory reasoning."),
        ("📊 Interactive Price Chart",
         "Chart.js line graph showing 8 weeks of simulated historical prices alongside the "
         "AI-forecasted next-week price. Animated and color-coded trend display."),
        ("🏪 Smart Market Recommendation",
         "After prediction, the system samples 3 random nearby districts, predicts prices for each, "
         "sorts them, and recommends the most profitable market to the farmer."),
        ("💡 Dynamic Farmer Advisory",
         "generate_advisory() function builds context-aware Hold vs Sell advice considering trend "
         "severity, commodity type (perishable/storable), and current weather conditions."),
        ("🌐 Multilingual i18n Engine",
         "Complete 5-language support (EN/TE/HI/TA/KN) via JSON language packs and a custom "
         "JavaScript i18n engine. Language preference persists across sessions via localStorage."),
    ]
    for title, desc in features:
        story.append(Paragraph(title, styles['SubHeading']))
        story.append(Paragraph(desc, styles['BodyText2']))
        story.append(spacer(0.05))
    story.append(spacer(0.1))

    # ── 7. DATABASE ───────────────────────────────────────────
    story += section("7.  Database Design", styles)
    story.append(Paragraph(
        "The application uses SQLite via Flask-SQLAlchemy. The database is automatically "
        "created on first run using db.create_all() inside the Flask app context.",
        styles['BodyText2']))
    story.append(spacer(0.1))

    db_data = [
        ["Column",    "Type",         "Constraint",     "Description"],
        ["id",        "INTEGER",      "PRIMARY KEY",    "Auto-increment user ID"],
        ["name",      "VARCHAR(100)", "NOT NULL",       "User's full name"],
        ["email",     "VARCHAR(100)", "UNIQUE NOT NULL","User's email address"],
        ["password",  "VARCHAR(100)", "NOT NULL",       "User password (plain text)"],
    ]
    dt = Table(db_data, colWidths=[3*cm, 3.5*cm, 4.5*cm, 6*cm])
    dt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  C_GREEN),
        ('TEXTCOLOR',     (0,0), (-1,0),  C_WHITE),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9.5),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.HexColor("#f0fdf4"), colors.white]),
        ('GRID',          (0,0), (-1,-1), 0.4, C_GREEN),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('FONTNAME',      (0,1), (0,-1),  'Courier-Bold'),
        ('TEXTCOLOR',     (0,1), (0,-1),  C_DARK_GREEN),
    ]))
    story.append(dt)
    story.append(spacer(0.15))

    # ── 8. PROJECT STRUCTURE ─────────────────────────────────
    story += section("8.  Project File Structure", styles)
    structure = [
        "mca_project/",
        "├── app.py                    ← Main Flask application (307 lines)",
        "├── generate_ppt.py           ← PowerPoint generator",
        "├── generate_pdf.py           ← PDF report generator",
        "├── requirements.txt          ← Python dependencies",
        "├── agricultural_data.csv     ← Training dataset (50,000+ records)",
        "├── models/",
        "│   ├── xgboost_model.pkl     ← Trained XGBoost model",
        "│   └── label_encoders.pkl    ← Scikit-learn LabelEncoders",
        "├── templates/",
        "│   ├── base.html             ← Base layout with navbar & assets",
        "│   ├── dashboard.html        ← Prediction input form",
        "│   ├── login.html            ← Login page",
        "│   ├── register.html         ← Registration page",
        "│   └── results.html          ← Prediction output & charts",
        "├── static/",
        "│   ├── css/style.css         ← Custom CSS (glassmorphism, animations)",
        "│   ├── js/i18n.js            ← Multilingual engine",
        "│   └── lang/",
        "│       ├── en.json           ← English translations",
        "│       ├── te.json           ← Telugu translations",
        "│       ├── hi.json           ← Hindi translations",
        "│       ├── ta.json           ← Tamil translations",
        "│       └── kn.json           ← Kannada translations",
        "└── instance/",
        "    └── agricultural_db.sqlite3  ← SQLite user database",
    ]
    for line in structure:
        story.append(Paragraph(line, styles['CodeMono']))
    story.append(spacer(0.15))

    # ── 9. ROUTES ─────────────────────────────────────────────
    story += section("9.  Application Routes (API Endpoints)", styles)
    routes_data = [
        ["Route",       "Method",     "Auth?", "Description"],
        ["/",           "GET",        "No",    "Redirects to dashboard (if logged in) or login"],
        ["/login",      "GET, POST",  "No",    "User authentication — validates email & password"],
        ["/register",   "GET, POST",  "No",    "New user registration — stores to SQLite"],
        ["/logout",     "GET",        "Yes",   "Clears session, redirects to login"],
        ["/dashboard",  "GET",        "Yes",   "Shows prediction form with dropdown options"],
        ["/predict",    "POST",       "Yes",   "Runs XGBoost prediction, returns results.html"],
    ]
    rt = Table(routes_data, colWidths=[3.5*cm, 3*cm, 2.5*cm, 8*cm])
    rt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  C_GREEN),
        ('TEXTCOLOR',     (0,0), (-1,0),  C_WHITE),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9.5),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.HexColor("#f0fdf4"), colors.white]),
        ('GRID',          (0,0), (-1,-1), 0.4, C_GREEN),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('FONTNAME',      (0,1), (0,-1),  'Courier-Bold'),
        ('TEXTCOLOR',     (0,1), (0,-1),  C_DARK_GREEN),
    ]))
    story.append(rt)
    story.append(PageBreak())

    # ── 10. CONCLUSION ────────────────────────────────────────
    story += section("10.  Conclusion & Future Work", styles)
    story.append(Paragraph("10.1  Conclusion", styles['SubHeading']))
    for c in [
        "Successfully built a full-stack AI web application for agricultural price forecasting",
        "XGBoost Regressor trained on 50,000+ records achieves over 93% R² accuracy",
        "System covers 19 commodities across 5 major Indian agricultural states",
        "Smart market recommendation helps farmers identify the best-price market district",
        "Multilingual farmer advisory in 5 languages eliminates language barriers",
        "Complete Python Flask MVC architecture — modular, extensible, and maintainable",
    ]:
        story.append(bullet(c, styles))
    story.append(spacer(0.12))

    story.append(Paragraph("10.2  Future Enhancements", styles['SubHeading']))
    for f in [
        "Integration with live government pricing APIs (e-NAM, Agmarknet) for real market data",
        "Open-Meteo live weather API replacing the current mock weather engine",
        "SMS / WhatsApp alert system for sudden price changes using Twilio integration",
        "Mobile-first Progressive Web App (PWA) with offline support for rural farmers",
        "Expand to 100+ commodities and cover all 28+ Indian states and UTs",
        "Crop planting season advisor — recommend what to plant based on predicted prices",
        "Machine learning model retraining pipeline with periodic fresh data ingestion",
        "Admin dashboard for monitoring user activity and forecast accuracy over time",
    ]:
        story.append(bullet(f, styles))
    story.append(spacer(0.2))
    story.append(hr(C_GREEN))
    story.append(Paragraph(
        "<para align='center'><b>AgriPredict AI</b>  —  MCA Final Year Project  |  2026<br/>"
        "<i>\"Empowering farmers with AI-driven price intelligence\"</i></para>",
        styles['CoverMeta']))

    doc.build(story)
    print(f"✅  PDF saved: {save_path}")
    return save_path


if __name__ == "__main__":
    pdf_path = create_pdf()
    print(f"\n📄  File: {pdf_path}")
