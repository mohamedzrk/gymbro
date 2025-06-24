from flask import Flask, request, jsonify
import mediapipe as mp
import numpy as np

app = Flask(__name__)

# Inicializamos MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Función para calcular los ángulos entre las articulaciones
def calculate_angle(a, b, c):
    # Esta función calcula el ángulo entre tres puntos: a, b, c (representados como [x, y])
    a = np.array(a)  # Primer punto
    b = np.array(b)  # Punto medio
    c = np.array(c)  # Segundo punto

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))

    # Asegurarse de que el ángulo esté entre 0 y 180 grados
    if angle > 180:
        angle = 360 - angle
    return angle

# Función para analizar la postura en sentadillas utilizando los landmarks
def analyze_squat_posture(landmarks):
    # Convertimos los landmarks en una matriz numpy
    landmarks = np.array(landmarks)

    # Los puntos clave para la sentadilla: rodillas, caderas y tobillos
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    
    # Calculamos el ángulo de la rodilla (simple análisis para sentadillas)
    left_knee_angle = calculate_angle(left_hip, left_knee, [left_knee[0], left_knee[1] + 0.05])
    right_knee_angle = calculate_angle(right_hip, right_knee, [right_knee[0], right_knee[1] + 0.05])

    # Verificamos si el ángulo de la rodilla es mayor que un umbral (por ejemplo, 140 grados)
    if left_knee_angle < 140 or right_knee_angle < 140:
        return 'Incorrecta'
    
    # Si la rodilla está en el rango adecuado, consideramos que la postura es correcta
    return 'Correcta'

@app.route('/analyze_squat', methods=['POST'])
def handle_squat_analysis():
    try:
        # Recibimos los landmarks en el cuerpo de la solicitud POST
        data = request.get_json()
        landmarks = data['landmarks']  # Los landmarks son los puntos clave de la postura

        # Llamamos a la función para analizar la postura de la sentadilla
        squat_status = analyze_squat_posture(landmarks)

        # Devolvemos el estado de la postura (Correcta/Incorrecta)
        return jsonify({'status': squat_status})

    except Exception as e:
        # Si ocurre un error, devolvemos un mensaje con el error
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Ejecutamos el microservicio Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
