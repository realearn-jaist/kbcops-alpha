import React from 'react';
import { Typography, Radio, FormControl, InputLabel, Select, MenuItem, Button, FormControlLabel, RadioGroup, SelectChangeEvent } from '@mui/material';
import { PlayArrow } from '@mui/icons-material';

interface ClassifierSectionProps {
  data_pack: {
    ontologyList: string[],
    selectedOntology: string,
    selectedAlgorithm: string,
    selectedCompletionType: string,
    selectedClassifier: string
  };
  handleCompletionTypeChange: (event: SelectChangeEvent<string>) => void;
  handleClassifierChange: (event: SelectChangeEvent<string>) => void;
  handleRunClick: () => void;
}

const ClassifierSection: React.FC<ClassifierSectionProps> = ({
  data_pack,
  handleCompletionTypeChange,
  handleClassifierChange,
  handleRunClick
}) => {


  return (
    <>
      <Typography variant='h6' sx={{ paddingLeft: '10px' }}>
        Classifier
      </Typography>
      <RadioGroup
        aria-label="classifier"
        name="classifier"
        value={data_pack.selectedCompletionType}
        onChange={handleCompletionTypeChange}
        sx={{ margin: '10px' }}
      >
        <FormControlLabel value="abox" control={<Radio />} label="ABox Completion" />
        <FormControlLabel value="tbox" control={<Radio />} label="TBox Completion" />
      </RadioGroup>

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
        disabled={data_pack.ontologyList.length === 0 || !data_pack.selectedOntology || !data_pack.selectedAlgorithm || !data_pack.selectedCompletionType || !data_pack.selectedClassifier}
        onClick={handleRunClick}
      >
        Run
      </Button>
    </>
  );
};

export default ClassifierSection;
