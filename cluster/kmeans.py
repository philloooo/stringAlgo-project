###############################################################################
####### This is a Semi-supervised K-Means clustering for learning the #########
####### labels for different word associations. The cluster centers   #########
####### are first defined using the seed sequences and then they are  #########
####### iteratively improved. Every time a used selects an associa-   #########
####### -tion the weight for that association is changed and it is    #########
####### re-classified.                                                #########
###############################################################################
import nltk
import sys
import numpy

#Function to define the cluster
def weightRel(allRelations):
    seeds = list()
    assocId = 0
    for relation in allRelations:
        assert(len(relation) == 6)
        label = relation[4]
        score = relation[5]
        if(label == 1):
            coordinates = numpy.array([score, 0])
        if(label == 2 or label == 0):
            coordinates = numpy.array([0,0])
        if(label == -1):
            coordinates = numpy.array([score, 0])
        seeds.append((coordinates, assocId, label))
        assocId += 1
    return seeds

#Function to calcualte the initial mean
def addToMeansList(to, source):
    assert(len(to) == len(source))
    for i in xrange(len(to)):
        to[i] += source[i]
    return to

#Get the initial means using the seed sequences
def initMeans(seeds, numClusters = 3):
    assert(numClusters == 3) #Num of clusters are always three.
    #Seeds are the associations which are pre-classified by the program.
    #Data structure: [(numpy.array([x,y]), assocId, label)]
    means = [numpy.array([0,0]) for i in xrange(numClusters)]
    count = [0]*numClusters
    assoc = list()
    if(seeds == list()): #No seeds available
        return means 
    for (coordinates, assocId, label) in seeds:
        try:
            assoc.append(coordinates)
            if(label == 1): #Positive
                count[0] += 1
                means[0] = addToMeansList(means[0], coordinates)
            elif(label == -1): #Negative
                count[1] += 1
                means[1] = addToMeansList(means[1], coordinates)
            elif(label == 0 or label == 2): #Neutral
                count[2] += 1
                means[2] = addToMeansList(means[2], coordinates)
            else:
                sys.exit("Invalid value for label")
        except TypeError:
            print"Label must be a integer value"
    for i in xrange(len(means)):
        if(count[i] > 0):
            means[i] = means[i]/float(count[i]) 
    return (means, assoc)

#Get the final clusterer object
def getClusterer(numClusters, seeds, distance, initial_means, repeats = 10):
    try:
        if(seeds == numpy.array([])):
            sys.exit("Cannot initiate clusters using empty array")
        else:
            clusterer = nltk.cluster.kmeans.KMeansClusterer(numClusters, 
                        distance, repeats, initial_means, avoid_empty_clusters = True)
            clusters = clusterer.cluster(seeds, True, trace=True)
            return clusterer
    except TypeError:
        print "Input must be in the numpy array format"
    except ValueError:
        print "Data is of the correct type but wrong value"

#Classify a new association 
def classifyAssociation(clusterer, association):
    return clusterer.classify(association)

def clusterResults(allRelations):
    seeds = weightRel(allRelations)
    assert(len(seeds) == len(allRelations))
    means, assoc = initMeans(seeds)
    clus = getClusterer(3, assoc, nltk.cluster.euclidean_distance, means)
    for i in xrange(len(seeds)):
        (coordinates, assocId, label) = seeds[i]
        (ID, sentence, gene1, gene2, label, score) = allRelations[i]
        label = classifyAssociation(clus, coordinates)
        if(label == 0):
            label = 1
        if(label == 1):
            label = -1
        else:
            label = 0
        seeds[i] = (coordinates, assocId, label)
        allRelations[i] = (ID, sentence, gene1, gene2, label, score)
    return allRelations


###############################################################################
################################# TEST CODE ###################################

vectors = [[1, "hello", "Lep", "Ins", 1, 100], [2, "HelloAgain", "Lep", "Ins", 0, 0],[3, "HI", "Lep", "TNF", -1, -100],[4, "Hola", "Ins", "TNF", 2, 0],]
print clusterResults(vectors)
#vectors = [(numpy.array([2,1]), 1, 1), (numpy.array([3,1]), 2, 1), (numpy.array([4,7]), 3,0), (numpy.array([6,7]),4,-1)]
#means, assoc = initMeans(vectors, 3)
#print assoc
#vectors = [numpy.array(f) for f in [[2, 1], [1, 3], [4, 7], [6, 7]]]
#print vectors
#means = [[4, 3], [5, 5]]
#clus = getClusterer(3, assoc, nltk.cluster.euclidean_distance, means)
#vector = numpy.array([3,3])
#print classifyAssociation(clus, vector)
