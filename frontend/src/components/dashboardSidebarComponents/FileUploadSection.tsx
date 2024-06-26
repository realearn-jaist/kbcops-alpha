import React from 'react';
import { TextField, Button, Box } from '@mui/material';
import { UploadFile } from '@mui/icons-material';
import FileUpload from './FileUpload';

interface FileUploadSectionProps {
  selectedFiles: File[];
  fileId: string;
  setFileId: (id: string) => void;
  handleUpload: () => void;
  handleFilesSelected: (files: File[]) => void;
}

const FileUploadSection: React.FC<FileUploadSectionProps> = ({
  selectedFiles,
  fileId,
  setFileId,
  handleUpload,
  handleFilesSelected,
}) => {
  return (
    <>
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
