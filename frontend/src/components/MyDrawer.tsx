import React from 'react';
import { Drawer, IconButton, Divider, TextField, Button } from '@mui/material';
import { styled } from '@mui/material/styles';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { UploadFile } from '@mui/icons-material';
import FileUpload from './DrawerComponents/FileUpload';
import EmbeddingForm from './DrawerComponents/EmbeddingForm';

const drawerWidth = 240; // Width of the drawer

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
  getEvaluate: (onto_id: string, algo: string) => void;
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
}) => {
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
      
      {/* File upload component */}
      <FileUpload onFilesSelected={handleFilesSelected} />
      
      {/* TextField for file identifier */}
      <TextField
        sx={{ margin: '10px' }}
        disabled={selectedFiles.length !== 1} // Disable if no file or more than one file is selected
        required
        id="identifier"
        label="Identifier"
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
      <Divider />
      
      {/* Embedding form component */}
      <EmbeddingForm
        ontologyList={ontologyList}
        trainEmbedder={trainEmbedder}
        getEvaluate={getEvaluate}
      />
    </Drawer>
  );
};

export default CustomDrawer;
