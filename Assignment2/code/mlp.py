'''
    This pre-code is a nice starting point, but you can
    change it to fit your needs.
'''
import numpy as np

class mlp:
    def __init__(self, inputs, targets, nhidden):
        self.beta = 1
        self.eta = 0.1
        self.momentum = 0.0
        
        self.weight1 = np.random.rand(np.shape(inputs)[1]+1, nhidden)
        self.weight2 = np.random.rand(nhidden+1, np.shape(targets)[1])
        
    # You should add your own methods as well!

    def earlystopping(self, inputs, targets, valid, validtargets):
           
        valid = np.concatenate((valid,-np.ones((np.shape(valid)[0],1))),axis=1)
        
        old_error =100000.0
        new_error = 99999.0
        
        while old_error - new_error >= 0.0:            
            self.train(inputs, targets)
            out = self.forward(valid)
            old_error = new_error            
            new_error = 0.5*np.sum((validtargets-out)**2)

              
    def train(self, inputs, targets, iterations=100):
        
        inputs = np.concatenate((inputs, -np.ones((np.shape(inputs)[0],1))),axis=1)

        for i in range(iterations):
            outputs = self.forward(inputs)
            dfo = self.beta*(outputs-targets)*outputs*(1-outputs)

            dfh = self.beta*(np.dot(self.weight2,np.transpose(dfo)))
            dfh = dfh.transpose()*self.hidden*(1-self.hidden)
            dfh=dfh[:,:-1]
            
            u2 = self.eta*np.dot(np.transpose(self.hidden),dfo)
            u1 = self.eta*np.dot(np.transpose(inputs),dfh)

            self.weight1 -= u1
            self.weight2 -= u2
            

            

    def forward(self, inputs):
        #saving hidden layer values for backpropagation
        self.hidden = np.dot(inputs, self.weight1)
        self.hidden = 1.0/(1.0 + np.exp(-self.hidden*self.beta))
        self.hidden = np.concatenate((self.hidden,-np.ones((np.shape(inputs)[0],1))),axis=1)

        output = np.dot(self.hidden, self.weight2)
        output = 1.0/(1.0 + np.exp(-output*self.beta))

        return output
        
    
    def confusion(self, inputs, targets):
        # Add the inputs that match the bias node
        inputs = np.concatenate((inputs,-np.ones((np.shape(inputs)[0],1))),axis=1)
        outputs = self.forward(inputs)
                
        nclasses = np.shape(targets)[1]

        outputs = np.argmax(outputs,1)
        targets = np.argmax(targets,1)
                    
        confusion_mat = np.zeros((nclasses, nclasses))
        for i,j in zip(outputs, targets):
            confusion_mat[i,j]+=1
           
        return confusion_mat
    
    
    def print_confusion(self, inputs, targets):
        
        confusion_mat = self.confusion(inputs, targets)
        print("Confusion matrix: \n",confusion_mat)
        cp = (np.trace(confusion_mat)/np.sum(confusion_mat)) * 100
        print("Percentage Correct: ", cp)



    def kfold(self, inputs, targets, valid, valid_targets, k=3):
        
        tsize = np.shape(inputs)[0]
        k_size = int(tsize/k)
              
        for i in range(k):        
            a = i*k_size
            b = (i+1)*k_size
                        
            test_data = inputs[a:b]
            test_targets = targets[a:b]         
            train_data = np.concatenate((inputs[0:a], inputs[b:tsize]))
            train_targets = np.concatenate((targets[0:a], targets[b:tsize]))
            
            #self.earlystopping(train_data, train_targets, valid, valid_targets)
            self.train(train_data, train_targets)
            
            conf_mat = self.confusion(test_data, test_targets)
            cp = (np.trace(conf_mat)/np.sum(conf_mat)) * 100
            print("Fold {0} Percentage Correct: {1}".format(i,cp))

  
        
        
        
        
        
        
        
        
        