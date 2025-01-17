import torch.nn.functional as F

from . import BaseTask, register_task
from ..dataset import build_dataset
from ..utils import Evaluator


@register_task("recommendation")
class Recommendation(BaseTask):
    """Recommendation tasks."""
    def __init__(self, args):
        super(Recommendation, self).__init__()
        self.n_dataset = args.dataset
        self.dataset = build_dataset(args.dataset, 'recommendation')
        # self.evaluator = Evaluator()
        self.train_hg, self.val_hg, self.test_hg = self.dataset.get_idx()
        self.evaluator = Evaluator(args.seed)

    def get_graph(self):
        return self.dataset.g

    def get_loss_fn(self):
        return F.binary_cross_entropy_with_logits

    def get_evaluator(self, name):
        if name == 'acc':
            return self.evaluator.author_link_prediction
        elif name == 'mrr':
            return self.evaluator.mrr_
        elif name == 'academic_lp':
            return self.evaluator.author_link_prediction

    def evaluate(self, y_true, y_score, name):
        if name == 'ndcg':
            return self.evaluator.ndcg(y_true, y_score)

    def get_idx(self):
        return self.train_hg, self.val_hg, self.test_hg

    def get_labels(self):
        return self.dataset.get_labels()

