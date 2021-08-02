
# * JacobEM Builder
# * Created by JacobEM.com
# * This program is licensed under the MIT License


from os import listdir, getcwd, mkdir
from os.path import isfile, isdir, join
import shutil
from json import loads

ignoreList = []

path = getcwd() + "\\"
src = path + "src"
build = path + "build"


try:
    ignoreListRaw = open("ignore_list.jemignore", "r")


    ignoreList = loads(ignoreListRaw.read())

    ignoreListRaw.close()
except:
    ignoreList = []


def copyFile(orig, dest):
    try:
        shutil.copyfile(orig, dest)
    except shutil.SameFileError:
        print("Source and destination represents the same file.")
    except IsADirectoryError:
        print("Destination is a directory.")
    except PermissionError:
        print("Permission denied.")
    except:
        print("Error occurred while copying file.")

def createFolder(dest):
    try:
        mkdir(dest)
    except:
        print('Error occurred while creating folder.', dest)



def checkFiles(files, filesDir):
    for thisFile in files:
        try:
            fileFullNameDir = filesDir + thisFile
            fileFullName = thisFile
            fileName = thisFile.split('.')[0]
            fileType = thisFile.split('.')[1]
        except:
            fileFullNameDir = filesDir + thisFile
            fileFullName = thisFile
            fileName = thisFile.split('.')[0]
            fileType = ""
            print(f'Warning, {fileFullName} does not have an extention.')

        if fileType == "md":
            print(f"Ignoring {fileFullName} > Reason: Markdown file.")
        elif fileType == "jemignore":
            print(f"Ignoring {fileFullName} > Reason: Building Application Ignore File.")
        elif fileFullName in ignoreList:
            pass
            print(f"Ignoring {fileFullName} > Reason: In Ignore-List.")
        else:
            dirAfterSrc = filesDir.split('\src')[1]
            copyFile(filesDir + thisFile, build + dirAfterSrc + thisFile)
            # print(f"Allowing {fileFullName}")




def forItem(dire):
    direForOthers = dire + "\\"

    files = [f for f in listdir(dire) if isfile(join(dire, f))]
    folders = [f for f in listdir(dire) if isdir(join(dire, f))]

    checkFiles(files, direForOthers)

    for folder in folders:
        if folder in ignoreList:
            print(f"Ignoring Folder: {folder} > Reason: In Ignore-List.")
        else:
            dirAfter = direForOthers.split('\src')[1]
            createFolder(join(build + dirAfter + folder))
            forItem(direForOthers + folder)




# Run the checker in the src directory
forItem(src)