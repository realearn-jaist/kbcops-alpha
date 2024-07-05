import React from 'react';
import { TextField, Button, Typography, Grid } from '@mui/material';
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
    <Grid container spacing={2}>
      {/* Title */}
      <Grid item xs={12}>
        <Typography variant='h6' sx={{ paddingLeft: '10px' }}>
          Uploading
        </Typography>
      </Grid>

      {/* TextField for owner's alias */}
      <Grid item xs={12}>
        <TextField
          fullWidth
          required
          id="owner_alias"
          label="Owner's Alias"
          value={alias}
          onChange={(e) => setAlias(e.target.value)}
        />
      </Grid>

      {/* File upload component */}
      <Grid item xs={12}>
        <FileUpload onFilesSelected={handleFilesSelected} />
      </Grid>

      {/* TextField for ontology name */}
      <Grid item xs={12}>
        <TextField
          fullWidth
          required
          id="ontology_name"
          label="Ontology Name"
          value={ontology_name}
          disabled={selectedFile === undefined}
          onChange={(e) => setOntologyName(e.target.value)}
        />
      </Grid>

      {/* Button to upload file */}
      <Grid item xs={12} sx={{ textAlign: 'center' }}>
        <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
          startIcon={<UploadFile />}
          sx={{height: '50px' }}
          disabled={selectedFile === undefined || ontology_name === '' || alias === ''}
          onClick={clickUpload}
          fullWidth
        >
          Upload file
        </Button>
      </Grid>
    </Grid>
  );
};

export default FileUploadSection;
