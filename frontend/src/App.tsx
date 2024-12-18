import React, { useState, useEffect } from "react";
import logo from "./common/logo2.png";
import {
  Container,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
  CircularProgress,
  Box,
  Snackbar,
  Alert,
} from "@mui/material";
import { styled } from "@mui/system";

interface SearchResult {
  name?: string[];
  image_url?: string[];
  introduction?: string[];
}

const LogoContainer = styled(Box)({
  display: "flex",
  flexDirection: "row",
  gap: "20px",
  alignItems: "center",
});

const SearchContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: theme.spacing(3),
  borderRadius: "8px",
  boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
  backgroundColor: "#e3fff5",
}));

const ResultsContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: theme.spacing(3),
  marginTop: theme.spacing(4),
  borderRadius: "8px",
  boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
  backgroundColor: "#e3fff5",
}));

const ResultItem = styled(ListItem)({
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  gap: "24px",
  borderBottom: "1px solid #ddd",
});

const SolrSearchApp: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState<boolean>(false); // Estado para rastrear se uma busca foi realizada
  const [openSnackbar, setOpenSnackbar] = useState<boolean>(false); // Estado para controlar o Snackbar

  useEffect(() => {
  }, [query]);

  useEffect(() => {
    console.log("Results state changed:", results);
  }, [results]);

  const fetchData = async () => {
    console.log("fetchData called");
    if (query.trim() === "") {
      setResults([]);
      setHasSearched(false); // Resetar se a consulta estiver vazia
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(false); // Opcional: pode definir como true aqui se preferir

    try {
      const solrQuery = encodeURIComponent(query);
      const url = `http://localhost:3000/solr/species/select?defType=edismax&indent=true&q.op=AND&q=${solrQuery}&qf=introduction%20sections&wt=json`;
      console.log("Fetching URL:", url);

      const response = await fetch(url);
      console.log("Fetch response:", response);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Response JSON:", data);
      setResults(data.response.docs);
      setHasSearched(true); // Definir como true após obter resultados
    } catch (error) {
      console.error("Error in fetchData:", error);
      setError("No results found. Please try again."); 
      setOpenSnackbar(true); // Abrir o Snackbar para mostrar o erro
      setHasSearched(false); // Garantir que o ResultsContainer não seja exibido
    } finally {
      setLoading(false);
    }
  };

  const handleSnackbarClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === "clickaway") {
      return;
    }
    setOpenSnackbar(false);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: hasSearched ? "flex-start" : "center",
        alignItems: "center",
        padding: 2,
      }}
    >
      <Container maxWidth="md">
        <SearchContainer>
          <LogoContainer>
            <img className="logoimage" src={logo} alt="BioFinder Logo" />
            <Typography variant="h4">BioFinder</Typography>
          </LogoContainer>
          <Box className="header-contents" sx={{ width: "100%", mt: 2 }}>
            
          </Box>
          <TextField
            label="Search"
            variant="outlined"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ex.: Venomous snakes in Portugal"
            fullWidth
            sx={{ mt: 2 }}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                fetchData();
              }
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={fetchData}
            disabled={loading}
            sx={{ mt: 2, width: "150px", alignSelf: "flex-start" }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : "Search"}
          </Button>
        </SearchContainer>

        {/* Renderizar ResultsContainer apenas se hasSearched for true e resultados existirem */}
        {hasSearched && (
          <ResultsContainer>
            <Typography variant="h5" gutterBottom>
              Search Results
            </Typography>
            <Typography variant="body1">Current Query: {query}</Typography>
            <Typography variant="body1">Total of Results: {results.length}</Typography>
            {results.length > 0 ? (
              <List sx={{ width: "100%" }}>
                {results.map((result, index) => (
                  <ResultItem key={index}>
                    <Box>
                      <img
                        src={
                          result.image_url?.[0]?.includes("icon_edit")
                            ? "https://via.placeholder.com/150"
                            : result.image_url?.[0] || "https://via.placeholder.com/150"
                        }
                        alt={
                          result.image_url?.[0]?.includes("icon_edit")
                            ? "No image available."
                            : result.name?.[0] || "No image available."
                        }
                        style={{ width: "150px", height: "auto", borderRadius: "4px" }}
                      />
                    </Box>
                    <Box>
                      <Typography variant="h6">
                        {result.name?.[0] || "No name available."}
                      </Typography>
                      <Typography variant="body2">
                        {result.introduction?.[0] || "No introduction available."}
                      </Typography>
                    </Box>
                  </ResultItem>
                ))}
              </List>
            ) : (
              <Typography variant="body1">
                {loading ? "Loading..." : "No results found :("}
              </Typography>
            )}
          </ResultsContainer>
        )}
      </Container>

      {/* Snackbar para exibir erros */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert onClose={handleSnackbarClose} severity="error" sx={{ width: "100%" }}>
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default SolrSearchApp;
