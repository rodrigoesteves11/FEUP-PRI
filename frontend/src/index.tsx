import React from "react";
import ReactDOM from "react-dom/client"; 
import SolrSearchApp from "./App";
import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./theme/theme"; 
import "./App.css";


const container = document.getElementById("root");

if (!container) {
  throw new Error("O elemento com id 'root' não foi encontrado no HTML.");
}

const root = ReactDOM.createRoot(container);

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SolrSearchApp />
    </ThemeProvider>
  </React.StrictMode>
);
