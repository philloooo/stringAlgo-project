def readf(filename):
    #returns a list of the words in our word files (in which the words are separated by a newline)
    file = open(filename,"r")

    # a = file.read()
    result=[]
    for line in file :
        result.append(line.replace('\r','').replace('\n',''))
    # a = a.split("\n")
    file.close()
    return result

def OutputRelations(abstractFileName,seta,negSet,neutralSet,negationSet,posSet,fullNames,threshold):
    #added threshold in input format
    #recent change: no longer using filename for abstract. instead, input the string of the abstract
                                                
                                                
                                                
    import nltk
    import copy
    import re
    from nltk.stem.lancaster import LancasterStemmer
    from nltk.stem import RegexpStemmer
    
    sentencedb = dict()
    fullnamestore = dict()
    a = readf(fullNames)
    for i in a:
        i = i.split(";")
        if len(i)>1:
            #storing the full names, using the short symbols as dict keys
            fullnamestore[i[0]] = i[1]
        else:
            fullnamestore[i[0]] = "none"
    #sentencedb indexes the sentences by a unique identifier (int)
    
    def isGene(x,t,sentence):
        
    
        #checks if gene 'x' in a list of tokens 't' is really a gene or a variable with the same name 
        if len(t)>1 and len(x)>2:
            
            if t.index(x) ==0:
                if t[t.index(x)+1] in [">","<","=","score"]:
                    return False
            elif t.index(x) ==len(t)-1:
                if t[t.index(x)-1] in [">","<","=","score"]:
                    return False
            elif(t[t.index(x)+1] in [">","<","=","score"])or (
                t[t.index(x)-1] in [">","<","=","score"]):
                return False
            elif (t[t.index(x)+1],t[t.index(x)-1])==(")","("):
                if x in fullnamestore:
                    if fullnamestore[x]!="none":
                        fullLength = len(d[x])
                        #full length is length of full name
                        if t.index(x)>len(d[x])+2:
                            if sentence[(t.index(x)-1-fullLength):(t.index(x)-1)]==d[x]:
                                return True
                            else:
                                return False
                        
            else:
                return True
            return True
        else:
            return False

    def countgenes(s,geneset):
        #counts the number of unique genes in a sentence  "s"
        ss=nltk.word_tokenize(s)
        numgenes=0
        existingGenes = []
        for i in s:
            if i in geneset and isGene(i,ss,s) and i not in existingGenes:
                numgenes+=1
                existingGenes.append(i)  
                
        
        return numgenes

    def countWords(gene1,gene2,token):
        
        #counts the words between gene 1 and gene2
        count = 0
        for i in xrange(token.index(gene1)+1,token.index(gene2) -1):
            count+=1
        return count
            
            

    
    #abstracts = open(abstractFileName,"r")
    
   
    storage = dict()
    
    
    

        
    b = []
#a=a.replace("\n"," ")
#for i in a.split("\n\n"):
 #   i=i.replace("\n"," ")
  #  b.append(i)
#print b[4]
#print b[-1].split()[3]
    for x in abstractFileName.split("\n\n"):
        x=x.replace("\n"," ")
        b.append(x)
        #print x
        #x =x.split("\t")
        #print x
    parsedB=[]
    for line in b:
        if len(line)>0:
            parsedB.append(line)
    b=parsedB
    # print b
    sentencelist =re.split("\. (?=[A-Z])",b[-2])
    sentencelistcopy=copy.deepcopy(sentencelist)
    l = len(sentencelist)
    for i in xrange(l):
        
        if countgenes(sentencelistcopy[i],seta)<2:
            sentencelist.remove(sentencelistcopy[i])
        # print b[-1]
        storage[b[-1].split()[1]] = sentencelist
        
    
    #abstracts.close()
    #print sentencelistcopy,sentencelist,storage
        


    
    num_genes=0
    bw=0
    gene_names = seta
    
    
 

    
    
    st = RegexpStemmer('ing$|s$|e$|ed$|es$', min=4)
    def findsuf(string,x):
        a = ""
        for i in xrange(x):
            a+=string[len(string)-1-(x-i-1)]
            
        return a
    finalOutput=[]

            
        
    for id in storage:
        countsentences=0
        for sentence in storage[id]:
            
            rlist = [0,0,0]
            #sentence = storage[id]
            
            tokens = nltk.word_tokenize(sentence)
            tokenscopy = copy.deepcopy(tokens)
            tagged = nltk.pos_tag(tokens)
            

            for x in tagged:
                
                if x[1] in ['VBP','VBN','VBZ','VBG','VB'] : 
                    tokenscopy[tagged.index(x)] = st.stem(x[0])
            store=0
            genes = []
            #print tokens,tokenscopy
            relation = 2
            currentlist = []
            direction = 0
            for x in tokens:
                
                if x in gene_names and x not in currentlist and isGene(x,tokens,sentence):
                    genes.append(x)
                    num_genes+=1
                    currentlist.append(x)
                    #store = tokens.index(x)
            
            in1 = tokens.index(genes[0])
            in2 = tokens.index(genes[1])
            indexx=0
            neg=1
            if countWords(genes[0],genes[1],tokenscopy)<=threshold:
                
                
                    
                    
                for i in xrange(in1 +1,in2):
                    
                    
                    if tokenscopy[i] in posSet:
                        relation = 1
                        
                        
                        
                    elif tokenscopy[i] in negSet:
                        relation = -1
                    #elif tokenscopy[i] in neutralSet:
                        #relation = 0
                    
                    if (tokenscopy[i] in negSet or tokenscopy[i] in
                        posSet):
                        for y in xrange(in1+1,tokenscopy.index(tokenscopy[i])):
                            if tokenscopy[y]=="not":
                                relation =0
                                #2 means neutral
                        if  findsuf(tokens[i],2)=="ed":
                            direction =1
                            
                        else:
                            direction =0
                        
                        
                if direction ==0:
                    rlist = [genes[0],genes[1],relation]
                    #print genes[0],relation,genes[1]
                elif direction == 1 :
                    rlist = [genes[1],genes[0],relation]
                    #print genes[1], relation, genes[0]
                # if relation!="none":
                if True:
                    #the above condition is so that it does not output sentences for which no relation
                    #has been found. This makes analysis easier. Must change this during final program.
                    sentencedb[countsentences]=sentence
                    #use this to have the sentences represented by a number
                    #change id to pmid
                    finalOutput.append([id,sentence,rlist[0],rlist[1],rlist[2]])
                    #use this to have the actual sentences in the output
                    #finalOutput.append([id,countsentences,rlist])
                    
                    countsentences+=1
          
             
    return finalOutput

#use below info to run
#abstractFileName="C:/Python27/abstractsNew.txt"
##abstractFileName = """1. Genome Res. 2007 Mar;17(3):311-9. Epub 2007 Feb 6.
##
##Sequencing and analysis of chromosome 1 of Eimeria tenella reveals a unique
##segmental organization.
##
##Ling KH, Rajandream MA, Rivailler P, Ivens A, Yap SJ, Madeira AM, Mungall K,
##Billington K, Yee WY, Bankier AT, Carroll F, Durham AM, Peters N, Loo SS, Isa MN,
##Novaes J, Quail M, Rosli R, Nor Shamsudin M, Sobreira TJ, Tivey AR, Wai SF, White
##S, Wu X, Kerhornou A, Blake D, Mohamed R, Shirley M, Gruber A, Berriman M, Tomley
##F, Dear PH, Wan KL.
##
##Malaysia Genome Institute, UKM-MTDC Smart Technology Centre, Universiti
##Kebangsaan Malaysia, 43600 UKM Bangi, Selangor DE, Malaysia.
##
##Eimeria tenella is an intracellular protozoan parasite that infects the
##intestinal tracts of domestic fowl and causes coccidiosis, a serious and
##sometimes lethal enteritis. Eimeria falls in the same phylum (Apicomplexa) as
##several human and animal parasites such as Cryptosporidium, Toxoplasma, and the
##malaria parasite, Plasmodium. Here we report the sequencing and analysis of the
##first chromosome of E. tenella, a chromosome believed to carry loci associated
##with drug resistance and known to differ between virulent and attenuated strains 
##of the parasite. The chromosome--which appears to be representative of the
##genome--is gene-dense and rich in simple-sequence repeats, many of which appear
##to give rise to repetitive amino acid tracts in the predicted proteins. Most
##striking is the segmentation of the chromosome into repeat-rich regions peppered 
##with transposon-like elements and telomere-like repeats, alternating with
##repeat-free regions. Predicted genes differ in character between the two types of
##segment, and the repeat-rich regions appear to be associated with
##strain-to-strain variation. QRFPR activates QRICH2 because I said so.
##
##PMCID: PMC1800922
##PMID: 17284678  [PubMed - indexed for MEDLINE]"""
##geneFileName="C:/Python27/finalGeneSymbols.txt"
##posFileName="C:/Python27/worddictionaries/posWords.txt"
##negFileName="C:/Python27/worddictionaries/negWords.txt"
##neutralFileName= "C:/Python27/worddictionaries/neutralWords.txt"
##negationsFileName="C:/Python27/worddictionaries/negations.txt"
##print OutputRelations(abstractFileName,geneFileName,posFileName,negFileName,neutralFileName,negationsFileName)
