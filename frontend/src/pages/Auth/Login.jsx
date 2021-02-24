import React, { useEffect, useRef, useState } from "react";
import { Redirect } from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import BodyContainer from "../../components/Layout/Layout";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { login, useAuth, logout } from "./Auth";
import Snackbars from "../../components/Snackbars/Snackbars";
import { FormattedMessage } from "react-intl";
const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `100%`,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function Login() {
  const classes = useStyles();
  const [logged] = useAuth();
  const username = useRef(null);
  const password = useRef(null);
  const rememberme = useRef(null);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = {
      username: username.current.value,
      password: password.current.value,
      rememberme: rememberme.current.checked,
    };

    fetch("/auth/login", {
      method: "post",
      body: JSON.stringify(data),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.access_token) {
          login(data);
        } else {
          setMsg("Please type in correct username/password");
          setStatusCode(400);
        }
      });
  };

  return logged ? (
    <Redirect to="/blogs"></Redirect>
  ) : (
    <BodyContainer size="sm">
      <Snackbars message={msg} statusCode={statusCode} />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          <FormattedMessage id="Sign in" defaultMessage="Sign in" />
        </Typography>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="email"
            label={
              <FormattedMessage
                id="Email Address"
                defaultMessage="Email Address"
              />
            }
            name="email"
            autoComplete="email"
            autoFocus
            inputRef={username}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label={<FormattedMessage id="Password" defaultMessage="Password" />}
            type="password"
            id="password"
            autoComplete="current-password"
            inputRef={password}
          />
          <FormControlLabel
            control={
              <Checkbox
                value="remember"
                color="primary"
                id="rememberme"
                name="rememberme"
                inputRef={rememberme}
              />
            }
            label={
              <FormattedMessage id="Remember me" defaultMessage="Remember me" />
            }
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Sign In
          </Button>
          <Grid container>
            <Grid item xs>
              <Link href="#" variant="body2">
                <FormattedMessage
                  id="Forgot password?"
                  defaultMessage="Forgot password?"
                />
              </Link>
            </Grid>
            <Grid item>
              <Link href="#" variant="body2">
                <FormattedMessage
                  id="Don't have an account? Sign Up"
                  defaultMessage="Don't have an account? Sign Up"
                />
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
    </BodyContainer>
  );
}
