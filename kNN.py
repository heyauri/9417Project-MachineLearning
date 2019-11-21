from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.decomposition import PCA
import numpy, pandas
import get_dataset
from matplotlib import pyplot as plt


def evaluate_model(x_train, x_test, y_train, y_test, model, decomposition=False):
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
    for feature_num in range(44, feature_upper + 1):
        print("current feature number: " + str(feature_num))
        dfs = get_dataset.get_k_features_by_importance(k=feature_num)
        for label in dfs:
            best_accuracy = 0
            df = dfs[label]
            x = df.drop(columns=label).to_numpy()
            y = df[label].to_numpy()
            # k fold cross validation
            KF = StratifiedKFold(n_splits=20, shuffle=True)
            for k in range(1, min(30, feature_num + 1)):
                accuracies = []
                for i_train, i_test in KF.split(x, y):
                    x_train, x_test = x[i_train], x[i_test]
                    y_train, y_test = y[i_train], y[i_test]
                    model = KNeighborsClassifier(n_neighbors=k)
                    accuracy = evaluate_model(x_train, x_test, y_train, y_test, model, decomposition=True)
                    accuracies.append(accuracy * 100)
                average_accuracy = sum(accuracies) / len(accuracies)
                best_accuracy = max([best_accuracy, average_accuracy])
                if average_accuracy > best_score[label] and len(accuracies) > 0:
                    best_score[label] = average_accuracy
                    best_k[label] = k
                    feature_nums[label] = feature_num
                    results[label] = accuracies.copy()
            results_trend_by_feature_num[label].append(best_accuracy)

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
    plt.xlabel('Feature numbers')
    plt.ylabel('Best ' + method + ' accuracy of corresponded feature numbers in (%)', fontsize=11)

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
