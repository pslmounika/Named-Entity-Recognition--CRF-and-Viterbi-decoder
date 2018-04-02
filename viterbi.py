import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
   
    #Transmission prob is P(currentTag/PreviousTag)
    #Emission prob is P(currentWord/currentTag)
    
    """
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
       
        y.append(i % L)
    # score set to 0
    LastColScore=[]
    #N is number of tags and L is number of words
    scoreMatrix=np.zeros((L,N+1),dtype=object);
    #scoreMatrix=[]
    #print "Score Matrix"
    #print scoreMatrix
    backpointers=[]


    
    PwordTag =0
    cellMax=[]
    cellMaxTuple=[]
    ColumnMax=[]
    ColumnMaxTuple=[]
    result=[]
    resultTuple=[]
    col=N
    for i in xrange(col+1):
        ColumnMaxTuple=[]
        if(i==0):
            for j in range(0,L):
                #print "j: "+str(j)
                if(i==0 and j<L):
                  
                    val=start_scores[j]+emission_scores[i,j]
                    scoreMatrix[j,i]=(val, j)
                    ColumnMaxTuple.append((scoreMatrix[j,i],j))


            ColumnMaxTuple.sort(key=lambda tup: tup[0], reverse=True)

        elif(i==N):
            
            for j in range(0,L):
                if (j < L):
                    val = end_scores[j] + scoreMatrix[j, i-1][0]
                    scoreMatrix[j, i] =(val,j)
                    #print"scoree-->"+str(scoreMatrix[j,i])
                    ColumnMaxTuple.append(scoreMatrix[j, i])
            
            ColumnMaxTuple.sort(key=lambda tup: tup[0], reverse=True)
            resultTuple.append(ColumnMaxTuple[0])
            


        else:

            for j in range(0,L):
                
                PwordTag=emission_scores[i,j]
                
                cellMax=[]

                for k in range(0,L):
                    val=scoreMatrix[k,i-1][0]+PwordTag+trans_scores[k,j]
                    
                    cellMax.append((val,k))
                
                cellMax.sort(key=lambda tup: tup[0], reverse=True)
                
                ColumnMaxTuple.append(cellMax[0])
                
                scoreMatrix[j,i]=cellMax[0]
            

    
    bp=resultTuple[0][1]
    for i in range(N,-1,-1):
        
        val=scoreMatrix[bp,i]
        
        if(i!=N-1):
            backpointers.insert(0,bp)
        bp=val[1]

 



    result=[x[1] for x in resultTuple]
    y=backpointers
    #print "result "+str(result)
    #print "y-->"+str(y)
    score=resultTuple[0][0]
    #f.write(scoreMatrix)
    #f.close()

    return (score, y)

