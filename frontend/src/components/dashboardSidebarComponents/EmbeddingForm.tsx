import React from 'react';
import { Typography, FormControl, InputLabel, MenuItem, Select, Button } from '@mui/material';
import { PlayArrow } from '@mui/icons-material';
import { SelectChangeEvent } from '@mui/material/Select';

interface EmbeddingFormProps {
  data_pack: {
    ontologyList: string[],
    selectedOntology: string,
    selectedAlgorithm: string,
    selectedClassifier: string
  };
  handleOntologyChange: (event: SelectChangeEvent<string>) => void;
  handleAlgorithmChange: (event: SelectChangeEvent<string>) => void;
  handleClassifierChange: (event: SelectChangeEvent<string>) => void;
  handleRunClick: () => void;
}

const EmbeddingForm: React.FC<EmbeddingFormProps> = ({ data_pack, handleOntologyChange, handleAlgorithmChange, handleClassifierChange, handleRunClick }) => {


  return (
    <>
      {/* Title */}
      <Typography variant='h6' sx={{ paddingLeft: '10px' }}>
        Embedding
      </Typography>

      {/* Ontology Selection */}
      <FormControl sx={{ margin: '10px' }}>
        <InputLabel id="onto-list-label">Ontologies</InputLabel>
        <Select
          labelId="onto-list-label"
          id="onto-list"
          label="Ontology"
          value={data_pack.selectedOntology}
          onChange={handleOntologyChange}
          disabled={data_pack.ontologyList.length === 0} // Disable if there are no ontologies
        >
          {data_pack.ontologyList.map((ontology, index) => (
            <MenuItem key={index} value={ontology}>
              {ontology}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* Algorithm Selection */}
      <FormControl sx={{ margin: '10px' }}>
        <InputLabel id="algo-list-label">Algorithms</InputLabel>
        <Select
          labelId="algo-list-label"
          id="algo-list"
          label="Algorithm"
          value={data_pack.selectedAlgorithm}
          onChange={handleAlgorithmChange}
          disabled={data_pack.ontologyList.length === 0} // Disable if there are no ontologies
        >
          <MenuItem value="owl2vec-star">OWL2Vec*</MenuItem>
          <MenuItem value="opa2vec">OPA2Vec</MenuItem>
          <MenuItem value="rdf2vec">RDF2Vec</MenuItem>
          <MenuItem value="onto2vec">Onto2Vec</MenuItem>
        </Select>
      </FormControl>

      {/* classifier selection */}
      <FormControl sx={{ margin: '10px' }}>
        <InputLabel id="classifier-label">Classifier</InputLabel>
        <Select
          labelId="classifier-label"
          id="classifier"
          label="classifier"
          value={data_pack.selectedClassifier}
          onChange={handleClassifierChange}
          disabled={data_pack.ontologyList.length === 0} // Disable if there are no ontologies
        >
          <MenuItem value="random-forest">Random Forest</MenuItem>
          <MenuItem value="mlp">Multi-layer Perceptron</MenuItem>
          <MenuItem value="logistic-regression">Logistic Regression</MenuItem>
          <MenuItem value="svm">SVM</MenuItem>
          <MenuItem value="linear-svc">Linear SVC</MenuItem>
          <MenuItem value="decision-tree">Decision Tree</MenuItem>
          <MenuItem value="sgd-log">SDG Log</MenuItem>
        </Select>
      </FormControl>

      {/* Run Button */}
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<PlayArrow />}
        sx={{ margin: '10px', height: '50px' }}
        disabled={data_pack.ontologyList.length === 0 || !data_pack.selectedOntology || !data_pack.selectedAlgorithm || !data_pack.selectedClassifier} // Disable if no ontology or algorithm is selected
        onClick={handleRunClick}
      >
        Run
      </Button>
    </>
  );
};

export default EmbeddingForm;
