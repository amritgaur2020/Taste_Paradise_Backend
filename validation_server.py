from flask import Flask, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

def load_licenses():
    """Load licenses from database"""
    try:
        with open('licenses_db.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_licenses(licenses):
    """Save licenses to database"""
    with open('licenses_db.json', 'w') as f:
        json.dump(licenses, f, indent=2)

@app.route('/api/validate', methods=['POST'])
def validate_license():
    """Validate license key and machine ID"""
    data = request.json
    license_key = data.get('license_key')
    machine_id = data.get('machine_id')
    
    print(f"Validation request: {license_key} from {machine_id}")
    
    licenses = load_licenses()
    
    # Find license
    license_record = None
    for lic in licenses:
        if lic['key'] == license_key:
            license_record = lic
            break
    
    if not license_record:
        return jsonify({
            'valid': False,
            'reason': 'License key not found'
        }), 404
    
    # Check if revoked
    if license_record.get('revoked'):
        return jsonify({
            'valid': False,
            'reason': 'License has been revoked'
        }), 403
    
    # Check if already activated on different machine
    if license_record.get('activated'):
        if license_record.get('machine_id') != machine_id:
            return jsonify({
                'valid': False,
                'reason': 'License already activated on another computer'
            }), 403
    else:
        # First activation - bind to this machine
        for lic in licenses:
            if lic['key'] == license_key:
                lic['activated'] = True
                lic['machine_id'] = machine_id
                lic['activation_date'] = datetime.now().isoformat()
        save_licenses(licenses)
        print(f"License {license_key} activated for machine {machine_id}")
    
    # Return success
    return jsonify({
        'valid': True,
        'customer': license_record['customer'],
        'plan': license_record['plan'],
        'expiry_date': license_record['expiry_date']
    })

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    from datetime import datetime
    print("Starting TasteParadise License Validation Server...")
    print("Running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
