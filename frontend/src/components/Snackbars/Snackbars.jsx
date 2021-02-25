import React, { useEffect, useState } from "react";
import Button from "@material-ui/core/Button";
import Snackbar from "@material-ui/core/Snackbar";
import MuiAlert from "@material-ui/lab/Alert";
import { makeStyles } from "@material-ui/core/styles";
import { snackBarTypes } from "../../constants/snackBarTypes";

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    "& > * + *": {
      marginTop: theme.spacing(2),
    },
  },
}));

export default function Snackbars(props) {
  const classes = useStyles();
  const { message, statusCode } = props;
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (message === null || message === "") {
      setOpen(false);
    } else {
      setOpen(true);
    }
  }, [message]);

  const getSnackBarType = () => {
    if (statusCode === 200) {
      return snackBarTypes.success;
    }
    return snackBarTypes.error;
  };

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpen(false);
  };

  return (
    <Snackbar
      open={open}
      autoHideDuration={6000}
      onClose={handleClose}
      key={"top" + "center"}
    >
      <Alert onClose={handleClose} severity={getSnackBarType()}>
        {message}
      </Alert>
    </Snackbar>
  );
}