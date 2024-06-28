import React, { useEffect, useState } from 'react';
import FileList from '../components/fileManagerComponents/FileList';
import { Box, Button, Container, CssBaseline, Grid, Theme, ThemeProvider, Typography, styled } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

interface FileManagerProps {
  theme: Theme;
  isAuthenticated: boolean;
  handleSignOut: () => void
}

interface ProcessFile {
  created_at: string;
  name: string;
}

interface Classifier {
  created_at: string;
  name: string;
  graph_fig: ProcessFile[];
  process_files: ProcessFile[];
}

interface Algorithm {
  created_at: string;
  name: string;
  classifier: Classifier[];
  process_files: ProcessFile[];
}

interface DataItem {
  created_at: string;
  name: string;
  algorithm: Algorithm[];
  process_files: ProcessFile[];
}

const SectionGrid = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

export default function FileManager({ theme, isAuthenticated, handleSignOut }: FileManagerProps) {
  const BACKEND_URI = import.meta.env.VITE_BACKEND_URI || "http://127.0.0.1:5000"
  const navigate = useNavigate();
  const [fileStructure, setFileStructure] = useState<DataItem[]>([]);

  const getFileList = () => {
    axios.get(`${BACKEND_URI}/api/explore`)
      .then((response) => {
        console.log("Get structure successful:", response.data);
        setFileStructure(response.data.ontology)
      })
      .catch((error) => {
        console.error("Get structure failed:", error);
      });
  }

  const hexToByteArray = (hexString: string): Uint8Array => {
    const byteArray = new Uint8Array(hexString.length / 2);
    for (let i = 0; i < byteArray.length; i++) {
      byteArray[i] = parseInt(hexString.substr(i * 2, 2), 16);
    }
    return byteArray;
  };

  const handleDownload = (ontologyName: string) => {
    axios.get<{ message: string, file: string }>(`${BACKEND_URI}/api/explore/` + ontologyName)
      .then((response) => {
        if (response.data.file) {
          console.error("Get file successful:", response.data);

          const byteArray = hexToByteArray(response.data.file);
          const blob = new Blob([byteArray], { type: 'application/zip' });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', ontologyName + '.zip');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }
      })
      .catch((error) => {
        console.log("Get file failed:", error);
      });
  };

  const handleDelete = (ontologyName: string) => {
    const token = localStorage.getItem('token');
    axios.delete(`${BACKEND_URI}/api/explore/` + ontologyName, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      console.log("Delete successful:", response.data);
      getFileList(); // Refresh the file list after deletion
    })
    .catch(error => {
      console.error("Delete failed:", error);
    });
  };

  useEffect(() => {
    getFileList();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Grid container sx={{ padding: 10 }} spacing={3}>
        <SectionGrid item xs={12}>
          <Box sx={{ display: 'flex', alignItems: "center", justifyContent: "space-between" }}>
            <Typography variant="h2" gutterBottom>
              File Manager
            </Typography>
            {!isAuthenticated ? (
              <Button variant="contained" color="primary" onClick={() => navigate('/login')}>
                Sign In
              </Button>
            ) : (
              <>
                <Button variant="contained" color="primary" onClick={handleSignOut}>
                  Sign Out
                </Button>
                {/* Add any other authenticated buttons or components here */}
              </>
            )}
          </Box>
        </SectionGrid>
        <SectionGrid item xs={12}>
          <FileList data={fileStructure} handleDownload={handleDownload} handleDelete={handleDelete} isAuthenticated={isAuthenticated}/>
        </SectionGrid>
      </Grid>
    </ThemeProvider>
  );
}
