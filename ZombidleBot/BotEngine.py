import cv2
import pytesseract
from . import ImageAnalyser as ia
import logging
from .settings.Point import Point

logger = logging.getLogger("ZombidleBotLogger")

def checkShard(img, settings):
    read = ia.readCharacters(img, settings.shardTileBox)
    logger.debug("read shard tile : " + read)
    if "SHARD" in read:
        return None
    else:
        read = ia.readCharacters(img, settings.shardEnterBox)
        logger.debug("read shard menu entry : " + read)
        if "SHARDS" in read:
            logger.debug("arcane img enter shard : " + str(img[settings.shardEnterRedPos.height, settings.shardEnterRedPos.width]))
            if img[settings.shardEnterRedPos.height, settings.shardEnterRedPos.width] > 55:
                logger.info("Arcane -- enter shard menu")
                return settings.shardEnterRedPos
            else:
                return None
        else:
            return None
    return None

def processArcane(img, settings):
    pr = img[settings.repeatLastCraftPos.height, settings.repeatLastCraftPos.width]
    pg = img[settings.fastGhostCraftPos.height, settings.fastGhostCraftPos.width]
    pc = img[settings.collectAllPos.height, settings.collectAllPos.width]
    pb = img[settings.nextBoostPos.height, settings.nextBoostPos.width]
    logger.debug("arcane img repeat : " + str(pr))
    logger.debug("arcane img ghost : " + str(pg))
    logger.debug("arcane img collect : " + str(pc))
    logger.debug("arcane img boost : " + str(pb))
    read = ia.readCharacters(img, settings.shardNoteBox)
    if "build one shard" in read:
        logger.debug("read shard note : " + read)
        logger.info("Arcane -- craft splinter or shard")
        return settings.shardCraftPos
    if pr == 61:
        r = checkShard(img, settings)
        if r != None:
            return r
        else:
            logger.info("Arcane -- repeat last craft")
            return settings.repeatLastCraftPos
    if pg == 61:
        r = checkShard(img, settings)
        if r != None:
            return r
        else:
            logger.info("Arcane -- fast ghost craft")
            return settings.fastGhostCraftPos
    if pc == 61:
        logger.info("Arcane -- collect all")
        return settings.collectAllPos
    if pb == 61:
        logger.info("Arcane -- craft boost")
        return settings.nextBoostPos
    if pr == 31 and pg == 31 and pc == 31 and pb == 31:
        logger.info("Arcane -- quit")
        return settings.arcaneQuitPos
    logger.info("Arcane -- wait")
    return None

def findPos(read1, read2, read3, ids, settings):
    if all(x in read1 for x in ids):
        return settings.reward1Pos
    if all(x in read2 for x in ids):
        return settings.reward2Pos
    if all(x in read3 for x in ids):
        return settings.reward3Pos
    return None

def processReward(img, settings):
    read1 = ia.readCharacters(img, settings.reward1Box)
    logger.debug("read reward1 : " + read1)
    read2 = ia.readCharacters(img, settings.reward2Box)
    logger.debug("read reward2 : " + read2)
    read3 = ia.readCharacters(img, settings.reward3Box)
    logger.debug("read reward3 : " + read3)
    p = findPos(read1, read2, read3, ["Chalice"], settings)
    if p != None:
        logger.info("Chest Reward -- Death Chalice")
        return p

    p = findPos(read1, read2, read3, ["cro Sw"], settings)
    if p != None:
        logger.info("Chest Reward -- Necro Sword")
        return p

    p = findPos(read1, read2, read3, ["abl"], settings)
    if p != None:
        logger.info("Chest Reward -- Stone Tablet")
        return p

    p = findPos(read1, read2, read3, ["Ring"], settings)
    if p != None:
        logger.info("Chest Reward -- Magic Ring")
        return p

    p = findPos(read1, read2, read3, ["ower"], settings)
    if p != None:
        logger.info("Chest Reward -- Power Potion")
        return p

    p = findPos(read1, read2, read3, ["ow", "x"], settings)
    if p != None:
        logger.info("Chest Reward -- Power Axe")
        return p

    p = findPos(read1, read2, read3, ["Collar"], settings)
    if p != None:
        logger.info("Chest Reward -- King's Collar")
        return p

    p = findPos(read1, read2, read3, ["Bear"], settings)
    if p != None:
        logger.info("Chest Reward -- Squid's Teddy Bear")
        return p

    p = findPos(read1, read2, read3, ["BC's"], settings)
    if p != None:
        logger.info("Chest Reward -- Lich's ABC's")
        return p

    p = findPos(read1, read2, read3, ["lagu"], settings)
    if p != None:
        logger.info("Chest Reward -- Plague in a Bottle")
        return p

    p = findPos(read1, read2, read3, ["ancy"], settings)
    if p != None:
        logger.info("Chest Reward -- Bat's Fancy Pin")
        return p

    p = findPos(read1, read2, read3, ["hys"], settings)
    if p != None:
        logger.info("Chest Reward -- Specter's Amethyst")
        return p

    p = findPos(read1, read2, read3, ["Knight"], settings)
    if p != None:
        logger.info("Chest Reward -- Red Knight's Lipstick")
        return p

    p = findPos(read1, read2, read3, ["Gian"], settings)
    if p != None:
        logger.info("Chest Reward -- Giant Zombie's Mace")
        return p

    p = findPos(read1, read2, read3, ["Zombie"], settings)
    if p != None:
        logger.info("Chest Reward -- Zombie Horde's Eye")
        return p

    logger.info("Chest Reward -- Left Item")
    return settings.reward1Pos

def determineAction(img, settings):
    logger.info("Action -- Start")
    read = ia.readCharacters(img, settings.dealBox)
    if read == "THE DEAL":
        logger.info("Action -- deal")
        read = ia.readCharacters(img, settings.dealContentBox)
        logger.debug("read deal : " + read)
        if len(read) < 40:
            logger.info("Deal -- message too short")
            return (0, )
        if "ull" in read or "minutes" in read:
            logger.info("Deal -- Skull x")
            return (1, settings.dealNoPos)
        if "chest" in read:
            logger.info("Deal -- Chest")
            return (1, settings.dealNoPos)
        if "amage" in read or ("sec" in read and "nds" in read):
            logger.info("Deal -- Damage x")
            return (1, settings.dealNoPos)
        if "craft" in read or "time" in read:
            logger.info("Deal -- Skip Craft Time")
            if "free" in read:
                return (1, settings.dealAwsomePos)
            else:
                return (1, settings.dealYesPos)
        if "x" in read:
            logger.info("Deal -- Diamonds")
            if "free" in read:
                return (1, settings.dealAwsomePos)
            else:
                return (1, settings.dealYesPos)
        logger.info("Deal -- ??")
        return (1, settings.dealNoPos)

    read = ia.readCharacters(img, settings.dealBox.offset(settings.dealTryAgainOffset))
    if read == "THE DEAL":
        logger.info("Action -- deal (after try again)")
        read = ia.readCharacters(img, settings.dealContentBox.offset(settings.dealTryAgainOffset))
        logger.debug("read deal : " + read)
        return (1, settings.dealYesPos.add(settings.dealTryAgainOffset))

    read = ia.readCharacters(img, settings.dealThanksBox)
    if read == "Thanks!":
        logger.info("Action -- thanks")
        return (1, settings.dealExitPubPos)

    template = cv2.imread(settings.ArcaneIMG, 0)
    res = ia.findTemplateInImage(img, template)
    if settings.arcaneIMGBox.contains(res):
        logger.info("Action -- in arcane")
        arcanePos = processArcane(img, settings)
        if arcanePos == None:
            return (0, )
        else:
            return (1, arcanePos)

    read = ia.readCharacters(img, settings.arcaneTimerBox)
    if "A" in read:
        logger.debug("read timer : " + read)
        template = cv2.imread(settings.GoToArcaneButtonIMG, 0)
        res = ia.findTemplateInImage(img, template)
        if settings.goToArcaneBox.contains(res):
            logger.info("Action -- click arcane button")
            return (1, settings.goToArcanePos)
        else:
            logger.info("Action -- click item tab")
            return (1, settings.itemTabPos)

    template = cv2.imread(settings.ScrollIMG, 0)
    res = ia.findTemplateInImage(img, template)
    if settings.notifBox.contains(res):
        logger.info("Action -- click Scroll")
        return (1, res.getCenterPoint())
    template = cv2.imread(settings.ChestCollectorIMG, 0)
    res = ia.findTemplateInImage(img, template)
    if settings.notifBox.contains(res):
        logger.info("Action -- click ChestCollector")
        return (1, res.getCenterPoint())

    read = ia.readCharacters(img, settings.rewardBox)
    if "REWARD" in read:
        logger.info("Action -- Choose Chest Reward")
        rewardPos = processReward(img, settings)
        return (1, rewardPos)

    read = ia.readCharacters(img, settings.gotDeathCoinBox)
    if "You got this!" in read:
        logger.info("Action -- Get Death Coins")
        return (1, settings.deahCoinOkPos)

    read = ia.readCharacters(img, settings.dealNothingHappensBox)
    if "smash that button" in read:
        logger.info("Action -- Nothing Happens")
        return (1, settings.dealNothingHappensPos)

    read = ia.readCharacters(img, settings.errorBox)
    if "Error" in read:
        logger.info("Action -- Error")
        return (1, settings.deahCoinOkPos)

    if img[settings.backArrowPos.height, settings.backArrowPos.width] == 211:
        logger.info("Action -- arrow")
        return (4, )
    logger.info("Action -- nothing")
    return (0, )

