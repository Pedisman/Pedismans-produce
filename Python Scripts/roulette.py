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
#left to right 1,2,3,4
moveLikelinessBox2Round1 = [0.05, 0.85, 0.05, 0.05]
	
boxesProbs = [moveLikelinessBox1Round1, moveLikelinessBox2Round1] 	
	
#left to right a, b, c, d
moveLikelinessBox1Round2 = [0.6, 0.25, 0.05, 0.05]
#left to right 1,2,3,4
moveLikelinessBox2Round2 = [0.05, 0.85, 0.05, 0.05]
	
def moveProbFromNN(moveset, boxes, boxesProbs):
	outputProb = [] #empty output array
	numBox = len(boxes)
	for move in moveset:
		probOfMove = 1
		for i in range(numBox):
			probOfMove *= boxesProbs[i][boxes[i].index(move[0][i])]
		outputProb += [[move[0], probOfMove]]
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
		outputProb += [movesetNN[i][0], particles]
	return outputProb
	
measureProbs = moveProbFromNN(possibleMoveSet1, boxes, boxesProbs)		
print(measureProbs)
moveDistribution = moveProbFromChessEngine(possibleMoveSet1, 100)
print(moveDistribution)

combinedOut = combineNNandChessEngine(measureProbs, moveDistribution)
print(combinedOut)

'''	
class assignParticleToMove(object):
	moves = []
	
	#box1 entries
	def __init__(self, boxes):
		self.boxes = boxes
	
print(rouletteSelect(population, numParticles))
print(throwAttempts(0.3, 100))
'''