import asyncio
from flask import Flask, request, jsonify
from github_integration import full_scan, scan_by_filters, update_exitsing
from config import DevelopmentConfig, ProductionConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())  # Use DevelopmentConfig or ProductionConfig as needed


@app.route('/scan_by_fillters', methods=['POST']) #todo scan by fillters
def scan_by_country_route():
    filters = request.json.get('fillters')
    if not filters:
        return jsonify({"message": "Country is required"}), 400
    scan_by_filters(filters)
    return jsonify({"message": "Scan by country initiated"}), 202
@app.route('/full_scan', methods=['GET'])
def trigger_full_scan():
    full_scan()
    return jsonify({"message": "Full scan initiated"}), 202

@app.route('/update_existing', methods=['GET'])
def trigger_full_scan():
    asyncio.create_task((update_exitsing()))
    return jsonify({"message": "Full scan initiated"}), 202
#todo flask cron

if __name__ == '__main__':
    app.run()




