import get_scores as gs


def check_plagiarism():
    file = 0
    while not file:
        text = input("Enter the file to check for plagiarism (.txt): ")
        try:
            with open(text,"r"):
                print("File Found, Please Wait for plagiarism detection, this could take some time...")
                file = 1
        except FileNotFoundError:
            print("Invalid File name")
        
    scores = gs.get_essay_scores(text)
    
    overall = "UNLIKELY PLAGIARIZED"
    highest_similarity = 0

    for score in scores:
        if score[0] >= .45 or (score[1] > .3 and score[2] > .3):
            overall = "VERY LIKELY PLAGIARIZED"
            if score[0] > highest_similarity:
                highest_similarity = score[0]
        elif .22 < score[0] < .45 or (.2 <= score[1] <= .30 and .2 <= score[2] <= .3):
            if overall != "VERY LIKELY PLAGIARIZED":
                overall = "POSSIBLY PLAGIARIZED"
            if score[0] > highest_similarity:
                highest_similarity = score[0]
        else:
            if overall != "VERY LIKELY PLAGIARIZED" and overall != "POSSIBLY PLAGIARIZED":
                overall =  "UNLIKELY PLAGIARIZED"
            if score[0] > highest_similarity:
                highest_similarity = score[0]
    print(f"Overall your essay is {overall} and recieved a max similarity score of {highest_similarity:.2f} when compared with webpages on the internet")
                


check_plagiarism()      

     
    
    