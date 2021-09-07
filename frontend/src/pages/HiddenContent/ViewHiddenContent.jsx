import React, { useEffect, useState, useRef } from "react";
import Typography from "@material-ui/core/Typography";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import { userContext, authFetch } from "../Auth/Auth";
import Button from "@material-ui/core/Button";
import Snackbars from "../../components/Snackbars/Snackbars";
import { FormattedMessage } from "react-intl";
import TextField from "@material-ui/core/TextField";
import List from "@material-ui/core/List";
import Chip from "@material-ui/core/Chip";
import Divider from "@material-ui/core/Divider";

const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `95%`,
  },
  container: {
    display: `block`,
    width: `100%`,
  },
  textArea: {
    marginTop: 15,
    borderRadius: 5,
    background: `#f7f7f7`,
    padding: 2,
    boxShadow: `inset 2px 2px 6px rgba(0,0,0,.08)`,
    minHeight: 100,
    width: `99%`,
    backgroundAttachment: `scroll`,
    resize: `none`,
    borderColor: `#c4c4c4`,
  },
  button: {
    marginTop: 15,
  },
  hr: {
    width: `100%`,
  },
}));
export default function ViewHiddenContent() {
  const classes = useStyles();
  const [labels, setLabels] = useState([]);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  let name = useRef("");

  useEffect(() => {
    authFetch("/api/labels", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setLabels(data);
      });
  }, []);

  const handleDelete = (id) => {
    var formData = new FormData();
    formData.append("id", id);

    authFetch("/api/labels/delete", {
      method: "DELETE",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    var formData = new FormData();
    formData.append("name", name.value);

    authFetch("/api/labels/create", {
      method: "POST",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  return (
    <BodyContainer size="md">
      <Snackbars message={msg} statusCode={statusCode} />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          Add a new Label
        </Typography>
        <form noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            id="name"
            label="name"
            name="name"
            autoComplete="name"
            inputRef={(input) => (name = input)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.button}
          >
            <FormattedMessage id="Submit" defaultMessage="Submit" />
          </Button>
        </form>
        <Divider variant="middle" className={classes.hr} />
        <List className={classes.container}>
          {labels.map((label) => (
            <React.Fragment key={label?.name + label?.id}>
              <Chip
                color="secondary"
                size="small"
                label={label.name}
                onDelete={() => handleDelete(label.id)}
                key={label?.name + label?.id}
              />
              <br />
            </React.Fragment>
          ))}
        </List>
      </div>
    </BodyContainer>
  );
}
