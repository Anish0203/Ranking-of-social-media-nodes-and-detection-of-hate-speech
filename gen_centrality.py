import snap
import os
curdir=os.getcwd()                               #Get current Directory
os.mkdir('centralities')                         #Make folder named "centralities"
newdir=os.path.join(curdir,"centralities")       #New directory inside centralities folder
ccd=os.path.join(newdir,"closeness.txt")
bcd=os.path.join(newdir,"betweenness.txt")
prd=os.path.join(newdir,"pagerank.txt")
G = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
n = G.GetNodes()                                  #Total no of nodes in G
######      Closeness Centrality     ######
def Closeness():
    fcctemp = open(ccd, "w")
    fcctemp.write("")
    fcctemp.close()
    CC = snap.TIntFltH()                      #Stores closeness centrality of each node
    norm1 = n - 1
    for node1 in G.Nodes():
        NIdToDistH = snap.TIntH()                     #Hashmap mapping shortest distances to all other nodes from the source node
        shortestPath = snap.GetShortPath(G, node1.GetId(), NIdToDistH)
        s = 0
        for key in NIdToDistH:
            s+=NIdToDistH[key]                          #Stores sum of distances
        CC[node1.GetId()] = round(norm1 / s, 6)         #Normalizind and rounding upto 6 decimal
    CC.SortByDat(False)                                  #Sorting in descending order
    fcc = open(ccd, "a")
    for k in CC:
        tempstr = str(k) + " " + str(CC[k]) + " \n"
        fcc.write(tempstr)                              #Writing into closeness centrality file
    fcc.close()

#######     Betweenness Centrality    #######
def Betweenness():
    fbctemp = open(bcd, "w")
    fbctemp.write("")
    fbctemp.close()
    norm2 = (n - 1) * (n - 2) * 0.5                      #Normalizing factor
    BC = snap.TIntFltH()                 #Stores betweenness centrality of each node
    Neighbor=snap.TIntIntVH()            #Stores neighbor of each node in vector
    for node in G.Nodes():
        BC[node.GetId()] = 0
        Neighbor.AddDat(node.GetId())         #Adding source node in hashmap
        for ID in node.GetOutEdges():
            Neighbor[node.GetId()].Add(ID)     #Adding neighbors to source node in vector form
    for node1 in G.Nodes():              #Followed Brandes Algorithm for Betweenness Centrality
        stack = snap.TIntV()            #Stores the nodes in the visited format
        sigma = snap.TIntFltH()         #Stores the no of shortest paths to that node
        d = snap.TIntFltH()             #Stores the distance from the source node
        delta = snap.TIntFltH()         #Contribution of the node in calculation of BC of the node
        P = snap.TIntIntVH()            #Stores the parents for each node
        stack.Clr()
        sigma.Clr()
        d.Clr()
        delta.Clr()
        P.Clr()
        for node2 in G.Nodes():          #Assigning intial values to features of each node
            P.AddDat(node2.GetId())
            sigma[node2.GetId()] = 0.0
            d[node2.GetId()] = -1.0
            delta[node2.GetId()] = 0.0
        sigma[node1.GetId()] = 1.0       #Assigning inital value to the source node
        d[node1.GetId()] = 0.0
        queue = snap.TIntV()
        queue.Clr()
        queue.Add(node1.GetId())         #queue to traverse the nodes in the graph
        while (queue.Empty() == False):
            v = queue[0]
            queue.Del(0)
            stack.Add(v)
            for ID in Neighbor[v]:         #Brandes algorithm continues
                if (d[ID] < 0):
                    queue.Add(ID)
                    d[ID] = d[v] + 1.0      #Getting the distance of the node
                if (d[ID] == (d[v] + 1.0)):
                    sigma[ID] += sigma[v]     #No of paths to reach node with node ID as ID
                    P[ID].Add(v)
        while (stack.Empty() == False):
            w = stack.Last()                 #Traversing the stack
            stack.Del(stack.LastValN())
            for v in P[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])     #Contribution
            if (w != node1.GetId()):
                BC[w] += delta[w]              #BC of node w

    for key in BC:
        BC[key] = BC[key] / 2                      #Since each path is traversed twice
        BC[key] = round(BC[key] / norm2, 6)        #Normalizing and rounding upto 6 decimal
    BC.SortByDat(False)                           #Sorting in descending order
    fbc = open(bcd, "a")
    for key in BC:
        tempstr = str(key) + " " + str(BC[key]) + " \n"
        fbc.write(tempstr)                        #Writing into the betweenness centrality file
    fbc.close()



#####   Biased PageRank   #####
def PageRank():
    fprtemp = open(prd, "w")
    fprtemp.write("")
    fprtemp.close()
    d = snap.TIntFltH()                     #Inital d value assigned to each node
    PR = snap.TIntFltH()                    #Stores PageRank of each node
    OutDeg = snap.TIntH()                   #Stores out degree of each node
    num4 = 0
    for node in G.Nodes():
        if (node.GetId() % 4 == 0):         #Count no of nodes divisible by 4
            num4 += 1
        OutDeg[node.GetId()] = node.GetOutDeg()       #Storing out degree for each node
    for node in G.Nodes():
        if (node.GetId() % 4 == 0):
            d[node.GetId()] = 1 / num4             #Biasing by providing d values to nodes divisble by 4
            PR[node.GetId()] = 1 / num4            #Same done with PR
        else:
            d[node.GetId()] = 0               #Other nodes assigned with 0 value
            PR[node.GetId()] = 0              #Same done with PR
    for i in range(100):                     #100 iterations
        normsum=0                            #Normalizing sum
        for node1 in G.Nodes():
            temp = 0
            for ID in node1.GetOutEdges():     #PageRank algorithm where we calculate the contributions of other nodes to source node
                temp += PR[ID] / OutDeg[ID]
            PR[node1.GetId()] = (0.8 * temp) + (0.2 * d[node1.GetId()])  #Damping factor taken as 0.8
            normsum += PR[node1.GetId()]        #Summing PRs of each node
        for key in PR:
            PR[key] = PR[key] / normsum         #Normalizing
    for key in PR:
        PR[key] = round(PR[key], 6)            #Rounding off to 6 decimal
    PR.SortByDat(False)                       #Sorting in descending order
    fpr = open(prd, "a")
    for key in PR:
        tempstr = str(key) + " " + str(PR[key]) + " \n"
        fpr.write(tempstr)                    #Writng in Pagerank file
    fpr.close()

Closeness()     #Function to compute Closeness Centrality
Betweenness()   #Function to compute Betweenness Centrality
PageRank()      #Function to compute PageRank
