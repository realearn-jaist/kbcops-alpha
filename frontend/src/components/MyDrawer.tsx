import React from 'react';
import { Drawer, IconButton, Divider, SelectChangeEvent } from '@mui/material';
import { styled } from '@mui/material/styles';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import EmbeddingForm from './DrawerComponents/EmbeddingForm';
import FileUploadSection from './DrawerComponents/FileUploadSection';
import ClassifierSection from './DrawerComponents/ClassifierSection';

const drawerWidth: number = 300; // Width of the drawer

// Styled component for the drawer header
const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

interface DrawerProps {
  open: boolean;
  toggleDrawer: () => void;
  selectedFiles: File[];
  fileId: string;
  setFileId: (id: string) => void;
  handleUpload: () => void;
  ontologyList: string[];
  handleFilesSelected: (files: File[]) => void;
  trainEmbedder: (onto_id: string, algo: string) => void;
  getEvaluate: (onto_id: string, algo: string, com_type: string, classifier: string) => void;
  evaluateEmbedder: (onto_id: string, algo: string, com_type: string, classifier: string) => void;
}

const CustomDrawer: React.FC<DrawerProps> = ({
  open,
  toggleDrawer,
  selectedFiles,
  fileId,
  setFileId,
  handleUpload,
  ontologyList,
  handleFilesSelected,
  trainEmbedder,
  getEvaluate,
  evaluateEmbedder,
}) => {
  // State variables for selected ontology, algorithm, classifier, completionType
  const [selectedOntology, setSelectedOntology] = React.useState("");
  const [selectedAlgorithm, setSelectedAlgorithm] = React.useState("");
  const [selectedClassifier, setSelectedClassifier] = React.useState("");
  const [selectedCompletionType, setSelectedCompletionType] = React.useState("");

  // Handler for changing the selected ontology
  const handleOntologyChange = (event: SelectChangeEvent<string>) => {
    const newOntology = event.target.value as string;
    setSelectedOntology(newOntology);
    getEvaluate(newOntology, selectedAlgorithm, selectedCompletionType, selectedClassifier); // Evaluate with the new ontology
  };

  // Handler for changing the selected algorithm
  const handleAlgorithmChange = (event: SelectChangeEvent<string>) => {
    const newAlgorithm = event.target.value as string;
    setSelectedAlgorithm(newAlgorithm);
    getEvaluate(selectedOntology, newAlgorithm, selectedCompletionType, selectedClassifier); // Evaluate with the new algorithm
  };

  // Handler for changing the selected CompletionType
  const handleCompletionTypeChange = (event: SelectChangeEvent<string>) => {
    const newCompletionType = event.target.value as string;
    setSelectedCompletionType(newCompletionType);
    getEvaluate(selectedOntology, selectedAlgorithm, newCompletionType, selectedClassifier); // Evaluate with the new Completion Type
  };

  // Handler for changing the selected Classifier
  const handleClassifierChange = (event: SelectChangeEvent<string>) => {
    const newClassifier = event.target.value as string;
    setSelectedClassifier(newClassifier);
    getEvaluate(selectedOntology, selectedAlgorithm, selectedCompletionType, newClassifier); // Evaluate with the new Classifier
  };

  // Handler for the Embed button click event
  const handleEmbedClick = () => {
    trainEmbedder(selectedOntology, selectedAlgorithm);
  };

  // Handler for the run button click event
  const handleRunClick = () => {
    evaluateEmbedder(selectedOntology, selectedAlgorithm, selectedCompletionType, selectedClassifier);
  };


  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
      variant="persistent"
      anchor="left"
      open={open}
    >
      {/* Drawer header with close button */}
      <DrawerHeader>
        <IconButton onClick={toggleDrawer}>
          <ChevronLeftIcon />
        </IconButton>
      </DrawerHeader>
      <Divider />

      {/* File upload section */}
      <FileUploadSection
        selectedFiles={selectedFiles}
        fileId={fileId}
        setFileId={setFileId}
        handleUpload={handleUpload}
        handleFilesSelected={handleFilesSelected}
      />

      <Divider />


      {/* Embedding form component */}
      <EmbeddingForm
        data_pack={{
          ontologyList: ontologyList,
          selectedOntology: selectedOntology,
          selectedAlgorithm: selectedAlgorithm,
          selectedCompletionType: selectedCompletionType,
          selectedClassifier: selectedClassifier
        }}
        handleOntologyChange={handleOntologyChange}
        handleAlgorithmChange={handleAlgorithmChange}
        handleEmbedClick={handleEmbedClick}
      />

      {/* Classifier section */}
      <ClassifierSection
        data_pack={{
          ontologyList: ontologyList,
          selectedOntology: selectedOntology,
          selectedAlgorithm: selectedAlgorithm,
          selectedCompletionType: selectedCompletionType,
          selectedClassifier: selectedClassifier
        }}
        handleCompletionTypeChange={handleCompletionTypeChange}
        handleClassifierChange={handleClassifierChange}
        handleRunClick={handleRunClick}
      />
    </Drawer>
  );
};

export default CustomDrawer;
