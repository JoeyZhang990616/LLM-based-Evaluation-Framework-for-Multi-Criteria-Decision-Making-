import pandas as pd
import re
from sklearn.metrics import confusion_matrix, accuracy_score

data = pd.read_csv('', header=None)

true_labels = {
    'Delivery Rating': [],
    'Profit Margin Rating': [],
    'Shipping Rating': [],
    'Market Rating': [],
    'Overall Score': []
}

pred_labels = {
    'Delivery Rating': [],
    'Profit Margin Rating': [],
    'Shipping Rating': [],
    'Market Rating': [],
    'Overall Score': []
}

def clean_rating(rating):
    if rating is None:
        return None

    cleaned = re.sub(r'[}\.]+$', '', rating.strip())
    return cleaned

def extract_rating(entry, rating_type):
    if pd.isna(entry):
        return None
    entry = str(entry)
    if rating_type == 'Overall Score':
        pattern = r'Overall Score:\s*{?(.*?)}?\.?\s*$'
    else:
        pattern_with_braces = rf'{{{rating_type}}}{{(.*?)}}\.?'
        pattern_without_braces = rf'{rating_type}: (.+?)(?:\s|$)'

        rating = re.search(pattern_with_braces, entry)
        if rating:
            return clean_rating(rating.group(1))

        rating = re.search(pattern_without_braces, entry)
        if rating:
            return clean_rating(rating.group(1))

        return None

    rating = re.search(pattern, entry)
    return clean_rating(rating.group(1)) if rating else None

for index, row in data.iterrows():
    for rating_type in true_labels.keys():

        true_labels[rating_type].append(extract_rating(str(row[0]), rating_type))
        pred_labels[rating_type].append(extract_rating(str(row[1]), rating_type))

for rating_type in true_labels.keys():
    print(f'\n{rating_type} True:')
    print(true_labels[rating_type])
    print(f'{rating_type} pre:')
    print(pred_labels[rating_type])

results = {}
all_accuracy = []
all_precision = []
all_recall = []
all_f1 = []

for rating_type in true_labels.keys():
    filtered_true_labels = [label for label in true_labels[rating_type] if label is not None]
    filtered_pred_labels = [pred for pred, true in zip(pred_labels[rating_type], true_labels[rating_type]) if
                            true is not None and pred is not None]

    if len(filtered_true_labels) != len(filtered_pred_labels):
        min_length = min(len(filtered_true_labels), len(filtered_pred_labels))
        filtered_true_labels = filtered_true_labels[:min_length]
        filtered_pred_labels = filtered_pred_labels[:min_length]

    if filtered_true_labels and filtered_pred_labels:
        cm = confusion_matrix(filtered_true_labels, filtered_pred_labels, labels=list(set(filtered_true_labels)))

        TP = sum(cm[i, i] for i in range(len(cm)))
        FP = sum(cm[:, i].sum() - cm[i, i] for i in range(len(cm)))
        FN = sum(cm[i, :].sum() - cm[i, i] for i in range(len(cm)))
        TN = cm.sum() - (TP + FP + FN)

        accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0

        precision = {}
        recall = {}
        f1 = {}

        for i in range(len(cm)):
            tp = cm[i, i]
            fp = sum(cm[:, i]) - tp
            fn = sum(cm[i, :]) - tp

            precision[i] = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall[i] = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1[i] = 2 * (precision[i] * recall[i]) / (precision[i] + recall[i]) if (precision[i] + recall[i]) > 0 else 0

            # print(f"类别 {i} 的指标:")
            # print(f"TP: {tp}, FP: {fp}, FN: {fn}")
            # print(f"精确率: {precision[i]:.4f}, 召回率: {recall[i]:.4f}, F1 分数: {f1[i]:.4f}")

        weighted_precision = sum(precision[i] * cm[i, :].sum() for i in range(len(cm))) / sum(cm.sum(axis=1))
        weighted_recall = sum(recall[i] * cm[i, :].sum() for i in range(len(cm))) / sum(cm.sum(axis=1))
        weighted_f1 = sum(f1[i] * cm[i, :].sum() for i in range(len(cm))) / sum(cm.sum(axis=1))

        results[rating_type] = {
            'Accuracy': accuracy_score(filtered_true_labels, filtered_pred_labels),
            'Precision': weighted_precision,
            'Recall': weighted_recall,
            'F1 Score': weighted_f1,
            'Confusion Matrix': cm
        }

        all_accuracy.append(results[rating_type]['Accuracy'])
        all_precision.append(weighted_precision)
        all_recall.append(weighted_recall)
        all_f1.append(weighted_f1)

    else:
        results[rating_type] = {
            'Accuracy': None,
            'Precision': None,
            'Recall': None,
            'F1 Score': None,
            'Confusion Matrix': None
        }

total_accuracy = sum(all_accuracy) / len(all_accuracy) if all_accuracy else None
total_precision = sum(all_precision) / len(all_precision) if all_precision else None
total_recall = sum(all_recall) / len(all_recall) if all_recall else None
total_f1 = sum(all_f1) / len(all_f1) if all_f1 else None

for rating_type, metrics in results.items():
    print(f'\n{rating_type} Metrics:')
    if metrics['Accuracy'] is not None:
        print(f'Accuracy: {metrics["Accuracy"]:.4f}')
        print(f'Precision: {metrics["Precision"]:.4f}')
        print(f'Recall: {metrics["Recall"]:.4f}')
        print(f'F1 Score: {metrics["F1 Score"]:.4f}')
        print(f'Confusion Matrix:\n{metrics["Confusion Matrix"]}')
    else:
        print("No valid metrics to display.")

print(f'\nTotal Metrics:')
print(f'Total Accuracy: {total_accuracy:.4f}' if total_accuracy is not None else "No valid total accuracy.")
print(f'Total Precision: {total_precision:.4f}' if total_precision is not None else "No valid total precision.")
print(f'Total Recall: {total_recall:.4f}' if total_recall is not None else "No valid total recall.")
print(f'Total F1 Score: {total_f1:.4f}' if total_f1 is not None else "No valid total F1 score.")