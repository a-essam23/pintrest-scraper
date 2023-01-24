import traceback
from os import path, makedirs

basePath = path.realpath('..')
srcPath = basePath + '\src'
outputPath = basePath + '\output'


def errorMessage(e):
    template = "An exception of type {0} occurred. Arguments:{1!r} in {2}"
    message = template.format(type(e).__name__, e.args, traceback.format_exc())
    print(message)


def createDirIfNone(path_):
    if not path.exists(path_):
        makedirs(path_)
    return


if __name__ == '__main__':
    createDirIfNone(outputPath)
