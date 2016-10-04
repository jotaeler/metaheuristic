class Greedy:


    def __init__(self, costs, matrix, rows,cols):
        self.costs=costs
        self.matrix=matrix
        self.rows=rows
        self.cols=cols

    """
    Returns how many sectors (cities) are covered by one subsector a.k.a. hospital
    """
    def getSubsectorCover(self,subsector,costs):
        pass

    """
    Returns column cost
    """
    def getSubsectorCost(self,subsector,costs):
        pass

    """
    Delete unnecessary subsectors a.k.a. hospitals
    """
    def delete(self,coverage):
        pass

    """
    Returns the next subsector to be taken
    """
    def select(self):
        pass

