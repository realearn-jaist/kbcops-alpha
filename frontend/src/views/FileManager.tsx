// src/App.tsx
import React, { useEffect, useState } from 'react';
import FileList from '../components/fileManagerComponents/FileList';
import { Box, Container, CssBaseline, Grid, Theme, ThemeProvider, Typography, styled, MenuItem, Select, FormControl, InputLabel, SelectChangeEvent } from '@mui/material';
import axios from 'axios';

interface FileManagerProps {
  theme: Theme;
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

interface Filters {
  ontology_name: string;
  algorithm: string;
  classifier: string;
}

const SectionGrid = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

export default function FileManager({ theme }: FileManagerProps) {
  const BACKEND_URI = import.meta.env.VITE_BACKEND_URI || "http://127.0.0.1:5000"

  const [fileStructure, setFileStructure] = useState<DataItem[]>([]);
  const [filters, setFilters] = useState({ ontology_name: '', algorithm: '', classifier: '' });

  const handleFilterChange = (event: SelectChangeEvent) => {
    const { name, value } = event.target;
    setFilters(prevFilters => ({ ...prevFilters, [name]: value }));

    if (filters.ontology_name === '') {
      setFilters({ ontology_name: '', algorithm: '', classifier: '' });
    } else if (filters.algorithm === '') {
      setFilters(prevFilters => ({ ...prevFilters, classifier: '' }));
    }
  };

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

  // Function to convert hex string to byte array
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

          // Convert hex string back to byte array
          const byteArray = hexToByteArray(response.data.file);

          // Create a Blob object from byte array
          const blob = new Blob([byteArray], { type: 'application/zip' });

          // Create a temporary URL to download the blob
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', ontologyName+'.zip');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }
      })
      .catch((error) => {
        console.log("Get file failed:", error);
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
          <Box sx={{ display: 'flex', alignItems: "center" }}>
            <Typography variant="h2" gutterBottom>
              File Manager
            </Typography>
          </Box>
        </SectionGrid>
        <SectionGrid item xs={12}>
          <FileList data={fileStructure} handleDownload={handleDownload} />
        </SectionGrid>
      </Grid>
    </ThemeProvider>
  );
};
