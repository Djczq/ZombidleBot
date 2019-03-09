import ZombidleBot.settings.Settings as bs
import cv2
import sys

if len(sys.argv) != 4:
    print("wrong number of arguments")
    sys.exit(1)

settings = bs.Settings()

img = cv2.imread(sys.argv[3])
pos = int(sys.argv[1])


name = None

if sys.argv[2] == "cc":
    name = settings.ChestCollectorPath
    crop_img = img[settings.notifPos.height : settings.notifPos.height + settings.notifSize.height,
        settings.notifPos.width + settings.notifDeplaSize.width * (pos - 1) : settings.notifPos.width + settings.notifSize.width + settings.notifDeplaSize.width * (pos - 1)].copy()
if sys.argv[2] == "sc":
    name = settings.ScrollPath
    crop_img = img[settings.notifPos.height : settings.notifPos.height + settings.notifSize.height,
        settings.notifPos.width + settings.notifDeplaSize.width * (pos - 1) : settings.notifPos.width + settings.notifSize.width + settings.notifDeplaSize.width * (pos - 1)].copy()
if sys.argv[2] == "ab":
    name = settings.GoToArcaneButtonPath
    crop_img = img[settings.goToArcaneBox.getSliceNP()]
if sys.argv[2] == "aIMG":
    name = settings.ArcanePath
    crop_img = img[settings.arcaneIMGBox.getSliceNP()]
if sys.argv[2] == "yc":
    name = settings.extendRPanelCrossPath
    crop_img = img[settings.extendRPanelCrossBox.getSliceNP()]


print(name)

if name != None:
    cv2.imwrite(name, crop_img)
