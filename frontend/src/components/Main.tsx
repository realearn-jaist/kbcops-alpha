import React from "react";
import { Box, Typography, Grid, Paper, Link, styled, Divider, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import StatCard from "./MainComponents/StatCard";
import Title from "./MainComponents/Title";
import RequestComponent from "./request_sender";

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

const drawerWidth: number = 240;

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
  onto_id: string;
  onto_data: {
    no_class: number;
    no_individual: number;
    no_axiom: number;
    no_annotation: number;
  };
  algo: string;
  eval_metric: {
    mrr: number,
    hit_at_1: number,
    hit_at_5: number,
    hit_at_10: number,
    garbage: number,
  };
  garbage_metric: GarbageMetric[],
  garbage_image: GarbageImage[],
}

const Main: React.FC<MainProps> = ({ open, onto_id, onto_data, algo, eval_metric, garbage_metric, garbage_image }) => {
  const StatCards = [
    { name: 'Classes', data: onto_data.no_class },
    { name: 'Individuals', data: onto_data.no_individual },
    { name: 'Axioms', data: onto_data.no_axiom },
    { name: 'Annotations', data: onto_data.no_annotation }
  ];

  const [garbageIndex, setGarbageIndex] = React.useState<number>(0);

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
          <Box sx={{ display: 'flex', alignItems: "center" }}>
            <Typography variant="h2" gutterBottom>
              {onto_id}
            </Typography>
            <Box component="section" sx={{ p: 2, border: '1px dashed grey', height: "72px", margin: "0px 0px 21px 20px", borderRadius: "10px", background: "gray" }}>
              <Typography variant="h4" gutterBottom>
                {onto_data.no_individual > 0 ? "TBox & Abox" : "TBox"}
              </Typography>

            </Box>
          </Box>

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

          <Typography variant="h2" gutterBottom>
            {algo}
          </Typography>
          <Grid container spacing={3}>
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
                      {"1"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
                        {(Math.round(eval_metric.hit_at_1 * 100) / 100).toFixed(2)}
                      </Typography>
                    </Box>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ display: "flex", flexGrow: 1 }}>
                    <Typography component="p" variant="h6" color="primary">
                      {"5"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
                        {(Math.round(eval_metric.hit_at_5 * 100) / 100).toFixed(2)}
                      </Typography>
                    </Box>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ display: "flex", flexGrow: 1 }}>
                    <Typography component="p" variant="h6" color="primary">
                      {"10"}
                    </Typography>
                    <Box sx={{ flexGrow: 1, display: "flex", justifyContent: "center" }}>
                      <Typography component="p" variant="h4" color="black">
                        {(Math.round(eval_metric.hit_at_10 * 100) / 100).toFixed(2)}
                      </Typography>
                    </Box>
                  </Box>
                </Box>

              </Paper>
            </Grid>
            <Grid item xs={12} md={12} lg={3}>
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
            <Grid item xs={12} md={12} lg={3}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 150,
                }}
              >
                <StatCard name={"Garbage"} data={eval_metric.garbage} type="int" />
              </Paper>
            </Grid>


          </Grid>

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

          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              // height: 500,
            }}
          >
            <img
              src={`data:image/png;base64,${garbage_image.length > 0? garbage_image[garbageIndex].image : "none"}`}
              alt="displayed"
              style={{ maxHeight: '100%', maxWidth: '100%' }}
            />
          </Paper>
          <br />
          <Grid container spacing={3}>

            <Grid item xs={12} md={6} lg={3}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 70,
                }}
              >
                <Typography variant="h6">
                  Ground Truth Score: {
                    (garbage_metric.length > 0) ?
                      (Math.round(garbage_metric[garbageIndex].Score_true * 100) / 100).toFixed(2) :
                      (Math.round(0)).toFixed(2)
                  }
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6} lg={3}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 70,
                }}
              >
                <Typography variant="h6">
                  Ground Truth Rank: {
                    (garbage_metric.length > 0) ?
                      garbage_metric[garbageIndex].True_rank :
                      0
                  }
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6} lg={3}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 70,
                }}
              >
                <Typography variant="h6">
                  Garbage Score: {
                    (garbage_metric.length > 0) ?
                      (Math.round(garbage_metric[garbageIndex].Score_predict * 100) / 100).toFixed(2) :
                      (Math.round(0)).toFixed(2)
                  }
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6} lg={3}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 70,
                }}
              >
                <Typography variant="h6">
                  Garbage Rank: {
                    (garbage_metric.length > 0) ?
                      garbage_metric[garbageIndex].Predicted_rank :
                      0
                  }
                </Typography>
              </Paper>
            </Grid>
          </Grid>


        </Box>
        <Copyright />
        {/* <RequestComponent /> */}
      </Box>
    </MainWrapper>
  );
};

export default Main;
