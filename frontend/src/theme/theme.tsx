// theme.js
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#216b39",
    },
    secondary: {
      main: "#053926",
    },
    // background: {
    //   default: "#aed6bf",
    // },
  },
  typography: {
    fontFamily: "'Montserrat', sans-serif",
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
    body1: {
      fontSize: "1rem",
    },
    body2: {
      fontSize: "0.875rem",
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background: "radial-gradient(circle, rgba(174,214,191,1) 0%, rgba(143,190,167,1) 100%)",
          minHeight: "100vh",
        },
      },
    },
  },
});

export default theme;
