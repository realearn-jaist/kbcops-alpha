import { useEffect, useState } from 'react';
import { Box, Grid, Theme, ThemeProvider, Typography, styled } from '@mui/material';
import { CssBaseline } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

interface InfoProps {
  theme: Theme;
}

const SectionGrid = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

const markdownContent = `
# Knowledge Base Completion Operations (KBCOps)

## What is Knowledge Base Completion (KBC)?

Knowledge Base Completion (KBC) is a task in Knowledge Graph (KG) completion that aims to predict missing relationships or facts in a knowledge base. The goal is to infer new knowledge based on existing information in the knowledge graph. Key points related to KBC include:

- **Task Definition:** KBC involves predicting missing links or triples in a knowledge graph by leveraging the existing information and relationships within the graph.

- **Methods:** Various machine learning and knowledge representation techniques are used for KBC, including embedding models (e.g., TransE, DistMult), rule-based reasoning, and neural network architectures.

- **Applications:** KBC has applications in recommendation systems, question answering, information retrieval, and semantic search, where completing the knowledge graph can enhance the performance of these tasks.

## Introduction of this project

Knowledge bases (KBs), particularly ontologies, are often incomplete, necessitating the need for Knowledge Base Completion. One critical aspect to consider in KB completion is the presence of **"garbage"** information. In this context, **"garbage"** refers to implicit or duplicated facts that do not contribute meaningfully to the completeness of the ontology.

These tools are designed to provide users with the ability to compare and evaluate the presence of garbage across different algorithms and ontologies used in KB completion operations. By offering transparency and insights into the quality of completion results, the monitoring tools aim to empower users to make informed decisions and optimize the completeness of knowledge bases effectively.

## Key Features

- **Upload Ontology**: Allows users to upload ontologies for processing and analysis.

- **Get Stats of Ontology**: Provides statistics of the uploaded ontology, such as the number of axioms, individuals, classes, etc.

- **Selecting Embedding Algorithms**: Users can choose from various embedding algorithms:

  - Onto2Vec
  - OPA2Vec
  - RDF2Vec
  - OWL2Vec\*

- **Display Embedding Prediction Stats**: Shows statistics of the embedding's predictions, including metrics like Hit@K, MRR (Mean Reciprocal Rank), etc.

- **Display Garbage**: Users can visualize garbage relationships in the graph, aiding in the identification and removal of erroneous or irrelevant data.

## Paper

#### **Title:** Are Embeddings All We Need for Knowledge Base Completion? Insights from Description Logicians

**Abstract:** Description Logic knowledge bases (KBs), i.e., ontologies, are often greatly incomplete, necessitating a demand for KB completion. Promising approaches to this aim are to embed KB elements such as classes, properties, and logical axioms into a low-dimensional vector space and and find missing elements by inferencing on the latent representation. Because these approaches make inference based solely on existing facts in KBs, the risk is that likelihood of KB completion with implicit (duplicated) facts could be high, making the performance of KB embedding models questionable. Thus, it is essential for the KB completion's procedure to prevent completing KBs by implicit facts. In this short paper, we present a new perspective of this problem based on the logical constructs in description logic. We also introduce a novel recipe for KB completion operations called KBCOps and include a demo that exhibits KB completion with fact duplication when using state-of-the-art KB embedding algorithms.

## Authors and Contacts (Alphabetical Order)

- **Chaphowasit Mahayossanan (Mahidol University, Thailand)**

  - Email: chaphowasit.mah@student.mahidol.edu

- **Teerapat Phopit (Mahidol University, Thailand)**

  - Email: teerapat.pho@student.mahidol.edu

- **Teeradaj Racharak (JAIST, Japan)**

  - Email: racharak@jaist.ac.jp

- **Kiattiphum Suwanarsa (Mahidol University, Thailand)**
  - Email: kiattiphum.intern@gmail.com

## References

- [OWL2Vec-Star](https://github.com/KRR-Oxford/OWL2Vec-Star)

- [kbc-ops](https://github.com/realearn-jaist/kbc-ops)
`;

export default function Info({ theme }: InfoProps) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SectionGrid container spacing={2}>
        <Grid item xs={12}>
        <Box padding={8}>
        <ReactMarkdown>{markdownContent}</ReactMarkdown>
          </Box>
          
        </Grid>
      </SectionGrid>
    </ThemeProvider>
  );
}
