import os
from time import sleep
from shutil import rmtree
from PIL import Image
from globals import createDirIfNone, errorMessage
from uuid import uuid4
from getters import getGroupConfigs
from pathlib import Path
from utils import getFileExtension, isImage


def destructModelFile(file, fileExtension):
    [file_code, file_serial] = file.split('-', 1)
    file_name = file.strip(fileExtension)
    file_serial = file_serial.strip(fileExtension)
    file_serial = int(file_serial)
    return [file_code, file_name, file_serial]


def createModelImage(imgPath, subdir, imgName):
    print('generating new image...')
    outputImgDir = rf'{subdir}\{imgName}'
    max_width = 512
    # max_height = 488
    try:
        print('resizing image for excel')
        img = Image.open(imgPath)
        width, height = img.size
        factor = width / max_width
        newSize = (max_width, round(height / factor))
        print(newSize)
        # if width > height:
        #     factor = width / max_width
        #     newSize = (max_width, round(height / factor))
        #     print(newSize)
        #     img = img.resize(newSize)
        # else:
        #     factor = height / max_width
        #     newSize=(round(width/ factor), max_height)
        #     print(newSize)
        img = img.resize(newSize)
        img.save(rf'{outputImgDir}\{imgName}.jpg')
    except Exception as e:
        errorMessage(e)
    return


def findFreeSerial(code, subdir, serial):
    temp_serial = serial
    while True:
        filePathJPG = subdir + rf'\{code}-{temp_serial}.jpg'
        filePathPNG = subdir + rf'\{code}-{temp_serial}.png'
        if Path(filePathJPG).is_file() | Path(filePathPNG).is_file():
            temp_serial += 1
        else:
            return temp_serial


def renameModelFile(code, subdir, serial, oldFile, extension):
    print("requesting to rename", oldFile, 'to', rf'{code}-{serial}{extension}')
    new_serial = findFreeSerial(code, subdir, serial)
    newFileName = rf'{code}-{new_serial}'
    newFileNameWithExtension = rf'{newFileName}{extension}'
    print('renaming', oldFile, 'to', newFileNameWithExtension, '\n')
    newPath = rf'{subdir}\{newFileNameWithExtension}'
    os.rename(rf'{subdir}\{oldFile}', newPath)
    # createResizedImg(rf'{subdir}\{newFileWithExtension}', rf'{subdir}\{newFile}', newFile)
    return [new_serial, newPath, newFileName, newFileNameWithExtension]


def assignSerialSoft(subdir, files, group):
    last_serial = 1
    for file in files:
        # if file is not an image skip
        fileExtension = getFileExtension(file)
        if not isImage(fileExtension):
            continue
        try:
            [file_code, file_name, file_serial] = destructModelFile(file, fileExtension)
            if (file_code == group["code"]):
                continue

            else:
                [new_serial, newPath, newFileName, newFileNameWithExtension] = renameModelFile(group["code"], subdir,
                                                                                               last_serial, file,
                                                                                               fileExtension)
                last_serial = new_serial
                createDirIfNone(rf'{subdir}\{group["code"]}-{last_serial}')
                createModelImage(newPath, subdir, newFileName)

        except Exception as e:
            # errorMessage(e)
            [new_serial, newPath, newFileName, newFileNameWithExtension] = renameModelFile(group["code"], subdir,
                                                                                           last_serial, file,
                                                                                           fileExtension)
            last_serial = new_serial
            createDirIfNone(rf'{subdir}\{group["code"]}-{last_serial}')
            sleep(.15)
            createModelImage(newPath, subdir, newFileName)
            continue


def assignSerialHard(subdir, dirs, files, group):
    for dir in dirs:
        try:
            [dir_code, dir_serial] = dir.split('-', 1)
            if dir_code == group["code"]:
                rmtree(rf'{subdir}\{dir}')
        except:
            continue
    for file in files:
        file_extension = getFileExtension(file)
        if not isImage(file_extension):
            continue

        try:
            os.rename(rf'{subdir}\{file}', rf'{subdir}\{uuid4()}{file_extension}')
        except Exception as e:
            print(e)
    return


def assignSerial(_group=None, hard=False):
    if hard:
        warningInput = input(
            "WARNING: enabling hard will delete generated model folder and ALL of its content. Continue? (y/N)\n")
        if warningInput == "y":
            pass
        elif warningInput == "N":
            hard = False
        else:
            quit()
    allGroups = getGroupConfigs()
    for group in allGroups:

        # rename only if file name does not start with group code
        # hard renames all images to random, deletes dirs, then assigns serials
        print(f'Locating all files in {group["name"]}\n')
        for (subdir, dirs, files) in os.walk(group["path"]):
            if hard:
                assignSerialHard(subdir, dirs, files, group)
            else:
                assignSerialSoft(subdir, files, group)
                return
            break
        for (subdir, dirs, files) in os.walk(group["path"]):
            assignSerialSoft(subdir, files, group)
            break

    return
