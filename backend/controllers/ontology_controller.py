import os
import random
from owlready2 import *
from tqdm import tqdm
from collections import defaultdict

from models.extract_model import (
    load_input_file,
    load_multi_input_files,
    save_annotations,
    save_axioms,
    save_classes,
    save_individuals,
    save_infer,
)
from models.ontology_model import (
    list_ontology,
    save_ontology,
)

from owl2vec_star.Onto_Projection import Reasoner, OntologyProjection
from owl2vec_star.Label import pre_process_words
from utils.directory_utils import get_path
from utils.exceptions import ExtractionException, FileException, OntologyException


def upload_ontology(file, ontology_name: str):
    """Upload ontology file to the server and save it to the database

    Args:
        file (File): The ontology file to upload
        ontology_name (str): The name of the ontology
    Returns:
        ontology_name (str): The name of the ontology that was saved
    """
    # Remove file extension if it exists
    if ontology_name.endswith(".owl"):
        ontology_name = ontology_name[:-4]

    filename = ontology_name + ".owl"

    path = save_ontology(file, ontology_name, filename)

    if not path:
        raise OntologyException("Failed to save ontology file")

    return ontology_name


def get_all_ontology():
    """Get all ontology in the database

    Returns:
        list: The list of ontology in the database
    """
    # Get all ontology in the database
    return list_ontology()


def get_onto_stat(ontology_name: str):
    """Get the statistics of the ontology

    Args:
        ontology_name (str): The name of the ontology
    Returns:
        dict: The statistics of the ontology
    """
    # Get the statistics of the ontology
    files_list = ["axioms", "classes", "individuals", "uri_labels", "annotations"]
    files = load_multi_input_files(ontology_name, files_list)

    return {
        "no_class": len(files["classes"]),
        "no_individual": len(files["individuals"]),
        "no_axiom": len(files["axioms"]),
        "no_annotation": len(files["uri_labels"] + files["annotations"]),
    }


## Refactor code from https://github.com/KRR-Oxford/OWL2Vec-Star/blob/master/OWL2Vec_Standalone.py  ###########
###############################################################################################################


def extract_data(ontology_name: str):
    """Extract data from the ontology file

    Args:
        ontology_name (str): The name of the ontology
    Returns:
        dict: The statistics of the ontology
    """
    try:
        onto_file_path = get_path(ontology_name, ontology_name + ".owl")

        # extract axiom, entity, annotation
        projection = OntologyProjection(
            onto_file_path,
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

        # save to files
        axioms = save_axioms(ontology_name, axioms)
        classes = save_classes(ontology_name, classes)
        individuals = save_individuals(ontology_name, individuals)
        annotations = save_annotations(ontology_name, annotations, projection)

        # extract axiom, entity, annotation
        world = World()
        onto = world.get_ontology(
            get_path(ontology_name, ontology_name + ".owl")
        ).load()

        print("start run sync reasoner")
        start_time = time.time()
        # run hermit reasoner
        sync_reasoner(onto)
        print(
            f"sync reasoner time usage for {ontology_name}:", time.time() - start_time
        )

        tbox_results = tbox_infer(onto)
        abox_results = abox_infer(onto)

        # save inferred classes to file
        save_infer(ontology_name, tbox_results + abox_results)

        files_list = ["classes", "individuals"]
        files = load_multi_input_files(ontology_name, files_list)

        individuals_count = len(files["individuals"])

        # check ontology type
        # consider as an ABox if individuals_count exceeds 10 percent of classes amount
        onto_type = (
            "abox" if individuals_count > int(0.1 * len(files["classes"])) else "tbox"
        )
        if onto_type == "abox":
            train_test_val_gen_abox(onto, ontology_name)
        else:
            train_test_val_gen_tbox(onto, ontology_name)

        return {
            "no_class": len(files["classes"]),
            "no_individual": len(files["individuals"]),
            "no_axiom": len(axioms),
            "no_annotation": len(annotations),
        }

    except FileNotFoundError as e:

        raise FileException(f"File not found: {e}", 404)

    except Exception as e:

        raise ExtractionException(f"Error extracting data: {e}")


##############################################################################################################
##############################################################################################################


def get_all_superclasses(cls, cache: dict):
    """Returns all superclasses of a class

    Args:
        cls (Class): The class to get the superclasses of
        cache (dict): A dictionary to store the superclasses
    Returns:
        list: The list of superclasses of the class
    """
    try:
        # Check if the superclasses are already in the cache
        if cls in cache:
            return cache[cls]

        # Get all superclasses of the class
        superclasses = []
        for sc in cls.is_a:
            if sc != owl.Thing:
                superclasses.append(sc)
                superclasses.extend(get_all_superclasses(sc, cache))

        cache[cls] = superclasses
        return superclasses

    except Exception as e:
        raise ExtractionException(f"Error retrieving superclasses for {cls}: {e}")


def abox_infer(onto: Ontology):
    """Infer the classes of the individuals in the abox

    Args:
        onto (Ontology): The ontology to infer the classes from
    Returns:
        list: The list of inferred classes of the individuals in the abox
    """
    superclass_cache = defaultdict(list)
    results = []

    try:
        # get all inferred classes of the individuals
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
    except Exception as e:
        raise ExtractionException(f"Error inferring classes in ABox: {e}")

    return results


def tbox_infer(onto: Ontology):
    """Infer the classes of the classes in the tbox

    Args:
        onto (Ontology): The ontology to infer the classes from
    Returns:
        list: The list of inferred classes of the classes in the tbox
    """
    superclass_cache = defaultdict(list)
    results = []

    try:
        # get all inferred classes of the classes
        for cls in tqdm(onto.classes(), desc="Processing classes"):
            cls_uri = cls.iri
            inferred_classes = get_all_superclasses(cls, superclass_cache)
            inferred_classes = inferred_classes[1:]
            inferred_classes = [sc for sc in inferred_classes if sc not in cls.is_a]
            inferred_classes_str = ",".join(
                cls.iri for cls in inferred_classes if hasattr(cls, "iri")
            )
            results.append(f"{cls_uri},{inferred_classes_str}")
    except Exception as e:
        raise ExtractionException(f"Error inferring classes in TBox: {e}")

    return results


def get_ground_truth(class_or_individuals):
    """Returns the ground truth of a class or individual

    Args:
        class_or_individuals (Class/Individual): The class or individual to get the ground truth of
    Returns:
        list: The list of ground truth of the class or individual
    """
    try:
        # get the ground truth of the class or individual
        immediate_superclasses = []
        for sc in class_or_individuals.is_a:
            if sc != owl.Thing:
                immediate_superclasses.append(sc)
        return immediate_superclasses
    except AttributeError as e:
        raise ExtractionException(f"Error getting ground truth: {e}")
    except Exception as e:
        raise ExtractionException(f"Unexpected error getting ground truth: {e}")


def train_test_val(class_or_individuals: list):
    """Splits the classes or individuals into train, test, and val sets.

    Args:
        class_or_individuals (list): The list of classes or individuals
    Returns:
        tuple: The train, test, and val sets of the classes or individuals
    """
    try:
        if not isinstance(class_or_individuals, list):
            raise OntologyException("Input must be a list of classes or individuals")

        if len(class_or_individuals) == 0:
            raise OntologyException("Empty list provided")

        # Split the classes or individuals into train, test, and val sets
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

    except TypeError as e:
        raise ExtractionException(f"TypeError in train_test_val: {e}")
    except ValueError as e:
        raise ExtractionException(f"ValueError in train_test_val: {e}")
    except Exception as e:
        raise ExtractionException(f"Unexpected error in train_test_val: {e}")


def write_positive_samples_to_csv(
    csv_path: str, classes_or_individuals: list, ontology_name: str
):
    """Writes the positive samples to a CSV file.

    Args:
        csv_path (str): The path to the CSV file
        classes_or_individuals (list): The list of classes or individuals
        ontology_name (str): The name of the ontology
    Returns:
        None
    """
    try:
        root = get_path(ontology_name)

        # Check if csv_path is writable
        if not os.access(os.path.dirname(csv_path), os.W_OK):
            raise FileException(f"Cannot write to {csv_path}. Permission denied.")

        # Write the positive samples to the CSV file
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

    except IOError as e:
        raise FileException(f"IOError: {e}")
    except Exception as e:
        raise ExtractionException(f"Unexpected error: {e}")


def write_negative_samples_to_csv(csv_path: str, negative_samples: list):
    """Writes the negative samples to a CSV file.

    Args:
        csv_path (str): The path to the CSV file
        negative_samples (list): The list of negative samples
    Returns:
        None
    """
    try:
        # write the negative samples to the CSV file
        with open(csv_path, "a") as f:
            for ind, negative_class, label in negative_samples:
                ind_uri = ind.iri
                f.write(f"{ind_uri},{negative_class},{label}\n")
        print(f"Negative samples appended successfully to: {csv_path}")

    except IOError as e:
        raise FileException(f"IOError: {e}")
    except Exception as e:
        raise ExtractionException(f"Unexpected error: {e}")


def read_infer_classes(file):
    """
    Reads the infer_classes file and returns a dictionary mapping individuals/classes to their inferred classes.

    Args:
        file (File): The infer_classes file
    Returns:
        dict: The dictionary mapping cls/ind to their inferred classes
    """
    infer_dict = {}
    try:
        for line in file:
            parts = line.strip().split(",")
            individual_or_classes = parts[0]
            inferred_classes = parts[1:]
            inferred_classes = [cls for cls in inferred_classes if cls]
            infer_dict[individual_or_classes] = inferred_classes
        return infer_dict
    except IOError as e:
        raise IOError(f"Error reading file 'inferred_ancestors.txt': {e}")
    except IndexError as e:
        raise ValueError(
            f"Error parsing line in file 'inferred_ancestors.txt': {e}. Check file format."
        )
    except Exception as e:
        raise Exception(f"Unexpected error reading file 'inferred_ancestors.txt': {e}")


def generate_negative_samples_abox(
    onto: Ontology, num_samples: int, infer_classes_path, label: int
):
    """Generates negative samples for the abox and returns them as a list.

    Args:
        onto (Ontology): The ontology to generate the negative samples from
        num_samples (int): The number of negative samples to generate
        infer_classes_path (File): The path to the infer_classes file
        label (int): The label for the negative samples
    Returns:
        list: The list of negative samples
    """
    try:
        all_individuals = list(onto.individuals())
        infer_classes = read_infer_classes(infer_classes_path)
        negative_samples = []

        num_random_class_samples = num_samples // 2
        num_inferred_class_samples = num_samples - num_random_class_samples

        print(f"Number of random class samples: {num_random_class_samples}")
        print(f"Number of inferred class samples: {num_inferred_class_samples}")

        # If label == 1, then we need to generate negative samples for inferred incorrect classes more to make the dataset balanced
        if label == 1:
            num_random_class_samples += num_samples
            num_samples *= 2

        with tqdm(
            total=num_random_class_samples, desc="Generating random class samples"
        ) as pbar1:
            while len(negative_samples) < num_random_class_samples:
                ind = random.choice(all_individuals)
                all_classes = list(onto.classes())
                negative_class = random.choice(all_classes)
                ind_classes_is_a = [cls.iri for cls in ind.is_a if hasattr(cls, "iri")]

                if (
                    negative_class.iri not in ind_classes_is_a
                    and negative_class.iri not in infer_classes.get(ind.iri, [])
                ):
                    negative_samples.append((ind, negative_class.iri, 0))
                    pbar1.update(1)

        with tqdm(
            total=num_inferred_class_samples, desc="Generating inferred class samples"
        ) as pbar2:
            while len(negative_samples) < num_samples:
                ind = random.choice(all_individuals)
                all_classes = list(onto.classes())
                negative_class_iri = random.choice(infer_classes.get(ind.iri, []))
                if negative_class_iri != "owl:Thing":
                    negative_samples.append((ind, negative_class_iri, label))
                    pbar2.update(1)

        return negative_samples

    except IOError as e:
        raise FileException(f"IOError: {e}")
    except KeyError as e:
        raise ExtractionException(f"KeyError: {e}")
    except Exception as e:
        raise ExtractionException(f"Unexpected error: {e}")


def generate_negative_samples_tbox(onto, num_samples, infer_classes_list, label):
    """Generates negative samples for the tbox and returns them as a list.

    Args:
        onto (Ontology): The ontology to generate the negative samples from
        num_samples (int): The number of negative samples to generate
        infer_classes_list (list): The path to the infer_classes file
        label (int): The label for the negative samples
    Returns:
        list: The list of negative samples
    """
    try:
        all_classes = list(onto.classes())
        infer_classes = read_infer_classes(infer_classes_list)
        negative_samples = []

        num_random_class_samples = num_samples // 2
        num_inferred_class_samples = num_samples - num_random_class_samples

        if label == 1:
            num_random_class_samples += num_samples
            num_samples *= 2

        with tqdm(
            total=num_random_class_samples, desc="Generating random class samples"
        ) as pbar:
            while len(negative_samples) < num_random_class_samples:
                cls = random.choice(all_classes)
                all_classes = list(onto.classes())
                negative_class = random.choice(all_classes)
                cls_classes_is_a = [cls.iri for cls in cls.is_a if hasattr(cls, "iri")]

                if (
                    negative_class.iri not in cls_classes_is_a
                    and negative_class.iri not in infer_classes[cls.iri]
                ):

                    negative_samples.append((cls, negative_class.iri, 0))
                    pbar.update(1)

        with tqdm(
            total=num_inferred_class_samples, desc="Generating inferred class samples"
        ) as pbar:
            while len(negative_samples) < num_samples:
                cls = random.choice(all_classes)
                all_classes = list(onto.classes())
                if infer_classes[cls.iri] != []:
                    negative_class_iri = random.choice(infer_classes[cls.iri])
                    negative_samples.append((cls, negative_class_iri, label))
                    pbar.update(1)
        return negative_samples

    except FileNotFoundError as e:
        raise FileException(f"File not found error: {e.filename}", 404)
    except IOError as e:
        raise FileException(
            f"File operation error: Could not read or write file {e.filename}", 500
        )
    except Exception as e:
        raise ExtractionException(f"Unexpected error: {e}")


def train_test_val_gen_abox(onto: Ontology, ontology_name: str):
    """Main function for generating training, test, and validation sets for the abox.

    Args:
        onto (Ontology): The ontology to generate the training, test, and validation sets from
        ontology_name (str): The id of the ontology
    Returns:
        None
    """
    try:
        all_individuals = list(onto.individuals())
        train_individuals, test_individuals, val_individuals = train_test_val(
            all_individuals
        )

        root = get_path(ontology_name)
        train_csv_path_0 = os.path.join(root, "train-infer-1.csv")
        train_csv_path_1 = os.path.join(root, "train-infer-0.csv")

        test_csv_path = os.path.join(root, "test.csv")
        val_csv_path = os.path.join(root, "valid.csv")

        # Write positive samples to CSV files
        write_positive_samples_to_csv(
            train_csv_path_0, train_individuals, ontology_name
        )
        write_positive_samples_to_csv(
            train_csv_path_1, train_individuals, ontology_name
        )
        write_positive_samples_to_csv(test_csv_path, test_individuals, ontology_name)
        write_positive_samples_to_csv(val_csv_path, val_individuals, ontology_name)

        # Generate and write negative samples to CSV files for train sets
        start_time = time.time()
        negative_samples = generate_negative_samples_abox(
            onto,
            len(train_individuals),
            load_input_file(ontology_name, "inferred_ancestors"),
            1,
        )
        write_negative_samples_to_csv(train_csv_path_0, negative_samples)
        print("abox negative sample (-1) time usage:", time.time() - start_time)

        start_time = time.time()
        negative_samples = generate_negative_samples_abox(
            onto,
            len(train_individuals),
            load_input_file(ontology_name, "inferred_ancestors"),
            0,
        )
        write_negative_samples_to_csv(train_csv_path_1, negative_samples)
        print("abox negative sample (-0) time usage:", time.time() - start_time)

    except FileNotFoundError as e:
        raise FileException(f"File not found: {e.filename}", 404)

    except IOError as io_error:
        raise FileException(f"IO Error: {io_error.strerror}", 500)

    except Exception as e:
        raise ExtractionException(f"Unexpected error: {e}")


def train_test_val_gen_tbox(onto, ontology_name):
    """Main function for generating training, test, and validation sets for the tbox.

    Args:
        onto (Ontology): The ontology to generate the training, test, and validation sets from
        ontology_name (str): The id of the ontology
    Returns:
        None
    """

    try:
        # Split classes into train, test, and val sets
        all_classes = list(onto.classes())
        train_classes, test_classes, val_classes = train_test_val(all_classes)

        root = get_path(ontology_name)
        train_csv_path_0 = os.path.join(root, "train-infer-1.csv")
        train_csv_path_1 = os.path.join(root, "train-infer-0.csv")

        test_csv_path = os.path.join(root, "test.csv")
        val_csv_path = os.path.join(root, "valid.csv")

        # Write positive samples to CSV files
        write_positive_samples_to_csv(train_csv_path_0, train_classes, ontology_name)
        write_positive_samples_to_csv(train_csv_path_1, train_classes, ontology_name)
        write_positive_samples_to_csv(test_csv_path, test_classes, ontology_name)
        write_positive_samples_to_csv(val_csv_path, val_classes, ontology_name)
        # Generate and write negative samples to CSV files for train sets
        start_time = time.time()
        negative_samples = generate_negative_samples_tbox(
            onto,
            len(train_classes),
            load_input_file(ontology_name, "inferred_ancestors"),
            1,
        )
        write_negative_samples_to_csv(train_csv_path_0, negative_samples)

        start_time = time.time()
        negative_samples = generate_negative_samples_tbox(
            onto,
            len(train_classes),
            load_input_file(ontology_name, "inferred_ancestors"),
            0,
        )
        write_negative_samples_to_csv(train_csv_path_1, negative_samples)
        print("tbox negative sample (-0) time usage:", time.time() - start_time)

    except FileNotFoundError as e:
        raise FileException(f"File not found: {e.filename}", 404)

    except IOError as io_error:
        raise FileException(f"IO Error: {io_error.strerror}", 500)

    except Exception as e:
        raise ExtractionException(f"Unexpected error: {e}")
