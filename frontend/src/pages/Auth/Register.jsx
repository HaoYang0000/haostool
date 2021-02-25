import React, { useRef, useState } from "react";
import { Redirect } from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import BodyContainer from "../../components/Layout/Layout";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
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
    height: `100%`,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  center: {
    textAlign: `center`,
  },
  hr: {
    width: `100%`,
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));
export default function Register() {
  const classes = useStyles();
  const [logged] = useAuth();
  const username = useRef(null);
  const email = useRef(null);
  const password = useRef(null);
  const nickname = useRef(null);
  const firstname = useRef(null);
  const lastname = useRef(null);
  const phonenumber = useRef(null);
  const rememberme = useRef(null);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = {
      username: username.current.value,
      email: email.current.value,
      password: password.current.value,
      nickname: null,
      firstname: firstname.current.value || null,
      lastname: lastname.current.value || null,
      phonenumber: phonenumber.current.value || null,
      rememberme: rememberme.current.checked,
    };

    fetch("/api/auth/register", {
      method: "post",
      body: JSON.stringify(data),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.access_token) {
          login(data);
        } else {
          setMsg("Something went wrong");
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
          <FormattedMessage id="Register" defaultMessage="Register" />
        </Typography>
        <hr className={classes.hr} />
        <Typography component="h6" variant="h6">
          <FormattedMessage
            id="Required infomation."
            defaultMessage="Required infomation."
          />
        </Typography>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label={
              <FormattedMessage id="User Name" defaultMessage="User Name" />
            }
            name="username"
            autoComplete="username"
            autoFocus
            inputRef={username}
          />
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
            inputRef={email}
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
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="repeatPassword"
            label={
              <FormattedMessage
                id="Repeat Password"
                defaultMessage="Repeat Password"
              />
            }
            type="repeatPassword"
            id="repeatPassword"
            autoComplete="repeat-password"
          />
          <hr className={classes.hr} />
          <Typography component="h6" variant="h6" className={classes.center}>
            <FormattedMessage
              id="Optional infomation."
              defaultMessage="Optional infomation."
            />
          </Typography>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="firstname"
            label={
              <FormattedMessage id="First Name" defaultMessage="First Name" />
            }
            name="firstname"
            autoComplete="firstname"
            inputRef={firstname}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="lastname"
            label={
              <FormattedMessage id="Last Name" defaultMessage="Last Name" />
            }
            name="lastname"
            autoComplete="lastname"
            inputRef={lastname}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="phonenumber"
            label={
              <FormattedMessage
                id="Phone Number"
                defaultMessage="Phone Number"
              />
            }
            name="phonenumber"
            autoComplete="phonenumber"
            inputRef={phonenumber}
          />
          <FormControlLabel
            control={
              <Checkbox
                value="rememberme"
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
            <FormattedMessage id="Register" defaultMessage="Register" />
          </Button>
        </form>
      </div>
    </BodyContainer>
  );
}
