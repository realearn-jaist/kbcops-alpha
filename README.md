# Knowledge Base Completion Operations (KBCOps)

## What is Knowledge Base Completion (KBC)?

Knowledge Base Completion (KBC) is a task in Knowledge Graph (KG) completion that aims to predict missing relationships or facts in a knowledge base. The goal is to infer new knowledge based on existing information in the knowledge graph. Key points related to KBC include:

- **Task Definition:** KBC involves predicting missing links or triples in a knowledge graph by leveraging the existing information and relationships within the graph.

- **Methods:** Various machine learning and knowledge representation techniques are used for KBC, including embedding models (e.g., TransE, DistMult), rule-based reasoning, and neural network architectures.

- **Applications:** KBC has applications in recommendation systems, question answering, information retrieval, and semantic search, where completing the knowledge graph can enhance the performance of these tasks.

## Introduction of this project

Knowledge bases (KBs), particularly ontologies, are often incomplete, necessitating the need for Knowledge Base Completion. One critical aspect to consider in KB completion is the presence of **"garbage"** information. In this context, **"garbage"** refers to implicit or duplicated facts that do not contribute meaningfully to the completeness of the ontology.

These tools are designed to provide users with the ability to compare and evaluate the presence of garbage across different algorithms and ontologies used in KB completion operations. By offering transparency and insights into the quality of completion results, the monitoring tools aim to empower users to make informed decisions and optimize the completeness of knowledge bases effectively.

## Key Features

- **Upload Ontology**: Allows users to upload ontologies for processing and analysis.

- **Get Stats of Ontology**: Provides statistics of the uploaded ontology, such as the number of axioms, individuals, classes, etc.

- **Selecting Embedding Algorithms**: Users can choose from various embedding algorithms:

  - Onto2Vec
  - OPA2Vec
  - RDF2Vec
  - OWL2Vec\*

- **Display Embedding Prediction Stats**: Shows statistics of the embedding's predictions, including metrics like Hit@K, MRR (Mean Reciprocal Rank), etc.

- **Display Garbage**: Users can visualize garbage relationships in the graph, aiding in the identification and removal of erroneous or irrelevant data.

## Folder Documentation

In backend/

- **controllers/**: Logic of the application for receiving requests from routes, processing data, and interacting with models to produce responses. Controllers in this directory have been adapted from and commented in the code:

  - [OWL2Vec-Star](https://github.com/KRR-Oxford/OWL2Vec-Star)
  - [kbc-ops](https://github.com/realearn-jaist/kbc-ops)

- **models/**: Holds modules that define the data structure and interact with the database or data storage mechanisms.

  - Encapsulate data-related logic, such as CRUD operations, data validation, and relationships between entities.

- **owl2vec-star/**: Contains a third-party library or module named owl2vec-star.

- **routes/**: Contains modules that define the application's endpoints or routes.

  - Each route module maps HTTP requests to specific controller methods.

- **storage/**: Serves as a storage directory where uploaded files or generated data are stored.

- **utils/**: Contains utility functions or modules that provide commonly used functionalities across the application.

- **app.py**: Typically the entry point of the application or the main application module.

## Online Application

Link :

## Requirements

To set up the KBCOps environment, ensure you have Python environment for version 3.8.10 or any compatible version installed. Then, install the following dependencies in **requirements.txt**:

```
alabaster==0.7.13
Babel==2.15.0
blinker==1.8.2
certifi==2024.6.2
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
contourpy==1.1.1
cycler==0.12.1
Cython==0.29.14
docutils==0.20.1
Flask==3.0.3
Flask-Cors==4.0.1
fonttools==4.53.0
gensim==4.3.2
gunicorn==22.0.0
idna==3.7
imagesize==1.4.1
importlib_metadata==7.1.0
importlib_resources==6.4.0
isodate==0.6.1
itsdangerous==2.2.0
Jinja2==3.1.4
joblib==1.4.2
kiwisolver==1.4.5
MarkupSafe==2.1.5
matplotlib==3.7.5
networkx==3.1
nltk==3.8.1
numpy==1.24.4
owlready2==0.46
packaging==24.1
pandas==2.0.3
pillow==10.3.0
pydot==1.4.2
Pygments==2.18.0
pyparsing==2.4.7
pyRDF2Vec==0.0.5
python-dateutil==2.9.0.post0
python-louvain==0.16
pytz==2024.1
rdflib==4.2.2
regex==2024.5.15
requests==2.32.3
scikit-learn==0.24.2
scipy==1.10.1
six==1.16.0
smart-open==7.0.4
snowballstemmer==2.2.0
Sphinx==7.1.2
sphinx-autodoc-typehints==2.0.1
sphinx-rtd-theme==2.0.0
sphinxcontrib-applehelp==1.0.4
sphinxcontrib-devhelp==1.0.2
sphinxcontrib-htmlhelp==2.0.1
sphinxcontrib-jquery==4.1
sphinxcontrib-jsmath==1.0.1
sphinxcontrib-qthelp==1.0.3
sphinxcontrib-serializinghtml==1.1.5
threadpoolctl==3.5.0
tqdm==4.66.4
tzdata==2024.1
urllib3==2.2.2
Werkzeug==3.0.3
wrapt==1.16.0
zipp==3.19.2
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/realearn-jaist/kbcops-alpha.git
   ```
2. Navigate to the project directory:
   ```bash
   cd kbcops-alpha
   ```
3. Create a Python environment (we used python 3.8.10) .

4. (If not installed) Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Start the backend server:
   ```bash
   python app.py
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the dependencies (first time only):
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   ```

### Running Tests

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Run all tests:
   ```bash
   python -m unittest discover -p "*.py"
   ```
3. Run a specific test:
   ```bash
   python ./test/{name_of_test_file}
   ```

### Create Documentation

1. Navigate to the docs directory:
   ```bash
   cd docs
   ```
2. Build the documentation (first time):
   ```bash
   make html
   ```
3. Clean and rebuild the documentation:
   ```bash
   make clean html
   ```

## Fixes Applied to Owl2vec\* Library

1. **Update in `embed.py`**:

   Change:

   ```python
   self.model* = Word2Vec(
       sentences,
       size=self.vector_size,
       window=self.window,
       workers=self.n_jobs,
       sg=self.sg,
       iter=self.max_iter,
       negative=self.negative,
       min_count=self.min_count,
       seed=42,
   )
   ```

   To:

   ```python
   self.model* = Word2Vec(
       sentences,
       vector_size=self.vector_size,
       window=self.window,
       workers=self.n_jobs,
       sg=self.sg,
       epochs=self.max_iter,
       negative=self.negative,
       min_count=self.min_count,
       seed=42,
   )
   ```

   Located in `kbcops-alpha/backend/owl2vec_star/rdf2vec/embed.py`.

2. **Update in `RDF2Vec_Embed.py`**:

   Change:

   ```python
   def get_rdf2vec_embed(onto_file, walker_type, walk_depth, embed_size, classes):
       kg, walker = construct_kg_walker(
           onto_file=onto_file, walker_type=walker_type, walk_depth=walk_depth
       )
       transformer = RDF2VecTransformer(walkers=[walker], vector_size=embed_size)
       instances = [rdflib.URIRef(c) for c in classes]
       walk_embeddings = transformer.fit_transform(graph=kg, instances=instances)
       return np.array(walk_embeddings)
   ```

   To:

   ```python
   def get_rdf2vec_embed(onto_file, walker_type, walk_depth, embed_size, classes):
       kg, walker = construct_kg_walker(
           onto_file=onto_file, walker_type=walker_type, walk_depth=walk_depth
       )
       transformer = RDF2VecTransformer(walkers=[walker], vector_size=embed_size)
       instances = [rdflib.URIRef(c) for c in classes]
       walk_embeddings = transformer.fit_transform(graph=kg, instances=instances)
       return np.array(walk_embeddings), transformer
   ```

   Located in `kbcops-alpha/backend/owl2vec_star/RDF2Vec_Embed.py`.

## Paper

#### **Title:** Are Embeddings All We Need for Knowledge Base Completion? Insights from Description Logicians

**Abstract:** Description Logic knowledge bases (KBs), i.e., ontologies, are often greatly incomplete, necessitating a demand for KB completion. Promising approaches to this aim are to embed KB elements such as classes, properties, and logical axioms into a low-dimensional vector space and and find missing elements by inferencing on the latent representation. Because these approaches make inference based solely on existing facts in KBs, the risk is that likelihood of KB completion with implicit (duplicated) facts could be high, making the performance of KB embedding models questionable. Thus, it is essential for the KB completion's procedure to prevent completing KBs by implicit facts. In this short paper, we present a new perspective of this problem based on the logical constructs in description logic. We also introduce a novel recipe for KB completion operations called KBCOps and include a demo that exhibits KB completion with fact duplication when using state-of-the-art KB embedding algorithms.

## Authors and Contacts (Alphabetical Order)

- **Chaphowasit Mahayossanan (Mahidol University, Thailand)**

  - Email: chaphowasit.mah@student.mahidol.edu

- **Teerapat Phopit (Mahidol University, Thailand)**

  - Email: teerapat.pho@student.mahidol.edu

- **Teeradaj Racharak (JAIST, Japan)**

  - Email: racharak@jaist.ac.jp

- **Kiattiphum Suwanarsa (Mahidol University, Thailand)**
  - Email: kiattiphum.intern@gmail.com

## References

- [OWL2Vec-Star](https://github.com/KRR-Oxford/OWL2Vec-Star)

- [kbc-ops](https://github.com/realearn-jaist/kbc-ops)
