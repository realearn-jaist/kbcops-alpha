from sklearn.ensemble import RandomForestClassifier
import numpy as np
import random
import gensim
import configparser
import os
import csv
import math

from owl2vec_star.Evaluator import Evaluator
from owl2vec_star.RDF2Vec_Embed import get_rdf2vec_walks

class InclusionEvaluator(Evaluator):
    def __init__(self, valid_samples, test_samples, train_X, train_y):
        super(InclusionEvaluator, self).__init__(valid_samples, test_samples, train_X, train_y)

    def evaluate(self, model, eva_samples, classes, classes_e, inferred_ancestors, ontology_file):
        candidate_num = len(classes)
        data = []
        MRR_sum, hits1_sum, hits5_sum, hits10_sum = 0, 0, 0, 0
        nifMRR_sum, nifhits1_sum, nifhits5_sum, nifhits10_sum = 0, 0, 0, 0
        avgDLRank, avgRank, DLcount = 0,0,0
        for k, sample in enumerate(eva_samples):
            sub, gt = sample[0], sample[1]
            sub_index = classes.index(sub)
            sub_v = classes_e[sub_index]
            X = np.concatenate((np.array([sub_v] * candidate_num), classes_e), axis=1)
            P = model.predict_proba(X)[:, 1]
            sorted_indexes = np.argsort(P)[::-1]
            score = [P[x] for x in sorted_indexes]
            sorted_classes = list()
            sorted_classes_non = list()
            for j in sorted_indexes:
                sorted_classes_non.append(classes[j])
                if classes[j] not in inferred_ancestors[sub]:
                    sorted_classes.append(classes[j])
            
            rank = sorted_classes.index(gt) + 1
            rank_non = sorted_classes_non.index(gt) + 1
            if rank_non > rank:
                csv_file_path = f'backend\storage\{ontology_file}\{ontology_file}_garbage.csv'
                unique_class = list(set(sorted_classes_non[:rank_non]).symmetric_difference(set(sorted_classes[:rank])))
                unique_class_sort = sorted([(x, sorted_classes_non.index(x)+1) for x in unique_class], key=lambda pair: pair[1])
                predicted_inf = f"{unique_class_sort[0][0].split(('/'))[-1]}"
                predicted_inf_rank = unique_class_sort[0][1]
                avgRank += rank_non
                avgDLRank += predicted_inf_rank
                DLcount += 1
                data.append({'Individual': sub.split(('/'))[-1], 'Predicted': predicted_inf, 'Predicted_rank': predicted_inf_rank, 'True': sorted_classes_non[rank_non-1].split(('/'))[-1], "True_rank" : rank_non, 'Score_predict': score[predicted_inf_rank-1], 'Score_true': score[rank_non-1], 'Dif' : rank_non - predicted_inf_rank})

            MRR_sum += 1.0 / rank
            hits1_sum += 1 if gt in sorted_classes[:1] else 0
            hits5_sum += 1 if gt in sorted_classes[:5] else 0
            hits10_sum += 1 if gt in sorted_classes[:10] else 0
            num = k + 1

            if num % 5 == 0:
                print('\n%d tested, MRR: %.4f, Hits@1: %.4f, Hits@5: %.4f, Hits@10: %.4f\n' %
                      (num, MRR_sum/num, hits1_sum/num, hits5_sum/num, hits10_sum/num))
                     
            nifMRR_sum += 1.0 / rank
            nifhits1_sum += 1 if gt in sorted_classes[:1] else 0
            nifhits5_sum += 1 if gt in sorted_classes[:5] else 0
            nifhits10_sum += 1 if gt in sorted_classes[:10] else 0

        data = sorted([x for x in data], key=lambda x: x['Dif'], reverse=True)
        data = data[:10] if len(data) >= 10 else data
        if not os.path.isfile(csv_file_path):
            with open(csv_file_path, 'w', newline='') as csv_file:
                column_names = list(data[0].keys())
                csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
                csv_writer.writeheader()
                print(f'File {csv_file_path} created.')
        with open(csv_file_path, 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
            csv_writer.writerows(data)
        eva_n = len(eva_samples)
        e_MRR, hits1, hits5, hits10 = MRR_sum / eva_n, hits1_sum / eva_n, hits5_sum / eva_n, hits10_sum / eva_n
        nife_MRR, nifhits1, nifhits5, nifhits10 = nifMRR_sum / eva_n, nifhits1_sum / eva_n, nifhits5_sum / eva_n, nifhits10_sum / eva_n
        
        print('Testing (No inference checking), MRR: %.3f, Hits@1: %.3f, Hits@5: %.3f, Hits@10: %.3f\n\n' % (nife_MRR, nifhits1, nifhits5, nifhits10))
        print("OWL2VECSTAR")
        avgDLRank = math.ceil(avgDLRank/DLcount)
        avgRank = math.ceil(avgRank/DLcount)
        print(f"""\nOWL2VecStar\ncount:{DLcount}, DL:{avgDLRank}, ground:{avgRank}\n""")
        return e_MRR, hits1, hits5, hits10, DLcount

    def run_random_forest(self, classes, classes_e, inferred_ancestors):
        rf = RandomForestClassifier(n_estimators=200)
        rf.fit(self.train_X, self.train_y)
        rf_best = rf
        MRR, hits1, hits5, hits10 = self.evaluate(model=rf_best, eva_samples=self.test_samples, 
                                                  classes=classes, classes_e=classes_e, 
                                                  inferred_ancestors=inferred_ancestors, ontology_file=ontology_file)
        print('Testing, MRR: %.3f, Hits@1: %.3f, Hits@5: %.3f, Hits@10: %.3f\n\n' % (MRR, hits1, hits5, hits10))

def embed(model, instances):
    feature_vectors = []
    for instance in instances:
        v_uri = model.wv.get_vector(instance) if instance in model.wv.index_to_key else np.zeros(model.vector_size)
        feature_vectors.append(v_uri)

    return feature_vectors

def predict_func(ontology_file, model_id):
    # load config file
    config_file = "backend\controllers\default.cfg"
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # load classes file
    class_file_path = f'backend\storage\{ontology_file}\classes.txt'
    classes = [line.strip() for line in open(class_file_path).readlines()]
    
    # load axiom file
    walk_sentences, axiom_sentences = list(), list()
    axiom_file_path = f'backend\storage\{ontology_file}\\axioms.txt'
    for line in open(axiom_file_path).readlines():
        axiom_sentence = [item for item in line.strip().split()]
        axiom_sentences.append(axiom_sentence)
    print('Extracted %d axiom sentences' % len(axiom_sentences))

    # load onto file
    ontology_file_path = f'backend\storage\\{ontology_file}\\{ontology_file}.owl'

    walks_ = get_rdf2vec_walks(onto_file=ontology_file_path, walker_type=config["MODEL_RDF2VEC"]["walker"],
                               walk_depth=int(config["MODEL_RDF2VEC"]["walk_depth"]), classes=classes)
                               
    print('Extracted {} walks for {} classes!'.format(len(walks_), len(classes)))
    walk_sentences += [list(map(str, x)) for x in walks_]

    URI_Doc = walk_sentences + axiom_sentences
    random.shuffle(URI_Doc)

    #loading algorithm
    model_path = f'backend\storage\\{ontology_file}\\{model_id}'
    model_ = gensim.models.Word2Vec.load(model_path)
    if len(URI_Doc) > 0:
        model_.min_count = 1
        model_.build_vocab(URI_Doc, update=True)
        model_.train(URI_Doc, total_examples=model_.corpus_count, epochs=100)
    
    classes_e = embed(model=model_, instances=classes)
    
    # load train test val file
    file_path = f'backend\storage\\{ontology_file}\\'
    train_samples = [line.strip().split(',') for line in open(file_path + 'train.csv').readlines()]
    valid_samples = [line.strip().split(',') for line in open(file_path + 'valid.csv').readlines()]
    test_samples = [line.strip().split(',') for line in open(file_path + 'test.csv').readlines()]
    random.shuffle(train_samples)
    
    train_x_list, train_y_list = list(), list()
    for s in train_samples:
        sub, sup, label = s[0], s[1], s[2]
        sub_v = classes_e[classes.index(sub)]
        sup_v = classes_e[classes.index(sup)]
        if not (np.all(sub_v == 0) or np.all(sup_v == 0)):
            train_x_list.append(np.concatenate((sub_v, sup_v)))
            train_y_list.append(int(label))
    train_X, train_y = np.array(train_x_list), np.array(train_y_list)
    print('train_X: %s, train_y: %s' % (str(train_X.shape), str(train_y.shape)))

    inferred_ancestors = dict()
    with open(f'backend\storage\\{ontology_file}\\inferred_ancestors.txt') as f:
        for line in f.readlines():
            all_infer_classes = line.strip().split(',')
            cls = all_infer_classes[0]
            inferred_ancestors[cls] = all_infer_classes

    # evaluate
    evaluate = InclusionEvaluator(valid_samples, test_samples, train_X, train_y)
    e_MRR, hits1, hits5, hits10, DLcount = evaluate.run_random_forest(classes, classes_e, inferred_ancestors, ontology_file)
    
    performance_csv_file_path = f'backend\storage\\{ontology_file}\\performance.txt'
    
    if not os.path.isfile(performance_csv_file_path):
        with open(performance_csv_file_path, 'w', newline='') as csv_file:
            column_names = list(data[0].keys())
            csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
            csv_writer.writeheader()
            print(f'File {csv_file_path} created.')
    
    return {
        "mrr": e_MRR, 
        "hit_at_1": hits1,
        "hit_at_5": hits5, 
        "hit_at_10": hits10, 
        "garbage": DLcount
    }