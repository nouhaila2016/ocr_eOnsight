import cv2
import easyocr
import json
import sys

# Vérifier si un chemin d'image est fourni en argument de ligne de commande
if len(sys.argv) > 1:
    image_path = sys.argv[1]  # Utiliser le chemin d'image fourni en argument
else:
    print("ERREUR | Entrez le nom de l'image en input :\npython3 ocr.py <nom de l'image>")
    exit(1)

# Fonction pour détecter et extraire le texte avec tracé de rectangles et sortie JSON
def detect_and_extract_text_with_json(image_path):
    # Charger l'image
    image = cv2.imread(image_path)
    
    # Initialiser le détecteur OCR
    reader = easyocr.Reader(['fr'])
    
    # Détecter et extraire le texte de l'image
    result = reader.readtext(image)
    
    # Initialiser une liste pour stocker les résultats au format JSON
    json_result = []
    
    # Dessiner des rectangles autour du texte détecté et enregistrer les coordonnées
    for detection in result:
        # Récupérer les coordonnées de la boîte englobante
        bbox = detection[0]
            # Dessiner le rectangle autour du texte
        cv2.rectangle(image, (int(bbox[0][0]), int(bbox[0][1])), (int(bbox[2][0]), int(bbox[2][1])), (0, 255, 0), 2)
        # Ajouter les coordonnées de la boîte englobante et la confiance au résultat JSON
        json_result.append({
            'Ville': detection[1],
            'localisation': [int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1])],
            'confidence': detection[2]
        })

    # Enregistrer l'image avec les rectangles
    cv2.imwrite('image_rectangles.png', image)
    
    # Convertir la liste des résultats JSON en format JSON avec l'option ensure_ascii=False
    json_output = json.dumps(json_result, indent=4, ensure_ascii=False)
    
    return json_output

# Appeler la fonction pour détecter et extraire le texte avec les rectangles et la sortie JSON
json_output = detect_and_extract_text_with_json(image_path)

# Afficher le résultat JSON
print(json_output)
