import numpy as np
from sklearn.preprocessing import normalize


class Network:

    def __init__(self, topology, mutations=None, copy=None):
        
        self.topology = topology
        
          

        if copy:
            print("Copying...")
            print("Hidden layer size: {}".format(copy.network.hidden_layer_size))
            self.W1 = copy.network.W1
            self.W2 = copy.network.W2
            self.b1 = copy.network.b1
            self.b2 = copy.network.b2
            self.hidden_layer_size = copy.network.hidden_layer_size

        elif mutations:
            self.W1 = mutations[0]
            self.W2 = mutations[1]
            self.b1 = mutations[2]
            self.b2 = mutations[3]
            self.hidden_layer_size = mutations[-1]

        else:
            self.in_layer_size = topology[0]
            self.hidden_layer_size = topology[1]
            self.out_layer_size = topology[2] 
            
            self.W1 = np.random.randn(self.hidden_layer_size, self.in_layer_size) * 50
            self.W2 = np.random.randn(self.out_layer_size, self.hidden_layer_size) * 50
            self.b1 = 1
            self.b2 = 1
            

        self.output = True


    # def feed_forward(self, X):

    #     # Normalize Input
    #     norm1 = X / np.linalg.norm(X)
    #     X_norm = normalize(X[:,np.newaxis], axis=0).ravel()
        
    #     # Feed forward
    #     Z1 = np.dot(self.W1, X_norm)
    #     Z1 = self.softmax(Z1)
    #     Z2 = np.dot(self.W2, Z1)
    #     print("Z2: {}".format(Z2))
    #     if Z2 <= 0:
    #         Z2 = 0
    #     else:
    #         Z2 = 1

    #     self.output = Z2


    # def feed_forward(self, X):

        
        
    #     # Feed forward
    #     Z1 = np.dot(self.W1, X)
        
    #     Z1 = self.sigmoid(Z1)
    #     #Z1 = self.softmax(Z1)
    #     Z2 = np.dot(self.W2, Z1)
        
    #     if Z2 <= 0:
    #         Z2 = 0
    #     else:
    #         Z2 = 1

    #     self.output = Z2


    def feed_forward(self, X):

        # Normalize Input
        norm1 = X / np.linalg.norm(X)
        X_norm = normalize(X[:,np.newaxis], axis=0).ravel()
        
        # Feed forward
        Z1 = np.dot(self.W1, X_norm)
        
        Z1 = self.sigmoid(Z1)
        #Z1 = self.softmax(Z1)
        Z2 = np.dot(self.W2, Z1)
        
        if Z2 <= 0:
            Z2 = 0
        else:
            Z2 = 1

        self.output = Z2


    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))


    def softmax(self, Z):
        soft_max = []
        for z in Z:
            numerator = np.exp(z)
            denom = np.sum(np.exp(Z))
            term = numerator / denom
            soft_max.append(term)
        return soft_max
    

    def set_fitness(self, fitness):
        self.fitness = fitness


    def mutate(self):
        
        network_elements = [self.W1, self.W2, self.b1, self.b2, self.hidden_layer_size]
        elements_size = len(network_elements)

        mutation_index = np.random.randint(elements_size)
        
        mutation_element = network_elements[mutation_index]

        # Weight matrix mutation
        if mutation_index == 0 or mutation_index == 1:
            print("\n\tMutation to Weight Matrix.\n")
            self.mutate_W(mutation_element)

        elif mutation_index == 2 or mutation_index == 3:
            print("\n\tMutation to Bias.\n")
            self.mutate_b(mutation_element)

        elif mutation_index == 4:
            print("\n\tMutation to Hidden Layer.\n")
            self.mutate_hidden_layer(self.W1, self.W2, mutation_element)
        
        return network_elements



    def mutate_W(self, element):
        num_rows = len(element)
        num_cols = len(element[0])
        
        mutation_row = np.random.randint(num_rows)
        mutation_col = np.random.randint(num_cols)
        #print("Mutation at {},{}: {}".format(mutation_row, mutation_col, element[mutation_row][mutation_col]))
        
        mutation = np.random.randn(1) * 50
        #print("Mutation: {}".format(mutation))
        element[mutation_row][mutation_col] += mutation
        #print("Post Mutation at {},{}: {}".format(mutation_row, mutation_col, element[mutation_row][mutation_col]))
        

    def mutate_b(self, element):
        mutation = np.random.randn(1) * 50
        element += mutation
        

    def mutate_hidden_layer(self, W1, W2, element):

        if np.random.randn(1) >= 0:
            node_change = 1
        else:
            if element > 1:
                node_change = -1

        element += node_change

        
        # Update W1
        W1_num_cols = len(W1[0])
        new_W1 = np.random.randn(element, W1_num_cols)
        for row_i, row in enumerate(new_W1[:element]):
            for col_i, ele in enumerate(row):
                new_W1[row_i][col_i] = ele

        W1 = new_W1


        # Update W2
        new_W2 = np.random.randn(1, element) * 50
        for index, col in enumerate(new_W2[0][:element]):
            new_W2[0][index] = col
            
        W2 = new_W2
        
                
