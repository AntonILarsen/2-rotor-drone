import pickle 

def storeData(data): 
    # initializing data to be stored in db 
    employee1 = {'key' : 'Engineer', 'name' : 'Harrison', 
    'age' : 21, 'IMU' : data} 
    employee2 = {'key' : 'LeadDeveloper', 'name' : 'Jack', 
    'age' : 50, 'pay' : 50000} 

    # database 
    db = {} 
    db['employee1'] = employee1 
    db['employee2'] = employee2 

    # Its important to use binary mode 
    dbfile = open('examplePickle', 'wb') 

    # source, destination 
    pickle.dump(db, dbfile)                   
    dbfile.close() 

def loadData(): 
    # for reading also binary mode is important 
    dbfile = open('examplePickle', 'rb')      
    db = pickle.load(dbfile) 
    for keys in db: 
        print(keys, '=>', db[keys]) 
    dbfile.close() 
