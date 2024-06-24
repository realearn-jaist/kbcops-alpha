import React from 'react';
import { Typography, FormControl, InputLabel, MenuItem, Select, Button } from '@mui/material';
import { PlayArrow } from '@mui/icons-material';
import { SelectChangeEvent } from '@mui/material/Select';

interface EmbeddingFormProps {
  data_pack: {
    ontologyList: string[], 
    selectedOntology: string, 
    selectedAlgorithm: string, 
    selectedCompletionType: string, 
    selectedClassifier: string
  };
  handleOntologyChange: (event: SelectChangeEvent<string>) => void;
  handleAlgorithmChange: (event: SelectChangeEvent<string>) => void;
  handleEmbedClick: () => void;
}

const EmbeddingForm: React.FC<EmbeddingFormProps> = ({ data_pack, handleOntologyChange, handleAlgorithmChange, handleEmbedClick }) => {


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
      
      {/* Run Button */}
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<PlayArrow />}
        sx={{ margin: '10px', height: '50px' }}
        disabled={data_pack.ontologyList.length === 0 || !data_pack.selectedOntology || !data_pack.selectedAlgorithm} // Disable if no ontology or algorithm is selected
        onClick={handleEmbedClick}
      >
        Embed
      </Button>
    </>
  );
};

export default EmbeddingForm;
