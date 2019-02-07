import cv2
import pytesseract
import ImageAnalyser as ia
import logging

logger = logging.getLogger("ZombidleBotLogger")

def processArcane(img, configs):
    if img[configs.repeatLastCraftPos[1], configs.repeatLastCraftPos[0]] > 55:
        logger.info("Arcane -- repeat last craft")
        return (configs.repeatLastCraftPos[0], configs.repeatLastCraftPos[1])
    if img[configs.fastGhostCraftPos[1], configs.fastGhostCraftPos[0]] > 55:
        logger.info("Arcane -- fast ghost craft")
        return (configs.fastGhostCraftPos[0], configs.fastGhostCraftPos[1])
    if img[configs.collectAllPos[1], configs.collectAllPos[0]] > 55:
        logger.info("Arcane -- collect all")
        return (configs.collectAllPos[0], configs.collectAllPos[1])
    if img[configs.nextBoostPos[1], configs.nextBoostPos[0]] > 55:
        logger.info("Arcane -- craft boost")
        return (configs.nextBoostPos[0], configs.nextBoostPos[1])
    logger.info("Arcane -- quit")
    return (configs.arcaneQuitPos[0], configs.arcaneQuitPos[1])

def findPos(read1, read2, read3, ids, configs):
    if all(x in read1 for x in ids):
        return configs.reward1Pos
    if all(x in read2 for x in ids):
        return configs.reward2Pos
    if all(x in read3 for x in ids):
        return configs.reward3Pos
    return None

def processReward(img, configs):
    read1 = ia.readCharacters(img, configs.reward1Box)
    logger.debug("read reward1 : " + read1)
    read2 = ia.readCharacters(img, configs.reward2Box)
    logger.debug("read reward2 : " + read2)
    read3 = ia.readCharacters(img, configs.reward3Box)
    logger.debug("read reward3 : " + read3)
    p = findPos(read1, read2, read3, ["Chalice"], configs)
    if p != None:
        logger.info("Chest Reward -- Death Chalice")
        return p

    p = findPos(read1, read2, read3, ["cro Sw"], configs)
    if p != None:
        logger.info("Chest Reward -- Necro Sword")
        return p

    p = findPos(read1, read2, read3, ["abl"], configs)
    if p != None:
        logger.info("Chest Reward -- Stone Tablet")
        return p

    p = findPos(read1, read2, read3, ["Ring"], configs)
    if p != None:
        logger.info("Chest Reward -- Magic Ring")
        return p

    p = findPos(read1, read2, read3, ["ower"], configs)
    if p != None:
        logger.info("Chest Reward -- Power Potion")
        return p

    p = findPos(read1, read2, read3, ["ow", "x"], configs)
    if p != None:
        logger.info("Chest Reward -- Power Axe")
        return p

    p = findPos(read1, read2, read3, ["Collar"], configs)
    if p != None:
        logger.info("Chest Reward -- King's Collar")
        return p

    p = findPos(read1, read2, read3, ["Bear"], configs)
    if p != None:
        logger.info("Chest Reward -- Squid's Teddy Bear")
        return p

    p = findPos(read1, read2, read3, ["BC's"], configs)
    if p != None:
        logger.info("Chest Reward -- Lich's ABC's")
        return p

    p = findPos(read1, read2, read3, ["lagu"], configs)
    if p != None:
        logger.info("Chest Reward -- Plague in a Bottle")
        return p

    p = findPos(read1, read2, read3, ["ancy"], configs)
    if p != None:
        logger.info("Chest Reward -- Bat's Fancy Pin")
        return p

    p = findPos(read1, read2, read3, ["hys"], configs)
    if p != None:
        logger.info("Chest Reward -- Specter's Amethyst")
        return p

    p = findPos(read1, read2, read3, ["Knight"], configs)
    if p != None:
        logger.info("Chest Reward -- Red Knight's Lipstick")
        return p

    p = findPos(read1, read2, read3, ["Gian"], configs)
    if p != None:
        logger.info("Chest Reward -- Giant Zombie's Mace")
        return p

    p = findPos(read1, read2, read3, ["Zombie"], configs)
    if p != None:
        logger.info("Chest Reward -- Zombie Horde's Eye")
        return p

    logger.info("Chest Reward -- Left Item")
    return configs.reward1Pos

def determineAction(img, configs):
    logger.info("Action -- Start")
    read = ia.readCharacters(img, configs.dealBox)
    if read == "THE DEAL":
        logger.info("Action -- deal")
        read = ia.readCharacters(img, configs.dealContentBox)
        logger.debug("read deal : " + read)
        if len(read) < 40:
            logger.info("Deal -- message too short")
            return (0, )
        if "ull" in read or "minutes" in read:
            logger.info("Deal -- Skull x")
            return (1, configs.dealNoPos[0], configs.dealNoPos[1])
        if "chest" in read:
            logger.info("Deal -- Chest")
            return (1, configs.dealNoPos[0], configs.dealNoPos[1])
        if "amage" in read or ("sec" in read and "nds" in read):
            logger.info("Deal -- Damage x")
            return (1, configs.dealNoPos[0], configs.dealNoPos[1])
        if "craft" in read or "time" in read:
            logger.info("Deal -- Skip Craft Time")
            if "free" in read:
                return (1, configs.dealAwsomePos[0], configs.dealAwsomePos[1])
            else:
                return (1, configs.dealYesPos[0], configs.dealYesPos[1])
        if "x" in read:
            logger.info("Deal -- Diamonds")
            if "free" in read:
                return (1, configs.dealAwsomePos[0], configs.dealAwsomePos[1])
            else:
                return (1, configs.dealYesPos[0], configs.dealYesPos[1])
        logger.info("Deal -- ??")
        return (1, configs.dealNoPos[0], configs.dealNoPos[1])

    read = ia.readCharacters(img, configs.dealThanksBox)
    if read == "Thanks!":
        logger.info("Action -- thanks")
        return (1, configs.dealExitPubPos[0], configs.dealExitPubPos[1])

    template = cv2.imread("ArcaneIMG.png", 0)
    res = ia.findTemplateInImage(img, template)
    if ia.isInside(res, configs.arcaneIMGBox):
        logger.info("Action -- in arcane")
        return (2, )

    read = ia.readCharacters(img, configs.arcaneTimerBox)
    if "A" in read:
        template = cv2.imread("GoToArcaneButton.png", 0)
        res = ia.findTemplateInImage(img, template)
        if ia.isInside(res, configs.goToArcaneBox):
            logger.info("Action -- click arcane button")
            return (1, configs.goToArcanePos[0], configs.goToArcanePos[1])
        else:
            logger.info("Action -- click item tab")
            return (1, configs.itemTabPos[0], configs.itemTabPos[1])

    template = cv2.imread("Scroll.png", 0)
    res = ia.findTemplateInImage(img, template)
    if ia.isInside(res, configs.notifBox):
        logger.info("Action -- click Scroll")
        return (1, (res[0] + res[2]) / 2, (res[1] + res[3]) / 2)
    template = cv2.imread("ChestCollector.png", 0)
    res = ia.findTemplateInImage(img, template)
    if ia.isInside(res, configs.notifBox):
        logger.info("Action -- click ChestCollector")
        return (1, (res[0] + res[2]) / 2, (res[1] + res[3]) / 2)

    read = ia.readCharacters(img, configs.rewardBox)
    if "REWARD" in read:
        logger.info("Action -- Choose Chest Reward")
        rewardPos = processReward(img, configs)
        return (1, rewardPos[0], rewardPos[1])

    read = ia.readCharacters(img, configs.gotDeathCoinBox)
    if "You got this!" in read:
        logger.info("Action -- Get Death Coins")
        return (1, configs.deahCoinOkPos[0], configs.deahCoinOkPos[1])

    if img[configs.backArrowPos[1], configs.backArrowPos[0]] == 211:
        logger.info("Action -- arrow")
        return (4, )
    logger.info("Action -- nothing")
    return (0, )

