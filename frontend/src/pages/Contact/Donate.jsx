import React from "react";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import DonateImage from "../../assets/contact/donate.jpg";

const useStyles = makeStyles((theme) => ({
  iconImg: {
    height: 500,
    width: 500,
    padding: 10,
  },
}));
export default function Donate() {
  const classes = useStyles();
  return (
    <BodyContainer size="sm">
      <img src={DonateImage} className={classes.iconImg} />
    </BodyContainer>
  );
}
