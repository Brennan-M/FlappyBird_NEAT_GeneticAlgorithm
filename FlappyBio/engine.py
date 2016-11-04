import modules.flappy as flpy
import modules.ann_feeder as ann_feeder

def main():
    scores = []
    num_games = 10

    
    
    for _ in range(num_games):
        network = ann_feeder.ann_feeder()
        results = flpy.main(network)
        scores.append(results['score'])

    print("Scores: {}".format(scores))
    


if __name__ == "__main__":
    main()