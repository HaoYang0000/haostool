import React from "react";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";
import Footer from "../Footer/Footer";
import Paper from "@material-ui/core/Paper";
import SpeedDials from "../SpeedDials/SpeedDials";
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
  paper: {
    marginTop: 75,
    marginBottom: 15,
    display: "flex",
    minHeight: "80vh",
    "& > *": {
      margin: theme.spacing(2),
    },
  },
}));
export default function BodyContainer(props) {
  const classes = useStyles();
  const { children, size, noPaper } = props;
  return (
    <React.Fragment>
      <ThemeProvider theme={theme}>
        <Container maxWidth={size} className={props?.container}>
          {noPaper ? (
            <React.Fragment>{children}</React.Fragment>
          ) : (
            <Paper className={classes.paper}>{children}</Paper>
          )}
        </Container>
        <SpeedDials />
        <Footer />
      </ThemeProvider>
    </React.Fragment>
  );
}
