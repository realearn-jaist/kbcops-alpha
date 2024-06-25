import React from 'react';
import { Grid, Paper, Typography } from '@mui/material';

interface GarbageMetric {
    Score_true: number;
    True_rank: number;
    Score_predict: number;
    Predicted_rank: number;
}

interface GarbageMetricProps {
    garbage_metric: GarbageMetric[];
    garbageIndex: number;
}

const GarbageMetrics: React.FC<GarbageMetricProps> = ({ garbage_metric, garbageIndex }) => {
  const groundTruthScore = (garbage_metric.length > 0)
    ? (Math.round(garbage_metric[garbageIndex].Score_true * 10000) / 100).toFixed(2)
    : (Math.round(0)).toFixed(2);
  const groundTruthRank = (garbage_metric.length > 0)
    ? garbage_metric[garbageIndex].True_rank
    : 0;
  const garbageScore = (garbage_metric.length > 0)
    ? (Math.round(garbage_metric[garbageIndex].Score_predict * 10000) / 100).toFixed(2)
    : (Math.round(0)).toFixed(2);
  const garbageRank = (garbage_metric.length > 0)
    ? garbage_metric[garbageIndex].Predicted_rank
    : 0;

  return (
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
            Ground Truth Score: {groundTruthScore}%
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
            Ground Truth Rank: {groundTruthRank}
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
            Garbage Score: {garbageScore}%
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
            Garbage Rank: {garbageRank}
          </Typography>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default GarbageMetrics;
