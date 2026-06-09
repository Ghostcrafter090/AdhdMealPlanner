import modules.pytools as pytools
import random

hasSaid = []

class globals:
    aProgram = False

def oneTimeMessage(text):
    if text not in hasSaid:
        print(text)
        hasSaid.append(text)

def getMealProgram():
    
    if not globals.aProgram:
    
        aProgram = pytools.IO.getJson("program.json")
        newProgram = aProgram
        for aMain in aProgram["mains"]:
            if "temp_cost" in newProgram["mains"][aMain]:
                if pytools.clock.dateArrayToUTC(newProgram["mains"][aMain]["temp_cost"][1]) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    oneTimeMessage("Adjusting cost for main " + str(aMain) + " from " + str(newProgram["mains"][aMain]["cost"]) + " to " + str(newProgram["mains"][aMain]["temp_cost"][0]))
                    newProgram["mains"][aMain]["cost"] = newProgram["mains"][aMain]["temp_cost"][0]
        
        i = 0
        for aVegitable in aProgram["vegetables"]:
            if len(aVegitable) > 4:
                if pytools.clock.dateArrayToUTC(aVegitable[4][1]) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    oneTimeMessage("Adjusting cost for vegitable " + str(aVegitable[0]) + " from " + str(newProgram["vegetables"][i][3]) + " to " + str(aVegitable[4][0]))
                    newProgram["vegetables"][i][3] = aVegitable[4][0]
            
            i = i + 1
            
        i = 0
        for aStarch in aProgram["starches"]:
            if len(aStarch) > 4:
                if pytools.clock.dateArrayToUTC(aStarch[4][1]) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    oneTimeMessage("Adjusting cost for vegitable " + str(aStarch[0]) + " from " + str(newProgram["starches"][i][3]) + " to " + str(aStarch[4][0]))
                    newProgram["starches"][i][3] = aStarch[4][0]
            
            i = i + 1
    
        globals.aProgram = newProgram
    
    return globals.aProgram

def getMealChance(cost): 
    return ((0.985779 ** (18.89997 * (float(cost) - 2.22658)) + 0.15198) ** 1.4) / 1.3

class meal:
    
    class main:
        
        aCount = {}
    
        def getCount(aMain):
            if aMain not in meal.main.aCount:
                return 0
            else:
                return meal.main.aCount[aMain]
    
        def select():
            aListOfMains = getMealProgram()["mains"]
            theMain = False
            
            loopCount = 0
            while (not theMain) and (loopCount < 10000) :
                aMain = random.choice(list(aListOfMains.keys()))
                if meal.main.getCount(aMain) < aListOfMains[aMain]["count"]:
                    if aMain not in meal.main.aCount:
                        meal.main.aCount[aMain] = 0
                    meal.main.aCount[aMain] = meal.main.aCount[aMain] + 1
                    
                    if (random.random() * 100) < aListOfMains[aMain]["chance"]:
                        theMain = aMain
                
                loopCount = loopCount + 1
                
            theMain = aMain

            return theMain, aListOfMains[theMain]["cost"]
    
    class vegitable:
        
        aCount = {}
        
        def getCount(aVegitable):
            if aVegitable not in meal.vegitable.aCount:
                return 0
            else:
                return meal.vegitable.aCount[aVegitable]
        
        def select(aMain):
            aListOfMains = getMealProgram()["mains"]
            aListOfVegitables = getMealProgram()["vegetables"]
            theChoices = []
            
            if aListOfMains[aMain]["vegetables"] == False:
                return False, 0.0
            
            if aListOfMains[aMain]["vegetables"]:
                if aListOfMains[aMain]["vegetables"] == "all":
                    theChoices = aListOfVegitables
                
                elif type(aListOfMains[aMain]["vegetables"]) == list:
                    for vegitable in aListOfMains[aMain]["vegetables"]:
                        if vegitable == "all":
                            theChoices.extend(aListOfVegitables)
                        elif vegitable:
                            for aVegitableType in aListOfVegitables:
                                if aVegitableType[0] == vegitable:
                                    theChoices.append(aVegitableType)
                                    break
                            
                        else:
                            theChoices.append([vegitable, 10000, 1])
            
            if len(theChoices) == 0:
                theChoices.append([False, 10000, 1])
            
            theVegitable = False
            
            loopCount = 0
            while (not theVegitable) and (loopCount < 10000) :
                aVegitable = random.choice(theChoices)
                if meal.vegitable.getCount(aVegitable[0]) < aVegitable[1]:
                    if aVegitable[0] not in meal.vegitable.aCount:
                        meal.vegitable.aCount[aVegitable[0]] = 0
                    meal.vegitable.aCount[aVegitable[0]] = meal.vegitable.aCount[aVegitable[0]] + 1
                    
                    if (random.random()) < aVegitable[2]:
                        theVegitable = aVegitable

                loopCount = loopCount + 1
                
            theVegitable = aVegitable
            
            try:
                return theVegitable[0], theVegitable[3]
            except:
                return theVegitable[0], 0.0
    class starch:
        
        aCount = {}
        
        def getCount(aStarch):
            if aStarch not in meal.starch.aCount:
                return 0
            else:
                return meal.starch.aCount[aStarch]
        
        def select(aMain):
            aListOfMains = getMealProgram()["mains"]
            aListOfStarchs = getMealProgram()["starches"]
            theChoices = []
            
            if aListOfMains[aMain]["starches"] == False:
                return False, 0.0
            
            if aListOfMains[aMain]["starches"]:
                if aListOfMains[aMain]["starches"] == "all":
                    theChoices = aListOfStarchs
                
                elif type(aListOfMains[aMain]["starches"]) == list:
                    for starch in aListOfMains[aMain]["starches"]:
                        if starch == "all":
                            theChoices.extend(aListOfStarchs)
                        elif starch:
                            for aStarchType in aListOfStarchs:
                                if aStarchType[0] == starch:
                                    theChoices.append(aStarchType)
                                    break
                            
                        else:
                            theChoices.append([starch, 10000, 1])
            
            if len(theChoices) == 0:
                theChoices.append([False, 10000, 1])
            
            theStarch = False
            
            loopCount = 0
            while (not theStarch) and (loopCount < 10000) :
                aStarch = random.choice(theChoices)
                if meal.starch.getCount(aStarch[0]) < aStarch[1]:
                    if aStarch[0] not in meal.starch.aCount:
                        meal.starch.aCount[aStarch[0]] = 0
                    meal.starch.aCount[aStarch[0]] = meal.starch.aCount[aStarch[0]] + 1
                    
                    if (random.random()) < aStarch[2]:
                        theStarch = aStarch

                loopCount = loopCount + 1
                
            theStarch = aStarch

            try:
                return theStarch[0], theStarch[3]
            except:
                return theStarch[0], 0.0
                    
    class alternate:
        def select(aMain):
            aListOfMains = getMealProgram()["mains"]
            
            theAlternate = False
            if "alternates" in aListOfMains[aMain]:
                theAlternate = random.choice(aListOfMains[aMain]["alternates"])

            cost = 1.57
            if theAlternate in getMealProgram()["alternates"]:
                cost = getMealProgram()["alternates"][theAlternate]
            
            return theAlternate, cost
        
    def generate(currentBudget, totalCost, currentDay):
        def _generate():
            currentCost = 1000
            currentMeal = []
            loopCount = 0
            
            while (((currentBudget - totalCost) / ((((-(((currentDay + 1) - 7.5) / 2.754) ** 2) + 6.63) / 1.5) + 1.5)) < currentCost) and (loopCount < 100):
                aMain, aMainCost = meal.main.select()
                aVegitable, aVegitableCost = meal.vegitable.select(aMain)
                aStarch, aStarchCost = meal.starch.select(aMain)
                anAlternate, anAlternateCost = meal.alternate.select(aMain)
                
                loopCount = loopCount + 1
                
                if (aMainCost + aVegitableCost + aStarchCost + anAlternateCost) < currentCost:
                    currentCost = (aMainCost + aVegitableCost + aStarchCost + anAlternateCost)
                    currentMeal = [aMain, aVegitable, aStarch, anAlternate]
        
            return [*currentMeal, currentCost]
        
        out = _generate()
        while (random.random() * 2) < getMealChance(out[4]):
            out = _generate()
            
        return out
    
    def prettyPrint(aMeal):
        strf = ""
        
        if (aMeal[3]):
            strf = aMeal[3] + " " + aMeal[0]
        else:
            strf = aMeal[0]
        
        if aMeal[2]:
            strf = strf + " with " + aMeal[2]
        
        if aMeal[1] and aMeal[2]:
            strf = strf + " and " + aMeal[1]
        elif aMeal[1]:
            strf = strf + " with " + aMeal[1]
            
        return strf + ", costing roughly $" + str(round(aMeal[4], 2))

def generateMealPlan(currentBudget):
    
    meal.main.aCount = {}
    meal.vegitable.aCount = {}
    meal.starch.aCount = {}
    
    
    totalCost = 0
    mealList = []
    day = 0
    while day < 14:
        if ((day + 1) % 7) != 0:
            aMeal = meal.generate(currentBudget, totalCost, day)
            mealList.append(meal.prettyPrint(aMeal))
            totalCost = totalCost + aMeal[4]
        else:
            mealList.append("pizza, costing roughly $8.86")
            totalCost = totalCost + 8.86
        day = day + 1
        
    return [mealList, totalCost]

def printMealPlan(aMealPlan, aCost):
    dayFormat = {
        1: "Saturday  ",
        2: "Sunday    ",
        3: "Monday    ",
        4: "Tuesday   ",
        5: "Wednesday ",
        6: "Thursday  ",
        0: "Friday    "
    }
    
    strf = ""
    
    day = 0
    while day < 14:
        strf = strf + "\n" + dayFormat[(day + 1) % 7] + ": " + aMealPlan[day]
        day = day + 1
        
    strf = strf + "\n" + "Total Estimated Plan Cost: $" + str(aCost)
        
    return strf

if __name__ == "__main__":
    mealPlanList = []
    lastMin = ["", getMealProgram()["currentBudget"]]
    
    def _minPlan(x):
        return x[1]
    
    i = 0
    n = 0
    while i < getMealProgram()["lowerAmountAggressivness"]:
        print("Starting pass " + str(n) + " + (index " + str(i) + ", with cost of " + str(lastMin[1]) + ")...")
        aMealPlan = generateMealPlan(getMealProgram()["currentBudget"])
        while aMealPlan[1] > getMealProgram()["currentBudget"]:
            aMealPlan = generateMealPlan(getMealProgram()["currentBudget"])
        
        mealPlanList.append(aMealPlan)
        
        if lastMin != min(mealPlanList, key=_minPlan):
            i = 0
        
        lastMin = min(mealPlanList, key=_minPlan)
        
        i = i + 1
        n = n + 1
    
    print(printMealPlan(*min(mealPlanList, key=_minPlan)))