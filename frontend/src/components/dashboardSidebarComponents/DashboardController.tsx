import * as React from 'react';

import { Divider, SelectChangeEvent } from '@mui/material';
import ClassifierSection from './ClassifierSection';
import EmbeddingForm from './EmbeddingForm';
import FileUploadSection from './FileUploadSection';

interface DrawerProps {
  setAlias: (alias: string) => void;
  selectedFiles: File[];
  fileId: string;
  setFileId: (id: string) => void;
  handleUpload: () => void;
  ontologyList: string[];
  handleFilesSelected: (files: File[]) => void;
  trainEmbedder: (onto_id: string, algo: string, classifier: string) => void;
  getEvaluate: (onto_id: string, algo: string, classifier: string) => void;
}

export default function DashboardController({
  setAlias,
  selectedFiles,
  fileId,
  setFileId,
  handleUpload,
  ontologyList,
  handleFilesSelected,
  trainEmbedder,
  getEvaluate,
}: DrawerProps) {
  // State variables for selected ontology, algorithm, classifier, completionType
  const [selectedOntology, setSelectedOntology] = React.useState("");
  const [selectedAlgorithm, setSelectedAlgorithm] = React.useState("");
  const [selectedClassifier, setSelectedClassifier] = React.useState("");

  // Handler for changing the selected ontology
  const handleOntologyChange = (event: SelectChangeEvent<string>) => {
    const newOntology = event.target.value as string;
    setSelectedOntology(newOntology);
    getEvaluate(newOntology, selectedAlgorithm, selectedClassifier); // Evaluate with the new ontology
  };

  // Handler for changing the selected algorithm
  const handleAlgorithmChange = (event: SelectChangeEvent<string>) => {
    const newAlgorithm = event.target.value as string;
    setSelectedAlgorithm(newAlgorithm);
    getEvaluate(selectedOntology, newAlgorithm, selectedClassifier); // Evaluate with the new algorithm
  };

  // Handler for changing the selected Classifier
  const handleClassifierChange = (event: SelectChangeEvent<string>) => {
    const newClassifier = event.target.value as string;
    setSelectedClassifier(newClassifier);
    getEvaluate(selectedOntology, selectedAlgorithm, newClassifier); // Evaluate with the new Classifier
  };

  // Handler for the Run button click event
  const handleRunClick = () => {
    trainEmbedder(selectedOntology, selectedAlgorithm, selectedClassifier);
  };


  return (
    <React.Fragment>
      {/* File upload section */}
      <FileUploadSection
        setAlias={setAlias}
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
          selectedClassifier: selectedClassifier
        }}
        handleOntologyChange={handleOntologyChange}
        handleAlgorithmChange={handleAlgorithmChange}
        handleClassifierChange={handleClassifierChange}
        handleRunClick={handleRunClick}
      />
    </React.Fragment>
  );
}
