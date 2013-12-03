import pydot
import dot_parser
import gradi
import os

#ID, Sentence, gene1, gene2 and relation
def is_valid_file(filename):
    if(os.path.isfile(filename)):
        return True
    return False
#Function to draw a node
def drawNode(geneName, strength, graph):
    lowColour = gradi.HTMLColorToRGB('FFCC00') #Yellow
    highColour = gradi.HTMLColorToRGB('FF0000') #Red
    colour = gradi.RGBToHTMLColor(gradi.RGBinterpolate(lowColour,
                                                       highColour, strength))
    node = pydot.Node("%s" %(geneName), style = "filled",
                      fillcolor = colour, shape = "circle")
    graph.add_node(node)
    return node

#Function to draw an edge
def drawEdge(start, end, startNode, endNode, graph,disease):
    hyperlink = "/static/webserver/diseases/%s/%s-%s.html" %(disease,start, end)
    graph.add_edge(pydot.Edge(startNode, endNode, URL = hyperlink))

def getSum(connections):
    totalSum = 0.0
    for gene in connections:
        totalSum += connections[gene]
    return totalSum

def getTotalConnections(relationships, path):
    totalConnections = dict()
    allRel = set()
    for i in xrange(len(relationships)):
        start = relationships[i][2]
        end = relationships[i][3]
        relFile = "%s-%s.html" %(start, end)
        allRel.add(relFile)
        addToHTML(relationships[i], path)
        if(start not in totalConnections):
            totalConnections[start] = 0
        if(end not in totalConnections):
            totalConnections[end] = 0
        totalConnections[start] += 1
        totalConnections[end] += 1
    allConnections = getSum(totalConnections)
    for gene in totalConnections:
        totalConnections[gene] /= allConnections
    for rel in allRel:
        closeHTML(relFile)
    return totalConnections

def insertStyle(filename):
    style = open("./style1.txt", "r")
    file = open ("%s" %(filename), "a")
    for line in style:
        print line

        file.write("%s\n" %line)
    file.close()
    style.close()
    
def closeHTML(filename):
    file = open(filename, "a")
    file.write("</html>\n</body>\n</table>\n")
    file.close()
    
def startHTML(filename):
    file = open(filename, "a")

    file.write('''<html>\n
        <head>
        <link href="../style1.css" rel="stylesheet" type="text/css">
        </head>
        <table border = 1>
        <tr>
        <th>PubMedID</th>
        <th>Sentence</th>
        <th>First Gene</th>
        <th>Second Gene</th>
        <th>Interaction</th>
        </tr>
        <body>\n''')
    # insertStyle(filename)
    file.close()
    
#Function to add data to the HTML file
def addToHTML(relation,path):
    filename = "%s/%s-%s.html" %(path, relation[2], relation[3])
    count = 0
    if(not(is_valid_file(filename))):
        startHTML(filename)
    file = open(filename, "a")
    if(count %2 == 0):
        file.write("<tr class = \"cellcolor\">\n")
    else:
        file.write("<tr>")
    for i in xrange(len(relation)):
        if(i == 4):
            if(relation[i] == 1):
                value = "Positive"
            elif(relation[i] == -1):
                value = "Negative"
            elif relation[i]==2:
                value='None'
            else:
                value = "Neutral"
        else:
            value = relation[i]
            if type(value)==unicode:
                value=value.encode('UTF-8')
        file.write("<td>%s</td>\n" %(value))
    file.write("</tr>\n")     
    file.close()
            
#Function to create a graph    
def makeGraph(relationships,disease):
    path='./webserver/static/webserver/diseases/'+disease
    if not os.path.isdir(path):
        os.mkdir(path)
    graph = pydot.Dot(graph_type = 'digraph')
    totalConnections = getTotalConnections(relationships, path)
    edges = set()
    for i in xrange(len(relationships)):
        assert(len(relationships[i]) == 5)
        ID = relationships[i][0]
        sentence = relationships[i][1]
        startGene = relationships[i][2]
        endGene = relationships[i][3]
        relation = int(relationships[i][4])
        edge = "%s-%s" %(startGene, endGene)
        startNode = drawNode(startGene, totalConnections[startGene], graph)
        endNode = drawNode(endGene, totalConnections[endGene], graph)
        if(edge not in edges):
            drawEdge(startGene, endGene, startNode, endNode, graph,disease)
            edges.add(edge)
    
    graph.write(path+'/result.svg', format='svg', prog='twopi')

################################################################################
################################### TEST CODE ##################################
# def main():
#     a = list()
#     b = [1, "hello", "Lep", "Ins", 1]
#     c = [2, "newthing", "Lep", "TNF", 1]
#     a.append(b)
#     a.append(c)
#     a.append(c)
#     print a
#     makeGraph(a)

# main()
