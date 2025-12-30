import similarity as sim



def check_essay(a,b):
    max_score, top_avg, coverage = sim.get_scores(a,b,.5)


check_essay("test.txt","test2.txt")
        

