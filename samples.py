import similarity as sim
import random as rand
import re
def get_samples(text):
    paras = sim.split_para(text)
    clean_samples = []
    for para in paras:
        sentences = [s.strip()
                     for s in re.split(r"[.!?]",para) 
                     if s.strip()]
        if len(sentences) > 3:
            samples = rand.sample(sentences,len(sentences)//3)
        else:
            samples = rand.sample(sentences,1)
        for sample in samples:
            clean_samples.append(sample)
    return clean_samples
        
