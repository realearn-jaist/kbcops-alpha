import React from 'react';
import { Typography, FormControl, InputLabel, MenuItem, Select, Button } from '@mui/material';
import { PlayArrow } from '@mui/icons-material';

interface EmbeddingFormProps {
  ontologyList: string[];
}

const EmbeddingForm: React.FC<EmbeddingFormProps> = ({ ontologyList }) => (
  <>
    <Typography variant='h6' sx={{ paddingLeft: '10px' }}>
      Embedding
    </Typography>
    <FormControl sx={{ margin: '10px' }}>
      <InputLabel id="onto-list-label">Ontologies</InputLabel>
      <Select labelId="onto-list-label" id="onto-list" label="Ontology" disabled={ontologyList.length === 0}>
        {ontologyList.map((ontology, index) => (
          <MenuItem key={index} value={ontology}>
            {ontology}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
    <FormControl sx={{ margin: '10px' }}>
      <InputLabel id="algo-list-label">Algorithms</InputLabel>
      <Select labelId="algo-list-label" id="algo-list" label="algology" disabled={ontologyList.length === 0}>
        <MenuItem value="owl2vec-star">OWL2Vec*</MenuItem>
        <MenuItem value="opa2vec">OPA2Vec</MenuItem>
        <MenuItem value="rdf2vec-star">RDF2Vec</MenuItem>
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
      disabled={ontologyList.length !== 1}
    >
      Run
    </Button>
  </>
);

export default EmbeddingForm;
