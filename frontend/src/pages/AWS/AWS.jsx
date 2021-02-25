import React, { useEffect, useState } from "react";
import Typography from "@material-ui/core/Typography";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import { userContext, authFetch } from "../../pages/Auth/Auth";
import Button from "@material-ui/core/Button";
import Snackbars from "../../components/Snackbars/Snackbars";
const useStyles = makeStyles({
  button: {
    minWidth: 80,
    height: 40,
  },
});
export default function AWS() {
  const classes = useStyles();
  const [vpnInfo, setVpnInfo] = useState({});
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  useEffect(() => {
    authFetch("/api/aws", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setVpnInfo(data);
      });
  }, []);
  const startInstance = () => {
    authFetch("/api/aws/start_instance", {
      method: "post",
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };
  const stopInstance = () => {
    authFetch("/api/aws/stop_instance", {
      method: "post",
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };
  const changeIp = () => {
    authFetch("/api/aws/change_ip", {
      method: "post",
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };
  return (
    <BodyContainer>
      <Snackbars message={msg} statusCode={statusCode} />
      <Typography variant="h5" component="h5">
        {"Vpn name: " +
          vpnInfo.name +
          ", type: " +
          vpnInfo.type +
          " , state: " +
          vpnInfo.state +
          ", IP Address: " +
          vpnInfo.ip_address}
      </Typography>
      <Button
        onClick={() => startInstance()}
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Start Instance
      </Button>
      <Button
        onClick={() => stopInstance()}
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Stop Instance
      </Button>
      <Button
        onClick={() => changeIp()}
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Replace IP
      </Button>
    </BodyContainer>
  );
}
