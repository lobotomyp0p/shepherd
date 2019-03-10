"""
SHEPHERD
The game of sheep husbandry
"""

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
import random
import numpy as np

## Constants
BANNER_PATH = "./banner.txt"
with open(BANNER_PATH) as f:
    BANNER_TXT = f.read()
HELP_PATH = "./help.txt"
with open(HELP_PATH) as f:
    HELP_TXT = f.read()
HELP_CMD = "help"
EXIT_TXT = "Exiting..."
EXIT_CMD = "exit"
CMD_ERR = "You can't do that."
SHEEP_COST = 300
SHEEP_SALE = 200
SHEEP_THRESH = 5
BUY_ERR = "You don't have enough money."
BUY_SUCCESS = "You bought {} for {} gold!"
NAMES_PATH = "./names.txt"
with open(NAMES_PATH) as f:
    SHEEP_NAMES = f.read().split("\n")
SHEEP_NAMES.remove("")
GRADE_RANGE = (1,100)
ORDER_NO_STR = "Quantity"
ORDER_GRADE_STR = "Grade"
BREED_ERR_1 = "USAGE: breed <sheep name 1> <sheep name 2>"
BREED_ERR_2 = "You don't have a sheep by the name of {}."
NMS_ERR = "Don't masturbate the sheep, you sheepfucker."
BREED_SUCCESS = "You successfully bred {} and {} to produce {}!"
ADD_SHEEP_ERR = "You can't handle another sheep! Sell some first."
SELL_ERR = "USAGE: sell <sheep name>"
SELL_SUCCESS = "You sold {} for {} gold!"
SHIP_ERR = "USAGE: ship <sheep name 1> <sheep name 2> ... <sheep name <ticket quantity>>"
SHIP_SUCCESS = "You sold {} sheep for {} gold!"
ORDER_STR = "You have a new ticket!"

## Setting up actions
ACTIONS = ('breed'
           ,'buy'
           ,'fold'
           ,'sell'
           ,'ship'
           ,'ticket'
           ,'help'
           ,'exit')
def doThing(game,cmd):
    """
    For selecting the available actions.
    """
    if cmd.strip().startswith(ACTIONS[0]):
        game.doBreed(cmd)
    elif cmd.strip().startswith(ACTIONS[1]):
        game.doBuy()
    elif cmd.strip().startswith(ACTIONS[2]):
        game.doFold()
    elif cmd.strip().startswith(ACTIONS[3]):
        game.doSell(cmd)
    elif cmd.strip().startswith(ACTIONS[4]):
        game.doShip(cmd)
    elif cmd.strip().startswith(ACTIONS[5]):
        game.doTicket()
    elif cmd.strip().lower().startswith(HELP_CMD):
        print(HELP_TXT)
    elif cmd.strip().lower().startswith(EXIT_CMD):
        print(EXIT_TXT)
        quit()
    else:
        print(CMD_ERR)

def getName():
    return random.choice(SHEEP_NAMES)

def getGrade():
    return random.randint(GRADE_RANGE[0],GRADE_RANGE[1])

class Game():
    """
    """
    def __init__(self):
        ## start with no money
        self.wallet = 0
        ## add initial sheep
        self.sheep = {}
        self.addSheep(None)
        self.addSheep(None)
        ## The first sheeps should have sufficiently different grades
        ## So until they're different enough, we'll remove and try new sheep
        while abs(list(self.sheep.values())[0] - list(self.sheep.values())[1]) < SHEEP_THRESH:
            self.sheep.popitem()
            self.addSheep(None)
        ## the order ticket is based on the initial sheep
        self.order = {ORDER_NO_STR : 3
                      , ORDER_GRADE_STR : [min(self.sheep.values())
                                           ,max(self.sheep.values())]
                      }
        ## and set up the first order
        print(ORDER_STR)
        self.doTicket()


    def addSheep(self,parents):
        """ Add a sheep to the fold.
        """
        ## Don't add more sheep than we have names for
        if len(self.sheep) == len(SHEEP_NAMES):
            print(ADD_SHEEP_ERR)
            return
        ## Give the sheep a unique name
        name = getName()
        while name in self.sheep:
            name = getName()
        ## If the sheep is not bred, assign it a random grade
        if parents == None:
            grade = getGrade()
        else: ## Otherwise grade it based on its parents
            grade = int(random.gauss(sum(parents)/2
                                     ,abs(parents[0]-parents[1])/4))
            while grade < min(GRADE_RANGE) or grade > max(GRADE_RANGE):
                grade = int(random.gauss(sum(parents)/2
                                         ,abs(parents[0]-parents[1])/4))
        self.sheep[name] = grade
        return name

    def newOrder(self,quantity):
        """ Put in a new order.
        """
        self.order[ORDER_NO_STR] = quantity
        grades = [getGrade(),getGrade()]
        while abs(grades[0]-grades[1]) < 5:
            grades = [getGrade(),getGrade()]
        self.order[ORDER_GRADE_STR] = grades
        print(ORDER_STR)
        self.doTicket()
        return
    
    def doBreed(self,cmd):
        ## parse the command for args
        cmd_list = cmd.split()
        if len(cmd_list) != 3:
            print(BREED_ERR_1)
            return
        ## match the args to sheep
        sheepa = cmd_list[1]
        if sheepa not in self.sheep:
            print(BREED_ERR_2.format(sheepa))
            return
        sheepb = cmd_list[2]
        if sheepb not in self.sheep:
            print(BREED_ERR_2.format(sheepb))
            return
        if sheepa == sheepb :
            print(NMS_ERR)
            return
        ## add a new sheep to the fold
        name = self.addSheep([self.sheep[sheepa]
                       ,self.sheep[sheepb]])
        if name != None:
            print(BREED_SUCCESS.format(sheepa,sheepb,name))
        return
    
    def doBuy(self):
        if self.wallet < SHEEP_COST:
            print(BUY_ERR)
            return
        ## deduct funds from wallet
        self.wallet += -1*SHEEP_COST
        ## add a new sheep to the fold
        name = self.addSheep(None)
        print(BUY_SUCCESS.format(name,SHEEP_COST))
        return
    
    def doFold(self):
        ## print the current fold
        print("You have {} gold.".format(self.wallet))
        print("You have {} sheep.".format(len(self.sheep)))
        print("GRADE\tNAME")
        for s in self.sheep:
            print("{}\t{}".format(self.sheep[s],s))
        return
    
    def doSell(self,cmd):
        ## parse the command for args
        cmd_list = cmd.split()
        if len(cmd_list) != 2:
            print(SELL_ERR)
            return
        ## match the args to sheep
        sheepa = cmd_list[1]
        if sheepa not in self.sheep:
            print(BREED_ERR_2.format(sheepa))
            return
        ## remove a sheep from the fold
        self.sheep.pop(sheepa)
        ## add funds to wallet
        self.wallet += SHEEP_SALE
        print(SELL_SUCCESS.format(sheepa,SHEEP_SALE))
        return
    
    def doShip(self,cmd):
        ## parse the command for args
        cmd_list = cmd.split()
        if len(cmd_list) != (1 + self.order[ORDER_NO_STR]):
            print(SHIP_ERR)
            return
        ## match the args to sheep
        sheepment = cmd_list[1:]
        for s in sheepment:
            if s not in self.sheep:
                print(BREED_ERR_2.format(s))
                return
        ## grade the shipment
        ## the ideal shipment is composed of evenly graded sheep
        grades = [self.sheep[s] for s in sheepment]
        #print("GRADES: {}".format(grades))
        grades.sort()
        #print("SORTED GRADES: {}".format(grades))
        ideal_grades = np.linspace(min(self.order[ORDER_GRADE_STR])
                                , max(self.order[ORDER_GRADE_STR])
                                , self.order[ORDER_NO_STR])
        #print("IDEAL GRADES: {}".format(ideal_grades))
        difference = sum((grades-ideal_grades)**2/ideal_grades)
        #print("DIFFERENCE: {}".format(difference))
        bonus = 100 * len(sheepment) - int(difference * 100)
        if bonus < 0:
            bonus = 0
        #print("BONUS: {}".format(bonus))
        ## calculate price
        base_price = SHEEP_SALE * len(sheepment)
        if min(grades) < min(self.order[ORDER_GRADE_STR]) or max(grades) > max(self.order[ORDER_GRADE_STR]):
            bonus = -100
        total = base_price + bonus
        ## add funds to wallet
        self.wallet += total
        ## remove sheep from the fold
        for s in sheepment:
            self.sheep.pop(s)
        print(SHIP_SUCCESS.format(len(grades),total))
        self.newOrder(self.order[ORDER_NO_STR]**2)
        return
    
    def doTicket(self):
        ## print the current order
        print("{}: {}".format(ORDER_NO_STR,self.order[ORDER_NO_STR]))
        print("Minimum Grade: {}".format(min(self.order[ORDER_GRADE_STR])))
        print("Maximum Grade: {}".format(max(self.order[ORDER_GRADE_STR])))
        return


print(BANNER_TXT)
GAME = Game()
while 1: ## Game loop
    ## Start a new order
    while 1: ## User input loop
        CURRENT_FOLD = [a for a in GAME.sheep.keys()]
        ACTIONS_LIST = list(ACTIONS)
        ACTIONS_LIST.extend(CURRENT_FOLD)
        COMPLETER = WordCompleter(ACTIONS_LIST)
        USER_INPUT = prompt(u'Shepherd>'
                            , completer=COMPLETER
                            ,)
        doThing(GAME,USER_INPUT)
