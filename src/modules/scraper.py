from concurrent.futures import ThreadPoolExecutor
from getters import getModels,getGroups
from _scrapers import scrapeModelsNoDriver,scrapeFolders

def scrapeModelsExecutor(limit=None):
    [allModels, allPaths] = getModels()
    with ThreadPoolExecutor(max_workers=limit) as executor:
        executor.map(scrapeModelsNoDriver, allPaths, allModels)

def scrapeFoldersExecutor(limit=None):
    # not tested
    allGroups = getGroups()
    with ThreadPoolExecutor(max_workers=limit) as executor:
        executor.map(scrapeFolders,allGroups)