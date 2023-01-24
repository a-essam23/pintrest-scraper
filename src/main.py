from excel import generateXLSL
from model import assignSerial
from autocad import generateDXF
from time import sleep
from scraper import scrapeModelsExecutor
if __name__ == '__main__':
    assignSerial()
    # sleep(1)
    # generateXLSL()
    generateDXF()
    # scrapeModelsExecutor()