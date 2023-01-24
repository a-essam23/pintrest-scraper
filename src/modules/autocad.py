from dxfwrite import DXFEngine as dxf
from globals import outputPath, createDirIfNone
from getters import getGroupConfigs

max_group_length = 200
max_group_width = 100
rect_width = 8.5
rect_height = 2
circle_radius = 0.5
text_height = 1
gutter = 0.1


def drawModel(doc, textContent, originRect=(0, 0), originCirc=(7.5, 1), originText=(0.5, 0.5), ):
    model_rectangle = dxf.rectangle(originRect, rect_width, rect_height)
    model_circle = dxf.circle(circle_radius, originCirc)
    model_serial = dxf.text(textContent, originText, text_height)
    doc.add(model_rectangle)
    doc.add(model_circle)
    doc.add(model_serial)
    return doc


def generateModelDXF(model):
    try:
        doc = dxf.drawing(f'{model["name"]}.dxf')
        doc = drawModel(doc, model["name"])
        doc.saveas(rf'{model["path"]}\{model["name"]}.dxf')
    except Exception as e:
        print(e)
    return


def generateGroupGlobalDXF(group):
    return


def generateGroupDXF(models):
    for model in models:
        generateModelDXF(model)
    return


def generateDXF():
    doc = dxf.drawing('group.dxf')
    outputDir = rf'{outputPath}\__CAD'
    createDirIfNone(outputDir)
    counter = 1
    originX = 0
    originY = 0
    current_length = 0
    current_width = 0
    for group in getGroupConfigs(withModels=True):
        for model in group["models"]:
            if (originX + rect_width) >= max_group_width:
                if (abs(originY) + rect_height) >= max_group_length:
                    doc.saveas(rf'{outputDir}\CAD-{counter}.dxf')
                    counter += 1
                    doc = dxf.drawing('group.dxf')
                    originX = 0
                    originY = 0
                else:
                    originY = originY - rect_height - gutter
                    originX = 0
            circleOrigin = (originX + 7.5, originY + 1)
            textOrigin = (originX + 0.5, originY + 0.5)
            doc = drawModel(doc, model["name"], (originX, originY), circleOrigin, textOrigin)
            originX = originX + rect_width + gutter

    doc.saveas(rf'{outputDir}\CAD-{counter}.dxf')
    return
