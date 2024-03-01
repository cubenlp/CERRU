from typing import List, Dict
from sklearn.metrics import f1_score

from eval.evaluate import Evaluate


class EvaluateTrack1(Evaluate):
    def get_vector(self, prediction: List[Dict[str, str]], key_name: str, label_list: List[str]) -> List[int]:
        return self.map_labels_to_vector(self.get_prediction(prediction, key_name), label_list)

    def evaluate(self):
        pred_rhetoric_list, pred_form_list = [], []
        truth_rhetoric_list, truth_form_list = [], []

        for i, (pred, truth) in enumerate(zip(self.prediction, self.ground_truth)):
            assert pred['id'] == truth['id']
            assert pred['sentence'] == truth['sentence']

            pred_rhetoric_list.append(self.get_vector(pred['prediction'], 'rhetorical', self.RHETORIC))
            pred_form_list.append(self.get_vector(pred['prediction'], 'form', self.FORM))
            truth_rhetoric_list.append(self.get_vector(truth['prediction'], 'rhetorical', self.RHETORIC))
            truth_form_list.append(self.get_vector(truth['prediction'], 'form', self.FORM))

        rhetoric_f1 = f1_score(truth_rhetoric_list, pred_rhetoric_list, average='macro', zero_division=1.0)
        form_f1 = f1_score(truth_form_list, pred_form_list, average='macro', zero_division=1.0)

        return 0.3 * rhetoric_f1 + 0.7 * form_f1
