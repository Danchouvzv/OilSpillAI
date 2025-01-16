import numpy as np
import seaborn as sns
from imblearn.over_sampling import ADASYN
from matplotlib import pyplot as plt
from numpy import mean, std
from pandas import read_csv
from collections import Counter
from sklearn.preprocessing import LabelEncoder, MaxAbsScaler
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score, train_test_split
from imblearn.metrics import geometric_mean_score
from sklearn.metrics import make_scorer, confusion_matrix, classification_report
from imblearn.pipeline import Pipeline
import lightgbm as lgb

dataset_path = 'oil-spill_Dataset.csv'

df = read_csv(dataset_path, header=None)

print('Dataset Dimensions:', df.shape)
print() 
print(df.head(5))
print()

axes = df.hist()

for axis in axes.flatten():
    axis.set_title('')
    axis.set_xticklabels([])
    axis.set_yticklabels([])
plt.show()

target = df.values[:, -1]
class_counter = Counter(target)
for key, value in class_counter.items():
    percentage = value / len(target) * 100
    print('Class= %d, Count= %d, Percentage= %.3f%%' % (key, value, percentage))
print()

def load_dataset(filename):
    data = read_csv(filename, header=None)
    data.drop(22, axis=1, inplace=True)
    data.drop(0, axis=1, inplace=True)
    data = data.values
    X, y = data[:, :-1], data[:, -1]
    y = LabelEncoder().fit_transform(y)
    return X, y

def evaluate_model(X, y, model):
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    metric = make_scorer(geometric_mean_score)
    scores = cross_val_score(model, X, y, scoring=metric, cv=cv, n_jobs=-1)
    return scores

plt.figure(figsize=(8, 6))
sns.countplot(x=df.values[:, -1], palette="rocket")
plt.xticks([0, 1], ['Non-Spill', 'Spill'], fontsize=15)
plt.show()

steps = [
    ('scaler', MaxAbsScaler()),
    ('classifier', lgb.LGBMClassifier(
        n_estimators=362, num_leaves=1208, min_child_samples=8,
        learning_rate=0.0207, colsample_bytree=0.3791,
        reg_alpha=0.00298, reg_lambda=1.1366
    ))
]
model = Pipeline(steps)

X, y = load_dataset(dataset_path)

print('Dataset dimensions after preprocessing:', X.shape, 'Class distribution:', Counter(y))
print()

oversampler = ADASYN()
X_resampled, y_resampled = oversampler.fit_resample(X, y)

print("Resampled dataset shape after ADASYN:")
plt.figure(figsize=(8, 6))
sns.countplot(x=y_resampled, palette="rocket")
plt.xticks([0, 1], ['Non-Spill', 'Spill'], fontsize=15)
plt.show()

resampled_counter = Counter(y_resampled)
for key, value in resampled_counter.items():
    percentage = value / len(y_resampled) * 100
    print('Class= %d, Count= %d, Percentage= %.3f%%' % (key, value, percentage))

X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, stratify=y_resampled, random_state=1)

scores = evaluate_model(X_resampled, y_resampled, model)
print('Final Model Evaluation Scores')
print('Mean G-Mean of 10 folds: %.3f - Std Dev: (%.3f)' % (mean(scores), std(scores)))
model.fit(X_resampled, y_resampled)

print()

test_scores = evaluate_model(X_test, y_test, model)
print('Mean G-Mean on Test Set: %.3f - Std Dev: (%.3f)' % (mean(test_scores), std(test_scores)))

print()

y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
