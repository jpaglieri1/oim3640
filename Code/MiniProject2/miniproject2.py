def resupload():
    resume = open(input("Input directory to file: "))
    return(resume)

def jobdesc():
    jd = open(input("Input directory to job description file: "))
    return(jd)

def dataclean(file):
    prepositions = ["in", "the", "it", "of", "a", "to", "with", "to", "for", "on", "at", "by", "from",
                    "into", "about", "between", "like", "after", "over", "through"]
    file = file.lower()
    for word in prepositions:
        for i in file:
            if word == i:
                file = file.remove(i)
    for " " in file:
        file = file.remove(" ")
    return file