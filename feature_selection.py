from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
import numpy, pandas
import get_dataset
from matplotlib import pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2
from scipy.stats import pearsonr
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import os.path
import process_output


def multivariate_pearsonr(X, y):
    scores, pvalues = [], []
    for column in range(X.shape[1]):
        cur_score, cur_p = pearsonr(X[:, column], y)
        scores.append(abs(cur_score))
        pvalues.append(cur_p)
    return (numpy.array(scores), numpy.array(pvalues))


def feature_select(x, y, labels, y_contin):
    scaling = StandardScaler()
    scaling.fit(x)
    x = scaling.transform(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10)

    # normalizing
    # print(x)

    forest = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1,
                                    max_depth=15)
    forest.fit(x, y)
    print("__________Evaluating by RandomForest importance and pearson correlation__________")
    print(
        "1) rank , 2) Feature name ,                                       3) RandomForest importance , "
        "4) Pearson Correlation , 5) p_value of pearson correlation")
    pearson_score, p_values = multivariate_pearsonr(x, y_contin)
    importances = forest.feature_importances_
    indices = numpy.argsort(importances)[::-1]
    for f in range(x_train.shape[1]):
        if pearson_score[indices[f]]>0.1 and  p_values[indices[f]] >0.1:
            print("%2d)         %-*s %-*f %-*f %-*f" % (
                f + 1, 63, labels[indices[f]], 26, importances[indices[f]], 26, pearson_score[indices[f]],
                26, p_values[indices[f]]))
    print("score:", forest.score(x_test, y_test))


if __name__ == "__main__":
    threshold = 0
    dfs = get_dataset.get_data_sets(threshold=threshold)
    results = {}
    for label in dfs:
        df = dfs[label]
        print("Evaluating features of " + label)
        # transfer the output values from Numeric to Class (0-> LOW , 1-> HIGH) using median
        y_median = df[label].median()
        y_contin = df[label]
        df.loc[df[label] <= y_median, label] = 0
        df.loc[df[label] > y_median, label] = 1
        x = df.drop(columns=label)
        # print(x.shape)
        labels = x.columns

        y = df[label].to_numpy()
        # k fold cross validation
        # KF = StratifiedKFold(n_splits=10, shuffle=True)

        accuracies = []

        feature_select(x, y, labels, y_contin)
