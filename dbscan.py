from scipy.spatial import distance


class dbscan(object):
    """ DBScan Clustering Algorithm """
    def __init__(self, min_pts, epsilon):
        self.min_pts = min_pts
        self.epsilon = epsilon
    
    def find_neighbours(self, point, NV):
        """ Returns the list of neighbouring points """
        nbrs = []
        for elem in NV:
            dst = distance.euclidean(point, elem)
            if dst <= self.epsilon and elem != point:
                nbrs.append(elem)
        return nbrs    
    
    def merge(self, nbr, nbr1):
        """ Merging elements of nbr1 list to nbr list """
        for elem in nbr1:
            if elem not in nbr:
                nbr.append(elem)
    
    def expand_cluster(self, pt, nbr, C, NV_list):
        """ Add given point pt to cluster C and all its neighbours - nbr """
        C.append(pt)
        print 'Expanding cluster'
        for point in nbr:
            print '.',
            
            if point in NV_list:
                NV_list.remove(point)
                nbr1 = self.find_neighbours(point, NV_list)
                
                if len(nbr1) >= self.min_pts:
                    self.merge(nbr, nbr1)
            
            for cluster in self.clusters:
                if point in cluster:
                    break
            else: C.append(point)                
        print '\nCurrent NV_list size:', len(NV_list)    
    
    def fit(self, X, y=None):
        """ Use data matrix X to compute model parameters """
        self.x_len = len(X)
        
        self.clusters = []
        NV = X[:] # NV - Not Visited
        NV_list = NV.tolist()
        
        print '\nCurrent NV_list size:', len(NV_list)
        for point in NV_list:
            NV_list.remove(point)
            nbr = self.find_neighbours(point, NV_list)
            
            if len(nbr) < self.min_pts:
                pass # TODO: To mark this point as a noise
            else:
                C = [] # The current cluster
                self.expand_cluster(point, nbr, C, NV_list)
                self.clusters.append(C)
        return self
    
    def predict(self, X):
        """ Using computed model parameters predict cluster for all objects from x """
        res = []
        for point in X.tolist():
            in_cluster = False
            for num, cluster in enumerate(self.clusters):
                if point in cluster:
                    res.append(num)
                    in_cluster = True
            
            if not in_cluster:
                res.append(-1) # Value -1 is a noise
        return res

