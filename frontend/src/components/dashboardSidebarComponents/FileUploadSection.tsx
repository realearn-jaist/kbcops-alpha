import React from 'react';
import { TextField, Button, Typography } from '@mui/material';
import { UploadFile } from '@mui/icons-material';
import FileUpload from './FileUpload';

interface FileUploadSectionProps {
  handleUpload: (file: File, fileId: string, alias: string) => void;
}

const FileUploadSection: React.FC<FileUploadSectionProps> = ({
  handleUpload,
}) => {
  const [alias, setAlias] = React.useState<string>("");
  const [selectedFile, setSelectedFile] = React.useState<File>();
  const [ontology_name, setOntologyName] = React.useState("");

  // Handle file selection
  const handleFilesSelected = (files: File[]) => {
    setSelectedFile(files[0]);

    if (files.length > 0) {
      setOntologyName(files[0].name);
    }
  };

  const clickUpload = () => {
    if (selectedFile != undefined && alias != "" && ontology_name != "") {
      handleUpload(selectedFile, ontology_name, alias);
    }
  }

  return (
    <>
      {/* Title */}
      <Typography variant='h6' sx={{ paddingLeft: '10px' }}>
        Uploading
      </Typography>

      {/* TextField for ontology name */}
      <TextField
        sx={{ margin: '10px' }}
        required
        id="owner_alias"
        label="Owner's Alias"
        onChange={(e) => setAlias(e.target.value)} // Update fileId state on change
      />

      {/* File upload component */}
      <FileUpload onFilesSelected={handleFilesSelected} />

      {/* TextField for ontology name */}
      <TextField
        sx={{ margin: '10px' }}
        disabled={selectedFile === undefined}
        required
        id="ontology_name"
        label="Ontology Name"
        value={selectedFile !== undefined ? ontology_name : ''} // Show identifier only if one file is selected
        onChange={(e) => setOntologyName(e.target.value)} // Update fileId state on change
      />

      {/* Button to upload file */}
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<UploadFile />}
        sx={{ margin: '10px', height: '50px' }}
        disabled={selectedFile === undefined || ontology_name === '' || alias === ''}
        onClick={clickUpload}
      >
        Upload file
      </Button>

    </>
  );
};

export default FileUploadSection;
