
import os # pour les chemins de fichiers
import json # pour les fichiers JSON
from PIL import Image
from PIL.ExifTags import TAGS # pour les métadonnées
from PIL.TiffImagePlugin import IFDRational
from torchvision.models.detection import fasterrcnn_resnet50_fpn # trouver les objets / visages

# encodeur json pour les bytes et les rationnels (pour les métadonnées)
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                return obj.decode('utf-8', 'replace')
        elif isinstance(obj, IFDRational):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

# chemin vers le dossier images
path_to_folder = os.path.abspath('/app/images')

# crée le dossier metadata s'il n'xiste pas
if not os.path.exists('metadata'):
    os.mkdir('metadata')

# boucle sur les images du dossier
for filename in os.listdir(path_to_folder):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # extrait les métadonnées
        image = Image.open(os.path.join(path_to_folder, filename))
        exifdata = image.getexif()
        metadata = {}

        # ajoute les métadonnées à la liste
        for tag_id, value in exifdata.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = value

        # Convert the dictionary to JSON and store it in a file
        json_filename = os.path.splitext(filename)[0] + '.json'
        with open(os.path.join('metadata', json_filename), 'w') as f:
            json.dump(metadata, f, cls=MyEncoder)