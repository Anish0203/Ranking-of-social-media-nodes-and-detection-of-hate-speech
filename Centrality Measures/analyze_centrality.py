import snap
import os
curdir=os.getcwd()
newdir=os.path.join(curdir,"centralities")
ccd=os.path.join(newdir,"closeness.txt")
bcd=os.path.join(newdir,"betweenness.txt")
prd=os.path.join(newdir,"pagerank.txt")
fcc=open(ccd,"r")
fbc=open(bcd,"r")
fpr=open(prd,"r")
G = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
n=G.GetNodes()
OCC=snap.TIntH()                #Hashmap stores the count of node occuring in top 100
OBC=snap.TIntH()                #If count=2, it means it is present in both our algorithm by task 1 and task 2
OPR=snap.TIntH()                #Else no overlapping takes place
#######  Closeness Centrality  #######
CC=snap.TIntFltH()
for node in G.Nodes():
    CC[node.GetId()]=snap.GetClosenessCentr(G, node.GetId())
    OCC[node.GetId()]=0
    OBC[node.GetId()]=0
    OPR[node.GetId()]=0
CC.SortByDat(False)
i=0
for key in CC:
    i=i+1
    OCC[key]+=1                 #Increases count for nodes in top 100 produced by inbuilt snap function
    if(i==100):                 #If top 100 are visited, then break
        break
i=0
for line in fcc:
    i+=1
    tokens=line.split(' ')
    OCC[int(tokens[0])]+=1        #Reading from already generated file and takes only the node id and increases count
    if(i==100):
        break
#######  Betweenness Centrality  #######
BC = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(G, BC, Edges, 0.8)
BC.SortByDat(False)
i=0
for key in BC:
    i+=1
    OBC[key]+=1                        #Same as Closeness Centrality
    if(i==100):
        break
i=0
for line in fbc:
    i+=1
    tokens=line.split(' ')
    OBC[int(tokens[0])]+=1
    if(i==100):
        break

#######  PageRank  #######
PR = snap.TIntFltH()
snap.GetPageRank(G, PR,0.8)
PR.SortByDat(False)
i=0
for key in PR:                     #Same as Closeness Centrality
    i+=1
    OPR[key]+=1
    if(i==100):
        break
i=0
for line in fpr:
    i+=1
    tokens=line.split(' ')
    OPR[int(tokens[0])]+=1
    if(i==100):
        break

anscc=0                    #To store the no of overlaps
ansbc=0
anspr=0
for key in OCC:
    if(OCC[key]==2):         #If count=2, then it is present in both algorithms in task 1 and task 2
        anscc+=1
for key in OBC:
    if(OBC[key]==2):
        ansbc+=1
for key in OPR:
    if(OPR[key]==2):
        anspr+=1

print("#overlaps for Closeness Centrality:",anscc)
print("#overlaps for Betweenness Centrality:",ansbc)
print("#overlaps for PageRank Centrality:",anspr)
