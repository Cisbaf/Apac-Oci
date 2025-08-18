import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

interface AccordionProps {
  title: string;
  children: React.ReactNode;
  defaultExpanded?: boolean; // <- nova prop opcional
}

export default function AccordionExpandIcon({ title, children, defaultExpanded = false }: AccordionProps) {
  return (
    <div>
      <Accordion defaultExpanded={defaultExpanded}>
        <AccordionSummary
          expandIcon={<ArrowDownwardIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
          sx={{backgroundColor: "#f5f5f5"}}>
          <Typography component="span">{title}</Typography>
        </AccordionSummary>
        <AccordionDetails>
          {children}
        </AccordionDetails>
      </Accordion>
    </div>
  );
}
