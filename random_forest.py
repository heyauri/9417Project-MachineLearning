from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.decomposition import PCA
import numpy, pandas
import get_dataset
from matplotlib import pyplot as plt


def evaluate_model(x_train, x_test, y_train, y_test, decomposition=False):
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, random_state=25)

    # normalizing
    scaling = StandardScaler()
    scaling.fit(x_train)
    x_train = scaling.transform(x_train)
    x_test = scaling.transform(x_test)
    # decomposition (optional)
    if decomposition and x_train.shape[0]>x_train.shape[1]:
        pca = PCA(n_components="mle")
        pca.fit(x_train)
        x_train = pca.transform(x_train)
        x_test = pca.transform(x_test)

    # train model
    model = RandomForestClassifier(n_estimators=1234,max_depth=15)
    model.fit(x_train, y_train)

    # evaluate accuracy
    return model.score(x_test, y_test)


if __name__ == "__main__":
    method="RandomForest"
    threshold=0.2
    dfs = get_dataset.get_k_features_by_importance(k=20)
    results={}
    print("Method: "+method)
    for label in dfs:
        df = dfs[label]
        x = df.drop(columns=label).to_numpy()
        y = df[label].to_numpy()
        # k fold cross validation
        KF = StratifiedKFold(n_splits=20,shuffle=True)

        accuracies = []
        for i_train, i_test in KF.split(x, y):
            x_train, x_test = x[i_train], x[i_test]
            y_train, y_test = y[i_train], y[i_test]
            accuracy = evaluate_model(x_train, x_test, y_train, y_test, decomposition=False)
            accuracies.append(accuracy*100)

        print("Average k-fold accuracy of "+label+" is: " + str(sum(accuracies) / len(accuracies))+"%")
        results[label]=accuracies
    fig, ax = plt.subplots()

    plt.xlabel('k folds epoch (times)')
    plt.ylabel('Model accuracy of '+method+' (%)')

    for label in results:
        x=[i for i in range(len(results[label]))]
        plt.plot(x, results[label], label=label)

    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.show()
