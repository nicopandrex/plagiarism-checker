import similarity as sim
import samples as samp
import get_articles as art



def check_essay(a):
    samples = samp.get_samples(a)
    article_list = []
    for sample in samples:
        articles = art.get_articles(sample)
        if articles:
            article_list.append(articles)
    return(article_list)
        
        
print(check_essay("test2.txt"))
    
    
    
    

        

