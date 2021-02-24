import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";

const useStyles = makeStyles({
  container: {
    marginTop: 65,
  },
});
export default function Game() {
  const classes = useStyles();
  return <BodyContainer>Game.</BodyContainer>;
}
