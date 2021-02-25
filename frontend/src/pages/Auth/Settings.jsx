import React, { useRef, useEffect, useContext, useState } from "react";
import { Redirect } from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import BodyContainer from "../../components/Layout/Layout";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { login, logout, useAuth, authFetch, userContext } from "./Auth";
import { FormattedMessage } from "react-intl";
const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `100%`,
    height: `100%`,
  },
  profileImg: {
    borderRadius: `50%`,
    height: 200,
    width: 200,
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
export default function Settings() {
  const classes = useStyles();
  const username = useRef(null);
  const email = useRef(null);
  const password = useRef(null);
  const firstname = useRef(null);
  const lastname = useRef(null);
  const phonenumber = useRef(null);
  const user = useContext(userContext);
  const [userInfo, setUserInfo] = useState({});
  const [logged] = useAuth();
  const [loaded, setLoaded] = useState(false);
  const [file, setFile] = useState(null);

  useEffect(() => {
    authFetch("/api/auth/get-user/" + user.id, {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setUserInfo(data);
        setLoaded(true);
      });
  }, []);
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleProfileImgUpdate = (event) => {
    event.preventDefault();
    var formData = new FormData();
    formData.append("file", file);
    authFetch("/api/auth/update-profile-img/" + user.id, {
      method: "post",
      body: formData,
    })
      .then((r) => r.json())
      .then((data) => {
        console.log(data);
      });
    window.location.reload();
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = {
      username: username.current.value || null,
      email: email.current.value || null,
      password: password.current.value || null,
      nickname: null,
      firstname: firstname.current.value || null,
      lastname: lastname.current.value || null,
      phonenumber: phonenumber.current.value || null,
    };

    authFetch("/api/auth/update/" + user.id, {
      method: "post",
      body: JSON.stringify(data),
    })
      .then((r) => r.json())
      .then((data) => {
        console.log(data);
      });
    window.location.reload();
  };
  return logged ? (
    <React.Fragment>
      {!loaded ? (
        <CircularProgress></CircularProgress>
      ) : (
        <BodyContainer size="sm">
          <div className={classes.paper}>
            <Typography component="h6" variant="h6">
              <FormattedMessage
                id="Update Profile Image"
                defaultMessage="Update Profile Image"
              />
            </Typography>
            <hr className={classes.hr} />
            <form
              className={classes.form}
              noValidate
              onSubmit={handleProfileImgUpdate}
            >
              <img
                src={
                  "http://" +
                  window.location.host +
                  "/static/" +
                  userInfo?.avatar
                }
                className={classes.profileImg}
              />
              <br />
              <Button variant="contained">
                <input name="file" type="file" onChange={handleFileChange} />
              </Button>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
              >
                <FormattedMessage id="Upload" defaultMessage="Upload" />
              </Button>
            </form>
            <Typography component="h6" variant="h6">
              <FormattedMessage
                id="Required infomation."
                defaultMessage="Required infomation."
              />
            </Typography>
            <hr className={classes.hr} />
            <form noValidate onSubmit={handleSubmit}>
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
                defaultValue={userInfo.username}
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
                defaultValue={userInfo.email}
                inputRef={email}
              />
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label={
                  <FormattedMessage id="Password" defaultMessage="Password" />
                }
                type="password"
                id="password"
                autoComplete="current-password"
                inputRef={password}
              />
              <hr className={classes.hr} />
              <Typography
                component="h6"
                variant="h6"
                className={classes.center}
              >
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
                  <FormattedMessage
                    id="First Name"
                    defaultMessage="First Name"
                  />
                }
                name="firstname"
                autoComplete="firstname"
                defaultValue={userInfo.first_name}
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
                defaultValue={userInfo.last_name}
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
                defaultValue={userInfo.phone_num}
                inputRef={phonenumber}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
              >
                <FormattedMessage id="Update" defaultMessage="Update" />
              </Button>
            </form>
          </div>
        </BodyContainer>
      )}
    </React.Fragment>
  ) : (
    <Redirect to="/auth/login"></Redirect>
  );
}
