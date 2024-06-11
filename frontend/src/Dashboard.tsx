import * as React from 'react';
import { createTheme, styled, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import axios from 'axios';
import MuiAppBar, { AppBarProps as MuiAppBarProps } from '@mui/material/AppBar';
import ChevronLeft from '@mui/icons-material/ChevronLeft';
import { ChevronRight, Inbox, Mail } from '@mui/icons-material';

import MyAppBar from './components/MyAppBar';
import MyDrawer from './components/MyDrawer'
import Main from './components/Main';
import { Divider, Drawer, IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemText, useTheme } from '@mui/material';

const defaultTheme = createTheme();

const drawerWidth: number = 240;




export default function Dashboard() {

  const [open, setOpen] = React.useState(true);
  const [selectedFiles, setSelectedFiles] = React.useState<File[]>([]);
  const [fileId, setFileId] = React.useState("");
  const [ontology_list, set_onto_list] = React.useState<string[]>([]);
  const [display_onto_id, set_display_onto_id] = React.useState<string>("<Ontology>");
  const [display_onto_data, set_display_onto_data] = React.useState<{
    abox: boolean;
    no_class: number;
    no_indiviual: number;
    no_axiom: number;
    no_annotation: number;
  }>({ abox: false, no_class: 0, no_indiviual: 0, no_axiom: 0, no_annotation: 0 })

  React.useEffect(() => {
    getOntologyList();
  }, []);

  const toggleDrawer = () => {
    setOpen(!open);
  };

  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles(files);
    // Do whatever you want with the selected files
    console.log("Selected files:", selectedFiles);

    if (files.length > 0) {
      setFileId(files[0].name);
    }
  };

  const handleUpload = () => {
    const file = selectedFiles[0];
    const formData = new FormData();
    formData.append('owl_file', file);
    formData.append('onto_id', fileId);

    axios
      .post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then((response) => {
        console.log("Upload successful:", response.data);
        getOntologyList();
        getOntologyStat(response.data.id);
      })
      .catch((error) => {
        console.error("Upload failed:", error);
        // Handle error
      });
  };

  const getOntologyStat = (file_id: string) => {
    axios
      .get("http://127.0.0.1:5000/extract/" + file_id)
      .then((response) => {
        console.log("Extract successful:", response.data);
        set_display_onto_id(fileId)
      })
      .catch((error) => {
        console.error("Extract failed:", error);
        // Handle error
      });
  }

  const getOntologyList = () => {
    axios
      .get("http://127.0.0.1:5000/ontology")
      .then((response) => {
        console.log("load successful:", response.data);
        set_onto_list(response.data.onto_list);
      })
      .catch((error) => {
        console.error("load failed:", error);
        // Handle error
      });
  }

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const theme = useTheme();

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex'}}>
        <MyAppBar open={open} toggleDrawer={toggleDrawer} />
        <MyDrawer
          open={open}
          toggleDrawer={toggleDrawer}
          selectedFiles={selectedFiles}
          fileId={fileId}
          setFileId={setFileId}
          handleUpload={handleUpload}
          ontologyList={ontology_list}
          handleFilesSelected={handleFilesSelected}
        />
        
        <Main
          open={open}
          onto_id={display_onto_id}
          onto_data={display_onto_data}
        />
      </Box>


    </ThemeProvider>
  );
}
