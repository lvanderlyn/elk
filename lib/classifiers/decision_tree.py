from sklearn import tree

def train(x, y, max_depth=3):
    clf = tree.DecisionTreeClassifier(max_depth=max_depth)
    clf.fit(x, y)
    return clf

def get_visualization(model):
    return tree.export_graphviz(model)
