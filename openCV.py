import cv2

# Chargement du modèle de détection d'objets
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Initialisation de la caméra
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    height, width, channels = frame.shape

    # Prétraitement de l'image
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Analyse des résultats
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Détection d'un objet
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Affichage de l'image
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if key == 27:  # Appuyer sur 'Esc' pour quitter
        break

cap.release()
cv2.destroyAllWindows()
