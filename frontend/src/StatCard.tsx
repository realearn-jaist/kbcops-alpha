import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';

// Correct function component definition with props type
const StatC: React.FC<{
  name: string;
  data: number;
}> = ({ name, data }) => {
  return (
    <React.Fragment>
      <Title>{name}</Title>
      <Typography component="p" variant="h4">
        {data}
      </Typography>
    </React.Fragment>
  );
};

export default StatC;
