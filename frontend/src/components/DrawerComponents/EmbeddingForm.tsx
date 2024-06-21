import React, { useState } from 'react';
import { Typography, FormControl, InputLabel, MenuItem, Select, Button } from '@mui/material';
import { PlayArrow } from '@mui/icons-material';
import { SelectChangeEvent } from '@mui/material/Select';

interface EmbeddingFormProps {
  ontologyList: string[];
  train_embedder: (onto_id: string, algo: string) => void;
  get_evaluate: (onto_id: string, algo: string) => void;
}

const EmbeddingForm: React.FC<EmbeddingFormProps> = ({ ontologyList, train_embedder, get_evaluate }) => {
  const [selectedOntology, setSelectedOntology] = useState('');
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');

  const handleOntologyChange = (event: SelectChangeEvent<string>) => {
    const newOntology = event.target.value as string;
    setSelectedOntology(newOntology);
    get_evaluate(newOntology, selectedAlgorithm); // Use newOntology directly
  };
  
  const handleAlgorithmChange = (event: SelectChangeEvent<string>) => {
    const newAlgorithm = event.target.value as string;
    setSelectedAlgorithm(newAlgorithm);
    get_evaluate(selectedOntology, newAlgorithm); // Use newAlgorithm directly
  };
  

  const handleRunClick = () => {
    train_embedder(selectedOntology, selectedAlgorithm);
  };

  return (
    <>
      <Typography variant='h6' sx={{ paddingLeft: '10px' }}>
        Embedding
      </Typography>
      <FormControl sx={{ margin: '10px' }}>
        <InputLabel id="onto-list-label">Ontologies</InputLabel>
        <Select
          labelId="onto-list-label"
          id="onto-list"
          label="Ontology"
          value={selectedOntology}
          onChange={handleOntologyChange}
          disabled={ontologyList.length === 0}
        >
          {ontologyList.map((ontology, index) => (
            <MenuItem key={index} value={ontology}>
              {ontology}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ margin: '10px' }}>
        <InputLabel id="algo-list-label">Algorithms</InputLabel>
        <Select
          labelId="algo-list-label"
          id="algo-list"
          label="Algorithm"
          value={selectedAlgorithm}
          onChange={handleAlgorithmChange}
          disabled={ontologyList.length === 0}
        >
          <MenuItem value="owl2vec-star">OWL2Vec*</MenuItem>
          <MenuItem value="opa2vec">OPA2Vec</MenuItem>
          <MenuItem value="rdf2vec">RDF2Vec</MenuItem>
          <MenuItem value="onto2vec">Onto2Vec</MenuItem>
        </Select>
      </FormControl>
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<PlayArrow />}
        sx={{ margin: '10px', height: '50px' }}
        disabled={ontologyList.length === 0 || !selectedOntology || !selectedAlgorithm}
        onClick={handleRunClick}
      >
        Run
      </Button>
    </>
  );
};

export default EmbeddingForm;
