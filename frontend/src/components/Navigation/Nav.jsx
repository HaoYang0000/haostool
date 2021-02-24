import React, { useEffect, useState, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import logo from "../../assets/ydaxian_logo.png";
import Typography from "@material-ui/core/Typography";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import Fade from "@material-ui/core/Fade";
import Skeleton from "@material-ui/lab/Skeleton";
import IconButton from "@material-ui/core/IconButton";
import GTranslateIcon from "@material-ui/icons/GTranslate";
import Hidden from "@material-ui/core/Hidden";
import {
  login,
  useAuth,
  authFetch,
  logout,
  userContext,
} from "../../pages/Auth/Auth";

const useStyles = makeStyles({
  container: {
    width: `100%`,
    position: `fixed`,
    top: 0,
    left: 0,
    height: 65,
    overflow: `auto`,
    zIndex: 2,
    boxShadow: `0px 0px 0px 2px #122849`,
    backgroundColor: `rgb(255, 255, 255)`,
  },
  logo: {
    height: 65,
    width: 65,
    display: `flex`,
    transition: `box-shadow 0.5s`,
  },
  text: {
    textDecoration: `none`,
    color: `black`,
    marginRight: 20,
  },
  profileImg: {
    borderRadius: `50%`,
    height: 50,
    width: 50,
    alignSelf: `flex-start`,
    transform: `translateY(10px)`,
  },
  button: {
    padding: `21px 12px`,
    textDecoration: `none`,
  },
  iconButton: {
    display: `inline-block`,
    borderRadius: 0,
  },
  link: {
    display: `inline-block`,
    padding: `22px 12px`,
    textDecoration: `none`,
    color: `black`,
    "&:hover": {
      backgroundColor: `#ddd`,
      transition: `0.5s`,
    },
  },
});

export default function Nav(props) {
  const classes = useStyles();
  const [logged] = useAuth();
  const [userInfo, setUserInfo] = useState({});
  const [anchorEl, setAnchorEl] = useState(null);
  const [anchorLang, setAnchorLang] = useState(null);
  const user = useContext(userContext);

  const handleLogout = () => {
    logout();
  };
  const handleTooltipClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleTooltipClose = () => {
    setAnchorEl(null);
  };
  const handleLangeClick = (event) => {
    setAnchorLang(event.currentTarget);
  };

  const handleLangeClose = () => {
    setAnchorLang(null);
  };

  const handleLangeChange = (lang) => {
    props.handleLangChange(lang);
    handleLangeClose();
  };

  useEffect(() => {
    if (logged) {
      authFetch("/auth/get-user/" + user.id, {
        method: "get",
        headers: {
          Authorization: "Bearer " + user.access_token,
        },
      })
        .then((r) => r.json())
        .then((data) => {
          setUserInfo(data);
        });
    }
  }, [logged]);

  return (
    <nav className={classes.container}>
      <Grid
        container
        direction="row"
        justify="space-between"
        alignItems="stretch"
      >
        <Hidden smDown>
          <Grid item>
            <img src={logo} className={classes.logo} />
          </Grid>
        </Hidden>
        <Grid item md={6}>
          <Grid container direction="row" justify="center" alignItems="stretch">
            <Grid item>
              <Link className={classes.link} to="/blogs">
                <FormattedMessage id="Blogs" defaultMessage="Blogs" />
              </Link>
            </Grid>
            <Grid item>
              <Link className={classes.link} to="/videos">
                <FormattedMessage id="Videos" defaultMessage="Videos" />
              </Link>
            </Grid>
            <Grid item>
              <Link className={classes.link} to="/timelines">
                <FormattedMessage id="Timelines" defaultMessage="Timelines" />
              </Link>
            </Grid>
            <Grid item>
              <Link className={classes.link} to="/comments">
                <FormattedMessage id="Comments" defaultMessage="Comments" />
              </Link>
            </Grid>
            {/* <Link className={classes.link} to="/games">
              Games
            </Link> */}
            {user.role === "root" || user.role === "admin" ? (
              <Grid item>
                <Button
                  aria-controls="simple-menu"
                  aria-haspopup="true"
                  variant="contained"
                  color="primary"
                  onClick={handleTooltipClick}
                  className={classes.button}
                >
                  <FormattedMessage
                    id="Admin Tools"
                    defaultMessage="Admin Tools"
                  />
                </Button>
                <Menu
                  id="simple-menu"
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleTooltipClose}
                  disableScrollLock={true}
                  TransitionComponent={Fade}
                  transformOrigin={{
                    vertical: "bottom",
                    horizontal: "center",
                  }}
                >
                  <MenuItem>
                    <Link className={classes.text} to="/videos/upload">
                      <FormattedMessage
                        id="Upload Videos"
                        defaultMessage="Upload Videos"
                      />
                    </Link>
                  </MenuItem>
                  <MenuItem>
                    <Link className={classes.text} to="/blogs/create-post">
                      <FormattedMessage
                        id="Write New Blog"
                        defaultMessage="Write New Blog"
                      />
                    </Link>
                  </MenuItem>
                  <MenuItem>
                    <Link className={classes.text} to="/aws">
                      <FormattedMessage id="AWS" defaultMessage="AWS" />
                    </Link>
                  </MenuItem>
                </Menu>
              </Grid>
            ) : null}
          </Grid>
        </Grid>
        <Grid item>
          <Grid
            container
            direction="row"
            justify="flex-end"
            alignItems="center"
          >
            <IconButton
              aria-label="lang"
              onClick={handleLangeClick}
              className={classes.iconButton}
            >
              <GTranslateIcon color="primary" />
            </IconButton>
            <Menu
              id="lang-menu"
              anchorEl={anchorLang}
              open={Boolean(anchorLang)}
              onClose={handleLangeClose}
              disableScrollLock={true}
              TransitionComponent={Fade}
              transformOrigin={{
                vertical: "bottom",
                horizontal: "center",
              }}
            >
              <MenuItem onClick={() => handleLangeChange("zh_CN")}>
                <FormattedMessage id="Chinese" defaultMessage="Chinese" />
              </MenuItem>
              <MenuItem onClick={() => handleLangeChange("en_US")}>
                <FormattedMessage id="English" defaultMessage="English" />
              </MenuItem>
            </Menu>
            {!logged ? (
              <React.Fragment>
                <Link className={classes.link} to="/auth/register">
                  <FormattedMessage id="Register" defaultMessage="Register" />
                </Link>
                <Link className={classes.link} to="/auth/login">
                  <FormattedMessage id="Login" defaultMessage="Login" />
                </Link>
              </React.Fragment>
            ) : (
              <React.Fragment>
                <Typography variant="h6" className={classes.text}>
                  <FormattedMessage
                    id="hi"
                    defaultMessage="Hi, {user}"
                    values={{ user: user.user_name }}
                  />
                </Typography>
                {userInfo?.avatar ? (
                  <img
                    src={
                      "http://" +
                      window.location.host +
                      "/static/" +
                      userInfo?.avatar
                    }
                    className={classes.profileImg}
                  />
                ) : (
                  <Skeleton variant="circle" width={50} height={50} />
                )}
                <Link className={classes.link} to="/auth/settings">
                  <FormattedMessage id="Settings" defaultMessage="Settings" />
                </Link>
                <Link
                  className={classes.link}
                  onClick={() => handleLogout()}
                  to="#"
                >
                  <FormattedMessage id="Logout" defaultMessage="Logout" />
                </Link>
              </React.Fragment>
            )}
          </Grid>
        </Grid>
      </Grid>
    </nav>
  );
}
