from modules.environment import Environment

def main(generations, organisms):
    scores = []
    
    environment = Environment(organisms)

    for generation in range(generations):

        environment.generate_fitness()
        environment.selection()
        environment.replication()


if __name__ == "__main__":
    
    generations = 100000
    organisms = 6  # number of neural nets per generation - NOTE: Must be even number
    main(generations, organisms)