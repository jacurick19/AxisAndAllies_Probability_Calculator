import math
attackList = []
defendList = []
manIndex = 0
tankIndex = 1
fighterIndex = 2
bomberIndex = 3
subIndex = 4
transportIndex = 5
battleshipIndex = 6
aircracftCarrierIndex = 7
AAAIndex = 8
attackValues = [1, 3, 3, 4, 2, 0, 4, 1]
defendValues = [2, 2, 4, 1, 2, 1, 4, 3, 1]
isFirstRound = True
MIN_PROB = .00000001

def getInput():
    print("Enter the attacker's information")

    attackList.append(int(input("How many men? ")))
    attackList.append(int(input("How many tanks? ")))
    attackList.append(int(input("How many fighters? ")))
    attackList.append(int(input("How many bombers? ")))
    attackList.append(int(input("How many submarines? ")))
    attackList.append(int(input("How many transports? ")))
    attackList.append(int(input("How many battleships? ")))
    attackList.append(int(input("How many aircraft carriers? ")))

    print("\nEnter the defenders's information")
    defendList.append(int(input("How many men? ")))
    defendList.append(int(input("How many tanks? ")))
    defendList.append(int(input("How many fighters? ")))
    defendList.append(int(input("How many bombers? ")))
    defendList.append(int(input("How many submarines? ")))
    defendList.append(int(input("How many transports? ")))
    defendList.append(int(input("How many battleships? ")))
    defendList.append(int(input("How many aircraft carriers? ")))
    defendList.append(int(input("How may AAA guns? ")))

def isAmphibious(unit_array):
    return sum(unit_array[:2]) > 0 and attackList[4] > 0

#Requires $numberOfHits < sum($unit_array)
#Returns $sumArray, an array of arrays of possible ways to achive $numberOfHits from $unit_array
def getGoodSubSums(unit_array, numberOfHits):
    goodSubSums = []
    retval = []
    for val in range(unit_array[0] + 1):
        if sum(unit_array[1:]) >= (numberOfHits - val) and len(unit_array[1:]) > 0:
            retval = getGoodSubSums(unit_array[1:], numberOfHits - val)
        for ar in retval:
            ar.insert(0, val)
            goodSubSums.append(ar)
            #base case
        if len(unit_array) == 1 and val == numberOfHits:
            goodSubSums.append([val])
    return goodSubSums

#Requires |$unit_array| = |$event|, $event[i] <= $unit_array[i]
#Returns the proability that the units in $unit_array hit the shots coresponding to $event
def probabilityOfEvent(unit_array, event, isAttack):
    prob = 1
    if isAttack:
        for i in range(len(unit_array)):
            if unit_array[i] > 0:
                prob *= math.pow((attackValues[i]/6),(event[i]))*(math.comb(unit_array[i], event[i]))*math.pow(((6 - attackValues[i])/6),(unit_array[i] - event[i]))
    else:
        for i in range(len(unit_array)):
            if unit_array[i] > 0:
                prob *= math.pow((defendValues[i]/6),(event[i]))*(math.comb(unit_array[i], event[i]))*math.pow(((6 - defendValues[i])/6),(unit_array[i] - event[i]))
    return prob

#Requires a valid unit unit_array, not including AAA shots, battle ship barrages, or submarine suprise attacks
#Returns a pair ($probability, $ammount) where $probability is the probability that $ammount is the number of hits scored by the units in $unit_array
def calculate_hit_probabilities(unit_array, isAttack):
    numberOfPossibleHits = sum(unit_array[:9]) + 1
    probabilities = []
    for i in range(numberOfPossibleHits):
        waysToHitIManyShots = getGoodSubSums(unit_array, i)
        prob = 0
        for event in waysToHitIManyShots:
            prob += probabilityOfEvent(unit_array, event, isAttack)
        probabilities.insert(0, [prob, i])
    return probabilities

def reapCasualities(oldAr, hitCount):
    newAr = []
    for x in oldAr:
        if hitCount - x >= 0:
            newAr.append(0)
            hitCount -= x
        else:
            newAr.append(x - hitCount)
            hitCount = 0
    return newAr
WinProbability = [0]
Uncert = [0]

def updateWinProb(newNum):
    WinProbability[0] += newNum

#Requires a valid unit unit_array
#Returns a list of lists [$array, $probability] where $probability is the probability that $array is the result of combat
#Ensures that every possible result of combat is one of $array, unless the probability of that branch of the chain is less than MIN_PROB
isFirstRound = True
def simulateRound(currentAttack, currentDefense, currentProb=1):
    #    if isFirstRoundand and defendList[AAAIndex] > 0 and (attackList[fighterIndex] > 0 or attackList[bomberIndex] > 0):
            #shoot AAA
        #TODO: submaries first shot, bombardment, AAA
    #    if isFirstRound and attackList[subIndex] > 0:
            #Subs attack
    #    if isFirstRound and isAmphibious(unit_array):
            #bombardment
        attackHits = calculate_hit_probabilities(currentAttack, True)
        defenseHits = calculate_hit_probabilities(currentDefense, False)
        for i in range(len(attackHits)):
            if attackHits[i][1] >= sum(currentDefense[:9]):
                updateWinProb(currentProb*attackHits[i][0])
                continue
            else:
                for j in range(len(defenseHits)):
                    if defenseHits[j][1] >= sum(currentAttack[:9]):
                        j = len(defenseHits)
                        continue
                    #this is suspicous, since we're factoring in the attack prob in the prob the defense wins
                    else:
                        newProb = currentProb*defenseHits[j][0]*attackHits[i][0]
                        if newProb < MIN_PROB:
                            Uncert[0] += MIN_PROB
                            return "I"
                        newAttack = reapCasualities(currentAttack, defenseHits[j][1])
                        newDefense = reapCasualities(currentDefense, attackHits[i][1])
                        simulateRound(newAttack, newDefense, newProb)


getInput()
simulateRound(attackList, defendList)
print("Win probability: "+ str(round(WinProbability[0]*100,4)) + "%")
print("Uncertainty: " + str(round(Uncert[0]*100,4)) + "%")
