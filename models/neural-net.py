from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix


#Neural Network supervised


'''Classify layers for neural networks'''
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30)) #30,30,30 refers to 3 layers with 30 being number of features

'''Fit the model'''
mlp.fit(X_train,y_train) #X_train: (n samples, n features), #y_train = n samples of target values (leading/trailing) 

'''Evaluate how our model performed on test sets'''
predictions = mlp.predict(X_test)
print(confusion_matrix(y_test,predictions)) #(y_true, y_prediction)
print(classification_report(y_test,predictions)) #Classification report 
len(mlp.coefs_) #list of weight matrices (weights between i and layer i+1)
len(mlp.coefs_[0])
len(mlp.intercepts_[0]) #bias value at index @ layer + 1

