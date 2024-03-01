from typing import List, Dict
from sklearn.metrics import f1_score

from eval.evaluate import Evaluate


class EvaluateTrack2(Evaluate):
    def get_vector(self, prediction: List[Dict[str, str]], key_name: str, label_list: List[str]) -> List[int]:
        return self.map_labels_to_vector(self.get_prediction(prediction, key_name), label_list)

    def evaluate(self):
        pred_rhetoric_list, pred_content_list = [], []
        truth_rhetoric_list, truth_content_list = [], []

        for i, (pred, truth) in enumerate(zip(self.prediction, self.ground_truth)):
            assert pred['id'] == truth['id']
            assert pred['sentence'] == truth['sentence']

            pred_rhetoric_list.append(self.get_vector(pred['prediction'], 'rhetorical', self.RHETORIC))
            pred_content_list.append(self.get_vector(pred['prediction'], 'content', self.CONTENT))
            truth_rhetoric_list.append(self.get_vector(truth['prediction'], 'rhetorical', self.RHETORIC))
            truth_content_list.append(self.get_vector(truth['prediction'], 'content', self.CONTENT))

        rhetoric_f1 = f1_score(truth_rhetoric_list, pred_rhetoric_list, average='macro', zero_division=1.0)
        content_f1 = f1_score(truth_content_list, pred_content_list, average='macro', zero_division=1.0)

        return 0.3 * rhetoric_f1 + 0.7 * content_f1
