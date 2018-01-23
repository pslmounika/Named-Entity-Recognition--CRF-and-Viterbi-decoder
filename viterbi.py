import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    #f = open('viterbi', 'w')
    #N is number of tags and L is number of words
    #print "Inside run_viterbi"
    #print "Emission "+str(emission_scores)
    #print"++++"+str(isinstance(emission_scores,np.ndarray))
    #print "Trans "+str(trans_scores)
    #print "Start "+str(start_scores)
    #print "End "+str(end_scores)
    #f.write("Emission Scores: \n"+str(emission_scores))
    #f.write("Transmission Scores: \n"+str(trans_scores))
    #f.write("Start scores: \n"+str(start_scores))
    #f.write("End scores: \n"+str(end_scores))
    """
    #Transmission prob is P(currentTag/PreviousTag)
    #Emission prob is P(currentWord/currentTag)
    

    N -->1
    L -->3
    Emission
    scores: [[-1.47603     0.60637284 - 0.26644169]]
    Transition
    scores: [[0.35167817 - 0.02388301  0.62558492]
             [-0.79025456 - 2.02647697 - 1.15672987]
             [0.12295652  0.07504267  0.3840484]]
    Start
    scores: [0.61050623  1.42860572  1.53900073]
    End
    scores: [0.02159275 - 0.63842309 - 0.03265809]"""


    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]
    #print "Emission probability: "+emission_scores
    score=0
    y = []
    for i in xrange(N):
        # stupid sequence
        y.append(i % L)
    # score set to 0
    LastColScore=[]
    #N is number of tags and L is number of words
    scoreMatrix=np.zeros((L,N+1),dtype=object);
    #scoreMatrix=[]
    #print "Score Matrix"
    #print scoreMatrix
    backpointers=[]


    #N=3
    #L=4
    #print emission_scores[0,1]
    PwordTag =0
    cellMax=[]
    cellMaxTuple=[]
    ColumnMax=[]
    ColumnMaxTuple=[]
    result=[]
    resultTuple=[]
    #print start_scores[0]
    col=N
    for i in xrange(col+1):
        #print i
        #xprint "Emission : "+str(emission_scores[0])
        ColumnMaxTuple=[]
        if(i==0):
            for j in range(0,L):
                #print "j: "+str(j)
                if(i==0 and j<L):
                    #i=0
                    #print start_scores[j]
                    #print "++++"+str(emission_scores[i,j])
                    val=start_scores[j]+emission_scores[i,j]
                    scoreMatrix[j,i]=(val, j)
                    ColumnMaxTuple.append((scoreMatrix[j,i],j))

            #print "Score matrix: \n"+str(scoreMatrix)
            #print "ColumnMatrix: "+str(ColumnMaxTuple)
            ColumnMaxTuple.sort(key=lambda tup: tup[0], reverse=True)
            #resultTuple.append(ColumnMaxTuple[0])
            #print "resultTuple: "+str(resultTuple)
        elif(i==N):
            #print"Score matrix until now: \n"+str(scoreMatrix)
            #print "col: "+str(col)
            #print "i: "+str(i)
            #print "end score: "+str(end_scores)
            #PwordTag = end_scores[N-1, 0]
            #print"Last PwordTag: "+str(PwordTag)
            for j in range(0,L):
                if (j < L):
                    val = end_scores[j] + scoreMatrix[j, i-1][0]
                    scoreMatrix[j, i] =(val,j)
                    #print"scoree-->"+str(scoreMatrix[j,i])
                    ColumnMaxTuple.append(scoreMatrix[j, i])
            #print "ColumnMatrix: " + str(ColumnMaxTuple)
            ColumnMaxTuple.sort(key=lambda tup: tup[0], reverse=True)
            resultTuple.append(ColumnMaxTuple[0])
            #print "resultTuple: " + str(resultTuple)


        else:

            for j in range(0,L):
                #print"***************"+str(j)
                PwordTag=emission_scores[i,j]
                #print"PwordTag: "+str(PwordTag)
                cellMax=[]

                for k in range(0,L):
                    #print "transscore: "+str(trans_scores[k,j])
                    #print "scoreMatrix[i-1,j]: "+str(scoreMatrix[k,i-1])
                    #print "scoreMatrix[i-1,j]: ----->" + str(scoreMatrix[k, i - 1][0])
                    #smVal=scoreMatrix[k, i - 1][0]

                    val=scoreMatrix[k,i-1][0]+PwordTag+trans_scores[k,j]
                    #print "val: "+str(val)
                    cellMax.append((val,k))
                #print "cellMax: "+str(cellMax)
                cellMax.sort(key=lambda tup: tup[0], reverse=True)
                #print "cellMax Sorted:   "+"i: "+str(i)+"j: "+str(j)+"\n"+str(cellMax)
                #print "^^^^^^"+str(cellMax[0])
                ColumnMaxTuple.append(cellMax[0])
                #print "after appending to column max tuple "+str(ColumnMaxTuple)
                scoreMatrix[j,i]=cellMax[0]
            #print "Score Matrix: "+"i: "+str(i)+"j: "+str(j)+"\n"+str(scoreMatrix)
            #print "cellMax: "+str(cellMax)
            #print "Column Max: "+str(ColumnMaxTuple)
            #ColumnMaxTuple.sort(key=lambda tup: tup[0], reverse=True)
            #print "Column Max after sorted: "+str(ColumnMaxTuple)
            #print "ColumnMaxTuple[0]: "+str(ColumnMaxTuple[0])
            #resultTuple.append(ColumnMaxTuple[0])
            #print "resultTuple:"+str(resultTuple)

    #print "SCORE MATRIX"
    #print scoreMatrix
    #print "result max tuple: "+str(resultTuple)
    #print "Initial J:"+str(resultTuple[0][1])
    bp=resultTuple[0][1]
    for i in range(N,-1,-1):
        #print "i: "+str(i)
        #print "bp: "+str(bp)
        val=scoreMatrix[bp,i]
        #print "val " + str(val)
        if(i!=N-1):
            backpointers.insert(0,bp)
        bp=val[1]

    #print "Backpointers: "+str(backpointers)



    result=[x[1] for x in resultTuple]
    y=backpointers
    #print "result "+str(result)
    #print "y-->"+str(y)
    score=resultTuple[0][0]
    #f.write(scoreMatrix)
    #f.close()

    return (score, y)

