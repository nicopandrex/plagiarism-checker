import similarity as sim
import samples as samp
import get_articles as art



def get_essay_scores(a):
    samples = samp.get_samples(a)
    article_list = []
    scores = []
    for i, sample in enumerate(samples):
        articles = art.get_articles(sample)
        print(f"Found {len(articles)} articles for sample {i+1}")
        if articles:
            article_list.append(articles)
    flat_articles = art.flatten_articles(article_list)
    for i, body in enumerate(flat_articles):
        max_score,average,coverage = sim.get_scores_articles(a,body,0.4)
        scores.append((float(max_score),float(average),float(coverage)))
        print(f"Calculated all scores when compared to article {i+1}")
    return scores
        
        
    
    
    
    
    

        

