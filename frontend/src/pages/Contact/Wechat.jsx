import React from "react";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import wechatImage from "../../assets/contact/wechat.jpg";
import Typography from "@material-ui/core/Typography";
import { FormattedMessage } from "react-intl";

const useStyles = makeStyles((theme) => ({
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `100%`,
  },
  iconImg: {
    height: 500,
    width: 500,
    padding: 10,
  },
}));
export default function Wechat() {
  const classes = useStyles();
  return (
    <BodyContainer size="sm">
      <div className={classes.container}>
        <img src={wechatImage} className={classes.iconImg} />
        <Typography gutterBottom variant="h5" component="h2">
          <FormattedMessage
            id="Contact me through Wechat"
            defaultMessage="Contact me through Wechat"
          />
        </Typography>
      </div>
    </BodyContainer>
  );
}
