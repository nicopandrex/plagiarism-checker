import similarity as sim
import samples as samp
import get_articles as art



def get_essay_scores(a):
    samples = samp.get_samples(a)
    article_list = []
    scores = []
    for sample in samples:
        articles = art.get_articles(sample)
        if articles:
            article_list.append(articles)
    flat_articles = art.flatten_articles(article_list)
    for i, body in enumerate(flat_articles):
        max_score,average,coverage = sim.get_scores_articles(a,body,0.4)
        scores.append((max_score,average,coverage))
    return scores
        
        
        
print(check_essay("test2.txt"))
    
    
    
    

        

