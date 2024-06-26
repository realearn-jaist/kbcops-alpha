import * as React from 'react';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';

import CloseIcon from '@mui/icons-material/Close';
import ExpandMoreRoundedIcon from '@mui/icons-material/ExpandMoreRounded';

import DashboardController from './DashboardController';

interface DrawerProps {
  selectedFiles: File[];
  fileId: string;
  setFileId: (id: string) => void;
  handleUpload: () => void;
  ontologyList: string[];
  handleFilesSelected: (files: File[]) => void;
  trainEmbedder: (onto_id: string, algo: string, classifier: string) => void;
  getEvaluate: (onto_id: string, algo: string, classifier: string) => void;
}

export default function DashboardControllerMobile({
  selectedFiles,
  fileId,
  setFileId,
  handleUpload,
  ontologyList,
  handleFilesSelected,
  trainEmbedder,
  getEvaluate,
}: DrawerProps) {
  const [open, setOpen] = React.useState(false);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpen(newOpen);
  };

  const DrawerList = (
    <Box sx={{ width: 'auto', px: 3, pb: 3, pt: 8 }} role="presentation">
      <IconButton
        onClick={toggleDrawer(false)}
        sx={{ position: 'absolute', right: 8, top: 8 }}
      >
        <CloseIcon />
      </IconButton>
      <DashboardController
        selectedFiles={selectedFiles}
        fileId={fileId}
        setFileId={setFileId}
        handleUpload={handleUpload}
        ontologyList={ontologyList}
        handleFilesSelected={handleFilesSelected}
        trainEmbedder={trainEmbedder}
        getEvaluate={getEvaluate}
      />
    </Box >
  );

  return (
    <div>
      <Button
        variant="text"
        endIcon={<ExpandMoreRoundedIcon />}
        onClick={toggleDrawer(true)}
      >
        View details
      </Button>
      <Drawer open={open} anchor="top" onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>
    </div>
  );
}
