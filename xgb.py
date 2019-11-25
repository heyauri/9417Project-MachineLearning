from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.decomposition import PCA
import numpy, pandas
import get_dataset
from matplotlib import pyplot as plt
import xgboost as xgb
from xgboost import plot_importance

params = {
    'booster': 'gbtree',
    'objective': 'multi:softmax',
    'gamma': 0.1,
    'num_class': 2,
    'max_depth': 6,
    'lambda': 2,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'min_child_weight': 0.01,
    'silent': 1,
    'eta': 0.01,
    'seed': 1000,
}


def evaluate_model(x_train, x_test, y_train, y_test, decomposition=False):
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, random_state=25)

    # normalizing
    scaling = StandardScaler()
    scaling.fit(x_train)
    x_train = scaling.transform(x_train)
    x_test = scaling.transform(x_test)
    # decomposition (optional)
    if decomposition and x_train.shape[0] > x_train.shape[1]:
        pca = PCA()
        pca.fit(x_train)
        x_train = pca.transform(x_train)
        x_test = pca.transform(x_test)

    # train model
    x_train = xgb.DMatrix(x_train, y_train)
    model = xgb.train(params, dtrain=x_train, num_boost_round=2000)
    x_test = xgb.DMatrix(x_test)
    predictions = model.predict(x_test)

    true_num=0
    for i in range(len(predictions)):
        if y_test[i]==predictions[i]:
            true_num+=1

    plot_importance(model)
    plt.show()
    # evaluate accuracy
    return true_num/len(y_test)


if __name__ == "__main__":
    method = "XGBoost"
    threshold = 0
    dfs = get_dataset.get_k_features_by_importance(k=20)
    results = {}
    print("Method: " + method)
    for label in dfs:
        df = dfs[label]
        # transfer the output values from Numeric to Class (0-> LOW , 1-> HIGH) using median
        y_median = df[label].median()
        df.loc[df[label] <= y_median, label] = 0
        df.loc[df[label] > y_median, label] = 1
        x = df.drop(columns=label).to_numpy()
        # print(df.columns)
        y = df[label].to_numpy()
        # k fold cross validation
        KF = StratifiedKFold(n_splits=10, shuffle=True)

        accuracies = []
        for i_train, i_test in KF.split(x, y):
            x_train, x_test = x[i_train], x[i_test]
            y_train, y_test = y[i_train], y[i_test]
            accuracy = evaluate_model(x_train, x_test, y_train, y_test, decomposition=False)
            accuracies.append(accuracy*100)

        print("Average k-fold accuracy of " + label + " is: " + str(sum(accuracies) / len(accuracies)) + "%")
        results[label] = accuracies
    fig, ax = plt.subplots()

    plt.xlabel('k folds epoch (times)')
    plt.ylabel('Model accuracy of ' + method + ' (%)')

    for label in results:
        x = [i for i in range(len(results[label]))]
        plt.plot(x, results[label], label=label)

    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    #plt.show()
