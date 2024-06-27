import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, Button, Collapse, IconButton, Card, CardContent, Grid, Typography } from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import axios from 'axios';

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

interface FileListProps {
  data: DataItem[];
  handleDownload: (ontologyName: string) => void;
}

export default function FileList({ data, handleDownload }: FileListProps) {
  const [openRows, setOpenRows] = useState<{ [key: string]: boolean }>({});

  const handleRowClick = (ontologyName: string) => {
    setOpenRows(prevState => ({ ...prevState, [ontologyName]: !prevState[ontologyName] }));
  };

  return (

    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Ontology</TableCell>
            <TableCell>Download</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item, index) => (
            <React.Fragment key={index}>
              <TableRow onClick={() => handleRowClick(item.name)} style={{ cursor: 'pointer' }}>
                <TableCell>
                  <Box display={"flex"}>
                    <Typography variant="subtitle1">
                      {item.name}
                    </Typography>
                    <IconButton size="small">
                      {openRows[item.name] ? <ExpandLess /> : <ExpandMore />}
                    </IconButton>
                  </Box>

                </TableCell>
                <TableCell style={{ whiteSpace: 'nowrap' }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDownload(item.name);
                    }}
                  >
                    Download
                  </Button>
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={2}>
                  <Collapse in={openRows[item.name]} timeout="auto" unmountOnExit>
                    <Box margin={1}>
                      {item.algorithm.length > 0 ? (
                        item.algorithm.map((algo, algoIndex) => (
                          <Card key={algoIndex} variant="outlined" style={{ marginBottom: '1rem' }}>
                            <CardContent>
                              <Typography variant="subtitle1">
                                {algo.name}
                              </Typography>
                              <Grid container spacing={1} style={{ marginTop: '0.5rem' }}>
                                {algo.classifier.map((classif, classifIndex) => (
                                  <Grid item xs={12} sm={6} md={4} lg={3} key={classifIndex}>
                                    <Card variant="outlined">
                                      <CardContent>
                                        <Typography variant="body2">
                                          {classif.name}
                                        </Typography>
                                      </CardContent>
                                    </Card>
                                  </Grid>
                                ))}
                              </Grid>
                            </CardContent>
                          </Card>
                        ))
                      ) : (
                        <Typography variant="body2" color="textSecondary">
                          No algorithms available.
                        </Typography>
                      )}
                    </Box>
                  </Collapse>
                </TableCell>
              </TableRow>
            </React.Fragment>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
