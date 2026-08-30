import os
import pickle
import sqlite3
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session, flash, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-opticrop-application-2026'

# Verify and initialize database on startup if db file doesn't exist
if not os.path.exists('opticrop.db'):
    init_db()

# Load model and ranges
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('crop_ranges.pkl', 'rb') as f:
        crop_ranges = pickle.load(f)
    with open('cluster_insights.pkl', 'rb') as f:
        cluster_insights = pickle.load(f)
except Exception as e:
    print(f"Error loading model assets: {e}")
    model = None
    crop_ranges = {}
    cluster_insights = {}

# Set up global user session loading
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()

# Context processor to make g.user and crops available in templates
@app.context_processor
def inject_globals():
    crops_list = sorted(list(crop_ranges.keys())) if crop_ranges else []
    return dict(crops_list=crops_list)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        role = request.form.get('role', 'Farmer')
        
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        conn = get_db_connection()
        try:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                         (username, email, hashed_password, role))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists.', 'danger')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/findyourcrop')
def findyourcrop():
    return render_template('findyourcrop.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Machine learning model is not available.'}), 500

    try:
        # Extract features
        if request.is_json:
            data = request.json
            nitrogen = float(data.get('nitrogen'))
            phosphorous = float(data.get('phosphorous'))
            potassium = float(data.get('potassium'))
            temperature = float(data.get('temperature'))
            humidity = float(data.get('humidity'))
            ph = float(data.get('ph'))
            rainfall = float(data.get('rainfall'))
        else:
            nitrogen = float(request.form.get('nitrogen'))
            phosphorous = float(request.form.get('phosphorous'))
            potassium = float(request.form.get('potassium'))
            temperature = float(request.form.get('temperature'))
            humidity = float(request.form.get('humidity'))
            ph = float(request.form.get('ph'))
            rainfall = float(request.form.get('rainfall'))
    except (ValueError, TypeError):
        error_msg = "Please provide valid numeric inputs for all environmental conditions."
        if request.is_json:
            return jsonify({'error': error_msg}), 400
        else:
            flash(error_msg, 'danger')
            return redirect(url_for('findyourcrop'))

    # Prepare features vector for prediction
    features = np.array([[nitrogen, phosphorous, potassium, temperature, humidity, ph, rainfall]])
    prediction = model.predict(features)
    predicted_crop = prediction[0]

    # Generate custom advice and recommendations for the predicted crop
    water_rec = "Medium"
    fertilizer_rec = "Standard balanced N-P-K fertilizer based on soil testing."
    
    conn = get_db_connection()
    crop_info = conn.execute('SELECT * FROM crops WHERE crop_name = ?', (predicted_crop,)).fetchone()
    if crop_info:
        water_val = crop_info['water_requirement']
        if water_val > 150:
            water_rec = "High (Requires frequent irrigation or high rainfall)"
        elif water_val < 80:
            water_rec = "Low (Drought-tolerant, minimal watering required)"
        else:
            water_rec = "Medium (Moderate regular watering)"

    # Formulate recommendations based on parameter values compared to crop mean
    recs = []
    if predicted_crop in crop_ranges:
        crop_stats = crop_ranges[predicted_crop]
        if nitrogen < crop_stats['nitrogen']['mean'] - crop_stats['nitrogen']['std']:
            recs.append("Nitrogen level is low. Add nitrogen-rich organic compost or urea fertilizer.")
        elif nitrogen > crop_stats['nitrogen']['mean'] + crop_stats['nitrogen']['std']:
            recs.append("Nitrogen level is high. Avoid excess nitrogen fertilizers to prevent vegetative growth over-activation.")
            
        if phosphorous < crop_stats['phosphorous']['mean'] - crop_stats['phosphorous']['std']:
            recs.append("Phosphorous level is low. Incorporate bone meal or superphosphate.")
            
        if potassium < crop_stats['potassium']['mean'] - crop_stats['potassium']['std']:
            recs.append("Potassium level is low. Add muriate of potash or potassium sulfate.")
            
        if ph < 5.5:
            recs.append("Soil is acidic. Application of agricultural lime (calcium carbonate) can help raise pH.")
        elif ph > 7.5:
            recs.append("Soil is alkaline. Add organic matter, peat moss, or sulfur to lower soil pH.")
    
    if not recs:
        recs.append("Soil nutrient levels and environmental conditions are highly optimal for this crop. Maintain current soil health.")

    recommendation_text = " ".join(recs)
    summary_text = f"Recommendation generated for {predicted_crop} with environmental conditions N:{nitrogen}, P:{phosphorous}, K:{potassium}, Temp:{temperature}°C, Hum:{humidity}%, pH:{ph}, Rain:{rainfall}mm."

    # Save to SQLite (Scenario 1 & 2 integration)
    try:
        user_id = session.get('user_id')  # Will be None if guest
        
        # 1. Insert SoilData
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO soil_data (nitrogen, phosphorous, potassium, temperature, humidity, ph, rainfall, season, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nitrogen, phosphorous, potassium, temperature, humidity, ph, rainfall, crop_info['season'] if crop_info else 'Unknown', user_id))
        soil_id = cursor.lastrowid

        # 2. Get crop_id and model_id
        crop_row = conn.execute('SELECT crop_id FROM crops WHERE crop_name = ?', (predicted_crop,)).fetchone()
        crop_id = crop_row['crop_id'] if crop_row else None

        model_row = conn.execute('SELECT model_id FROM ml_models WHERE model_name = ?', ('Logistic Regression',)).fetchone()
        model_id = model_row['model_id'] if model_row else None

        # 3. Insert Prediction
        cursor.execute('''
            INSERT INTO predictions (soil_id, crop_id, model_id, confidence_score)
            VALUES (?, ?, ?, ?)
        ''', (soil_id, crop_id, model_id, 0.94))
        prediction_id = cursor.lastrowid

        # 4. Insert Report
        cursor.execute('''
            INSERT INTO reports (prediction_id, summary, recommendations)
            VALUES (?, ?, ?)
        ''', (prediction_id, summary_text, recommendation_text))
        
        conn.commit()
    except Exception as db_err:
        print(f"Database logging error: {db_err}")
    finally:
        conn.close()

    result_data = {
        'crop': predicted_crop.upper(),
        'water': water_rec,
        'fertilizer': fertilizer_rec,
        'advice': recs,
        'nitrogen': nitrogen,
        'phosphorous': phosphorous,
        'potassium': potassium,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph,
        'rainfall': rainfall
    }

    if request.is_json:
        return jsonify(result_data)
    else:
        prediction_text = f"Best crop for given conditions is {predicted_crop}"
        return render_template('findyourcrop.html', prediction_text=prediction_text, result=result_data)

@app.route('/suitability')
def suitability():
    return render_template('suitability.html')

@app.route('/evaluate_suitability', methods=['POST'])
def evaluate_suitability():
    if not crop_ranges:
        return jsonify({'error': 'Crop statistics are not loaded.'}), 500

    try:
        crop_name = request.form.get('crop_name', '').lower().strip()
        nitrogen = float(request.form.get('nitrogen'))
        phosphorous = float(request.form.get('phosphorous'))
        potassium = float(request.form.get('potassium'))
        temperature = float(request.form.get('temperature'))
        humidity = float(request.form.get('humidity'))
        ph = float(request.form.get('ph'))
        rainfall = float(request.form.get('rainfall'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Please check that all inputs are valid numeric values and a crop is selected.'}), 400

    if crop_name not in crop_ranges:
        return jsonify({'error': f'Crop "{crop_name}" not found in our database.'}), 404

    stats = crop_ranges[crop_name]
    inputs = {
        'nitrogen': nitrogen,
        'phosphorous': phosphorous,
        'potassium': potassium,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph,
        'rainfall': rainfall
    }

    # Evaluate compatibility for each metric
    report_details = {}
    total_score = 0.0

    for metric, val in inputs.items():
        mean = stats[metric]['mean']
        std = stats[metric]['std']
        min_val = stats[metric]['min']
        max_val = stats[metric]['max']

        # Determine deviation
        z_score = abs(val - mean) / std if std > 0 else 0
        
        # Calculate percentage match
        if val >= min_val and val <= max_val:
            match_pct = 100.0 - (z_score * 10)  # High score if within bounds
            match_pct = max(min(match_pct, 100.0), 80.0)
            status = "Optimal"
            feedback = f"Optimal parameter level for {crop_name.capitalize()}."
        else:
            # Out of bounds
            deviation_pct = min(abs(val - mean) / mean if mean > 0 else 0, 1.0)
            match_pct = max(100.0 - (deviation_pct * 100.0), 30.0)
            status = "Sub-Optimal"
            if val < min_val:
                feedback = f"Too low. Ideal range is {min_val:.1f} to {max_val:.1f}."
            else:
                feedback = f"Too high. Ideal range is {min_val:.1f} to {max_val:.1f}."

        report_details[metric] = {
            'value': val,
            'ideal_min': round(min_val, 1),
            'ideal_max': round(max_val, 1),
            'ideal_mean': round(mean, 1),
            'status': status,
            'score': round(match_pct, 1),
            'feedback': feedback
        }
        total_score += match_pct

    overall_compatibility = round(total_score / 7.0, 1)
    
    # Classify overall productivity potential
    if overall_compatibility >= 85:
        potential = "Excellent Potential"
        color_class = "success"
        advice = f"Highly compatible! The soil conditions match the requirements of {crop_name.capitalize()} almost perfectly. Expect bumper yields under standard agricultural practices."
    elif overall_compatibility >= 65:
        potential = "Moderate Potential"
        color_class = "warning"
        advice = f"Moderately compatible. Some soil parameters deviate slightly from ideal levels. Amending the soil (using fertilizers or adjusting irrigation) can improve the suitability for cultivating {crop_name.capitalize()}."
    else:
        potential = "Low Potential"
        color_class = "danger"
        advice = f"Not recommended under current conditions. Significant environmental factors (like rainfall, temperature, or critical soil nutrients) are outside the tolerable limits for {crop_name.capitalize()}. Crop failure is highly likely unless major soil amendments or greenhouse cultivation are used."

    # Fetch crop type and watering requirements from SQLite
    conn = get_db_connection()
    crop_info = conn.execute('SELECT * FROM crops WHERE crop_name = ?', (crop_name,)).fetchone()
    conn.close()

    result = {
        'crop_name': crop_name.upper(),
        'crop_type': crop_info['crop_type'] if crop_info else 'General',
        'season': crop_info['season'] if crop_info else 'All Season',
        'score': overall_compatibility,
        'potential': potential,
        'color_class': color_class,
        'advice': advice,
        'metrics': report_details
    }

    return jsonify(result)

@app.route('/insights')
def insights():
    # Gather statistics and records from the database for Scenario 3
    conn = get_db_connection()
    
    # Fetch recent predictions
    recent_predictions = conn.execute('''
        SELECT p.prediction_id, p.prediction_date, s.nitrogen, s.phosphorous, s.potassium, 
               s.temperature, s.humidity, s.ph, s.rainfall, c.crop_name, m.model_name
        FROM predictions p
        JOIN soil_data s ON p.soil_id = s.soil_id
        LEFT JOIN crops c ON p.crop_id = c.crop_id
        LEFT JOIN ml_models m ON p.model_id = m.model_id
        ORDER BY p.prediction_date DESC
        LIMIT 10
    ''').fetchall()

    # Fetch total prediction stats per crop
    crop_stats = conn.execute('''
        SELECT c.crop_name, COUNT(p.prediction_id) as count
        FROM predictions p
        JOIN crops c ON p.crop_id = c.crop_id
        GROUP BY c.crop_name
        ORDER BY count DESC
    ''').fetchall()

    # Get total records count in system database
    total_submissions = conn.execute('SELECT COUNT(*) FROM soil_data').fetchone()[0]
    total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    
    conn.close()

    # Format cluster groupings for display
    # Let's map cluster groups to meaningful categories if available
    formatted_clusters = {}
    if cluster_insights:
        for cluster_id, crops in cluster_insights.items():
            formatted_clusters[cluster_id] = ", ".join([c.capitalize() for c in crops if str(c) != 'nan'])

    return render_template(
        'insights.html',
        recent_predictions=recent_predictions,
        crop_stats=crop_stats,
        total_submissions=total_submissions,
        total_users=total_users,
        cluster_insights=formatted_clusters
    )

if __name__ == '__main__':
    app.run(debug=True)
