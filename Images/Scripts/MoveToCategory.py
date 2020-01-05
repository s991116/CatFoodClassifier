import io
import os
import shutil
import xml.etree.ElementTree as ET
import argparse

def MoveToCategory(imageSourcePath, imageOutputSourceBasePath, annotationFilename, trainPerTestImage):
    
    imageCounter = 0

    categories = set()

    for filename in os.listdir(imageSourcePath):
        if filename.endswith(".xml"):
            xmlSourceFilename = os.path.join(imageSourcePath, filename)
            xmlDoc = ET.parse(xmlSourceFilename).getroot()
            jpgSourceFilename = xmlDoc.find("path").text

            imageCounter += 1
            if imageCounter % (trainPerTestImage+1) == 0:
                trainTestPath = "Test"
            else:
                trainTestPath = "Train"

            categoriesId = xmlDoc.findall("object")
            for categoryId in categoriesId:
                category = categoryId.find("name").text
                categories.add(category)

            xmlDistinationFilename = os.path.join(imageOutputSourceBasePath,trainTestPath,filename)
            jpgDistinationFilename = os.path.join(imageOutputSourceBasePath,trainTestPath,xmlDoc.find("filename").text)

            shutil.copy(xmlSourceFilename, xmlDistinationFilename)
            shutil.copy(jpgSourceFilename, jpgDistinationFilename)


    pbtextTemplate = '''item {{
      id: %id%
      name: %name%
    )}
    '''

    f= open(annotationFilename,"w+")

    categoryId = 1
    for category in categories:
        cateogryText = pbtextTemplate.replace("%id%", str(categoryId)).replace("%name%", category)
        categoryId += 1
        f.write(cateogryText)

def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Move images and XML to Train and Test folders and create Annotationfile")
    parser.add_argument("-i",
                        "--inputDir",
                        help="Path to the folder where the input .jpg and .xml files are stored",
                        required=True,
                        type=str)
    parser.add_argument("-o",
                        "--outputDir",
                        help="Path to the train and test folder where the .jpg and .xml files should be copied to",
                        required=True,
                        type=str)
    parser.add_argument("-a",
                        "--annotationFile",
                        help="Full filename to annotation file",
                        required=True,
                        type=str)
    parser.add_argument("-p",
                        "--trainPerTestImage",
                        help="Full filename to annotation file",
                        type=int)

    args = parser.parse_args()

    if(args.trainPerTestImage is None):
        args.trainPerTestImage = 5

    MoveToCategory(args.inputDir, args.outputDir, args.annotationFile, args.trainPerTestImage)
    print('Successfully moved images and XML file and create annotationfile')

if __name__ == '__main__':
    main()