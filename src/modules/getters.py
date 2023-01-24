from globals import outputPath
import os
from pathlib import Path


def getGroups():
    allGroups = []
    with open(f'{outputPath}\groups.txt', 'r', encoding='utf-8') as file:
        filesLines = file.readlines()
        for i in range(0, len(filesLines), 2):
            group = {}
            [name, name_value] = filesLines[i].split(' ', 1)
            groupPath = outputPath + rf'\{name_value}'
            [link, link_value] = filesLines[i + 1].split(' ', 1)
            try:
                group[name] = name_value.strip('\n')
                group[link] = link_value.strip('\n')
                group["path"] = groupPath.strip('\n')
                allGroups.append(group)
            except:
                return
    return allGroups


def getModels():
    allGroups = getGroups()
    allModels = []
    allPaths = []
    for group in allGroups:
        try:
            with open(rf'{group["path"]}\models.txt', 'r', encoding='utf-8') as file:
                fileLines = file.readlines()
                allModels += fileLines
                allPaths += [group['name']] * len(fileLines)
        except:
            continue
    return [allModels, allPaths]


# folder :
#     {
#     name
#     link
#     code
#     serial
#     }


def getGroupConfigs(withModels=False):
    # get all configs
    allGroups = getGroups()
    allFolders = []
    for group in allGroups:
        folderConfigPath = group["path"] + '\.config'
        with open(folderConfigPath, 'r', encoding='utf-8') as file:
            for line in file:
                [key, value] = line.split(' ', 1)
                group[key.strip('\n')] = value.strip('\n')
        # check if any have missing codes >> ask for code inputs
        if 'code' not in group:
            while True:
                code = input(
                    f'A_   {group.get("name")}   _A is missing a code, please enter a new code to be added.\n code:')
                if len(code) == 0 | len(code) > 3:
                    print('Code is invalid. Please keep it at 3 or less characters')
                else:
                    # write the new code
                    open(folderConfigPath, 'a', encoding='utf-8').write(f'\ncode {code.upper()}\n')
                    break
        if (withModels):
            models = []
            for (subdir, dirs, files) in os.walk(group["path"]):
                # for directory in dirs:
                #     subFolder = {}
                #     try:
                #         [directory_code, directory_serial] = directory.split('-', 1)
                #         directory_serial = int(directory_serial)
                #         if (directory_code == group["code"]):
                #             subFolder[directory_serial] = True
                #             models.append(subFolder)
                #     except:
                #         continue
                for file in files:
                    try:
                        subFolder = {}
                        fileExtension = Path(file).suffix
                        if fileExtension not in ['.jpg', '.png']:
                            continue
                        [file_code, file_serial] = file.split('-', 1)
                        file_serial = file_serial.strip(fileExtension)
                        if (file_code == group["code"]):
                            subFolder["name"] = f'{group["code"]}-{file_serial}'
                            subFolder["path"] = rf'{subdir}\{group["code"]}-{file_serial}'
                            models.append(subFolder)
                    except Exception as e:
                        print(e)
                        continue
                break
            group['models'] = models

        allFolders.append(group)
    return allFolders
