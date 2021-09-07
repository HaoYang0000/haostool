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
import LinearProgress from "@material-ui/core/LinearProgress";
import BlogPost from "../../components/Blog/BlogPost";
import Grid from "@material-ui/core/Grid";

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
    marginTop: 15,
  },
}));
export default function HiddenContent() {
  const classes = useStyles();
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const [blogs, setBlogs] = useState([]);
  let code = useRef("");

  const handleSubmit = (event) => {
    event.preventDefault();
    authFetch("/api/hidden-content/content/" + code.value, {
      method: "GET",
    }).then((res) =>
      res.json().then((data) => {
        console.log(data);
        setBlogs(data);
      })
    );
  };

  return (
    <BodyContainer size="md">
      <Snackbars message={msg} statusCode={statusCode} />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          <FormattedMessage
            id="Invitation Code"
            defaultMessage="Invitation Code"
          />
        </Typography>
        <form noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            id="code"
            label="code"
            name="code"
            autoComplete="code"
            required
            inputRef={(input) => (code = input)}
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
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
          spacing={1}
        >
          {blogs.map((blog) => (
            <BlogPost
              blog={blog}
              key={blog.uuid}
              handleLabelChange={null}
              allowHidden={true}
            />
          ))}
        </Grid>
      </div>
    </BodyContainer>
  );
}
