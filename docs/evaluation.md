# 使用eval

我们提供了一个模块`eval`和一些测试样例`test_examples/`用于演示如何评测你的结果以及最终提交评测结果的文件格式。

## 文件格式

详细的文件格式可以参考目录`test_examples/`中的文件，`prediction.json`即最终提交的评测结果。

Track1和Track2类似，需要包括`id`（对应测试集中的`id`）、`sentence`（对应测试集中的`sentence`）和`prediction`表示你的预测结果。

其中，Track1的`prediction`包括`rhetorical`和`form`两个字段，分别表示修辞粗粒度分类和形式细粒度分类。Track2的`prediction`包括`rhetorical`和`content`两个字段，分别表示修辞粗粒度分类和内容细粒度分类。

请注意，如果该句包括多种修辞手法，需要全部在`prediction`字段中列出；如果该句不包括任何修辞手法，则`prediction`字段应当置空（`null`）。

下面是Track1的一个例子，Track2的例子请参考`test_examples/track2/prediction.json`

```json
[
  {
    "id": 1,
    "sentence": "这是第一个测试样例，用于测试track1的评测。",
    "prediction": [
      {
        "rhetorical": "比喻",
        "form": "明喻"
      }
    ]
  },
  {
    "id": 2,
    "sentence": "这是第二个测试样例，用于测试track1的评测。",
    "prediction": null
  }
]
```

对于Track3，`id`和`sentence`同上，`prediction`字段包括`conjunctionBeginIdx`、`conjunctionEndIdx`、`tenorBeginIdx`、`tenorEndIdx`、`vehicleBeginIdx`和`vehicleEndIdx`六个字段，分别表示连接词的起始和结束位置、描写对象的起始和结束位置、描写内容的起始和结束位置。

请注意，如果该句包括多个修辞成分，需要全部在`prediction`字段中列出；如果该句不包括任何修辞成分，则`prediction`字段应当置空（`null`）。

```json
[
  {
    "id": 1,
    "sentence": "这是第一个测试样例，用于测试track3的评测。",
    "prediction": [
      {
        "conjunctionBeginIdx": 1,
        "conjunctionEndIdx": 2,
        "tenorBeginIdx": null,
        "tenorEndIdx": null,
        "vehicleBeginIdx": 5,
        "vehicleEndIdx": 8
      }
    ]
  },
  {
    "id": 2,
    "sentence": "这是第二个测试样例，用于测试track3的评测。",
    "prediction": null
  }
]
```

## eval使用方法

`eval`模块提供一个命令行工具来评测结果，使用方法如下：

```bash
python -m eval --track 1 --prediction test_examples/track1/prediction.json --truth test_examples/track1/ground_truth.json
```

- `--track`参数指定评测任务的赛道，可选值为`1`、`2`和`3`
- `--prediction`参数指定你的预测结果文件
- `--truth`参数指定真实结果的文件

此外，`eval`也可以作为一个模块直接在代码中使用：

```python
from eval.eval_track1 import EvaluateTrack1

prediction_file_path = 'test_examples/track1/prediction.json'
ground_truth_file_path = 'test_examples/track1/ground_truth.json'

evaluator = EvaluateTrack1(prediction_file_path, ground_truth_file_path)
f1 = evaluator.evaluate()
```