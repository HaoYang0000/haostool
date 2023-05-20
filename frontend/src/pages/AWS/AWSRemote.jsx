import React, { useEffect, useState } from "react";
import Typography from "@material-ui/core/Typography";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import { userContext, authFetch } from "../Auth/Auth";
import Button from "@material-ui/core/Button";
import Snackbars from "../../components/Snackbars/Snackbars";
const useStyles = makeStyles({
  button: {
    minWidth: 80,
    height: 40,
  },
});
export default function AWSRemote(props) {
  const classes = useStyles();
  const [vpnInfo, setVpnInfo] = useState({});
  const [msg, setMsg] = useState("");
  const action = props.match.params.action;
  const device = props.match.params.device;
  const token = props.match.params.token;
  const [statusCode, setStatusCode] = useState(null);
  useEffect(() => {
    if (action === "start") {
      fetch("/api/aws/remote/start-instance/" + device + "/" + token, {
        method: "get",
      })
        .then((r) => r.json())
        .then((data) => {
          setMsg(data);
          setStatusCode(200);
        });
    } else if (action === "stop") {
      fetch("/api/aws/remote/stop-instance/" + device + "/" + token, {
        method: "get",
      })
        .then((r) => r.json())
        .then((data) => {
          setMsg(data);
          setStatusCode(200);
        });
    } else {
      setMsg("Bad request");
      setStatusCode(400);
    }
    setTimeout(function () {}, "30000");
    fetch("/api/aws", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setVpnInfo(data);
      });
  }, []);

  return (
    <BodyContainer>
      <Snackbars message={msg} statusCode={statusCode} />
      <Typography variant="h5" component="h5">
        {"Vpn name: " +
          vpnInfo?.name +
          ", type: " +
          vpnInfo?.type +
          " , state: " +
          vpnInfo?.state +
          ", IP Address: " +
          vpnInfo?.ip_address}
      </Typography>
    </BodyContainer>
  );
}
