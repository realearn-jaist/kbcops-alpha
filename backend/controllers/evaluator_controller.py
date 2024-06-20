import numpy as np
import random
import os
import math

from tqdm import tqdm

from models.extract_model import (
    load_classes,
    load_individuals,
)
from controllers.graph_controller import create_graph
from models.evaluator_model import write_garbage_metrics, write_evaluate
from models.ontology_model import get_path_ontology_directory
from models.embed_model import load_embedding
from models.extract_model import load_classes
from owl2vec_star.Evaluator import Evaluator


def get_subfix(value):
    """Get the subfix of a string

    Args:
        value (str): The string to get the subfix of
    Returns:
        str: The subfix of the string
    """
    delimiter = "#" if "#" in value else "/"
    subfix = value.rsplit(delimiter, 1)[-1]
    return subfix


class InclusionEvaluator(Evaluator):
    def __init__(
        self,
        valid_samples,
        test_samples,
        train_X,
        train_y,
        classes,
        classes_e,
        individuals,
        individuals_e,
        inferred_ancestors,
        ontology,
        algorithm,
        onto_type,
    ):
        super(InclusionEvaluator, self).__init__(
            valid_samples, test_samples, train_X, train_y
        )
        self.inferred_ancestors = inferred_ancestors
        self.ontology = ontology
        self.classes = classes
        self.classes_e = classes_e
        self.individuals = individuals
        self.individuals_e = individuals_e
        self.algorithm = algorithm
        self.onto_type = onto_type
        self.result = dict()

    def evaluate(self, model, eva_samples):
        """Evaluate the model

        Args:
            model (object): The model to evaluate
            eva_samples (list): The list of samples to evaluate
        Returns:
            tuple: The evaluation metrics
        """
        print("start evaluate")
        candidate_num = len(self.classes)
        data = []  # garbage
        MRR_sum, hits1_sum, hits5_sum, hits10_sum = 0, 0, 0, 0
        nifMRR_sum, nifhits1_sum, nifhits5_sum, nifhits10_sum = 0, 0, 0, 0
        avgDLRank, avgRank, DLcount = 0, 0, 0

        # test sample
        progress_bar = tqdm(eva_samples, desc="Evaluating Samples")
        for k, sample in enumerate(progress_bar):
            sub, gt = sample[0], sample[1]
            sub_v = None
            if self.onto_type == "TBox":
                sub_index = self.classes.index(sub)
                sub_v = self.classes_e[sub_index]
            else:
                sub_index = self.individuals.index(sub)
                sub_v = self.individuals_e[sub_index]
            X = np.concatenate(
                (np.array([sub_v] * candidate_num), self.classes_e), axis=1
            )
            P = model.predict_proba(X)[:, 1]
            sorted_indexes = np.argsort(P)[::-1]
            score = [P[x] for x in sorted_indexes]

            sorted_classes = list()
            sorted_classes_non = list()

            for j in sorted_indexes:
                sorted_classes_non.append(self.classes[j])
                if self.classes[j] not in self.inferred_ancestors[sub]:
                    sorted_classes.append(self.classes[j])

            rank = sorted_classes.index(gt) + 1
            rank_non = sorted_classes_non.index(gt) + 1

            if rank_non > rank:
                unique_class = list(
                    set(sorted_classes_non[:rank_non]).symmetric_difference(
                        set(sorted_classes[:rank])
                    )
                )
                unique_class_sort = sorted(
                    [(x, sorted_classes_non.index(x) + 1) for x in unique_class],
                    key=lambda pair: pair[1],
                )
                predicted_inf = f"{unique_class_sort[0][0].split(('/'))[-1]}"
                predicted_inf_rank = unique_class_sort[0][1]
                avgRank += rank_non
                avgDLRank += predicted_inf_rank
                DLcount += 1
                data.append(
                    {
                        "Individual": get_subfix(sub),
                        "Predicted": get_subfix(predicted_inf),
                        "Predicted_rank": predicted_inf_rank,
                        "True": get_subfix(sorted_classes_non[rank_non - 1]),
                        "True_rank": rank_non,
                        "Score_predict": score[predicted_inf_rank - 1],
                        "Score_true": score[rank_non - 1],
                        "Dif": rank_non - predicted_inf_rank,
                    }
                )

            MRR_sum += 1.0 / rank
            hits1_sum += 1 if gt in sorted_classes[:1] else 0
            hits5_sum += 1 if gt in sorted_classes[:5] else 0
            hits10_sum += 1 if gt in sorted_classes[:10] else 0
            num = k + 1

            progress_bar.set_postfix(
                MRR=MRR_sum / num,
                Hits1=hits1_sum / num,
                Hits5=hits5_sum / num,
                Hits10=hits10_sum / num,
            )

            nifMRR_sum += 1.0 / rank
            nifhits1_sum += 1 if gt in sorted_classes[:1] else 0
            nifhits5_sum += 1 if gt in sorted_classes[:5] else 0
            nifhits10_sum += 1 if gt in sorted_classes[:10] else 0

        data = sorted([x for x in data], key=lambda x: x["Dif"], reverse=True)
        garbage_data = data[:5] if len(data) >= 5 else data
        write_garbage_metrics(self.ontology, self.algorithm, garbage_data)

        eva_n = len(eva_samples)
        e_MRR, hits1, hits5, hits10 = (
            MRR_sum / eva_n,
            hits1_sum / eva_n,
            hits5_sum / eva_n,
            hits10_sum / eva_n,
        )
        nife_MRR, nifhits1, nifhits5, nifhits10 = (
            nifMRR_sum / eva_n,
            nifhits1_sum / eva_n,
            nifhits5_sum / eva_n,
            nifhits10_sum / eva_n,
        )

        print(
            "Testing (No inference checking), MRR: %.3f, Hits@1: %.3f, Hits@5: %.3f, Hits@10: %.3f\n\n"
            % (nife_MRR, nifhits1, nifhits5, nifhits10)
        )
        avgDLRank = math.ceil(avgDLRank / DLcount)
        avgRank = math.ceil(avgRank / DLcount)
        print(f"""count:{DLcount}, DL:{avgDLRank}, ground:{avgRank}\n""")

        performance_data = {
            "mrr": e_MRR,
            "hit_at_1": hits1,
            "hit_at_5": hits5,
            "hit_at_10": hits10,
            "garbage": DLcount,
        }

        write_evaluate(self.ontology, self.algorithm, performance_data)

        self.result = {
            "message": "evaluate successful!",
            "performance": performance_data,
            "garbage": garbage_data,
        }

        return (
            performance_data.get("mrr"),
            performance_data.get("hit_at_1"),
            performance_data.get("hit_at_5"),
            performance_data.get("hit_at_10"),
        )


def predict_func(ontology, algorithm):
    """Predict the ontology with the algorithm

    Args:
        ontology (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        dict: The result of the prediction
    """
    # load individuals
    individuals = load_individuals(ontology)
    individuals_count = len(individuals)

    # load classes file
    print(f"load {ontology} classes")
    classes = load_classes(ontology)

    onto_type = "ABox" if individuals_count > int(0.1 * len(classes)) else "TBox"

    # embed class with model
    print(f"embedding {ontology} classes")
    classes_e, individuals_e = load_embedding(ontology, algorithm)

    # load train test val file
    print(f"load {ontology} train/test/validate")

    file_path = get_path_ontology_directory(ontology)

    train_path = os.path.join(file_path, "train-infer-0.csv")
    valid_path = os.path.join(file_path, "valid.csv")
    test_path = os.path.join(file_path, "test.csv")

    train_samples = [line.strip().split(",") for line in open(train_path).readlines()]
    valid_samples = [line.strip().split(",") for line in open(valid_path).readlines()]
    test_samples = [line.strip().split(",") for line in open(test_path).readlines()]
    random.shuffle(train_samples)

    # split value in file
    train_x_list, train_y_list = list(), list()
    for s in train_samples:
        # when it come to ABox sub will consider as a individual and sup consider as a class
        sub, sup, label = s[0], s[1], s[2]
        sub_v = None
        if onto_type == "TBox":
            sub_v = classes_e[classes.index(sub)]
        else:
            sub_v = individuals_e[individuals.index(sub)]
        sup_v = classes_e[classes.index(sup)]
        if not (np.all(sub_v == 0) or np.all(sup_v == 0)):
            train_x_list.append(np.concatenate((sub_v, sup_v)))
            train_y_list.append(int(label))
    train_X, train_y = np.array(train_x_list), np.array(train_y_list)
    print("train_X: %s, train_y: %s" % (str(train_X.shape), str(train_y.shape)))

    # load infer file
    print(f"load {ontology} inferences")
    inferred_ancestors = dict()
    infer_path = os.path.join(
        get_path_ontology_directory(ontology), "inferred_ancestors.txt"
    )
    with open(infer_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            all_infer_classes = line.strip().split(",")
            cls = all_infer_classes[0]
            inferred_ancestors[cls] = (
                all_infer_classes if onto_type == "TBox" else all_infer_classes[1:]
            )

    # evaluate
    print(f"evaluate {ontology} with {algorithm} embedding algorithm on random forest")
    evaluate = InclusionEvaluator(
        valid_samples,
        test_samples,
        train_X,
        train_y,
        classes,
        classes_e,
        individuals,
        individuals_e,
        inferred_ancestors,
        ontology,
        algorithm,
        onto_type,
    )
    evaluate.run_random_forest()

    # load image
    evaluate.result["images"] = create_graph(ontology, algorithm)

    return evaluate.result
