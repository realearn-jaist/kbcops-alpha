import React from 'react';
import { Drawer as MuiDrawer, IconButton, Divider, TextField, Button, Toolbar, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Drawer } from '@mui/material';
import { styled } from '@mui/material/styles';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { ChevronLeft, ChevronRight, Inbox, Mail, UploadFile } from '@mui/icons-material';
import FileUpload from './DrawerComponents/FileUpload.tsx';
import EmbeddingForm from './DrawerComponents/EmbeddingForm.tsx';

const drawerWidth = 240;

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
  run_embedder: (onto_id: string, algo: string) => void;
}

const CustomDrawer: React.FC<DrawerProps> = ({ open, toggleDrawer, selectedFiles, fileId, setFileId, handleUpload, ontologyList, handleFilesSelected, run_embedder }) => {
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
      <DrawerHeader>
        <IconButton onClick={toggleDrawer}>
          <ChevronLeftIcon />
        </IconButton>
      </DrawerHeader>
      <Divider />
      <FileUpload onFilesSelected={handleFilesSelected} />
      <TextField
        sx={{ margin: '10px' }}
        disabled={selectedFiles.length !== 1}
        required
        id="identifier"
        label="Identifier"
        value={selectedFiles.length === 1 ? fileId : ''}
        onChange={(e) => setFileId(e.target.value)}
      />
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<UploadFile />}
        sx={{ margin: '10px', height: '50px' }}
        disabled={selectedFiles.length !== 1}
        onClick={handleUpload}
      >
        Upload file
      </Button>
      <Divider />
      <EmbeddingForm ontologyList={ontologyList} run_embedder={run_embedder} />
    </Drawer>
  );
};

export default CustomDrawer;
