import modules.pytools as pytools
import random

def getMealProgram():
    return pytools.IO.getJson("program.json")

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

            return theMain
    
    class vegitable:
        
        aCount = {}
        
        def getCount(aVegitable):
            if aVegitable not in meal.vegitable.aCount:
                return 0
            else:
                return meal.vegitable.aCount[aVegitable]
        
        def select(aMain):
            aListOfMains = getMealProgram()["mains"]
            aListOfVegitables = getMealProgram()["vegitables"]
            theChoices = []
            
            if aListOfMains[aMain]["vegitables"]:
                if aListOfMains[aMain]["vegitables"] == "all":
                    theChoices = aListOfVegitables
                
                elif type(aListOfMains[aMain]["vegitables"]) == list:
                    for vegitable in aListOfMains[aMain]["vegitables"]:
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

            return theVegitable[0]

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

            return theStarch[0]
                    
    class alternate:
        def select(aMain):
            aListOfMains = getMealProgram()["mains"]
            
            theAlternate = False
            if "alternates" in aListOfMains[aMain]:
                theAlternate = random.choice(aListOfMains[aMain]["alternates"])

            return theAlternate
        
    def generate():
        aMain = meal.main.select()
        aVegitable = meal.vegitable.select(aMain)
        aStarch = meal.starch.select(aMain)
        anAlternate = meal.alternate.select(aMain)
        
        return [aMain, aVegitable, aStarch, anAlternate]
    
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
            
        return strf


def generateMealPlan():
    
    meal.main.aCount = {}
    meal.vegitable.aCount = {}
    meal.starch.aCount = {}
    
    mealList = []
    day = 0
    while day < 14:
        if ((day + 1) % 7) != 0:
            mealList.append(meal.prettyPrint(meal.generate()))
        else:
            mealList.append("pizza")
        day = day + 1
        
    return mealList

def printMealPlan(aMealPlan):
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
        
    return strf

if __name__ == "__main__":
    print(printMealPlan(generateMealPlan()))