import numpy as np

#distribute particles via roulette
def rouletteSelect(buckets, numParticles):
	sumBucket = float(sum(buckets))
	relativeBucket = [b/sumBucket for b in buckets]
	
	probs = [sum(relativeBucket[:r+1]) for r in range(len(relativeBucket))] #since index starts from 0 we add 1
	#print(probs)
	# Assign particles
	newBuckets = np.zeros(len(buckets))
	for n in range(numParticles):
		r = np.random.rand() #generate a random number 
		for i, particle in enumerate(newBuckets):
			if r <= probs[i]:
				newBuckets[i] += 1
				break
	return newBuckets
	
population = [0.3, 0.6, 0.1, 0.05, 0.09, 0.0]
numParticles = 100

#for roulette with a set particle count
def throwAttempts(prob, numThrows):
	bullseyes = 0
	for n in range(numThrows):
		r = np.random.rand()
		if (r <= prob):
			bullseyes += 1

	return bullseyes
	
#possible movesets
#assigning equal probability to all possible moves
movesetProb1 = 1.0/8 #in the actual version we can replace with 1.0/len(moveset1)
movesetProb2 = 1.0/7 
possibleMoveSet1 = [['a2', movesetProb1], ['a3', movesetProb1], ['b2', movesetProb1], ['b3', movesetProb1], ['c2', movesetProb1], ['c3', movesetProb1], ['d2', movesetProb1], ['d3', movesetProb1]]
#possibleMoveSet2 = [['1', movesetProb1], ['2', movesetProb1], ['3', movesetProb1], ['4', movesetProb1]]

#box1 entries
box1 = ['a', 'b', 'c', 'd']
box2 = ['1', '2', '3', '4']

boxes = [box1, box2]

#move likeliness (move likelinesses will be the output of the neural network in softmax)
#left to right a, b, c, d
moveLikelinessBox1Round1 = [0.2, 0.05, 0.7, 0.05]
#moveLikelinessBox1Round1 = [0.05, 0.05, 0.85, 0.05]
#left to right 1,2,3,4
#moveLikelinessBox2Round1 = [0.05, 0.85, 0.05, 0.05]
#moveLikelinessBox2Round1 = [0.85, 0.05, 0.05, 0.05]
moveLikelinessBox2Round1 = [0.05, 0.85, 0.05, 0.05]

#List containing the list of all box probabilities	
boxesProbs = [moveLikelinessBox1Round1, moveLikelinessBox2Round1] 	
	
#left to right a, b, c, d
moveLikelinessBox1Round2 = [0.6, 0.25, 0.05, 0.05]
#left to right 1,2,3,4
moveLikelinessBox2Round2 = [0.05, 0.85, 0.05, 0.05]
	
boxesProbs2 = [moveLikelinessBox1Round2, moveLikelinessBox2Round2]
	
def moveProbFromNN(moveset, boxes, boxesProbs):
	outputProb = [] #empty output array
	numBox = len(boxes)
	for move in moveset:
		probOfMove = 1
		for i in range(numBox):
			probOfMove *= boxesProbs[i][boxes[i].index(move[0][i])]
		outputProb += [[move[0], probOfMove]]
	return outputProb
	
def moveProbFromNNv2(moveset, boxes, boxesProbs):
	outputProb = [] #empty output array
	numBox = len(boxes)
	for move in moveset:
		probOfMove = 0
		for i in range(numBox):
			probOfMove += boxesProbs[i][boxes[i].index(move[0][i])]
		outputProb += [[move[0], probOfMove/numBox]]
	return outputProb	

def moveProbFromChessEngine(moveset, numParticles):
	subList = [moveset[i][1] for i in range(len(moveset))] 
	particleDistribution = rouletteSelect(subList, numParticles)
	moveDist = []
	for i in range(len(moveset)):
		moveDist += [[moveset[i][0], int(particleDistribution[i])]]
	return moveDist

def combineNNandChessEngine(movesetNN, movesetChess):
	outputProb = []
	for i in range(len(movesetNN)):
		#print(movesetNN[i][1], movesetChess[i][1])
		particles = throwAttempts(movesetNN[i][1], movesetChess[i][1])
		outputProb += [[movesetNN[i][0], particles]]
	return outputProb

'''	
measureProbs = moveProbFromNN(possibleMoveSet1, boxes, boxesProbs)		
print(measureProbs)
moveDistribution = moveProbFromChessEngine(possibleMoveSet1, 100)
print(moveDistribution)

combinedOut = combineNNandChessEngine(measureProbs, moveDistribution)
print(combinedOut)
'''

def calcBestMove(list):
	bestMove = list[0]
	for move in list:
		if move[1] > bestMove[1]:
			bestMove = move
	return bestMove

def removeBelowThreshold(list, threshold):
	copyList = []
	for item in list:
		if item[1] >= threshold: #same as <= threshold remove item
			copyList += [item]
	return copyList

def scaleToTotal(input, desiredTotal):
	copyList = []
	subList = [i[1] for i in input]
	divider = sum(subList)
	#print(divider)
	multiplier = desiredTotal/divider
	#print(multiplier)
	summer = 0
	for item in input:
		copyList += [[item[0], item[1]*multiplier]]
		summer += item[1]*multiplier	
	#print(summer)
	secondaryList = moveProbFromChessEngine(copyList, desiredTotal - summer)
	#print(secondaryList)
	for i in range(len(copyList)):
		copyList[i][1] += secondaryList[i][1]
	return copyList

def checkSum(list):
	summ = 0
	for item in list:
		summ += item[1]
	return summ
	
def calcSecondMove(movePair):
	movesetProb1 = 1
	eightInitial = [['a2', movesetProb1], ['a3', movesetProb1], ['b2', movesetProb1], ['b3', movesetProb1], ['c2', movesetProb1], ['c3', movesetProb1], ['d2', movesetProb1], ['d3', movesetProb1]]
	possibleMoves = []
	for move in eightInitial:
		if move[0] == movePair[0]:
			passtimb5225
			
		else:
			possibleMoves += [move]
	return possibleMoves

def find3Largest(list):
	first = ['empty', 0]
	second = ['empty', 0]
	third = ['empty', 0]
	for move in list:
		if move[1] >= first[1]:
			first = move
			second = first
			third = second
		elif move[1] >= second[1]:
			second = move
			third = second
		elif move[1] >= third[1]:
			third = move
	return [first, second, third]
	
	
	
def calculateBranches(moveset, boxes, boxesProbs, numParticles, filterThresh = 1):
	#calculate the move probability given the NN character recognition output
	measureProbs = moveProbFromNNv2(moveset, boxes, boxesProbs)
	#print(measureProbs)
	#calculate the particle distribution given the probability for each move (equal at this stage)
	particleDistribution = moveProbFromChessEngine(moveset, numParticles)
	#print(particleDistribution)
	#determine the likeliness of a given move considering both the measuredProb and the move likeliness
	combinedOut = combineNNandChessEngine(measureProbs, particleDistribution)
	#print(combinedOut)
	print(combinedOut)
	
	#threeLargest = find3Largest(combinedOut)
	#print(threeLargest)
	
	
	filteredOutput = removeBelowThreshold(combinedOut, filterThresh)
	
	scaled = scaleToTotal(filteredOutput, numParticles)
	#print(scaled)
	
	#print(checkSum(scaled))
	
	#resample to bring particle count back to numParticles
	#combinedOut = moveProbFromChessEngine(filteredOutput, numParticles)
	#return combinedOut
	return scaled
	
output = calculateBranches(possibleMoveSet1, boxes, boxesProbs, 200, filterThresh = 1)			
print(output)
bestMove = calcBestMove(output)
print(bestMove)

print('second move sets')

secondMoves = []
for move in output:
	#print('move: ', move, calcSecondMove(move))
	branch = calculateBranches(calcSecondMove(move), boxes, boxesProbs2, move[1])
	secondMoves += [branch]
	print(branch)
	print('')

bests = []
for moveset in secondMoves:
	bestMove = calcBestMove(moveset)
	bests += [bestMove]

overalBest = calcBestMove(bests)
print('overalBest is:')
print(overalBest)
	

'''	
class assignParticleToMove(object):
	moves = []
	
	#box1 entries
	def __init__(self, boxes):
		self.boxes = boxes
	
print(rouletteSelect(population, numParticles))
print(throwAttempts(0.3, 100))
'''