import random
from random import randint
from operator import itemgetter
import copy


def initializePopulation(populationSize): 
  population = []
  for chromosome_it in range(populationSize):
    chromosome = []
    for gene in range(15):
      gene = random.choice(['C','D'])
      chromosome.append(gene)
      ##print('random number: ', gene)
    
    population.append(chromosome)
     
  return population


def playCompetition(population):
  for chromosomeIterator in range(len(population)):
    score = 0
    chromosome = population[chromosomeIterator]
    #print(chromosome[chromosomeIterator] + 'chromosoom in competitie')
    
    for contestorIndex in range(len(population)):
      contestor = population[contestorIndex]
      if(chromosome!=contestor):
        score += playOneGame(chromosome, contestor)
    
    chromosome.append(score)  

  #printPopulation(population)
  return

def printPopulation(population):
    for chromosome in population:
      print(chromosome)


def playOneGame(chromosome, contestor):
  
  totalScore = 0
  historyForChromosome = [None, None, None]
  historyForContestor = [None, None, None]
  for iterations in range(100):
    result = playIteration(chromosome, contestor, historyForChromosome, historyForContestor)
    totalScore += result["score"]
    historyForChromosome = updateHistory(historyForChromosome, result["moveChromosome"])
    historyForContestor = updateHistory(historyForContestor, result["moveContestor"])
  return totalScore

def playIteration(chromosome, contestor, historyForChromosome, historyForContestor):
  
  result = {}  #dictionary
  moveChromosome = findMoveChromosome(chromosome, contestor, historyForChromosome, historyForContestor)
  moveContestor = findMoveChromosome(contestor, chromosome, 
    historyForContestor, historyForChromosome)
  
  score = calculateScore(moveChromosome, moveContestor)
  #print('history contestor: ', historyForContestor)
  #print(moveChromosome, ': moveChromosome; ', moveContestor, ' : move contestor; ', score, ' : score' )

  result["score"] = score
  result["moveChromosome"] = moveChromosome
  result["moveContestor"] = moveContestor
  return result

def findMoveChromosome(chromosome1, chromosome2, history1, history2):
  historyOfOpponentAsNumber = convertHistoryToNumber(history2)
  return chromosome1[int(historyOfOpponentAsNumber)]

def convertHistoryToNumber(history):
  asBinary = 0;
  if(history[0]==None): 
    return asBinary
  if(history[1] == None):
    asBinaryList = [h.replace('C', '1') for h in history[:1]]
    asBinaryList = [h.replace('D', '0') for h in asBinaryList]
    asBinary = ''.join(asBinaryList)
    return 1 + int(asBinary, 2)
  if(history[2] == None):
    asBinaryList = [h.replace('C', '1') for h in history[:2]]
    asBinaryList = [h.replace('D', '0') for h in asBinaryList]
    asBinary = ''.join(asBinaryList)
    return 3 + int(asBinary, 2)

  
  asBinaryList = [h.replace('C', '1') for h in history[:3]]
  asBinaryList = [h.replace('D', '0') for h in asBinaryList]

  asBinary = ''.join(asBinaryList)

  return 7 + int(asBinary, 2)


def calculateScore(firstMove, secondMove):
  if(firstMove == 'C' and secondMove== 'C'):
    return 3
  if(firstMove == 'C' and secondMove== 'D'):
    return 0;
  if(firstMove=='D' and secondMove =='D'):
    return 1;
  if(firstMove == 'D' and secondMove == 'C'):
    return 5;
  return -10000; #error value

    
def updateHistory(history, move):
  history.insert(0, move)
  history.pop()
  return history
  

def generateNewPopulation(population):
  newPopulation = []
  for chromosome in population:
    chromosome.pop()
    newPopulation.append(chromosome)
    
    newChromosome = mutate(chromosome)
    newPopulation.append(newChromosome)
  
  for index in range(len(population)):
    firstChromosomeForCrossover = population[randomPopulationIndex(len(population))]
    secondChromosomeForCrossover = population[randomPopulationIndex(len(population))]
    newPopulation = newPopulation + crossover(firstChromosomeForCrossover, secondChromosomeForCrossover)
  return newPopulation  



def randomPopulationIndex(size):
  return randint(0, (size - 1))

def randomChangeIndex():
  return randint(0, 14)

def crossover(firstChromosome, secondChromosome):
  newChromosomes = []
  crossoverIndex = randomChangeIndex()
  newChromosomes.append(firstChromosome[0:crossoverIndex] + secondChromosome[crossoverIndex:len(secondChromosome)])
  newChromosomes.append(secondChromosome[0:crossoverIndex] + firstChromosome[crossoverIndex:len(firstChromosome)])
  return newChromosomes


def mutate(chromosome):
  mutationIndex = randomChangeIndex()
  newChromosome = copy.deepcopy(chromosome)
  oldValue = newChromosome[mutationIndex]
  newValue = 'D' if oldValue == 'C' else 'C'
  newChromosome[mutationIndex] = newValue
  return newChromosome

def testConvertToHistoryNumber():
  print(convertHistoryToNumber([None,None,None]))
  print(convertHistoryToNumber(['D',None,None]))
  print(convertHistoryToNumber(['C',None,None]))
  print(convertHistoryToNumber(['D','D',None]))
  print(convertHistoryToNumber(['D','C',None]))
  print(convertHistoryToNumber(['C','D',None]))
  print(convertHistoryToNumber(['C','C',None]))

  print(convertHistoryToNumber(['D','D','D']))
  print(convertHistoryToNumber(['D','D','C']))
  print(convertHistoryToNumber(['D','C','D']))
  print(convertHistoryToNumber(['D','C','C']))
  print(convertHistoryToNumber(['C','D','D']))
  print(convertHistoryToNumber(['C','D','C']))
  print(convertHistoryToNumber(['C','C','D']))
  print(convertHistoryToNumber(['C','C','C']))


#testConvertToHistoryNumber()
populationSize = 40

population = initializePopulation(populationSize)

for round in range(100):
  playCompetition(population)
  population = sorted(population, key=itemgetter(15), reverse=True)
  print( "sorted population: ")
  printPopulation(population)

  best10FromPopulation = population[:10]
  population = generateNewPopulation(best10FromPopulation)
  print( "new population: ")
  printPopulation(population)