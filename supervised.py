from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
    
    ##supervised!
    
def get_predictions(df, dflabel, target):
    #set up targets
    dflabel = dflabel.copy()
    dflabel[target] = [1 if dflabel['category'][i]==target else 0 for i in range(len(dflabel))]
    
    #train
    X = dflabel[dflabel.columns[3:-1]]
    y = dflabel[target]
    
    rf = RandomForestClassifier(n_estimators=100)
    try:
        X.drop('cluster', axis=1, inplace=True)
    except:
        pass
    rf.fit(X,y)
    #predict
    Xtest = df[df.columns[1:]]
    predictions = rf.predict(Xtest)
    return predictions
    
    
def plot_predictions(tsne_results, predictions):
    fig = plt.figure(figsize=(15,12))
    ax = fig.add_subplot(111)

    mask = predictions==1
    
    plt.scatter(tsne_results[mask][:,0], tsne_results[mask][:,1], s=100,c='green',alpha=.4,label=('Predicted exchanges'))

    plt.scatter(tsne_results[~mask][:,0], tsne_results[~mask][:,1], c='gray',s=20, alpha=.1)

    leg = plt.legend(bbox_to_anchor=(1, 1))
    for lh in leg.legendHandles: 
        lh.set_alpha(1)




    plt.title('T-SNE', fontsize=20)
    plt.xlabel('first principal component')
    plt.ylabel('second principal component')
    plt.show()