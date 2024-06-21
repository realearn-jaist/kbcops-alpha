import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';

// Correct function component definition with props type
const StatC: React.FC<{
  name: string;
  data: number;
  type: string;
}> = ({ name, data, type }) => {
  return (
    <React.Fragment>
      <Title>{name}</Title>
      <Typography component="p" variant="h4">
        {type == "float" ? (Math.round(data * 100) / 100).toFixed(2) : Math.round(data)}
      </Typography>
    </React.Fragment>
  );
};

export default StatC;
