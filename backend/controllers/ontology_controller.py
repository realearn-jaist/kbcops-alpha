import os
import random
from owlready2 import *
from tqdm import tqdm
from collections import defaultdict

from models.extract_model import (
    load_annotations,
    load_axioms,
    load_classes,
    load_individuals,
    load_infer,
    save_annotations,
    save_axioms,
    save_classes,
    save_individuals,
    save_infer,
)
from models.ontology_model import (
    getPath_ontology_directory,
    list_ontology,
    save_ontology,
    getPath_ontology,
)

from owl2vec_star.Onto_Projection import Reasoner, OntologyProjection  # type: ignore
from owl2vec_star.Label import pre_process_words  # type: ignore


def upload_ontology(file, id):
    if id.endswith(".owl"):
        id = id[:-4]

    filename = id + ".owl"
    
    path = save_ontology(file, id, filename)

    return id if path else None

def getAll_ontology():
    return list_ontology()


def get_onto_stat(id):
    axioms = load_axioms(id)
    classes = load_classes(id)
    individuals = load_individuals(id)
    annotations = load_annotations(id)

    return {
        "no_class": len(classes),
        "no_individual": len(individuals),
        "no_axiom": len(axioms),
        "no_annotation": len(annotations),
    }


def get_all_superclasses(cls, cache):
    if cls in cache:
        return cache[cls]

    superclasses = []
    for sc in cls.is_a:
        if sc != owl.Thing:
            superclasses.append(sc)
            superclasses.extend(get_all_superclasses(sc, cache))

    cache[cls] = superclasses
    return superclasses


def abox_infer(onto):
    superclass_cache = defaultdict(list)
    results = []
    for ind in tqdm(onto.individuals(), desc="Processing individuals"):
        ind_uri = ind.iri
        inferred_classes = get_all_superclasses(ind, superclass_cache)
        inferred_classes = inferred_classes[1:]
        inferred_classes = [sc for sc in inferred_classes if sc not in ind.is_a]
        inferred_classes_str = ",".join(
            cls.iri for cls in inferred_classes if hasattr(cls, "iri")
        )
        if inferred_classes_str and not inferred_classes_str.endswith(","):
            inferred_classes_str += ","
        inferred_classes_str += "owl:Thing"
        results.append(f"{ind_uri},{inferred_classes_str}")
    return results


def tbox_infer(onto):
    superclass_cache = defaultdict(list)
    results = []
    for cls in tqdm(onto.classes(), desc="Processing classes"):
        cls_uri = cls.iri
        inferred_classes = get_all_superclasses(cls, superclass_cache)
        inferred_classes = inferred_classes[1:]
        inferred_classes = [sc for sc in inferred_classes if sc not in cls.is_a]
        inferred_classes_str = ",".join(
            cls.iri for cls in inferred_classes if hasattr(cls, "iri")
        )
        results.append(f"{cls_uri},{inferred_classes_str}")
    return results


def get_ground_truth(class_or_individuals):
    """Returns the ground truth of a class or individual"""
    immediate_superclasses = []
    for sc in class_or_individuals.is_a:
        if sc != owl.Thing:
            immediate_superclasses.append(sc)
    return immediate_superclasses


def train_test_val(class_or_individuals):
    """Splits the classes or individuals into train, test, and val sets."""
    train_proportion = 0.7
    test_proportion = 0.2

    print(f"Total classes/individuals: {len(class_or_individuals)}")
    train_size = int(train_proportion * len(class_or_individuals))
    test_size = int(test_proportion * len(class_or_individuals))
    val_size = len(class_or_individuals) - train_size - test_size
    print(f"Train size: {train_size}, Test size: {test_size}, Val size: {val_size}")

    train = class_or_individuals[:train_size]
    test = class_or_individuals[train_size : train_size + test_size]
    val = class_or_individuals[train_size + test_size :]
    return train, test, val


def writePositiveSamplesToCSV(csv_path, classes_or_individuals, id):
    """Writes the positive samples to a CSV file."""
    root = getPath_ontology_directory(id)
    with open(csv_path, "w") as f:
        for ind in classes_or_individuals:
            ind_ground_truth = get_ground_truth(ind)
            ind_uri = ind.iri
            ground_truth_list = [
                gt.iri for gt in ind_ground_truth if hasattr(gt, "iri")
            ]
            if csv_path == os.path.join(
                root, "train-infer-1.csv"
            ) or csv_path == os.path.join(root, "train-infer-0.csv"):
                for gt in ground_truth_list:
                    f.write(f"{ind_uri},{gt},1\n")
            else:
                for gt in ground_truth_list:
                    f.write(f"{ind_uri},{gt}\n")
        print(f"CSV created successfully at: {csv_path}")


def writeNegativeSamplesToCSV(csv_path, negative_samples):
    """Writes the negative samples to a CSV file."""
    with open(csv_path, "a") as f:
        for ind, negative_class, label in negative_samples:
            ind_uri = ind.iri
            f.write(f"{ind_uri},{negative_class},{label}\n")


def read_infer_classes(file):
    """
    Reads the infer_classes file and returns a dictionary mapping individuals to their inferred classes.
    """
    infer_dict = {}
    for line in file:
        parts = line.strip().split(",")
        individual_or_classes = parts[0]
        inferred_classes = parts[1:]
        inferred_classes = [cls for cls in inferred_classes if cls]
        infer_dict[individual_or_classes] = inferred_classes
    return infer_dict


def generate_negative_samples_abox(ontology, num_samples, infer_classes_path, label):
    """Generates negative samples for the ABox and returns them as a list."""
    all_individuals = list(ontology.individuals())
    infer_classes = read_infer_classes(infer_classes_path)
    negative_samples = []

    num_random_class_samples = num_samples // 2
    num_inferred_class_samples = num_samples - num_random_class_samples
    ind = random.choice(all_individuals)
    print(f"Number of random class samples: {num_random_class_samples}")
    print(f"Number of inferred class samples: {num_inferred_class_samples}")

    # if label == 1, then we need to generate negative samples for inferred incorrect classes more to make the dataset balanced
    if label == 1:
        num_random_class_samples += num_samples
        num_samples *= 2

    while len(negative_samples) < num_random_class_samples:
        ind = random.choice(all_individuals)
        all_classes = list(ontology.classes())
        negative_class = random.choice(all_classes)
        ind_classes_is_a = [cls.iri for cls in ind.is_a if hasattr(cls, "iri")]

        if (
            negative_class.iri not in ind_classes_is_a
            and negative_class.iri not in infer_classes[ind.iri]
        ):

            negative_samples.append((ind, negative_class.iri, 0))

    while len(negative_samples) < num_samples:
        ind = random.choice(all_individuals)
        all_classes = list(ontology.classes())
        negative_class_iri = random.choice(infer_classes[ind.iri])
        if negative_class_iri != "owl:Thing":
            negative_samples.append((ind, negative_class_iri, label))
    return negative_samples


def generate_negative_samples_tbox(ontology, num_samples, infer_classes_path, label):
    """Generates negative samples for the TBox and returns them as a list."""
    all_classes = list(ontology.classes())
    infer_classes = read_infer_classes(infer_classes_path)
    negative_samples = []

    num_random_class_samples = num_samples // 2
    # num_inferred_class_samples = num_samples - num_random_class_samples

    if label == 1:
        num_random_class_samples += num_samples
        num_samples *= 2

    while len(negative_samples) < num_random_class_samples:
        cls = random.choice(all_classes)
        all_classes = list(ontology.classes())
        negative_class = random.choice(all_classes)
        cls_classes_is_a = [cls.iri for cls in cls.is_a if hasattr(cls, "iri")]

        if (
            negative_class.iri not in cls_classes_is_a
            and negative_class.iri not in infer_classes[cls.iri]
        ):

            negative_samples.append((cls, negative_class.iri, 0))

    while len(negative_samples) < num_samples:
        cls = random.choice(all_classes)
        all_classes = list(ontology.classes())
        # handle case where there are no inferred classes
        # negative_class_iri = owl.Thing.iri
        if infer_classes[cls.iri] != []:
            negative_class_iri = random.choice(infer_classes[cls.iri])
            negative_samples.append((cls, negative_class_iri, label))
    return negative_samples


def train_test_val_abox(onto, id):
    """Main function for generating training, test, and validation sets for the ABox."""
    all_individuals = list(onto.individuals())
    train_individuals, test_individuals, val_individuals = train_test_val(
        all_individuals
    )

    root = getPath_ontology_directory(id)
    train_csv_path_0 = os.path.join(root, "train-infer-1.csv")
    train_csv_path_1 = os.path.join(root, "train-infer-0.csv")

    test_csv_path = os.path.join(root, "test.csv")
    val_csv_path = os.path.join(root, "val.csv")

    writePositiveSamplesToCSV(train_csv_path_0, train_individuals, id)
    writePositiveSamplesToCSV(train_csv_path_1, train_individuals, id)

    writePositiveSamplesToCSV(test_csv_path, test_individuals, id)
    writePositiveSamplesToCSV(val_csv_path, val_individuals, id)
    # i want to set seed to 0 so that the negative samples are the same for both infered classes to 0 and 1

    negative_samples = generate_negative_samples_abox(
        onto, len(train_individuals), load_infer(id), 1
    )
    writeNegativeSamplesToCSV(train_csv_path_0, negative_samples)

    negative_samples = generate_negative_samples_abox(
        onto, len(train_individuals), load_infer(id), 0
    )
    writeNegativeSamplesToCSV(train_csv_path_1, negative_samples)


def train_test_val_tbox(onto, id):
    """Main function for generating training, test, and validation sets for the TBox."""

    # split classes into train, test, and val
    all_classes = list(onto.classes())
    train_classes, test_classes, val_classes = train_test_val(all_classes)

    root = getPath_ontology_directory(id)
    train_csv_path_0 = os.path.join(root, "train-infer-1.csv")
    train_csv_path_1 = os.path.join(root, "train-infer-0.csv")

    test_csv_path = os.path.join(root, "test.csv")
    val_csv_path = os.path.join(root, "val.csv")

    # write positive samples to csv
    # train have 2 csv files, one for considering infered classes to 0 and one for 1
    writePositiveSamplesToCSV(train_csv_path_0, train_classes, id)
    writePositiveSamplesToCSV(train_csv_path_1, train_classes, id)

    # test and val have only 1 csv file
    writePositiveSamplesToCSV(test_csv_path, test_classes, id)
    writePositiveSamplesToCSV(val_csv_path, val_classes, id)

    # generate negative samples for considering infered classes to 1 and save to csv
    negative_samples = generate_negative_samples_tbox(
        onto, len(train_classes), load_infer(id), 1
    )
    writeNegativeSamplesToCSV(train_csv_path_0, negative_samples)

    # generate negative samples for considering infered classes to 0 and save to csv
    negative_samples = generate_negative_samples_tbox(
        onto, len(train_classes), load_infer(id), 0
    )
    writeNegativeSamplesToCSV(train_csv_path_1, negative_samples)


def extract_data(id):
    onto_file = getPath_ontology(id)

    # projection
    projection = OntologyProjection(
        onto_file,
        reasoner=Reasoner.STRUCTURAL,
        only_taxonomy=False,
        bidirectional_taxonomy=True,
        include_literals=True,
        avoid_properties=set(),
        additional_preferred_labels_annotations=set(),
        additional_synonyms_annotations=set(),
        memory_reasoner="13351",
    )

    # axioms
    projection.createManchesterSyntaxAxioms()
    axioms = projection.axioms_manchester

    # entities (classes and individuals)
    projection.extractEntityURIs()
    classes = projection.getClassURIs()
    individuals = projection.getIndividualURIs()
    entities = classes.union(individuals)

    # annotations
    projection.indexAnnotations()
    uri_label, annotations = dict(), list()
    for e in tqdm(entities, desc="Processing Preferred Labels"):
        if (
            e in projection.entityToPreferredLabels
            and len(projection.entityToPreferredLabels[e]) > 0
        ):
            label = list(projection.entityToPreferredLabels[e])[0]
            uri_label[e] = pre_process_words(words=label.split())
    for e in tqdm(entities, desc="Processing Lexical Labels"):
        if e in projection.entityToAllLexicalLabels:
            for v in projection.entityToAllLexicalLabels[e]:
                if (v is not None) and (
                    not (
                        e in projection.entityToPreferredLabels
                        and v in projection.entityToPreferredLabels[e]
                    )
                ):
                    annotation = [e] + v.split()
                    annotations.append(annotation)

    axioms = save_axioms(id, axioms)
    classes = save_classes(id, classes)
    individuals = save_individuals(id, individuals)
    annotations = save_annotations(id, annotations, projection)

    # extract axiom, entity, annotation
    onto = get_ontology(getPath_ontology(id)).load()

    sync_reasoner()

    tbox_results = tbox_infer(onto)
    abox_results = abox_infer(onto)

    save_infer(id, tbox_results + abox_results)
    # individuals = list(em.load_individuals(ontology)) # there is a error
    individuals = load_individuals(id)
    individuals_count = len(individuals)

    # classes = [line.strip() for line in load_classes(ontology)] # there is a error
    classes = load_classes(id)

    # check onto type
    # consider as a ABox iff individuals_count is excess 10 percent of classes amount
    onto_type = "ABox" if individuals_count > int(0.1 * len(classes)) else "TBox"
    if onto_type == "ABox":
        train_test_val_abox(onto, id)

    else:
        train_test_val_tbox(onto, id)
    return {
        "no_class": len(classes),
        "no_individual": len(individuals),
        "no_axiom": len(axioms),
        "no_annotation": len(annotations),
    }
