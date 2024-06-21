import React, { useState } from 'react';
import { Typography, FormControl, InputLabel, MenuItem, Select, Button } from '@mui/material';
import { PlayArrow } from '@mui/icons-material';
import { SelectChangeEvent } from '@mui/material/Select';

interface EmbeddingFormProps {
  ontologyList: string[];
  trainEmbedder: (onto_id: string, algo: string) => void;
  getEvaluate: (onto_id: string, algo: string) => void;
}

const EmbeddingForm: React.FC<EmbeddingFormProps> = ({ ontologyList, trainEmbedder, getEvaluate }) => {
  // State variables for selected ontology and algorithm
  const [selectedOntology, setSelectedOntology] = useState('');
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');

  // Handler for changing the selected ontology
  const handleOntologyChange = (event: SelectChangeEvent<string>) => {
    const newOntology = event.target.value as string;
    setSelectedOntology(newOntology);
    getEvaluate(newOntology, selectedAlgorithm); // Evaluate with the new ontology and current algorithm
  };

  // Handler for changing the selected algorithm
  const handleAlgorithmChange = (event: SelectChangeEvent<string>) => {
    const newAlgorithm = event.target.value as string;
    setSelectedAlgorithm(newAlgorithm);
    getEvaluate(selectedOntology, newAlgorithm); // Evaluate with the current ontology and new algorithm
  };

  // Handler for the run button click event
  const handleRunClick = () => {
    trainEmbedder(selectedOntology, selectedAlgorithm);
  };

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
          value={selectedOntology}
          onChange={handleOntologyChange}
          disabled={ontologyList.length === 0} // Disable if there are no ontologies
        >
          {ontologyList.map((ontology, index) => (
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
          value={selectedAlgorithm}
          onChange={handleAlgorithmChange}
          disabled={ontologyList.length === 0} // Disable if there are no ontologies
        >
          <MenuItem value="owl2vec-star">OWL2Vec*</MenuItem>
          <MenuItem value="opa2vec">OPA2Vec</MenuItem>
          <MenuItem value="rdf2vec">RDF2Vec</MenuItem>
          <MenuItem value="onto2vec">Onto2Vec</MenuItem>
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
        disabled={ontologyList.length === 0 || !selectedOntology || !selectedAlgorithm} // Disable if no ontology or algorithm is selected
        onClick={handleRunClick}
      >
        Run
      </Button>
    </>
  );
};

export default EmbeddingForm;
