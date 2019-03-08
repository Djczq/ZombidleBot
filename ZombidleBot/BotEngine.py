import cv2
import pytesseract
from . import ImageAnalyser as ia
import logging, importlib
from .settings.Point import Point
from .settings.Rectangle import Rectangle

logger = logging.getLogger("ZombidleBotLogger")

def reloadModules():
    importlib.reload(ia)

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
        read = ia.readCharacters(img, settings.shardCraftBox)
        if "RAF" in read:
            logger.debug("read shard box : " + read)
            logger.info("Arcane -- craft splinter or shard")
            return settings.shardCraftBox.getCenterPoint()
    else:
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


def findRigthPanelCursorPos(img, settings):
    return ia.findCenterSameColorHor(img, settings.rigthPanelBarBox, 5, 211, 220)

def findMinionTilesPos(img, settings):
    return ia.findCenterSameColorHor(img, settings.rigthPanelMinionBox, 5, 19, 25)


def levelUpMinions(img, settings):
    pm = img[settings.minionTabPos.height, settings.minionTabPos.width]
    logger.debug("img minion tab : " + str(pm))
    if len(findRigthPanelCursorPos(img, settings)) != 2:
        return None
    if pm != 29:
        return (1, settings.minionTabPos)
    r = [2]
    l = findMinionTilesPos(img, settings)
    king = False
    carl = False
    read = ia.readCharacters(img, settings.multipleBuyBox)
    logger.debug("read multiple buy box : " + read)
    if "MAX" not in read:
        r.append(settings.multipleBuyBox.getCenterPoint())
        logger.debug("append multiple buy")
        r[0] = 1
        return r
    for i in range(0, len(l), 2):
        p = l[i]
        if p.width >= settings.rigthPanelMinionBox.topleft.width - 2 and l[i+1] >= settings.minionTileWidth - settings.minionPortraitWidth:
            box = Rectangle.fromValues(p.width + l[i+1] - settings.minionTileWidth + settings.minionPortraitWidth, settings.minionNameBot, p.width + l[i+1], settings.minionNameTop)
            readname = ia.readCharacters(img, box)
            logger.debug("read minion name box 1 : " + readname)
            if "Tomb" in readname:
                king = True
            if "CARL" in readname:
                carl = True

            box = Rectangle.fromValues(p.width + 10, settings.levelUpBot, p.width + settings.levelUpWidth, settings.levelUpTop)
            point = box.getCenterPoint()
            pixel = img[settings.levelUpRedHeight, int(point.width)]
            logger.debug("pos level up 1 : " + str(point.width) + " " + str(settings.levelUpRedHeight))
            logger.debug("img level up 1 : " + str(pixel))
            if pixel == 29:
                continue
            if pixel == 53 or pixel == 25:
                r.append(point)
            else:
                r.append(Point(p.width + l[i+1] / 2, settings.buyHeight))
            continue

        if p.width + l[i+1] >= settings.rigthPanelMinionBox.botrigth.width - 2 and l[i+1] >= settings.levelUpWidth:
            box = Rectangle.fromValues(p.width + 10, settings.levelUpBot, p.width + settings.levelUpWidth, settings.levelUpTop)
            read = ia.readCharacters(img, box)
            logger.debug("read level up box 3 : " + read)
            continue
            if "LEVEL" in read:
                r.append(box.getCenterPoint())
            else:
                r.append(Point(p.width + l[i+1] / 2, settings.buyHeight))
                r.append(settings.rigthPanelRigthArrowPos)
                r[0] = 1

    logger.debug("carl " + str(carl))
    logger.debug("king " + str(king))
    if carl != True or king != True:
        r[0] = 1
        if carl == True:
            r.append(settings.rigthPanelLeftArrowPos)
            logger.debug("append left")
        if king == True:
            r.append(settings.rigthPanelRigthArrowPos)
            logger.debug("append right")
    if carl != True and king != True:
        r.append(settings.rigthPanelRigthArrowPos)
        logger.debug("append right")
        r[0] = 1

    if len(r) > 1:
        return r
    else:
        return None


def determineAction(img, settings, mode = 0):
    logger.debug("mode : " + str(mode))
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
    if "READY" in read:
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
    logger.debug("read reward box : " + read)
    if "REWARD" in read or "Things" in read:
        logger.info("Action -- Choose Chest Reward")
        rewardPos = processReward(img, settings)
        return (1, rewardPos)

    read = ia.readCharacters(img, settings.gotDeathCoinBox)
    if "You got this!" in read:
        logger.info("Action -- Get Death Coins")
        return (1, settings.okPos)

    read = ia.readCharacters(img, settings.dealNothingHappensBox)
    if "smash that button" in read:
        logger.info("Action -- Nothing Happens")
        return (1, settings.dealNothingHappensPos)

    read = ia.readCharacters(img, settings.errorBox)
    if "Error" in read:
        logger.info("Action -- Error")
        return (1, settings.okPos)

    if mode == 1:
        logger.debug("level up minions")
        r = levelUpMinions(img, settings)
        if r != None:
            return r

    read = ia.readCharacters(img, settings.HPBox)
    logger.debug("read HP box : " + read)
    if "HP" in read:
        logger.info("Action -- Can click")
        return (4, )

    logger.info("Action -- nothing")
    return (0, )

