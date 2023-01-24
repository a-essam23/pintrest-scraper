from pathlib import Path
import os
from getters import getGroupConfigs
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from globals import errorMessage,createDirIfNone


def generateGlobalXLSL():
    return


def generateXLSL():
    allGroups = getGroupConfigs(withModels=True)
    for group in allGroups:
        createDirIfNone(rf'{group["path"]}\{group["code"]}')
        generateGroupXLSL(group)
    return


def generateGroupXLSL(group):
    for model in group["models"]:
        generateModelXLSL(model, group["name"])
    return


def generateModelXLSL(model, group_name):
    code_cell = "B4"
    roman_logo_cell = "B1"
    length_cell = "B8"
    width_cell = "B10"
    depth_cell = "B12"
    weight_cell = "B14"
    group_cell = "B16"
    signature_cell = "B18"
    model_img_cell = "F4"
    try:
        workbook = load_workbook('form.xlsx')
        worksheet = workbook["Sheet1"]
        outputXLSLpath = rf'{model["path"]}\{model["name"]}.xlsx'
        print('generating excel file for', model["name"], model["path"])
        model_img = Image(model["path"] + rf'\{model["name"]}.jpg')
        worksheet[code_cell] = model["name"]
        worksheet[group_cell] = group_name
        worksheet.add_image(model_img, model_img_cell)
        if Path(outputXLSLpath).is_file():
            print('found existing file... deleting')
            os.remove(outputXLSLpath)
        workbook.save(outputXLSLpath)
    except Exception as e:
        errorMessage(e)
    return
