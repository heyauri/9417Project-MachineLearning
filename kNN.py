from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.decomposition import PCA
import numpy, pandas
import get_dataset
from matplotlib import pyplot as plt


def evaluate_model(x_train, x_test, y_train, y_test, model, decomposition=False):

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
    model.fit(x_train, y_train)

    # evaluate accuracy
    return model.score(x_test, y_test)


if __name__ == "__main__":
    method = "kNN"
    print("Method: " + method)
    default_dict = {"FlourishingScale": 0, "Positive": 0, "Negative": 0}
    feature_nums = default_dict.copy()
    results = {"FlourishingScale": [], "Positive": [], "Negative": []}
    results_trend_by_feature_num = {"FlourishingScale": [], "Positive": [], "Negative": []}
    best_score = default_dict.copy()
    best_k = default_dict.copy()
    feature_upper = 80
    #compare the score between different numbers of feature
    for feature_num in range(1, feature_upper + 1):
        print("current feature number: " + str(feature_num))
        dfs = get_dataset.get_k_features_by_importance(k=feature_num)
        for label in dfs:
            average_accuracies = []
            df = dfs[label]
            x = df.drop(columns=label).to_numpy()
            y = df[label].to_numpy()
            # k fold cross validation
            for k in range(1, 30):
                accuracies = []
                KF = StratifiedKFold(n_splits=20, shuffle=True)
                for i_train, i_test in KF.split(x, y):
                    x_train, x_test = x[i_train], x[i_test]
                    y_train, y_test = y[i_train], y[i_test]
                    model = KNeighborsClassifier(n_neighbors=k)
                    accuracy = evaluate_model(x_train, x_test, y_train, y_test, model, decomposition=False)
                    accuracies.append(accuracy * 100)

                average_accuracy = sum(accuracies) / len(accuracies)
                average_accuracies.append(average_accuracy)
                if average_accuracy > best_score[label] and len(accuracies) > 0:
                    best_score[label] = average_accuracy
                    best_k[label] = k
                    feature_nums[label] = feature_num
                    results[label] = accuracies.copy()
            results_trend_by_feature_num[label].append(sum(average_accuracies) / len(average_accuracies))

    fig, ax = plt.subplots(figsize=(8, 8))

    plt.xlabel('20-fold epoch (times)')
    plt.ylabel('Model accuracy of ' + method + ' (%) with corresponded best feature number', fontsize=11)

    plt.ylim(0, 110)
    plt.xlim(0, 21)
    plt.yticks(numpy.arange(0, 110, 10))
    plt.xticks(numpy.arange(1, 21, 1))
    for label in results:
        print("Average 20-fold accuracy of %s while k=%d and feature number=%d is %d %s" %
              (label, best_k[label], feature_nums[label], best_score[label], "%"))
        x = [i + 1 for i in range(len(results[label]))]
        plt.plot(x, results[label], label=label)

    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.savefig("./imgs/" + method + "_best_score.png")
    plt.show()
    fig, ax = plt.subplots(figsize=(10,10))

    plt.xlabel('Feature numbers')
    plt.ylabel('Average ' + method + ' accuracy of corresponded feature numbers in (%)', fontsize=11)

    plt.ylim(0, 110)
    plt.xlim(0, feature_upper + 1)
    plt.yticks(numpy.arange(0, 110, 10))
    if feature_upper < 21:
        plt.xticks(numpy.arange(1, feature_upper + 1, 1))
    else:
        plt.xticks(numpy.arange(5, feature_upper + 1, 5))

    for label in results:
        x = [i + 1 for i in range(len(results_trend_by_feature_num[label]))]
        plt.plot(x, results_trend_by_feature_num[label], label=label)

    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.savefig("./imgs/" + method + "_trend_by_feature_number.png")
    plt.show()
