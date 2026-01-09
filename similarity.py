from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import get_articles as art

def _cosim(a,b,vectorizer):
    X = vectorizer.fit_transform([a,b])
    return cosine_similarity(X[0],X[1])[0][0]


def check_similarity(text1,text2): #using TF-IDF(turn text to numbers) and Cosine Similarity(compare those numbers)
    
    #tfidf shows how imortant the word is in the text compared to other text
    #tdidf total frequency  * inverse document frequency
    char_vec  = TfidfVectorizer( #character similarity catching copypasre
        analyzer= "char_wb",
        ngram_range= (3,6), 
        lowercase= True
    )
    char_score = _cosim(text1,text2,char_vec)
    
    word_vec = TfidfVectorizer(
        stop_words = "english", #ignore common filler words
        ngram_range= (1,2) #one word two word
    )
    word_score = _cosim(text1,text2,word_vec)
    
    score = (0.65 * char_score) + (0.35 * word_score) #weighting char overlap more
    
    return score


#splitting essay into paragraphs
def split_para(a):
    with open(a,"r", encoding="utf-8", errors = "replace") as file_a:
        para_a = file_a.read().strip().split("\n\n")
    return para_a


    
#getting coverage percent, basically how many paragraphs are suspiscious out of all the paragraphs, getting the highest score, and the top3 average score acrosss all paragraphs
def get_scores(text1,text2,threshold):
    paras_a = split_para(text1)
    paras_b = split_para(text2)
    print(len(paras_a))
    print(len(paras_b))
    suspicious = 0
    max_score = 0
    scores = []
    for pa in paras_a:
        best_pa = 0
        for pb in paras_b:
            score = check_similarity(pa,pb)
            best_pa = max(best_pa, score)
        if best_pa >= threshold:
                suspicious += 1
        if best_pa >= max_score:
            max_score = best_pa
        scores.append(best_pa)
    scores.sort() 
    
    k = min(3,len(scores))
    if not k:
        top_avg = 0
    else:
        top_avg = sum(scores[-k:] ) / k
    
    if len(paras_a) > 0:
        coverage = suspicious / len(paras_a)
    else:
        coverage = 0.0
    print(max_score)
    print(top_avg)
    print(coverage)
    return max_score,top_avg,coverage
    


def cheap_relevance(sample, body):
    word_vec = TfidfVectorizer(
        stop_words = "english", #ignore common filler words
        ngram_range= (1,1) #one word 
    )
    score = _cosim(sample,body,word_vec)
    return score


def get_scores_articles(a,b,threshold):
    paras_a = split_para(a)
    paras_b = art.split_article_into_chunks(b)

    suspicious = 0
    max_score = 0.0
    best_scores_per_para = []

    for pa in paras_a:
        best_pa = 0.0
        for pb in paras_b:
            score = check_similarity(pa, pb)
            if score > best_pa:
                best_pa = score

        if best_pa >= threshold:
            suspicious += 1

        if best_pa > max_score:
            max_score = best_pa

        best_scores_per_para.append(best_pa)

    best_scores_per_para.sort()
    k = min(3, len(best_scores_per_para))
    top_avg = (sum(best_scores_per_para[-k:]) / k) if k else 0.0
    coverage = (suspicious / len(paras_a)) if paras_a else 0.0

    return max_score, top_avg, coverage    

