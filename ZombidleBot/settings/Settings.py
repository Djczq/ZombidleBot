import json
from Point import Point

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
        self.notifBox = data["Box"]["notifBox"]
        self.itemTabPos = Point.fromArray(data["Point"]["itemTabPos"])
        self.clickPos = Point.fromArray(data["Point"]["clickPos"])
        self.goToArcaneBox = data["Box"]["goToArcaneBox"]
        self.arcaneIMGBox = data["Box"]["arcaneIMGBox"]
        self.goToArcanePos = Point.fromArray(data["Point"]["goToArcanePos"])
        self.arcaneTimerBox = data["Box"]["arcaneTimerBox"]
        self.arcaneQuitPos = Point.fromArray(data["Point"]["arcaneQuitPos"])
        self.nextBoostPos = Point.fromArray(data["Point"]["nextBoostPos"])
        self.collectAllPos = Point.fromArray(data["Point"]["collectAllPos"])
        self.fastGhostCraftPos = Point.fromArray(data["Point"]["fastGhostCraftPos"])
        self.repeatLastCraftPos = Point.fromArray(data["Point"]["repeatLastCraftPos"])
        self.dealBox = data["Box"]["dealBox"]
        self.errorBox = data["Box"]["errorBox"]
        self.dealThanksBox = data["Box"]["dealThanksBox"]
        self.dealContentBox = data["Box"]["dealContentBox"]
        self.dealAwsomeBox = data["Box"]["dealAwsomeBox"]
        self.dealNothingHappensBox = data["Box"]["dealNothingHappensBox"]
        self.dealNothingHappensPos = Point.fromArray(data["Point"]["dealNothingHappensPos"])
        self.dealAwsomePos = Point.fromArray(data["Point"]["dealAwsomePos"])
        self.dealNoPos = Point.fromArray(data["Point"]["dealNoPos"])
        self.dealYesPos = Point.fromArray(data["Point"]["dealYesPos"])
        self.dealExitPubPos = Point.fromArray(data["Point"]["dealExitPubPos"])
        self.backArrowPos = Point.fromArray(data["Point"]["backArrowPos"])
        self.rewardBox = data["Box"]["rewardBox"]
        self.reward1Box = data["Box"]["reward1Box"]
        self.reward2Box = data["Box"]["reward2Box"]
        self.reward3Box = data["Box"]["reward3Box"]
        self.reward1Pos = Point.fromArray(data["Point"]["reward1Pos"])
        self.reward2Pos = Point.fromArray(data["Point"]["reward2Pos"])
        self.reward3Pos = Point.fromArray(data["Point"]["reward3Pos"])
        self.gotDeathCoinBox = data["Box"]["gotDeathCoinBox"]
        self.deahCoinOkPos = Point.fromArray(data["Point"]["deathCoinOkPos"])

        self.ArcaneIMG = 'settings/' + profile + '/' + data["IMG"]["Arcane"]
        self.ChestCollectorIMG = 'settings/' + profile + '/' + data["IMG"]["ChestCollector"]
        self.GoToArcaneButtonIMG = 'settings/' + profile + '/' + data["IMG"]["GoToArcaneButton"]
        self.ScrollIMG = 'settings/' + profile + '/' + data["IMG"]["Scroll"]
