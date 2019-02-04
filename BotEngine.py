import cv2
import pytesseract
import ImageAnalyser as ia
import logging

logger = logging.getLogger("ZombidleBotLogger")

def processDeal(img, configs):
    read = ia.readCharacters(img, configs.dealContentBox)
    logger.info("Process deal")
    logger.debug("read : " + read)
    if "Skull" in read or "damage" in read or "chest" in read or "minutes" in read:
        return (configs.dealNoPos[0], configs.dealNoPos[1])
    if "sec" in read and "nds" in read:
        return (configs.dealNoPos[0], configs.dealNoPos[1])
    if "x" in read or "craft" in read or "time" in read:
        if "free" in read:
            return (configs.dealAwsomePos[0], configs.dealAwsomePos[1])
        else:
            return (configs.dealYesPos[0], configs.dealYesPos[1])
    return (configs.dealNoPos[0], configs.dealNoPos[1])

def processArcane(img, configs):
    if img[configs.collectAllPos[1], configs.collectAllPos[0]] > 55:
        logger.info("Arcane -- collect all")
        return (configs.collectAllPos[0], configs.collectAllPos[1])
    if img[configs.repeatLastCraftPos[1], configs.repeatLastCraftPos[0]] > 55:
        logger.info("Arcane -- repeat last craft")
        return (configs.repeatLastCraftPos[0], configs.repeatLastCraftPos[1])
    if img[configs.fastGhostCraftPos[1], configs.fastGhostCraftPos[0]] > 55:
        logger.info("Arcane -- fast ghost craft")
        return (configs.fastGhostCraftPos[0], configs.fastGhostCraftPos[1])
    if img[configs.nextBoostPos[1], configs.nextBoostPos[0]] > 55:
        logger.info("Arcane -- craft boost")
        return (configs.nextBoostPos[0], configs.nextBoostPos[1])
    logger.info("Arcane -- quit")
    return (configs.arcaneQuitPos[0], configs.arcaneQuitPos[1])

def determineAction(img, configs):
    read = ia.readCharacters(img, configs.dealBox)
    if read == "THE DEAL":
        logger.info("Action -- deal")
        return (3, )

    read = ia.readCharacters(img, configs.dealThanksBox)
    if read == "Thanks!":
        logger.info("Action -- thanks")
        return (7, configs.dealExitPubPos[0], configs.dealExitPubPos[1])

    template = cv2.imread("ArcaneIMG.png", 0)
    res = ia.findTemplateInImage(img, template)
    if ia.isInside(res, configs.arcaneIMGBox):
        logger.info("Action -- in arcane")
        return (5, )

    template = cv2.imread("Scroll.png", 0)
    res = ia.findTemplateInImage(img, template)
    if ia.isInside(res, configs.notifBox):
        logger.info("Action -- click Scroll")
        return (1, (res[0] + res[2]) / 2, (res[1] + res[3]) / 2)
    template = cv2.imread("ChestCollector.png", 0)
    res = ia.findTemplateInImage(img, template)
    if ia.isInside(res, configs.notifBox):
        logger.info("Action -- click ChestCollector")
        return (2, (res[0] + res[2]) / 2, (res[1] + res[3]) / 2)

    read = ia.readCharacters(img, configs.arcaneTimerBox)
    if "A" in read:
        template = cv2.imread("GoToArcaneButton.png", 0)
        res = ia.findTemplateInImage(img, template)
        if ia.isInside(res, configs.goToArcaneBox):
            logger.info("Action -- click arcane button")
            return (4, configs.goToArcanePos[0], configs.goToArcanePos[1])
        else:
            logger.info("Action -- click item tab")
            return (4, configs.itemTabPos[0], configs.itemTabPos[1])

    if img[configs.backArrowPos[1], configs.backArrowPos[0]] == 211:
        logger.info("Action -- arrow")
        return (6, )
    logger.info("Action -- nothing")
    return (0, )

