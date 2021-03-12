import React from "react";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";
import Footer from "../Footer/Footer";
import Paper from "@material-ui/core/Paper";
import SpeedDials from "../SpeedDials/SpeedDials";
import Box from "@material-ui/core/Box";
import {
  createMuiTheme,
  makeStyles,
  ThemeProvider,
} from "@material-ui/core/styles";
import { blue, deepOrange } from "@material-ui/core/colors";
const theme = createMuiTheme({
  palette: {
    primary: blue,
    secondary: deepOrange,
  },
});
const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: 75,
    marginBottom: 15,
    display: "flex",
    minHeight: "90vh",
    flexDirection: `column`,
    alignItems: `center`,
    padding: theme.spacing(1),
  },
}));
export default function BodyContainer(props) {
  const classes = useStyles();
  const { children, size, noPaper } = props;
  return (
    <React.Fragment>
      <ThemeProvider theme={theme}>
        <Container maxWidth={size}>
          {noPaper ? (
            <Box
              className={
                props?.container ? props?.container : classes.container
              }
            >
              {children}
            </Box>
          ) : (
            <Paper
              className={
                props?.container ? props?.container : classes.container
              }
            >
              {children}
            </Paper>
          )}
        </Container>
        <SpeedDials />
        <Footer />
      </ThemeProvider>
    </React.Fragment>
  );
}
