import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import axios from 'axios';

import MyAppBar from '../components/MyAppBar';
import MyDrawer from '../components/MyDrawer';
import Main from '../components/Main';

// Define the theme for the app
const defaultTheme = createTheme();

export default function Dashboard() {
  const BACKEND_URI = import.meta.env.VITE_BACKEND_URI || "http://127.0.0.1:5000"

  // State variables
  const [open, setOpen] = React.useState(true);
  const [selectedFiles, setSelectedFiles] = React.useState<File[]>([]);
  const [fileId, setFileId] = React.useState("");
  const [ontologyList, setOntologyList] = React.useState<string[]>([]);
  const [displayOntoId, setDisplayOntoId] = React.useState<string>("<Ontology>");
  const [displayOntoData, setDisplayOntoData] = React.useState<{
    no_class: number;
    no_individual: number;
    no_axiom: number;
    no_annotation: number;
  }>({ no_class: 0, no_individual: 0, no_axiom: 0, no_annotation: 0 });
  const [displayAlgo, setDisplayAlgo] = React.useState<string>("<Embedding Algorithm>");
  const [displayEvalMetric, setDisplayEvalMetric] = React.useState<{
    mrr: number,
    hit_at_1: number,
    hit_at_5: number,
    hit_at_10: number,
    garbage: number
  }>({ mrr: 0, hit_at_1: 0, hit_at_5: 0, hit_at_10: 0, garbage: 0 });

  // Types for garbage metrics and images
  type GarbageMetric = {
    Individual: string;
    Predicted: string;
    Predicted_rank: number;
    True: string;
    True_rank: number;
    Score_predict: number;
    Score_true: number;
    Dif: number;
  };
  const [displayGarbageMetric, setDisplayGarbageMetric] = React.useState<GarbageMetric[]>([]);

  type GarbageImage = {
    image: string;
  };
  const [displayGarbageImage, setDisplayGarbageImage] = React.useState<GarbageImage[]>([]);

  // Fetch the ontology list when the component mounts
  React.useEffect(() => {
    getOntologyList();
  }, []);

  // Toggle the drawer open/close state
  const toggleDrawer = () => {
    setOpen(!open);
  };

  // Handle file selection
  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles(files);

    if (files.length > 0) {
      setFileId(files[0].name);
    }
  };

  // Handle file upload
  const handleUpload = () => {
    const file = selectedFiles[0];
    const formData = new FormData();
    formData.append('owl_file', file);
    formData.append('onto_id', fileId);

    axios.post(`${BACKEND_URI}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then((response) => {
      console.log("Upload successful:", response.data);
      getOntologyList();
      extractOntology(response.data.onto_id);
    })
    .catch((error) => {
      console.error("Upload failed:", error);
    });
  };

  // Extract ontology data
  const extractOntology = (onto_id: string) => {
    axios.get(`${BACKEND_URI}/extract/${onto_id}`)
    .then((response) => {
      console.log("Extract successful:", response.data);
      setDisplayOntoId(onto_id);
      setDisplayOntoData(response.data.onto_data);
    })
    .catch((error) => {
      console.error("Extract failed:", error);
    });
  };

  // Fetch ontology statistics
  const getOntologyStat = (onto_id: string) => {
    axios.get(`${BACKEND_URI}/ontology/${onto_id}`)
    .then((response) => {
      console.log("Get stat successful:", response.data);
      setDisplayOntoId(onto_id);
      setDisplayOntoData(response.data.onto_data);
    })
    .catch((error) => {
      console.error("Get stat failed:", error);
    });
  };

  // Fetch the ontology list
  const getOntologyList = () => {
    axios.get(`${BACKEND_URI}/ontology`)
    .then((response) => {
      console.log("Load successful:", response.data);
      setOntologyList(response.data.onto_list);
    })
    .catch((error) => {
      console.error("Load failed:", error);
    });
  };

  // Train the embedder
  const trainEmbedder = (onto_id: string, algo: string) => {
    axios.get(`${BACKEND_URI}/embed/${onto_id}?algo=${algo}`)
    .then((response) => {
      console.log("Embed successful:", response.data);
      evaluateEmbedder(response.data.onto_id, response.data.algo);
    })
    .catch((error) => {
      console.error("Embed failed:", error);
    });
  };

  // Evaluate the embedder
  const evaluateEmbedder = (onto_id: string, algo: string) => {
    axios.get(`${BACKEND_URI}/evaluate/${onto_id}/${algo}`)
    .then((response) => {
      console.log("Evaluate successful:", response.data);
      getOntologyStat(onto_id);
      setDisplayAlgo(algo);
      setDisplayEvalMetric(response.data.performance);
      setDisplayGarbageMetric(response.data.garbage);
      setDisplayGarbageImage(response.data.images);
    })
    .catch((error) => {
      console.error("Evaluate failed:", error);
    });
  };

  // Fetch evaluation statistics
  const getEvaluate = (onto_id: string, algo: string) => {
    if (onto_id === "" || algo === "") return;

    getOntologyStat(onto_id);
    setDisplayAlgo(algo);

    axios.get(`${BACKEND_URI}/evaluate/${onto_id}/${algo}/stat`)
    .then((response) => {
      console.log("Get evaluate stat successful:", response.data);
      setDisplayEvalMetric(response.data.performance);
      setDisplayGarbageMetric(response.data.garbage);
      setDisplayGarbageImage(response.data.images);
    })
    .catch((error) => {
      console.error("Get evaluate stat failed:", error);
      setDisplayEvalMetric({ mrr: 0, hit_at_1: 0, hit_at_5: 0, hit_at_10: 0, garbage: 0 });
      setDisplayGarbageMetric([]);
      setDisplayGarbageImage([]);
    });
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <MyAppBar open={open} toggleDrawer={toggleDrawer} />
        <MyDrawer
          open={open}
          toggleDrawer={toggleDrawer}
          selectedFiles={selectedFiles}
          fileId={fileId}
          setFileId={setFileId}
          handleUpload={handleUpload}
          ontologyList={ontologyList}
          handleFilesSelected={handleFilesSelected}
          trainEmbedder={trainEmbedder}
          getEvaluate={getEvaluate}
        />
        
        <Main
          open={open}
          onto_id={displayOntoId}
          onto_data={displayOntoData}
          algo={displayAlgo}
          eval_metric={displayEvalMetric}
          garbage_metric={displayGarbageMetric}
          garbage_image={displayGarbageImage}
        />
      </Box>
    </ThemeProvider>
  );
}
