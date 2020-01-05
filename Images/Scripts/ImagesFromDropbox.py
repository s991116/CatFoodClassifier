import dropbox
import io
import os
from pathlib import Path
from PIL import Image
import json
import argparse

def ImagesFromDropbox(downloadPath, dropboxToken, dropboxPath, imagewidth):
    db = dropbox.Dropbox(dropboxToken)

    files = db.files_list_folder(dropboxPath).entries

    filenames = [o.name for o in files]

    for filename in filenames:
        rawData = db.files_download(dropboxPath + filename)
        imageData = io.BytesIO(rawData[1].content)
        image = Image.open(imageData)
        wpercent = (imagewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((imagewidth,hsize), Image.ANTIALIAS)
        image.save(os.path.join(downloadPath,filename))

def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Download and resize images from Dropbox folder")
    parser.add_argument("-d",
                        "--downloadDir",
                        help="Path for the downloaded images",
                        required=True,
                        type=str)
    parser.add_argument("-t",
                        "--dropboxToken",
                        help="String with token for Dropbox",
                        required=True,
                        type=str)
    parser.add_argument("-p",
                        "--dropboxPath",
                        help="Path to the images in DropBox",
                        required=True,
                        type=str)
    parser.add_argument("-w",
                        "--imageWidth",
                        help="ImageWidth to resize to when downloading images",
                        required=True,
                        type=int)

    args = parser.parse_args()
    ImagesFromDropbox(args.downloadDir, args.dropboxToken, args.dropboxPath, args.imageWidth)

if __name__ == '__main__':
    main()