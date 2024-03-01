import argparse

from eval.eval_track1 import EvaluateTrack1
from eval.eval_track2 import EvaluateTrack2
from eval.eval_track3 import EvaluateTrack3


parser = argparse.ArgumentParser()
parser.add_argument('--track', type=int, choices=[1, 2, 3], required=True, help='Track number')
parser.add_argument('--prediction', type=str, required=True, help='Path to prediction file')
parser.add_argument('--truth', type=str, required=True, help='Path to ground truth file')
args = parser.parse_args()

if args.track == 1:
    evaluator = EvaluateTrack1(args.prediction, args.truth)
elif args.track == 2:
    evaluator = EvaluateTrack2(args.prediction, args.truth)
else:
    evaluator = EvaluateTrack3(args.prediction, args.truth)

if __name__ == '__main__':
    print(evaluator.evaluate())
