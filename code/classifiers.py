"""

Title: Retweet Us, We Will Retweet You: Spotting Collusive Retweeters 
Involved in Blackmarket Services. (ASONAM 2018)

Authors: Hridoy Sankar Dutta, Aditya Chetan, Brihi Joshi, Tanmoy Chakraborty

"""



import sys
from sklearn import svm
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve, auc
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
import numpy as np
import pickle
from scipy import interp

from sklearn.svm import LinearSVC

# Change to micro and macro accordingly
def multiClassROCAUCmicro(y_test, y_pred):
	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()


	roc_auc = dict()
	for i in range(4):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])

	# Compute micro-average ROC curve and ROC area
	fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_pred.ravel())
	roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
	return roc_auc["micro"]

def multiClassROCAUCmacro(y_test, y_pred, n_classes):
	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()

	roc_auc = dict()
	for i in range(4):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])

	# Compute micro-average ROC curve and ROC area
	# Compute macro-average ROC curve and ROC area

	# First aggregate all false positive rates
	all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

	# Then interpolate all ROC curves at this points
	mean_tpr = np.zeros_like(all_fpr)
	for i in range(n_classes):
		mean_tpr += interp(all_fpr, fpr[i], tpr[i])

	# Finally average it and compute AUC
	mean_tpr /= n_classes

	fpr["macro"] = all_fpr
	tpr["macro"] = mean_tpr
	roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

	return roc_auc["macro"]






fin = open("../data/data.csv")

data_points = []
labels = []

num_lines = 0

for line in fin:

	if num_lines!=0:
		toks = line.strip().split(",")
		tmp = toks[1:-1]
		inp = [float(tok) for tok in tmp]
		label = int(toks[-1])
		data_points.append(inp)
		labels.append(label)
	num_lines+=1

y = labels



# Binarize labels

if sys.argv[1] == "-b":
	for i in range(len(y)):

		if y[i] == 0 or y[i] == 1 or y[i] == 2:

			y[i] = 0

		else:

			y[i] = 1


# X_train, X_test, y_train, y_test = train_test_split(data_points, labels, test_size=0.2, shuffle=True, stratify=labels)


data_points = np.array(data_points)
kf = StratifiedKFold(n_splits=10,shuffle=True)


micro_stats = []
macro_stats = []
auc_svm_micro = []
auc_svm_macro = []
accuracy_score_svm = []

micro_stats_lin = []
macro_stats_lin = []
auc_svm_micro_lin = []
auc_svm_macro_lin = []
accuracy_score_lin = []

micro_stats_rdf = []
macro_stats_rdf = []
auc_rdf_micro = []
auc_rdf_macro = []
accuracy_score_rdf = []

micro_stats_ada = []
macro_stats_ada = []
auc_ada_micro = []
auc_ada_macro = []
accuracy_score_ada = []

micro_stats_dt = []
macro_stats_dt = []
auc_dt_micro = []
auc_dt_macro = []
accuracy_score_dt = []

micro_stats_lr = []
macro_stats_lr = []
auc_lr_micro = []
auc_lr_macro = []
accuracy_score_lr = []

micro_stats_knn = []
macro_stats_knn = []
auc_knn_micro = []
auc_knn_macro = []
accuracy_score_knn = []


micro_stats_gnb = []
macro_stats_gnb = []
auc_gnb_micro = []
auc_gnb_macro = []
accuracy_score_gnb = []

micro_stats_bag = []
macro_stats_bag = []
auc_bag_micro = []
auc_bag_macro = []
accuracy_score_bag = []

if sys.argv[1] == "-b":

	class_names = ['genuine', 'non-genuine']

else:

	class_names = ['bots', 'normal', 'promotional', 'genuine']







data_points = np.array(data_points)
y = np.array(y)

for train_index, test_index in kf.split(data_points, y):

	X_train, X_test = data_points[train_index], data_points[test_index]
	y_train, y_test = y[train_index], y[test_index]


	X_train = preprocessing.scale(X_train)
	X_test = preprocessing.scale(X_test)

	clf = svm.SVC()
	clf.fit(X_train, y_train)
	y_pred = clf.predict(X_test)

	filename = 'svm_binary_model.sav'
	pickle.dump(clf, open(filename, 'wb'))


	clf_lin = LinearSVC(random_state=0)
	clf_lin.fit(X_train, y_train)
	y_pred_lin_svm = clf_lin.predict(X_test)

	clf_rd = RandomForestClassifier()
	clf_rd.fit(X_train, y_train)
	y_pred_rd = clf_rd.predict(X_test)

	clf_ada = AdaBoostClassifier()
	clf_ada.fit(X_train, y_train)
	y_pred_ada = clf.predict(X_test)

	clf_dt = tree.DecisionTreeClassifier()
	clf_dt.fit(X_train, y_train)
	y_pred_dt = clf_dt.predict(X_test)

	clf_lr = LogisticRegression()
	clf_lr.fit(X_train, y_train)
	y_pred_lr = clf_lr.predict(X_test)

	clf_knn = KNeighborsClassifier(n_neighbors=5)
	clf_knn.fit(X_train, y_train) 
	y_pred_knn = clf_knn.predict(X_test)

	clf_gnb = GaussianNB()
	clf_gnb.fit(X_train, y_train)
	y_pred_gnb = clf_gnb.predict(X_test)

	clf_bagging = BaggingClassifier(base_estimator=None)
	clf_bagging.fit(X_train, y_train)
	y_pred_bagging = clf_bagging.predict(X_test)



	classification_report_svm = classification_report(y_test, y_pred, target_names=class_names)
	accuracy_score_svm.append(accuracy_score(y_test, y_pred, normalize=True))
	micro_stats.append(precision_recall_fscore_support(y_test, y_pred, average='micro'))
	macro_stats.append(precision_recall_fscore_support(y_test, y_pred, average='macro'))

	if sys.argv[1] == "-b":
		auc_svm_micro.append(roc_auc_score(y_test, y_pred, average='micro', sample_weight=None))
		auc_svm_macro.append(roc_auc_score(y_test, y_pred, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_svm = OneVsRestClassifier(LinearSVC(random_state=0))
		n_classes = y_test_new.shape[1]
		y_pred_multi_svm = clf_multi_svm.fit(X_train, y_train).decision_function(X_test)
		auc_svm_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_svm))
		auc_svm_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_svm, n_classes))


	# classification_report_rdf = classification_report(y_test, y_pred_rd, target_names=class_names)
	accuracy_score_rdf.append(accuracy_score(y_test, y_pred_rd, normalize=True))
	micro_stats_rdf.append(precision_recall_fscore_support(y_test, y_pred_rd, average='micro'))
	macro_stats_rdf.append(precision_recall_fscore_support(y_test, y_pred_rd, average='macro'))

	if sys.argv[1] == "-b":
		auc_rdf_micro.append(roc_auc_score(y_test, y_pred_rd, average='micro', sample_weight=None))
		auc_rdf_macro.append(roc_auc_score(y_test, y_pred_rd, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_rd = RandomForestClassifier()
		n_classes = y_test_new.shape[1]
		y_pred_multi_rd = clf_multi_rd.fit(X_train, y_train).predict_proba(X_test)
		auc_rdf_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_rd))
		auc_rdf_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_rd, n_classes))


	# classification_report_ada = classification_report(y_test, y_pred_knn, target_names=class_names)
	accuracy_score_ada.append(accuracy_score(y_test, y_pred_knn, normalize=True))
	micro_stats_ada.append(precision_recall_fscore_support(y_test, y_pred_knn, average='micro'))
	macro_stats_ada.append(precision_recall_fscore_support(y_test, y_pred_knn, average='macro'))

	if sys.argv[1] == "-b":
		auc_ada_micro.append(roc_auc_score(y_test, y_pred_ada, average='micro', sample_weight=None))
		auc_ada_macro.append(roc_auc_score(y_test, y_pred_ada, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_ada = OneVsRestClassifier(AdaBoostClassifier())
		n_classes = y_test_new.shape[1]
		y_pred_multi_ada = clf_multi_ada.fit(X_train, y_train).decision_function(X_test)
		auc_ada_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_ada))
		auc_ada_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_ada, n_classes))


	# classification_report_dt = classification_report(y_test, y_pred_dt, target_names=class_names)
	accuracy_score_dt.append(accuracy_score(y_test, y_pred_dt, normalize=True))
	micro_stats_dt.append(precision_recall_fscore_support(y_test, y_pred_dt, average='micro'))
	macro_stats_dt.append(precision_recall_fscore_support(y_test, y_pred_dt, average='macro'))

	if sys.argv[1] == "-b":
		auc_dt_micro.append(roc_auc_score(y_test, y_pred_dt, average='micro', sample_weight=None))
		auc_dt_macro.append(roc_auc_score(y_test, y_pred_dt, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_dt = tree.DecisionTreeClassifier()
		n_classes = y_test_new.shape[1]
		y_pred_multi_dt = clf_multi_dt.fit(X_train, y_train).predict_proba(X_test)
		auc_dt_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_dt))
		auc_dt_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_dt, n_classes))


	classification_report_lr = classification_report(y_test, y_pred_lr, target_names=class_names)
	accuracy_score_lr.append(accuracy_score(y_test, y_pred_lr, normalize=True))
	micro_stats_lr.append(precision_recall_fscore_support(y_test, y_pred_lr, average='micro'))
	macro_stats_lr.append(precision_recall_fscore_support(y_test, y_pred_lr, average='macro'))

	if sys.argv[1] == "-b":
		auc_lr_micro.append(roc_auc_score(y_test, y_pred_knn, average='micro', sample_weight=None))
		auc_lr_macro.append(roc_auc_score(y_test, y_pred_knn, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_lr = LogisticRegression(random_state=0, multi_class='ovr')
		n_classes = y_test_new.shape[1]
		y_pred_multi_lr = clf_multi_lr.fit(X_train, y_train).predict_proba(X_test)
		auc_lr_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_lr))
		auc_lr_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_lr, n_classes))
		


	# classification_report_knn = classification_report(y_test, y_pred_knn, target_names=class_names)
	accuracy_score_knn.append(accuracy_score(y_test, y_pred_knn, normalize=True))
	micro_stats_knn.append(precision_recall_fscore_support(y_test, y_pred_knn, average='micro'))
	macro_stats_knn.append(precision_recall_fscore_support(y_test, y_pred_knn, average='macro'))

	if sys.argv[1] == "-b":
		auc_knn_micro.append(roc_auc_score(y_test, y_pred_knn, average='micro', sample_weight=None))
		auc_knn_macro.append(roc_auc_score(y_test, y_pred_knn, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_knn = KNeighborsClassifier(n_neighbors=5)
		n_classes = y_test_new.shape[1]
		y_pred_multi_knn = clf_multi_knn.fit(X_train, y_train).predict_proba(X_test)
		auc_knn_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_knn))
		auc_knn_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_knn, n_classes))

	# classification_report_gnb = classification_report(y_test, y_pred_gnb, target_names=class_names)
	accuracy_score_gnb.append(accuracy_score(y_test, y_pred_gnb, normalize=True))
	micro_stats_gnb.append(precision_recall_fscore_support(y_test, y_pred_gnb, average='micro'))
	macro_stats_gnb.append(precision_recall_fscore_support(y_test, y_pred_gnb, average='macro'))

	if sys.argv[1] == "-b":
		auc_gnb_micro.append(roc_auc_score(y_test, y_pred_gnb, average='micro', sample_weight=None))
		auc_gnb_macro.append(roc_auc_score(y_test, y_pred_gnb, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_gnb = GaussianNB()
		n_classes = y_test_new.shape[1]
		y_pred_multi_gnb = clf_multi_dt.fit(X_train, y_train).predict_proba(X_test)
		auc_gnb_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_gnb))
		auc_gnb_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_gnb, n_classes))

	# classification_report_bag = classification_report(y_test, y_pred_bagging, target_names=class_names)
	accuracy_score_bag.append(accuracy_score(y_test, y_pred_bagging, normalize=True))
	micro_stats_bag.append(precision_recall_fscore_support(y_test, y_pred_bagging, average='micro'))
	macro_stats_bag.append(precision_recall_fscore_support(y_test, y_pred_bagging, average='macro'))

	if sys.argv[1] == "-b":
		auc_bag_micro.append(roc_auc_score(y_test, y_pred_bagging, average='micro', sample_weight=None))
		auc_bag_macro.append(roc_auc_score(y_test, y_pred_bagging, average='macro', sample_weight=None))
	else:
		y_test_new = label_binarize(y_test, classes=[0,1,2,3])
		clf_multi_bag = OneVsRestClassifier(BaggingClassifier(base_estimator=None))
		n_classes = y_test_new.shape[1]
		y_pred_multi_bag = clf_multi_bag.fit(X_train, y_train).predict_proba(X_test)
		auc_bag_micro.append(multiClassROCAUCmicro(y_test_new, y_pred_multi_bag))
		auc_bag_macro.append(multiClassROCAUCmacro(y_test_new, y_pred_multi_bag, n_classes))



print "-------------------- SVM -----------------------\n"
print "Classification report:\n"
print classification_report_svm
print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_svm))/len(accuracy_score_svm)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats]))/len(micro_stats)
print "Recall: ", float(sum([p[1] for p in micro_stats]))/len(micro_stats)
print "F1-score: ", float(sum([p[2] for p in micro_stats]))/len(micro_stats)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats]))/len(macro_stats)
print "Recall: ", float(sum([p[1] for p in macro_stats]))/len(macro_stats)
print "F1-score: ", float(sum([p[2] for p in macro_stats]))/len(macro_stats)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_svm_micro))/len(auc_svm_micro), "\nMacro -- ", float(sum(auc_svm_macro))/len(auc_svm_macro)

print "\n"

print "-------------------- RDF -----------------------\n"
# print "Classification report:\n"
# print classification_report_rdf
# print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_rdf))/len(accuracy_score_rdf)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats_rdf]))/len(micro_stats_rdf)
print "Recall: ", float(sum([p[1] for p in micro_stats_rdf]))/len(micro_stats_rdf)
print "F1-score: ", float(sum([p[2] for p in micro_stats_rdf]))/len(micro_stats_rdf)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats_rdf]))/len(macro_stats_rdf)
print "Recall: ", float(sum([p[1] for p in macro_stats_rdf]))/len(macro_stats_rdf)
print "F1-score: ", float(sum([p[2] for p in macro_stats_rdf]))/len(macro_stats_rdf)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_rdf_micro))/len(auc_rdf_micro), "\nMacro -- ", float(sum(auc_rdf_macro))/len(auc_rdf_macro)


print "-------------------- ADA -----------------------\n"
# print "Classification report:\n"
# print classification_report_ada
# print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_ada))/len(accuracy_score_ada)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats_ada]))/len(micro_stats_ada)
print "Recall: ", float(sum([p[1] for p in micro_stats_ada]))/len(micro_stats_ada)
print "F1-score: ", float(sum([p[2] for p in micro_stats_ada]))/len(micro_stats_ada)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats_ada]))/len(macro_stats_ada)
print "Recall: ", float(sum([p[1] for p in macro_stats_ada]))/len(macro_stats_ada)
print "F1-score: ", float(sum([p[2] for p in macro_stats_ada]))/len(macro_stats_ada)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_ada_micro))/len(auc_ada_micro), "\nMacro -- ", float(sum(auc_ada_macro))/len(auc_ada_macro)



print "-------------------- DTREE -----------------------\n"
# print "Classification report:\n"
# print classification_report_dt
# print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_dt))/len(accuracy_score_dt)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats_lr]))/len(micro_stats_lr)
print "Recall: ", float(sum([p[1] for p in micro_stats_lr]))/len(micro_stats_lr)
print "F1-score: ", float(sum([p[2] for p in micro_stats_lr]))/len(micro_stats_lr)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats_dt]))/len(macro_stats_dt)
print "Recall: ", float(sum([p[1] for p in macro_stats_dt]))/len(macro_stats_dt)
print "F1-score: ", float(sum([p[2] for p in macro_stats_dt]))/len(macro_stats_dt)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_dt_micro))/len(auc_dt_micro), "\nMacro -- ", float(sum(auc_dt_macro))/len(auc_dt_macro)


print "-------------------- LOGR -----------------------\n"
print "Classification report:\n"
print classification_report_lr
print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_lr))/len(accuracy_score_lr)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats_lr]))/len(micro_stats_lr)
print "Recall: ", float(sum([p[1] for p in micro_stats_lr]))/len(micro_stats_lr)
print "F1-score: ", float(sum([p[2] for p in micro_stats_lr]))/len(micro_stats_lr)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats_lr]))/len(macro_stats_lr)
print "Recall: ", float(sum([p[1] for p in macro_stats_lr]))/len(macro_stats_lr)
print "F1-score: ", float(sum([p[2] for p in macro_stats_lr]))/len(macro_stats_lr)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_lr_micro))/len(auc_lr_micro), "\nMacro -- ", float(sum(auc_lr_macro))/len(auc_lr_macro)



print "-------------------- KNN -----------------------\n"
# print "Classification report:\n"
# print classification_report_lr
# print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_knn))/len(accuracy_score_knn)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats_knn]))/len(micro_stats_knn)
print "Recall: ", float(sum([p[1] for p in micro_stats_knn]))/len(micro_stats_knn)
print "F1-score: ", float(sum([p[2] for p in micro_stats_knn]))/len(micro_stats_knn)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats_knn]))/len(macro_stats_knn)
print "Recall: ", float(sum([p[1] for p in macro_stats_knn]))/len(macro_stats_knn)
print "F1-score: ", float(sum([p[2] for p in macro_stats_knn]))/len(macro_stats_knn)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_knn_micro))/len(auc_knn_micro), "\nMacro -- ", float(sum(auc_knn_macro))/len(auc_knn_macro)


print "-------------------- BAGGING -----------------------\n"
# print "Classification report:\n"
# print classification_report_lr
# print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_bag))/len(accuracy_score_bag)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats_bag]))/len(micro_stats_bag)
print "Recall: ", float(sum([p[1] for p in micro_stats_bag]))/len(micro_stats_bag)
print "F1-score: ", float(sum([p[2] for p in micro_stats_bag]))/len(micro_stats_bag)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats_bag]))/len(macro_stats_bag)
print "Recall: ", float(sum([p[1] for p in macro_stats_bag]))/len(macro_stats_bag)
print "F1-score: ", float(sum([p[2] for p in macro_stats_bag]))/len(macro_stats_bag)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_bag_micro))/len(auc_bag_micro), "\nMacro -- ", float(sum(auc_bag_macro))/len(auc_bag_macro)


print "-------------------- GNB -----------------------\n"
# print "Classification report:\n"
# print classification_report_lr
# print "\n"

print "Accuracy score: (average)\n"
print float(sum(accuracy_score_gnb))/len(accuracy_score_gnb)
print "\n"

print "Micro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in micro_stats_gnb]))/len(micro_stats_gnb)
print "Recall: ", float(sum([p[1] for p in micro_stats_gnb]))/len(micro_stats_gnb)
print "F1-score: ", float(sum([p[2] for p in micro_stats_gnb]))/len(micro_stats_gnb)
print "\n"

print "Macro (Precision, recall, f1-score, support)\n"
print "Precision: ", float(sum([p[0] for p in macro_stats_gnb]))/len(macro_stats_gnb)
print "Recall: ", float(sum([p[1] for p in macro_stats_gnb]))/len(macro_stats_gnb)
print "F1-score: ", float(sum([p[2] for p in macro_stats_gnb]))/len(macro_stats_gnb)
print "\n"

print "AUC-ROC Scores: \nMicro -- ", float(sum(auc_gnb_micro))/len(auc_gnb_micro), "\nMacro -- ", float(sum(auc_gnb_macro))/len(auc_gnb_macro)


