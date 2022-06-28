class Dataset:
    def __init__(self):
        self.dataset = None
    
    def prepare(self):
        pass
    
    def filterByEntity(self, iso_code):
        return self.dataset.loc[self.dataset['iso_code'] == iso_code].drop(['entity', 'iso_code'], axis='columns')
        
    def getEntityList(self):
        return list(zip(self.dataset["entity"].unique(), self.dataset["iso_code"].unique()))