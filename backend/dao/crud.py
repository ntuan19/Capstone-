from flask import request, flash 
from app import clientCollection,investmentCollection

class Crud():
    def __init__(self,dic_data) -> None:
        self.dic_data = dic_data
    
    def insert(self):
        #NEEDED pydantic to check data format here
        # pass them through pydantic/make sure the input is the right format
        #check if the information already exists
        check_infor = self.find(self.dic_data)
        if check_infor:
            raise Exception("Already containing this information")
        else:
            clientCollection.insert_one(self.dic_data)    
    def find(self):
        result = clientCollection.find_one(self.dic_data)
        return result 
    
    def update(self,replace_val):
        #pydantic would take care of old values & its updated value
        result = clientCollection.update_one(self.dic_data,{"$set":replace_val})
        return result 
    def read(self):
        query = {}
        result = clientCollection.find_one({query})
        return result
    def insert_investment(self):
        #NEEDED pydantic to check data format here
        # pass them through pydantic/make sure the input is the right format
        #check if the information already exists
        check_infor = self.find_investment()
        if check_infor:
            result = "Already containing this information"
            return False 
        else:
            investmentCollection.insert_one(self.dic_data)   
            return True

    def find_investment(self):
        result = investmentCollection.find_one(self.dic_data)
        if not result:
            return False
        return result 
    
    def query_filter(self,filter):
        result = investmentCollection.find(filter,{'_id': 0})
        return result
        
        

        

        

        
       
      
    


        
         
         
         

    





