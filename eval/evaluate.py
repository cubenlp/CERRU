import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class Evaluate(ABC):
    RHETORIC = ['比喻', '比拟', '夸张', '排比']
    FORM = [
        '明喻', '暗喻', '借喻',
        '名词', '动词', '形容词', '副词',
        '直接夸张', '间接夸张', '融合夸张',
        '成分排比', '句子排比'
    ]
    CONTENT = [
        '实在物', '动作', '抽象概念',
        '拟人', '拟物',
        '扩大夸张', '缩小夸张', '超前夸张',
        '并列', '承接', '递进'
    ]

    def __init__(self, prediction_filepath: str, ground_truth_filepath: str = '/path/to/ground_truth.json'):
        self.prediction_filepath = prediction_filepath
        self.ground_truth_filepath = ground_truth_filepath

        self.prediction = self.load_json(self.prediction_filepath)
        self.ground_truth = self.load_json(self.ground_truth_filepath)

    @staticmethod
    def load_json(filepath: str):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def map_labels_to_vector(labels: List[str], label_list: List[str]) -> List[int]:
        vector = [0 for _ in range(len(label_list))]
        if labels is None:
            vector[-1] = 1
            return vector

        for label in labels:
            vector[label_list.index(label)] = 1
        return vector

    @staticmethod
    def get_prediction(prediction: List[Dict[str, str]], key_name: str) -> Optional[List[str]]:
        return [item[key_name] for item in prediction] if prediction is not None else None

    @abstractmethod
    def evaluate(self):
        raise NotImplementedError
