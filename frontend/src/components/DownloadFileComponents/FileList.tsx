// src/components/FileList.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { 
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';

interface File {
  name: string;
  path: string;
}

const FileList: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);

  useEffect(() => {
    // axios.get('/api/files')  // Replace with your API endpoint
    //   .then(response => {
    //     setFiles(response.data);
    //   })
    //   .catch(error => {
    //     console.error('Error fetching files:', error);
    //   });
  }, []);

  const handleCheckboxChange = (filePath: string) => {
    setSelectedFiles(prevSelected =>
      prevSelected.includes(filePath)
        ? prevSelected.filter(path => path !== filePath)
        : [...prevSelected, filePath]
    );
  };

  const handleDownload = () => {
    selectedFiles.forEach(file => {
      axios.get(`/api/download?file=${encodeURIComponent(file)}`, {
        responseType: 'blob',
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', file.split('/').pop() || 'file');
        document.body.appendChild(link);
        link.click();
        link.parentNode?.removeChild(link);
      })
      .catch(error => {
        console.error('Error downloading file:', error);
      });
    });
  };

  return (
    <Box sx={{ p: 3 }}>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>File Name</TableCell>
              <TableCell>Download</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {files.map((file) => (
              <TableRow key={file.path}>
                <TableCell>{file.name}</TableCell>
                <TableCell>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={selectedFiles.includes(file.path)}
                        onChange={() => handleCheckboxChange(file.path)}
                      />
                    }
                    label="Select"
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Button
        variant="contained"
        color="primary"
        onClick={handleDownload}
        disabled={selectedFiles.length === 0}
        sx={{ mt: 2 }}
      >
        Download Selected
      </Button>
    </Box>
  );
};

export default FileList;
