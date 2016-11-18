import numpy as np

#distribute particles via roulette
def rouletteSelect(buckets, numParticles):
	sumBucket = float(sum(buckets))
	relativeBucket = [b/sumBucket for b in buckets]
	
	probs = [sum(relativeBucket[:r+1]) for r in range(len(relativeBucket))] #since index starts from 0 we add 1
	# Assign particles
	newBuckets = np.zeros(len(buckets))
	for n in range(numParticles):
		r = np.random.rand() #generate a random number 
		for i, particle in enumerate(newBuckets):
			if r <= probs[i]:
				newBuckets[i] += 1
				break
	return newBuckets
	
population = [0.3, 0.6, 0.1]
numParticles = 100

#for roulette with a set particle count
def throwAttempts(prob, numThrows):
	bullseyes = 0
	for n in range(numThrows):
		r = np.random.rand()
		if (r <= prob):
			bullseyes += 1

	return bullseyes
	
print(rouletteSelect(population, numParticles))
print(throwAttempts(0.3, 100))