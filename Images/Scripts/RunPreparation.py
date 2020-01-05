import MoveToCategory
import XmlToCsv
import ImagesFromDropbox
import json
from pathlib import Path

scriptPath = Path(__file__).parent
imagePath = scriptPath.parent
rootFolder = imagePath.parent

with open(scriptPath.joinpath("Secrets.json"), 'r') as f:
    Secrets = json.load(f)

#ImagesFromDropbox.ImagesFromDropbox(imagePath.joinpath("Uncategorised"), Secrets["DropboxToken"], "/Pics/", 320)
MoveToCategory.MoveToCategory(imagePath.joinpath("Uncategorised"), imagePath, rootFolder.joinpath("Annotations/label_map.pbtxt"), 5)
XmlToCsv.convertToCSV(str(imagePath.joinpath("Train/")),rootFolder.joinpath("Annotations/train_labels.csv"))
XmlToCsv.convertToCSV(str(imagePath.joinpath("Test/")), rootFolder.joinpath("Annotations/test_labels.csv"))