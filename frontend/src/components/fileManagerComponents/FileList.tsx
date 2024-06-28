import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  Button,
  Collapse,
  IconButton,
  Card,
  CardContent,
  Grid,
  Typography
} from '@mui/material';
import { ExpandLess, ExpandMore, Delete } from '@mui/icons-material';

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
  alias: string; // Added alias field
  algorithm: Algorithm[];
  process_files: ProcessFile[];
}

interface FileListProps {
  data: DataItem[];
  handleDownload: (ontologyName: string) => void;
  handleDelete: (ontologyName: string) => void;
  isAuthenticated: boolean;
}

export default function FileList({ data, handleDownload, handleDelete, isAuthenticated }: FileListProps) {
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
            <TableCell>Owner</TableCell>
            <TableCell>Created At</TableCell> {/* Added Created At column */}
            <TableCell>Download</TableCell>
            {isAuthenticated && <TableCell>Delete</TableCell>}
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
                <TableCell>
                  <Typography variant="body1">
                    {item.alias}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body1">
                    {item.created_at}
                  </Typography>
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
                {isAuthenticated && (
                  <TableCell style={{ whiteSpace: 'nowrap' }}>
                    <IconButton
                      color="secondary"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(item.name);
                      }}
                    >
                      <Delete />
                    </IconButton>
                  </TableCell>
                )}
              </TableRow>
              <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={isAuthenticated ? 5 : 4}>
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
}
