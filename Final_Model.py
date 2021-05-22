import pandas as pd
import pickle
data= pd.read_csv('Final_Data.csv')
print(data)
X=data.iloc[:,:9]
y=data.iloc[:,9:]
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 20, criterion = 'entropy', random_state = 42)
classifier.fit(X, y)
accuracy = classifier.score(X, y)
print(accuracy)
rfc_predictions = classifier.predict(X)
pickle.dump(classifier, open('model_final.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model_final.pkl','rb'))
print(model.predict([[31,23,77,1,8,0,0,0,1]]))