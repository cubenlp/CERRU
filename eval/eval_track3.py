from typing import List, Optional, Dict
from sklearn.metrics import f1_score

from eval.evaluate import Evaluate


class EvaluateTrack3(Evaluate):
    @staticmethod
    def get_component_vector(sentence: str, begin_idx: Optional[List[int]], end_idx: Optional[List[int]]) -> List[int]:
        vector = [0 for _ in range(len(sentence))]
        if begin_idx is None or end_idx is None:
            return vector

        assert len(begin_idx) == len(end_idx)
        for i, (begin, end) in enumerate(zip(begin_idx, end_idx)):
            if begin is not None and end is not None:
                assert 0 <= begin <= end < len(sentence)
            else:
                assert (begin is None and end is None) or (begin is not None and end is not None)
            if begin is not None and end is not None:
                vector[begin:end+1] = [1 for _ in range(end - begin + 1)]

        return vector

    @staticmethod
    def calculate_f1_score(truth_list: List[List[int]], pred_list: List[List[int]]) -> float:
        f1 = 0.0
        for truth, pred in zip(truth_list, pred_list):
            f1 += f1_score(truth, pred, average='binary', zero_division=1.0)
        return f1 / len(truth_list)

    def get_vector(self, prediction: List[Dict[str, str]], key_name: str, sentence: str) -> List[int]:
        begin_idx = self.get_prediction(prediction, f'{key_name}BeginIdx')
        end_idx = self.get_prediction(prediction, f'{key_name}EndIdx')
        return self.get_component_vector(sentence, begin_idx, end_idx)

    def evaluate(self):
        pred_conjunction_list, pred_tenor_list, pred_vehicle_list = [], [], []
        truth_conjunction_list, truth_tenor_list, truth_vehicle_list = [], [], []

        for i, (pred, truth) in enumerate(zip(self.prediction, self.ground_truth)):
            assert pred['id'] == truth['id']
            assert pred['sentence'] == truth['sentence']

            pred_conjunction_list.append(self.get_vector(pred['prediction'], 'conjunction', pred['sentence']))
            pred_tenor_list.append(self.get_vector(pred['prediction'], 'tenor', pred['sentence']))
            pred_vehicle_list.append(self.get_vector(pred['prediction'], 'vehicle', pred['sentence']))
            truth_conjunction_list.append(self.get_vector(truth['prediction'], 'conjunction', truth['sentence']))
            truth_tenor_list.append(self.get_vector(truth['prediction'], 'tenor', truth['sentence']))
            truth_vehicle_list.append(self.get_vector(truth['prediction'], 'vehicle', truth['sentence']))

        conjunction_f1 = self.calculate_f1_score(truth_conjunction_list, pred_conjunction_list)
        tenor_f1 = self.calculate_f1_score(truth_tenor_list, pred_tenor_list)
        vehicle_f1 = self.calculate_f1_score(truth_vehicle_list, pred_vehicle_list)

        return (conjunction_f1 + tenor_f1 + vehicle_f1) / 3.0
