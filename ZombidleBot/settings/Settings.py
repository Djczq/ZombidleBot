import json
from Point import Point
from Rectangle import Rectangle

class Settings:
    # coord : (width = left-->rigth (x), heigh = top-->bottom (y))
    # box : (top-left width, top-left heigh, bottom-rigth width, bottom-rigth heigh)
    def __init__(self):
        with open('settings/profile.json') as f:
            data = json.load(f)
        profile = data["profile"]

        with open('settings/' + profile + '/settings.json') as f:
            data = json.load(f)

        self.notifDeplaSize = Point.fromArray(data["Point"]["notifDeplaSize"])
        self.notifSize = Point.fromArray(data["Point"]["notifSize"])
        self.notifPos = Point.fromArray(data["Point"]["notifPos"])
        self.itemTabPos = Point.fromArray(data["Point"]["itemTabPos"])
        self.clickPos = Point.fromArray(data["Point"]["clickPos"])
        self.goToArcanePos = Point.fromArray(data["Point"]["goToArcanePos"])
        self.arcaneQuitPos = Point.fromArray(data["Point"]["arcaneQuitPos"])
        self.nextBoostPos = Point.fromArray(data["Point"]["nextBoostPos"])
        self.collectAllPos = Point.fromArray(data["Point"]["collectAllPos"])
        self.fastGhostCraftPos = Point.fromArray(data["Point"]["fastGhostCraftPos"])
        self.repeatLastCraftPos = Point.fromArray(data["Point"]["repeatLastCraftPos"])
        self.dealNothingHappensPos = Point.fromArray(data["Point"]["dealNothingHappensPos"])
        self.dealAwsomePos = Point.fromArray(data["Point"]["dealAwsomePos"])
        self.dealNoPos = Point.fromArray(data["Point"]["dealNoPos"])
        self.dealYesPos = Point.fromArray(data["Point"]["dealYesPos"])
        self.dealExitPubPos = Point.fromArray(data["Point"]["dealExitPubPos"])
        self.backArrowPos = Point.fromArray(data["Point"]["backArrowPos"])
        self.reward1Pos = Point.fromArray(data["Point"]["reward1Pos"])
        self.reward2Pos = Point.fromArray(data["Point"]["reward2Pos"])
        self.reward3Pos = Point.fromArray(data["Point"]["reward3Pos"])
        self.deahCoinOkPos = Point.fromArray(data["Point"]["deathCoinOkPos"])
        self.dealTryAgainOffset = Point.fromArray(data["Point"]["dealTryAgainOffset"])

        self.gotDeathCoinBox = Rectangle.fromArray(data["Box"]["gotDeathCoinBox"])
        self.notifBox = Rectangle.fromArray(data["Box"]["notifBox"])
        self.goToArcaneBox = Rectangle.fromArray(data["Box"]["goToArcaneBox"])
        self.arcaneIMGBox = Rectangle.fromArray(data["Box"]["arcaneIMGBox"])
        self.rewardBox = Rectangle.fromArray(data["Box"]["rewardBox"])
        self.reward1Box = Rectangle.fromArray(data["Box"]["reward1Box"])
        self.reward2Box = Rectangle.fromArray(data["Box"]["reward2Box"])
        self.reward3Box = Rectangle.fromArray(data["Box"]["reward3Box"])
        self.dealBox = Rectangle.fromArray(data["Box"]["dealBox"])
        self.errorBox = Rectangle.fromArray(data["Box"]["errorBox"])
        self.dealThanksBox = Rectangle.fromArray(data["Box"]["dealThanksBox"])
        self.dealContentBox = Rectangle.fromArray(data["Box"]["dealContentBox"])
        self.dealAwsomeBox = Rectangle.fromArray(data["Box"]["dealAwsomeBox"])
        self.dealNothingHappensBox = Rectangle.fromArray(data["Box"]["dealNothingHappensBox"])
        self.arcaneTimerBox = Rectangle.fromArray(data["Box"]["arcaneTimerBox"])

        self.ArcaneIMG = 'settings/' + profile + '/' + data["IMG"]["Arcane"]
        self.ChestCollectorIMG = 'settings/' + profile + '/' + data["IMG"]["ChestCollector"]
        self.GoToArcaneButtonIMG = 'settings/' + profile + '/' + data["IMG"]["GoToArcaneButton"]
        self.ScrollIMG = 'settings/' + profile + '/' + data["IMG"]["Scroll"]
