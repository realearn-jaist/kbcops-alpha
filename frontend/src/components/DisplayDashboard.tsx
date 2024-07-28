import * as React from 'react';

import Grid from '@mui/material/Grid';
import { styled } from '@mui/system';
import { Box, Divider, FormControl, InputLabel, MenuItem, Paper, Select, SelectChangeEvent, Typography } from '@mui/material';
import StatCard from './displayDashboardComponents/StatCard';
import Title from './displayDashboardComponents/Title';
import GarbageMetrics from './displayDashboardComponents/GarbageMetrics';
import InfoButton from './displayDashboardComponents/InfoButton';
import Graphviz from 'graphviz-react';

const SectionGrid = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

// Type definitions for the component props and data structures
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

type GarbageImage = {
  dot_file: string;
};

interface MainProps {
  ontology_name: string;
  onto_data: {
    no_class: number;
    no_individual: number;
    no_axiom: number;
    no_annotation: number;
  };
  algo: string;
  classifier: string;
  eval_metric: {
    mrr: number;
    hit_at_1: number;
    hit_at_5: number;
    hit_at_10: number;
    garbage: number;
    total: number;
    average_garbage_Rank: number;
    average_Rank: number;
  };
  setGarbageIndex: (value: number) => void;
  garbageIndex: number;
  garbage_metric: GarbageMetric[];
  garbage_image: GarbageImage[];
}


export default function DisplayDashboard({ ontology_name, onto_data, algo, classifier, eval_metric, setGarbageIndex, garbageIndex, garbage_metric, garbage_image }: MainProps) {
  const StatCards = [
    { name: 'Classes', data: onto_data.no_class },
    { name: 'Individuals', data: onto_data.no_individual },
    { name: 'Axioms', data: onto_data.no_axiom },
    { name: 'Annotations', data: onto_data.no_annotation }
  ];

  React.useEffect(() => {
    // Check if garbageIndex is out of bounds
    if (garbageIndex < 0 || garbageIndex >= garbage_image.length || garbageIndex >= garbage_metric.length) {
      setGarbageIndex(0); // Reset to 0 or adjust as per your business logic
    }
  }, [garbage_image, garbage_metric]); // Run effect whenever garbage_image or garbage_metric changes

  const handleGarbageChange = (event: SelectChangeEvent<string>) => {
    const newIndex = parseInt(event.target.value, 10); // Assuming event.target.value is the index selected

    // Ensure the newIndex is within bounds of garbage_image and garbage_metric
    if (newIndex >= 0 && newIndex < garbage_image.length && newIndex < garbage_metric.length) {
      setGarbageIndex(newIndex);
    } else {
      setGarbageIndex(0); // If newIndex is out of bounds, reset to 0 or adjust as per your business logic
    }
  };

  return (
    <Grid container spacing={3}>
      {/* Display ontology ID and TBox/ABox information */}
      <SectionGrid item xs={12}>
        <Box display={"flex"} justifyContent='space-between' alignContent={'center'} margin="20px 0px 0px 0px" >
          <Typography variant="h2" gutterBottom>
            {ontology_name}: {ontology_name !== "<Ontology>" ? (onto_data.no_individual > 0 ? "TBox & ABox" : "TBox") : "None"}
          </Typography>
          <InfoButton
            title="Ontology Data"
            description={{
              main_description: `The statistics value of '${ontology_name}' ontology`,
              sub_description: {
                Classes: `Number of classes: ${onto_data.no_class}`,
                Individuals: `Number of individuals: ${onto_data.no_individual}`,
                Axioms: `Number of axioms: ${onto_data.no_axiom}`,
                Annotations: `Number of annotations: ${onto_data.no_annotation}`
              }
            }}
          />
        </Box>
      </SectionGrid>

      {/* Stat cards displaying ontology data */}
      <SectionGrid item xs={12}>
        <Grid container spacing={3}>
          {StatCards.map((stat, index) => (
            <Grid item xs={12} md={6} lg={3} key={index}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 150,
                }}
              >
                <StatCard name={stat.name} data={stat.data} type="int" />
              </Paper>
            </Grid>
          ))}
        </Grid>
      </SectionGrid>

      {/* Display algorithm name and classifier*/}
      <SectionGrid item xs={12}>
        <Box display={"flex"} justifyContent='space-between' alignContent={'center'} margin="20px 0px 0px 0px">
          <Typography variant="h2" gutterBottom>
            {algo}: {classifier}
          </Typography>
          <InfoButton
            title="Ontology Data"
            description={{
              main_description: `The statistics value of '${ontology_name}' ontology to be embedding with '${algo}', and evaluate the link prediction with '${classifier}'.`,
              sub_description: {
                "Total Test Sample": `Amount of test samples that randomly picked from the ontology (20% of ...): ${eval_metric.total}`,
                "MRR": `Mean Reciprocal Rank (MRR): ${eval_metric.mrr.toFixed(2)}`,
                "Hit@K=1": `Hit@K=1: ${(Math.round(eval_metric.hit_at_1 * 10000) / 100).toFixed(2)}%`,
                "Hit@K=5": `Hit@K=5: ${(Math.round(eval_metric.hit_at_5 * 10000) / 100).toFixed(2)}%`,
                "Hit@K=10": `Hit@K=10: ${(Math.round(eval_metric.hit_at_10 * 10000) / 100).toFixed(2)}%`,
                "Garbage / Total": `The ratio of garbage that have found by test sample: ${eval_metric.total === 0 ? "None" : `${eval_metric.garbage}/${eval_metric.total}`}`,
                "Percent": `The percentage of garbage that have found by test sample: ${eval_metric.total === 0 ? "None" : `${(Math.round(eval_metric.garbage / eval_metric.total * 10000) / 100).toFixed(2)}%`}`,
                "Avg. Garbage Rank": `Average garbage rank: ${eval_metric.average_garbage_Rank}`,
                "Avg. Ground Truth Rank": `Average ground truth rank: ${eval_metric.average_Rank}`
              }
            }}
          />
        </Box>

      </SectionGrid>

      {/* Display evaluation metrics */}
      <SectionGrid item xs={12}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 150,
              }}
            >
              <StatCard name={"Total Test Sample"} data={eval_metric.total} type="int" />
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 150,
              }}
            >
              <StatCard name={"MRR"} data={eval_metric.mrr} type="float" />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 150,
              }}
            >
              <Title>{"Hit@K"}</Title>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  '& svg': {
                    m: 1,
                  },
                  '& hr': {
                    mx: 0.5,
                  },
                }}
              >
                <Box sx={{ display: "flex", flexGrow: 1 }}>
                  <Typography component="p" variant="h6" >
                    {"K=1"}
                  </Typography>
                  <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                    <Typography component="p" variant="h4">
                      {(Math.round(eval_metric.hit_at_1 * 10000) / 100).toFixed(2)}%
                    </Typography>
                  </Box>
                </Box>
                <Divider orientation="vertical" flexItem />
                <Box sx={{ display: "flex", flexGrow: 1 }}>
                  <Typography component="p" variant="h6" >
                    {"K=5"}
                  </Typography>
                  <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                    <Typography component="p" variant="h4">
                      {(Math.round(eval_metric.hit_at_5 * 10000) / 100).toFixed(2)}%
                    </Typography>
                  </Box>
                </Box>
                <Divider orientation="vertical" flexItem />
                <Box sx={{ display: "flex", flexGrow: 1 }}>
                  <Typography component="p" variant="h6" >
                    {"K=10"}
                  </Typography>
                  <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                    <Typography component="p" variant="h4">
                      {(Math.round(eval_metric.hit_at_10 * 10000) / 100).toFixed(2)}%
                    </Typography>
                  </Box>
                </Box>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} md={12} lg={6}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 150,
              }}
            >
              <Title>{"Garbage / Total"}</Title>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  '& svg': {
                    m: 1,
                  },
                  '& hr': {
                    mx: 0.5,
                  },
                }}
              >
                <Box sx={{ display: "flex", flexGrow: 1 }}>
                  <Typography component="p" variant="h6" >
                    {"Total"}
                  </Typography>
                  <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                    <Typography component="p" variant="h4" >
                      {eval_metric.total === 0 ? "None" : String(eval_metric.garbage) + "/" + String(eval_metric.total)}
                    </Typography>
                  </Box>
                </Box>
                <Divider orientation="vertical" flexItem />
                <Box sx={{ display: "flex", flexGrow: 1 }}>
                  <Typography component="p" variant="h6" >
                    {"Percent"}
                  </Typography>
                  <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                    <Typography component="p" variant="h4" >
                      {eval_metric.total === 0 ? "None" : String((Math.round(eval_metric.garbage / eval_metric.total * 10000) / 100).toFixed(2)) + "%"}
                    </Typography>
                  </Box>
                </Box>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 150,
              }}
            >
              <StatCard name={"Avg. Garbage Rank"} data={eval_metric.average_garbage_Rank} type="int" />
            </Paper>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 150,
              }}
            >
              <StatCard name={"Avg. Ground Truth Rank"} data={eval_metric.average_Rank} type="int" />
            </Paper>
          </Grid>
        </Grid>
      </SectionGrid>

      {/* Display Garbage header*/}
      <SectionGrid item xs={12}>
        <Box display={"flex"} justifyContent='space-between' alignContent={'center'} margin="20px 0px 0px 0px">
          <Typography variant="h2" gutterBottom>
            Garbage
          </Typography>
          <InfoButton
            title="Garbage Metrics"
            description={{
              main_description: "Select and view details of garbage metrics for test individual/class that its rank differ most from the true classes (top 5)",
              sub_description: {

                "Color details (blue node)": "represents test individual/class for the prediction",
                "Color details (green node)": "represents true class (ground truth) of the test",
                "Color details (orange node)": "represent inferable node (garbage) that were predicted with higher score than the true class",
                "Color details (gray node)": "represent classes other than the above in the extracted relations",
                "Selected Garbage": garbage_metric.length > 0 ? (garbageIndex !== -1 ? garbage_metric[garbageIndex].Individual : "None selected") : "No garbage metrics available",
                "Ground Truth Score": garbage_metric.length > 0 ? (garbageIndex !== -1 ? `${(Math.round(garbage_metric[garbageIndex].Score_true * 10000) / 100).toFixed(2)}%` : "None selected") : "None selected",
                "Ground Truth Rank": garbage_metric.length > 0 ? (garbageIndex !== -1 ? `${garbage_metric[garbageIndex].True_rank}` : "None selected") : "None selected",
                "Garbage Score": garbage_metric.length > 0 ? (garbageIndex !== -1 ? `${(Math.round(garbage_metric[garbageIndex].Score_predict * 10000) / 100).toFixed(2)}%` : "None selected") : "None selected",
                "Garbage Rank": garbage_metric.length > 0 ? (garbageIndex !== -1 ? `${garbage_metric[garbageIndex].Predicted_rank}` : "None selected") : "None selected",
              }
            }}
          />
        </Box>
      </SectionGrid>

      {/* Dropdown for selecting garbage metrics */}
      <SectionGrid item xs={12}>
        <FormControl fullWidth>
          <InputLabel id="select-garbage-label">Select Garbage</InputLabel>
          <Select
            labelId="select-garbage-label"
            id="select-garbage"
            label="Select Garbage"
            value={garbageIndex === -1 ? "" : garbageIndex.toString()}
            onChange={handleGarbageChange}
            disabled={garbage_image.length === 0 || garbage_metric.length === 0}
          >
            {garbage_metric.map((garbage, index) => (
              <MenuItem key={index} value={index.toString()}>
                {garbage.Individual}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </SectionGrid>

      {/* Conditionally render sections below */}
      {garbageIndex !== -1 && garbage_image.length > 0 && garbage_metric.length > 0 && (
        <>
          {/* Display selected garbage image */}
          <SectionGrid item xs={12}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                backgroundColor: 'white',
                alignItems: 'center',
              }}
            >
              {garbage_image.length > 0 && (
                <Graphviz
                  dot={garbage_image[garbageIndex].dot_file}
                />
              )}
            </Paper>
          </SectionGrid>

          <SectionGrid item xs={12}>
            <GarbageMetrics garbage_metric={garbage_metric} garbageIndex={garbageIndex} />
          </SectionGrid>
        </>
      )}
    </Grid>
  );
}
