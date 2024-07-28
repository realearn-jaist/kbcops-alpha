import React from 'react';
import { Typography, FormControl, InputLabel, MenuItem, Select, Button, Grid } from '@mui/material';
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

const EmbeddingSection: React.FC<EmbeddingFormProps> = ({ data_pack, handleOntologyChange, handleAlgorithmChange, handleClassifierChange, handleRunClick }) => {

  return (
    <Grid container spacing={2}>
      {/* Title */}
      <Grid item xs={12}>
        <Typography variant='h6' sx={{ paddingLeft: '10px' }}>
          Embedding
        </Typography>
      </Grid>

      {/* Ontology Selection */}
      <Grid item xs={12}>
        <FormControl fullWidth>
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
      </Grid>

      {/* Algorithm Selection */}
      <Grid item xs={12}>
        <FormControl fullWidth>
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
      </Grid>

      {/* Classifier Selection */}
      <Grid item xs={12}>
        <FormControl fullWidth>
          <InputLabel id="classifier-label">Classifier</InputLabel>
          <Select
            labelId="classifier-label"
            id="classifier"
            label="Classifier"
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
            <MenuItem value="sgd-log">SGD Log</MenuItem>
          </Select>
        </FormControl>
      </Grid>

      {/* Run Button */}
      <Grid item xs={12} sx={{ textAlign: 'center' }}>
        <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
          startIcon={<PlayArrow />}
          sx={{ height: '50px' }}
          disabled={data_pack.ontologyList.length === 0 || !data_pack.selectedOntology || !data_pack.selectedAlgorithm || !data_pack.selectedClassifier} // Disable if no ontology or algorithm is selected
          onClick={handleRunClick}
          fullWidth
        >
          Run
        </Button>
      </Grid>
    </Grid>
  );
};

export default EmbeddingSection;
