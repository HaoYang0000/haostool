import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import Typography from "@material-ui/core/Typography";
import ErrorOutlineSharpIcon from "@material-ui/icons/ErrorOutlineSharp";

const useStyles = makeStyles({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `95%`,
  },
  icno: {
    height: 400,
    width: 400,
  },
});
export default function NotFound(props) {
  const classes = useStyles();
  return (
    <BodyContainer size="sm">
      <div className={classes.paper}>
        <ErrorOutlineSharpIcon className={classes.icno} />
        <Typography component="h1" variant="h5">
          Url: {props.location.pathname} Not Found
        </Typography>
      </div>
    </BodyContainer>
  );
}
