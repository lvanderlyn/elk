from sklearn import naive_bayes

def train(x, y):
    clf = naive_bayes.MultinomialNB()
    clf.fit(x, y)
    return clf
