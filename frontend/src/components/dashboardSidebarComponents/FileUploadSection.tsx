import React from 'react';
import { TextField, Button, Typography } from '@mui/material';
import { UploadFile } from '@mui/icons-material';
import FileUpload from './FileUpload';

interface FileUploadSectionProps {
  setAlias: (alias: string) => void;
  selectedFiles: File[];
  fileId: string;
  setFileId: (id: string) => void;
  handleUpload: () => void;
  handleFilesSelected: (files: File[]) => void;
}

const FileUploadSection: React.FC<FileUploadSectionProps> = ({
  setAlias,
  selectedFiles,
  fileId,
  setFileId,
  handleUpload,
  handleFilesSelected,
}) => {
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
        disabled={selectedFiles.length !== 1} // Disable if no file or more than one file is selected
        required
        id="ontology_name"
        label="Ontology Name"
        value={selectedFiles.length === 1 ? fileId : ''} // Show identifier only if one file is selected
        onChange={(e) => setFileId(e.target.value)} // Update fileId state on change
      />

      {/* Button to upload file */}
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<UploadFile />}
        sx={{ margin: '10px', height: '50px' }}
        disabled={selectedFiles.length !== 1} // Disable if no file or more than one file is selected
        onClick={handleUpload} // Call handleUpload function on click
      >
        Upload file
      </Button>

    </>
  );
};

export default FileUploadSection;
