from pathlib import Path



def getFileExtension(fileName):
    return Path(fileName).suffix


def isImage(fileExtension):
    if fileExtension not in ['.jpg', '.png']:
        return False
    return True

