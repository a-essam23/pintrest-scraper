import ezdxf
from getters import getGroupConfigs

def generateModelCAD(doc, model):
    msp = doc.modelspace()
    print('Generating', model["name"])
    for e in msp:
        if e.dxftype() == "MTEXT":
            x = '{\H5x;'
            # {\H5x;FIN-13\fArial|b0|i0|c178|p34;34}
            # {\H5x;FIN-6973}
            e.dxf.text = x + rf'{model["name"]}' + '}'
            # print(e.dxf.text)
            doc.saveas(rf'{model["path"]}\{model["name"]}.dxf')
            return

    return


def generateGroupCAD(models):
    try:
        doc = ezdxf.readfile("template.dxf")
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        return
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        return

    for model in models:
        try:
            generateModelCAD(doc, model)
        except Exception as e:
            print(e)

    return


def generateCAD():
    for group in getGroupConfigs(withModels=True):
        generateGroupCAD(group["models"])
    return


def generateGlobalCad():
    doc = ezdxf.new("R2007")
    msp = doc.modelspace()



    return