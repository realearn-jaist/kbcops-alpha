import React from "react";
import {
  Box,
  Typography,
  Grid,
  Paper,
  Link,
  styled,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";
import StatCard from "./MainComponents/StatCard";
import Title from "./MainComponents/Title";
import GarbageMetrics from "./MainComponents/GarbageMetrics";

function Copyright(props: any) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="#">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const drawerWidth: number = 300;

// Styled component for the main content area, adjusting width and margin based on drawer state
const MainWrapper = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })<{
  open?: boolean;
}>(({ theme, open }) => ({
  flexGrow: 1,
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  alignItems: 'flex-start',
  width: `100vw`,
  marginLeft: `-${drawerWidth}px`,
  ...(open && {
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    width: `calc(100vw - ${drawerWidth}px)`,
    marginLeft: 0,
  }),
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
  open: boolean;
  ontology_name: string;
  onto_data: {
    no_class: number;
    no_individual: number;
    no_axiom: number;
    no_annotation: number;
  };
  algo: string;
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

// Main component
const Main: React.FC<MainProps> = ({ open, ontology_name, onto_data, algo, eval_metric, garbage_metric, garbage_image }) => {
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
    <MainWrapper open={open} sx={{ mt: 8, overflow: "hidden" }}>
      <Box
        component="main"
        sx={{
          backgroundColor: (theme) =>
            theme.palette.mode === 'light'
              ? theme.palette.grey[100]
              : theme.palette.grey[900],
          overflow: 'auto',
          justifyContent: 'center',
          flexGrow: 1
        }}
      >
        <Box
          sx={{
            bgcolor: '#f5f5f5', // Gray background color
            margin: '10px',
            maxWidth: '1200px',
          }}
        >
          {/* Display ontology ID and TBox/ABox information */}
          <Box sx={{ display: 'flex', alignItems: "center" }}>
            <Typography variant="h2" gutterBottom>
              {ontology_name}
            </Typography>
            <Box component="section" sx={{ p: 2, border: '1px dashed grey', height: "72px", margin: "0px 0px 21px 20px", borderRadius: "10px", background: "gray" }}>
              <Typography variant="h4" gutterBottom>
                {onto_data.no_individual > 0 ? "TBox & ABox" : "TBox"}
              </Typography>
            </Box>
          </Box>

          {/* Stat cards displaying ontology data */}
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

          <br />
          <Divider />
          <br />

          {/* Display algorithm name and evaluation metrics */}
          <Typography variant="h2" gutterBottom>
            {algo}
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} lg={3}>
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
            <Grid item xs={12} md={6} lg={3}>
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
            <Grid item xs={12} md={12} lg={6}>
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
                    bgcolor: 'background.paper',
                    color: 'text.secondary',
                    '& svg': {
                      m: 1,
                    },
                    '& hr': {
                      mx: 0.5,
                    },
                  }}
                >
                  <Box sx={{ display: "flex", flexGrow: 1 }}>
                    <Typography component="p" variant="h6" color="primary">
                      {"K=1"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
                        {(Math.round(eval_metric.hit_at_1 * 10000) / 100).toFixed(2)}%
                      </Typography>
                    </Box>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ display: "flex", flexGrow: 1 }}>
                    <Typography component="p" variant="h6" color="primary">
                      {"K=5"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
                        {(Math.round(eval_metric.hit_at_5 * 10000) / 100).toFixed(2)}%
                      </Typography>
                    </Box>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ display: "flex", flexGrow: 1 }}>
                    <Typography component="p" variant="h6" color="primary">
                      {"K=10"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
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
                    bgcolor: 'background.paper',
                    color: 'text.secondary',
                    '& svg': {
                      m: 1,
                    },
                    '& hr': {
                      mx: 0.5,
                    },
                  }}
                >
                  <Box sx={{ display: "flex", flexGrow: 1 }}>
                    <Typography component="p" variant="h6" color="primary">
                      {"Total"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
                        {eval_metric.total === 0 ? "None" : String(eval_metric.garbage) + "/" + String(eval_metric.total)}
                      </Typography>
                    </Box>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ display: "flex", flexGrow: 1 }}>
                    <Typography component="p" variant="h6" color="primary">
                      {"Percent"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
                        {eval_metric.total === 0 ? "None" : String((Math.round(eval_metric.garbage/eval_metric.total * 10000) / 100).toFixed(2)) + "%"}
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

          {/* Dropdown for selecting garbage metrics */}
          <FormControl fullWidth sx={{ margin: "20px 0px" }}>
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

          {/* Display selected garbage image */}
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <img
              src={`data:image/png;base64,${garbage_image.length > 0 ? garbage_image[garbageIndex].image : "none"}`}
              alt="displayed"
              style={{ maxHeight: '100%', maxWidth: '100%' }}
            />
          </Paper>
          <br />

          {/* Display selected garbage metrics */}
          <GarbageMetrics garbage_metric={garbage_metric} garbageIndex={garbageIndex} />
        </Box>
        <Copyright />
      </Box>
    </MainWrapper>
  );
};

export default Main;
