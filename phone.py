from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import requests

# ===== API SERVER =====
app = Flask(__name__)

@app.route('/api/phone/lookup', methods=['POST'])
def phone_lookup():
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400
    
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        
        result = {
            'phone_number': phone_number,
            'is_valid': phonenumbers.is_valid_number(parsed_number),
            'country_code': parsed_number.country_code,
            'national_number': parsed_number.national_number,
            'international_format': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'e164_format': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/phone/detailed', methods=['POST'])
def phone_detailed():
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400
    
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        
        # Get the detailed location description
        location_description = geocoder.description_for_number(parsed_number, "en") if phonenumbers.is_valid_number(parsed_number) else "Unknown"
        
        # IMPROVED LOCATION PARSING
        location_parts = location_description.split(', ') if location_description and location_description != "Unknown" else []
        
        # Better location parsing logic
        if len(location_parts) == 1:
            # Only country available
            country = location_parts[0]
            region = "Unknown"
            town = "Unknown"
        elif len(location_parts) == 2:
            # Region and country (most common)
            region = location_parts[0]
            country = location_parts[1]
            town = "Unknown"
        elif len(location_parts) >= 3:
            # Town, region, and country (rare but possible)
            town = location_parts[0]
            region = location_parts[1]
            country = location_parts[2]
        else:
            town = "Unknown"
            region = "Unknown"
            country = "Unknown"
        
        # Get additional information
        carrier_name = carrier.name_for_number(parsed_number, "en") if phonenumbers.is_valid_number(parsed_number) else "Unknown"
        timezones = timezone.time_zones_for_number(parsed_number) if phonenumbers.is_valid_number(parsed_number) else []
        
        # Get number type
        number_type = "Unknown"
        if phonenumbers.is_valid_number(parsed_number):
            from phonenumbers import number_type
            try:
                num_type = number_type(parsed_number)
                type_map = {
                    0: "FIXED_LINE",
                    1: "MOBILE", 
                    2: "FIXED_LINE_OR_MOBILE",
                    3: "TOLL_FREE",
                    4: "PREMIUM_RATE",
                    5: "SHARED_COST",
                    6: "VOIP",
                    7: "PERSONAL_NUMBER",
                    8: "PAGER",
                    9: "UAN",
                    10: "VOICEMAIL",
                    27: "UNKNOWN"
                }
                number_type = type_map.get(num_type, "UNKNOWN")
            except:
                number_type = "UNKNOWN"
        
        result = {
            'phone_number': phone_number,
            'is_valid': phonenumbers.is_valid_number(parsed_number),
            'country_code': parsed_number.country_code,
            'national_number': parsed_number.national_number,
            'international_format': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'e164_format': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
            
            # LOCATION INFORMATION
            'town': town,
            'region': region, 
            'country': country,
            'full_location': location_description,
            
            'carrier': carrier_name,
            'timezones': list(timezones),
            'is_possible': phonenumbers.is_possible_number(parsed_number),
            'number_type': number_type
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def home():
    return '''
    <h1>Phone Number API</h1>
    <p>Endpoints:</p>
    <ul>
        <li>POST /api/phone/lookup - Basic phone info</li>
        <li>POST /api/phone/detailed - Detailed phone info</li>
    </ul>
    <p>Send JSON with {"phone_number": "+1234567890"}</p>
    '''

# ===== CLIENT FUNCTIONS =====
class PhoneNumberClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
    
    def basic_lookup(self, phone_number: str):
        endpoint = f"{self.base_url}/api/phone/lookup"
        payload = {'phone_number': phone_number}
        
        try:
            response = requests.post(endpoint, json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"Request failed: {str(e)}"}
    
    def detailed_lookup(self, phone_number: str):
        endpoint = f"{self.base_url}/api/phone/detailed"
        payload = {'phone_number': phone_number}
        
        try:
            response = requests.post(endpoint, json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"Request failed: {str(e)}"}

def quick_lookup(phone_number: str):
    client = PhoneNumberClient()
    return client.detailed_lookup(phone_number)

# ===== TEST FUNCTION =====
def test_api():
    """Test the API with some example numbers"""
    client = PhoneNumberClient()
    
    test_numbers = [
        "+14155552671",  # US number
        "+442079460000",  # UK number
    ]
    
    print("Testing Phone Number API...")
    
    for phone in test_numbers:
        print(f"\n📞 Looking up: {phone}")
        print("-" * 40)
        
        detailed = client.detailed_lookup(phone)
        for key, value in detailed.items():
            print(f"{key}: {value}")

# ===== MAIN EXECUTION =====
if __name__ == '__main__':
    print("Starting Phone Number API Server...")
    print("API available at: http://localhost:5000")
    print("To test the API, run this in another terminal:")
    print("python -c \"from all_in_one_phone_api import PhoneNumberClient; client = PhoneNumberClient(); print(client.detailed_lookup('+14155552671'))\"")
    print("\nStarting server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

# ===== MAIN EXECUTION =====
if __name__ == '__main__':
    print("Starting Phone Number API Server...")
    print("API available at: http://localhost:5000")
    print("To test the API, run this in another terminal:")
    print("python -c \"from all_in_one_phone_api import PhoneNumberClient; client = PhoneNumberClient(); print(client.detailed_lookup('+14155552671'))\"")
    print("\nStarting server...")
    app.run(debug=True, host='0.0.0.0', port=5000)