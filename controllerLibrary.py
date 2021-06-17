from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRCTORY = os.path.join(USERAPPDIR, 'controllerLibrary')


def createDirectory(directory = DIRCTORY):
    """
    Creates the given directory if it doesn't exist already
    Args:
        directory (str): The directory to create

    """
    if not os.path.exists(directory):
        os.mkdir(directory)


class controllerLibrary(dict):

    def save(self, name, directory=DIRCTORY, screenshot=True, **info):

        createDirectory(directory)

        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        if cmds.ls(selection=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)

        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['Screenshot'] = self.saveScreenshot(name, directory=directory)

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = info

    def find(self, directory=DIRCTORY):

        self.clear()

        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)

            infoFile = '%s.json' % name
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    info = json.load(f)

            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['Screenshot'] = os.path.join(directory, name)

            info['name'] = name
            info['path'] = path

            self[name] = info


    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def saveScreenshot(self, name, directory=DIRCTORY):
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path, forceOverwrite=True,
                       format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1,
                       viewer=False)

        return path

