from flask import Flask, request, jsonify
from db import init_db
from github_integration import full_scan, scan_by_country
from config import DevelopmentConfig, ProductionConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())  # Use DevelopmentConfig or ProductionConfig as needed

db = init_db()

@app.route('/scan_by_country', methods=['POST'])
def scan_by_country_route():
    country = request.json.get('country')
    if not country:
        return jsonify({"message": "Country is required"}), 400
    scan_by_country(db, country)
    return jsonify({"message": "Scan by country initiated"}), 202

@app.route('/full_scan', methods=['GET'])
def trigger_full_scan():
    full_scan(db)
    return jsonify({"message": "Full scan initiated"}), 202


if __name__ == '__main__':
    app.run()
