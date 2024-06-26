import * as React from 'react';

import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Grid from '@mui/material/Grid';
import OutlinedInput from '@mui/material/OutlinedInput';
import { styled } from '@mui/system';
import { Box, Divider, FormControl, InputLabel, MenuItem, Paper, Select, SelectChangeEvent, Typography } from '@mui/material';
import StatCard from './displayDashboardComponents/StatCard';
import Title from './displayDashboardComponents/Title';
import GarbageMetrics from './displayDashboardComponents/GarbageMetrics';

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
  image: string;
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
  garbage_metric: GarbageMetric[];
  garbage_image: GarbageImage[];
}


export default function DisplayDashboard({ ontology_name, onto_data, algo, classifier, eval_metric, garbage_metric, garbage_image }: MainProps) {
  const StatCards = [
    { name: 'Classes', data: onto_data.no_class },
    { name: 'Individuals', data: onto_data.no_individual },
    { name: 'Axioms', data: onto_data.no_axiom },
    { name: 'Annotations', data: onto_data.no_annotation }
  ];

  const [garbageIndex, setGarbageIndex] = React.useState<number>(0);

  // Handler for changing the selected garbage metric
  const handleGarbageChange = (event: SelectChangeEvent<string>) => {
    setGarbageIndex(parseInt(event.target.value, 10));
  };

  return (
    <Grid container spacing={3}>
      {/* Display ontology ID and TBox/ABox information */}
      <SectionGrid item xs={12}>
        <Box sx={{ display: 'flex', alignItems: "center" }}>
          <Typography variant="h2" gutterBottom>
            {ontology_name}: {ontology_name !== "<Ontology>" ? (onto_data.no_individual > 0 ? "TBox & ABox" : "TBox") : "None"}
          </Typography>
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
        <Box sx={{ display: 'flex', alignItems: "center", margin: "20px 0px 0px 0px" }}>
          <Typography variant="h2" gutterBottom>
            {algo}: {classifier}
          </Typography>
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
              <StatCard name={"Total Validate Sample"} data={eval_metric.total} type="int" />
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

      {/* Dropdown for selecting garbage metrics */}
      <SectionGrid item xs={12}>
        <FormControl fullWidth sx={{ margin: "20px 0px 0px 0px" }}>
          <InputLabel id="select-garbage-label">Select Garbage</InputLabel>
          <Select
            labelId="select-garbage-label"
            id="select-garbage"
            label="Select Garbage"
            onChange={handleGarbageChange}
          >
            {garbage_metric.map((garbage, index) => (
              <MenuItem key={index} value={index}>
                {garbage.Individual}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </SectionGrid>

      {/* Display selected garbage image */}
      <SectionGrid item xs={12}>
        <Paper
          sx={{
            p: 2,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <img
            src={garbage_image.length > 0 ? `data:image/png;base64,${garbage_image[garbageIndex].image}` : "none"}
            alt="displayed"
            style={{ maxHeight: '100%', maxWidth: '100%' }}
          />
        </Paper>
      </SectionGrid>

      <SectionGrid item xs={12}>
        <GarbageMetrics garbage_metric={garbage_metric} garbageIndex={garbageIndex} />
      </SectionGrid>
    </Grid>
  );
}
