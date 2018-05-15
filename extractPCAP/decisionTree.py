from sklearn import tree
from sklearn.datasets import load_iris
import graphviz

data_input = []
for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                for m in range(2):
                    data_input.append([i,j,k,l,m])
data_output = [1,2,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,0,0,0,3,0,0,0,1,1,1,1,3,0,0,0]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(data_input, data_output)

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("Protocols")

feature_names = ['Obj size', 'loss', 'RTT', 'Obj #', 'BW']
target_names = ['HTTP/1.1', 'SPDY', 'SPDY/HTTP2', 'HTTP/2']
dot_data = tree.export_graphviz(clf, out_file=None, feature_names=feature_names, class_names=target_names, filled=True, rounded=True, special_characters=True)
graph = graphviz.Source(dot_data)
graph
