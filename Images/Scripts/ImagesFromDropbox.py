import dropbox
import io
import os
from pathlib import Path
from PIL import Image
import json

scriptPath = os.path.dirname(__file__)

dropboxPath = "/Pics/"
downloadPath = Path(scriptPath).parent.joinpath("Uncategorised")
secretFilename =  os.path.join(scriptPath, 'Secrets.json')
with open(secretFilename, 'r') as f:
    Secrets = json.load(f)

db = dropbox.Dropbox(Secrets["DropboxToken"])

files = db.files_list_folder(dropboxPath).entries

filenames = [o.name for o in files]

baseImagewidth = 320

for filename in filenames:
    rawData = db.files_download(dropboxPath + filename)
    imageData = io.BytesIO(rawData[1].content)
    image = Image.open(imageData)
    wpercent = (baseImagewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((baseImagewidth,hsize), Image.ANTIALIAS)
    image.save(os.path.join(downloadPath,filename)) 