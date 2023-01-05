import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import os
import requests
from bs4 import BeautifulSoup


def setupChromeDriver():
    options = Options()
    options.add_argument('headless')
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def awaitElement(driver, id, className, time, CSSSelector):
    if id:
        try:
            WebDriverWait(driver, time).until(
                EC.visibility_of_element_located((By.ID, id))
            )
            return
        except:
            exit()
        return
    if className:
        try:
            WebDriverWait(driver, time).until(
                EC.visibility_of_element_located((By.CLASS_NAME, className))
            )
        except:
            exit()
        return
    if CSSSelector:
        try:
            WebDriverWait(driver, time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, CSSSelector))
            )
        except:
            exit()
        return


def scrapeGroups(createFiles=False):
    driver = setupChromeDriver()
    open(f'{outputPath}\groups.txt', 'w', encoding='utf-8')
    allGroups = {}

    def parseAddGroup(allGroups, groups):
        groupCounter = 0
        for group in groups:
            groupName = group.find_element(By.CSS_SELECTOR, '*[data-test-id="board-card-title"]').text
            groupLink = group.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if groupName not in allGroups:
                groupCounter += 1
                print('Appending... ', groupName)
                allGroups[groupName] = groupLink
                with open(f'{outputPath}\groups.txt', 'a', encoding='utf-8') as file:
                    file.write(f'name {groupName}\nlink {groupLink}\n')
        return groupCounter

    driver.get("https://www.pinterest.com/mostafaroman/_saved/")
    awaitElement(driver, 'profileBoardsFeed', None, 15)
    pageBody = driver.find_element(By.TAG_NAME, 'html')
    # x = 0
    # previousDistanceToTop=-1
    while (True):
        # distanceToTop = driver.execute_script("return window.pageYOffset;")
        # if previousDistanceToTop==distanceToTop:
        #     print(previousDistanceToTop, distanceToTop)
        #     break
        groups = driver.find_elements(By.CSS_SELECTOR, '*[data-test-id="board-card"]')
        groupCounter = parseAddGroup(allGroups, groups)
        if groupCounter == 0:
            break
        pageBody.send_keys(Keys.PAGE_DOWN)
        sleep(2)
        # x+=1
        # previousDistanceToTop = distanceToTop
    if createFiles:
        for groupName in allGroups:
            try:
                path = outputPath + f'\\{groupName}'
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(f'{path}\.config', 'w', encoding='utf-8') as file:
                    file.write(f'name {groupName}\nlink {allGroups[groupName]}')
            except:
                continue

    driver.close()
    return allGroups


def scrapeFolders(name, link, ):
    driver = setupChromeDriver()
    open(rf'{outputPath}\{name}\{"models"}.txt', 'w', encoding='utf-8')
    allModels = set()

    def parseAddModel(allModels, models, ):
        modelCounter = 0
        for model in models:
            modelLink = model.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if modelLink not in allModels:
                modelCounter += 1
                print('Adding model... ', modelLink)
                allModels.add(modelLink)
                with open(rf'{outputPath}\{name}\models.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{modelLink}\n')
        return modelCounter

    driver.get(link)
    awaitElement(driver, None, 'gridCentered', 30)
    pageBody = driver.find_element(By.TAG_NAME, 'html')
    # x = 0
    # previousDistanceToTop=-1
    while (True):
        # distanceToTop = driver.execute_script("return window.pageYOffset;")
        # if previousDistanceToTop==distanceToTop:
        #     print(previousDistanceToTop, distanceToTop)
        #     break
        models = driver.find_elements(By.CSS_SELECTOR, '*[role="listitem"]')
        groupCounter = parseAddModel(allModels, models)
        if groupCounter == 0:
            break
        pageBody.send_keys(Keys.PAGE_DOWN)
        sleep(3)
        # x+=1
        # previousDistanceToTop = distanceToTop

    driver.close()
    return allModels


def scrapeModels(name, link):
    print(name)
    try:
        driver = setupChromeDriver()
        driver.get(link.strip('\n'))
        awaitElement(driver, None, None, 300, '[data-layout-shift-boundary-id="CloseupPageBody"]')
        modelContainer = driver.find_element(By.CSS_SELECTOR, '*[data-layout-shift-boundary-id="CloseupPageBody"]')
        model = modelContainer.find_element(By.CSS_SELECTOR, '[data-test-id="pin-closeup-image"]')
        modelImageLink = model.find_element(By.TAG_NAME, 'img').get_attribute('src')
        modelImageType = modelImageLink[modelImageLink.rfind('.'):]
        with open(rf'{outputPath}\{name}\{str(uuid.uuid4())}{modelImageType}', 'wb') as handle:
            img_data = requests.get(modelImageLink).content
            handle.write(img_data)
        driver.close()
        return
    except:
        exit()


def scrapeModelsNoDriver(name, link):
    try:
        session = requests.Session()
        r = session.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        modelImageLink = soup.find("img", {"elementtiming": "closeupImage"})
        modelImage = modelImageLink['src']
        modelImageType = modelImage[modelImage.rfind('.'):]
        with open(rf'{outputPath}\{name}\{str(uuid.uuid4())}{modelImageType}', 'wb') as handle:
            img_data = requests.get(modelImage).content
            handle.write(img_data)
            print(link,'added to',name)
        return
    except Exception as e:
        print(e)
        exit()


def getGroups():
    allGroups = {}
    with open(f'{outputPath}\groups.txt', 'r', encoding='utf-8') as file:
        filesLines = file.readlines()
        for i in range(0, len(filesLines), 2):
            groupName = filesLines[i].split(' ', 1)[1].strip('\n')
            groupLink = filesLines[i + 1].split(' ', 1)[1].strip('\n')
            try:
                allGroups[groupName] = groupLink
            except:
                return
    return allGroups


def getModels():
    allGroups = getGroups()
    allModels = []
    allPaths = []
    for key in allGroups:
        try:
            with open(rf'{outputPath}\{key}\models.txt', 'r', encoding='utf-8') as file:
                fileLines = file.readlines()
                allModels += fileLines
                allPaths += [key] * len(fileLines)
        except:
            continue
    return [allModels, allPaths]


if __name__ == '__main__':
    basePath = os.path.realpath('..')
    outputPath = basePath + '\output'
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    [allModels, allPaths] = getModels()

    # scrapeModelsNoDriver(allPaths[0],allModels[0])

    # model = scrapeModels(allPaths[0], allModels[0])

    with ThreadPoolExecutor(max_workers=None) as executor:
        executor.map(scrapeModelsNoDriver, allPaths, allModels)


    # print(model)
    # allModels = scrapeFolders(setupChromeDriver(), "موديرن", allGroups['موديرن'])
    # with ThreadPoolExecutor(max_workers=None) as executor:
    #     executor.map(scrapeFolders,list(allGroups.keys()),list(allGroups.values()))
    # print(len(allModels))
