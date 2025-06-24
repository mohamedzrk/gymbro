from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

POSTURE_SERVICE_URL = 'http://posture-service:5000/analyze_posture'  # Comunicación con el microservicio de postura

@app.route('/get_posture_status', methods=['POST'])
def get_posture_status():
    landmarks = request.json.get('landmarks')  # Puntos de la postura

    # Llamamos al servicio de detección de postura
    response = requests.post(POSTURE_SERVICE_URL, json={'landmarks': landmarks})
    posture_status = response.json()

    return jsonify(posture_status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
