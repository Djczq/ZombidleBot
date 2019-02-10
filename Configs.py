import json

class Configs:
    # coord : (width = left-->rigth (x), heigh = top-->bottom (y))
    # box : (top-left width, top-left heigh, bottom-rigth width, bottom-rigth heigh)
    def __init__(self):
        with open('settings/profile.json') as f:
            data = json.load(f)
        profile = data["profile"]

        with open('settings/' + profile + '/settings.json') as f:
            data = json.load(f)

        self.notifDeplaSize = data["Point"]["notifDeplaSize"]
        self.notifSize = data["Point"]["notifSize"]
        self.notifPos = data["Point"]["notifPos"]
        self.notifBox = data["Box"]["notifBox"]
        self.itemTabPos = data["Point"]["itemTabPos"]
        self.clickPos = data["Point"]["clickPos"]
        self.goToArcaneBox = data["Box"]["goToArcaneBox"]
        self.arcaneIMGBox = data["Box"]["arcaneIMGBox"]
        self.goToArcanePos = data["Point"]["goToArcanePos"]
        self.arcaneTimerBox = data["Box"]["arcaneTimerBox"]
        self.arcaneQuitPos = data["Point"]["arcaneQuitPos"]
        self.nextBoostPos = data["Point"]["nextBoostPos"]
        self.collectAllPos = data["Point"]["collectAllPos"]
        self.fastGhostCraftPos = data["Point"]["fastGhostCraftPos"]
        self.repeatLastCraftPos = data["Point"]["repeatLastCraftPos"]
        self.dealBox = data["Box"]["dealBox"]
        self.errorBox = data["Box"]["errorBox"]
        self.dealThanksBox = data["Box"]["dealThanksBox"]
        self.dealContentBox = data["Box"]["dealContentBox"]
        self.dealAwsomeBox = data["Box"]["dealAwsomeBox"]
        self.dealNothingHappensBox = data["Box"]["dealNothingHappensBox"]
        self.dealNothingHappensPos = data["Point"]["dealNothingHappensPos"]
        self.dealAwsomePos = data["Point"]["dealAwsomePos"]
        self.dealNoPos = data["Point"]["dealNoPos"]
        self.dealYesPos = data["Point"]["dealYesPos"]
        self.dealExitPubPos = data["Point"]["dealExitPubPos"]
        self.backArrowPos = data["Point"]["backArrowPos"]
        self.rewardBox = data["Box"]["rewardBox"]
        self.reward1Box = data["Box"]["reward1Box"]
        self.reward2Box = data["Box"]["reward2Box"]
        self.reward3Box = data["Box"]["reward3Box"]
        self.reward1Pos = data["Point"]["reward1Pos"]
        self.reward2Pos = data["Point"]["reward2Pos"]
        self.reward3Pos = data["Point"]["reward3Pos"]
        self.gotDeathCoinBox = data["Box"]["gotDeathCoinBox"]
        self.deahCoinOkPos = data["Point"]["deathCoinOkPos"]

        self.ArcaneIMG = 'settings/' + profile + '/' + data["IMG"]["Arcane"]
        self.ChestCollectorIMG = 'settings/' + profile + '/' + data["IMG"]["ChestCollector"]
        self.GoToArcaneButtonIMG = 'settings/' + profile + '/' + data["IMG"]["GoToArcaneButton"]
        self.ScrollIMG = 'settings/' + profile + '/' + data["IMG"]["Scroll"]
