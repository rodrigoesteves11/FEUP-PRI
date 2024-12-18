import React, { useState, useEffect } from "react";
import logo from "./common/BioFinder.png";
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
  InputAdornment,
  IconButton,
  Grow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import { borderRadius, styled, keyframes } from "@mui/system";
import SearchIcon from "@mui/icons-material/Search";
import CloseIcon from "@mui/icons-material/Close";
import theme from "./theme/theme";
import AnimatedBackground from "./components/AnimatedBackground";


interface SearchResult {
  name?: string;
  image_url?: string;
  introduction?: string;
  conservation_status?: string;
  family?: string;
  genus?: string;
  id?: string;
  kingdom?: string;
  order?: string;
  sections?: string;
  species?: string;
  who_discovered?: string;
}

const removeItens: string[] = ["icon_edit", "Status_iucn"];

const shine = keyframes`
  to {
    background-position: 200% center;
  }
`;

const AnimatedBorderWrapper = styled("div")(({ theme }) => ({
  position: "relative",
  display: "inline-block",
  borderRadius: "30px",
  padding: "2px",
  background:
    "linear-gradient(270deg, #216b39 20%, #053926 40%,#216b39 50%, rgb(24, 161, 111) 55%, rgb(24, 161, 111) 70%, #216b39 100%)",
  backgroundSize: "200% auto",
  animation: `${shine} 3s linear infinite`,
  "&::before": {
    content: '""',
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    borderRadius: "30px",
    background: "transparent",
    zIndex: -1,
  },
}));

const CustomTextField = styled(TextField)(({ theme }) => ({
  width: "100%",
  "& .MuiOutlinedInput-root": {
    "& fieldset": {
      border: "none", 
      borderRadius: "28px", 
    },
    "&:hover fieldset": {
      border: "none",
    },
    "&.Mui-focused fieldset": {
      border: "none",
    },
  },
  backgroundColor: "#aed6bf",
  borderRadius: "28px",
}));

const LogoContainer = styled(Box)({
  display: "flex",
  flexDirection: "row",
  gap: "20px",
  alignItems: "center",
});

const SearchContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  padding: theme.spacing(3),
  borderRadius: "8px",
  paddingTop: 0,
}));

const ResultsContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: theme.spacing(3),
  marginTop: theme.spacing(4),
  borderRadius: "8px",
  border: `1px solid ${theme.palette.primary.main}`,
  backgroundColor: "#aed6bf",
}));

const ResultItem = styled(ListItem)(({ theme }) => ({
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  gap: "24px",
  divider: false,
  borderBottom: `1px solid ${theme.palette.primary.main}`,
}));

const DetailItem: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <Box mb={1}>
    <Typography variant="body1" fontWeight="bold">
      {label}
    </Typography>
    <Typography variant="body1">{value}</Typography>
  </Box>
);

const SolrSearchApp: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState<boolean>(false);
  const [openSnackbar, setOpenSnackbar] = useState<boolean>(false);
  const [selectedResult, setSelectedResult] = useState<SearchResult | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  useEffect(() => {
    setHasSearched(false);
  }, [query]);

  useEffect(() => {
    console.log("Results state changed:", results);
  }, [results]);

  const fetchData = async () => {
    console.log("fetchData called");
    if (query.trim() === "") {
      setResults([]);
      setHasSearched(false);
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(false);

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
      setHasSearched(true);
    } catch (error) {
      console.error("Error in fetchData:", error);
      setError("No results found. Please try again.");
      setOpenSnackbar(true);
      setHasSearched(false);
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

  const handleOpenModal = (result: SearchResult) => {
    setSelectedResult(result);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedResult(null);
    setIsModalOpen(false);
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
      <AnimatedBackground />
      <LogoContainer>
        <img className="logoimage" src={logo} alt="BioFinder Logo" />
      </LogoContainer>
      <Container>
        <SearchContainer>
          <AnimatedBorderWrapper>
            <CustomTextField
              variant="outlined"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="E.g., Venomous snakes in Portugal"
              fullWidth
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  fetchData();
                }
              }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={fetchData}
                      disabled={loading}
                      aria-label="search"
                    >
                      {loading ? (
                        <CircularProgress size={24} />
                      ) : (
                        <SearchIcon
                          sx={{ color: "#216b39" }}
                          fontSize="large"
                        />
                      )}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </AnimatedBorderWrapper>
        </SearchContainer>

        {/* Render ResultsContainer only if hasSearched is true*/}
        {hasSearched && (
          <ResultsContainer>
            <Typography variant="h5" gutterBottom>
              Search Results
            </Typography>
            <Typography variant="body1">Current Query: {query}</Typography>
            <Typography variant="body1">
              Total Results: {results.length}
            </Typography>
            {results.length > 0 ? (
              <List sx={{ width: "100%" }}>
                {results.map((result, index) => (
                  <Grow key={index} in={hasSearched} timeout={500}>
                    <ResultItem
                      onClick={() => handleOpenModal(result)}
                      sx={{ cursor: "pointer" }}
                    >
                      <Box>
                        <img
                          className="resultimage"
                          src={
                            removeItens.some((item) =>
                              result.image_url?.[0]?.includes(item)
                            )
                              ? "https://via.placeholder.com/150"
                              : result.image_url?.[0] ||
                                "https://via.placeholder.com/150"
                          }
                          alt={
                            result.image_url?.[0]?.includes("icon_edit")
                              ? "Image not found."
                              : result.name?.[0] || "Image not found."
                          }
                          style={{
                            width: "150px",
                            height: "auto",
                            borderRadius: "4px",
                          }}
                        />
                      </Box>
                      <Box>
                        <Typography variant="h6">
                          {result.name?.[0] || "Name Not Available."}
                        </Typography>
                        <Typography variant="body2">
                          {result.introduction?.[0] ||
                            "Introduction Not Available."}
                        </Typography>
                      </Box>
                    </ResultItem>
                  </Grow>
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

      {/* Modal */}
      <Dialog
        open={isModalOpen}
        onClose={handleCloseModal}
        fullWidth
        maxWidth="md"
        scroll="body"
        PaperProps={{
          sx: {
            background: "radial-gradient(circle, rgb(183, 212, 196) 0%, rgb(189, 219, 205) 100%)",
            borderRadius: '16px',
          },
        }}
      >
        <DialogTitle>
          {selectedResult?.name?.[0] || "Name not available."}
          <IconButton
            aria-label="close"
            onClick={handleCloseModal}
            sx={(theme) => ({
              position: "absolute",
              right: 8,
              top: 8,
              color: theme.palette.grey[500],
            })}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers sx={{ borderTop: `1px solid ${theme.palette.primary.main}` }}>
          <Box sx={{ display: "flex", flexDirection: "row", gap: 3 }}>
            <Box sx={{ }}>
              <img
                src={
                  removeItens.some((item) =>
                    selectedResult?.image_url?.[0]?.includes(item)
                  )
                    ? "https://via.placeholder.com/250"
                    : selectedResult?.image_url?.[0] ||
                      "https://via.placeholder.com/250"
                }
                alt={
                  removeItens.some((item) =>
                    selectedResult?.image_url?.[0]?.includes(item)
                  )
                    ? "Image not found."
                    : selectedResult?.name?.[0] || "Image not found."
                }
                style={{
                  width: "100%",
                  height: "auto",
                  borderRadius: "8px",
                  minWidth: "250px",
                  minHeight: "250px",
                }}
              />
              <Box mt={1}>
                <DetailItem
                  label="Conservation Status:"
                  value={selectedResult?.conservation_status?.[0] || "N/A"}
                />
                <DetailItem
                  label="Kingdom:"
                  value={selectedResult?.kingdom?.[0] || "N/A"}
                />
                <DetailItem
                  label="Order:"
                  value={selectedResult?.order?.[0] || "N/A"}
                />
                <DetailItem
                  label="Family:"
                  value={selectedResult?.family?.[0] || "N/A"}
                />
                <DetailItem
                  label="Genus:"
                  value={selectedResult?.genus?.[0] || "N/A"}
                />
                <DetailItem
                  label="Species:"
                  value={selectedResult?.species || "N/A"}
                />
                <DetailItem
                  label="Discovered by:"
                  value={selectedResult?.who_discovered?.[0] || "N/A"}
                />
              </Box>
            </Box>

            <Box sx={{ mt: 1 }}>
              <DetailItem
                label="Introduction:"
                value={selectedResult?.introduction?.[0] || "N/A"}
              />
              <DetailItem
                label="Sections:"
                value={selectedResult?.sections || "N/A"}
              />
            </Box>
          </Box>
        </DialogContent>
      </Dialog>

      {/* Snackbar to display errors */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity="error"
          sx={{ width: "100%" }}
        >
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default SolrSearchApp;
