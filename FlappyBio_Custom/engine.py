from modules.environment import Environment

def main(generations, organisms):
    scores = []
    
    environment = Environment(organisms)

    for generation in range(generations):

        environment.generate_fitness()
        environment.selection()
        environment.replication()


if __name__ == "__main__":
    
    generations = 100
    organisms = 10   # number of neural nets per generation
    main(generations, organisms)