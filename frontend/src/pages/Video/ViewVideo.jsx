import React, { useEffect, useRef, useState, useContext } from "react";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import BodyContainer from "../../components/Layout/Layout";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Skeleton from "@material-ui/lab/Skeleton";
import thumbUpImg from "../../assets/icon/thumb_up.png";
import viewedNumImg from "../../assets/icon/viewed_num.png";
import Paper from "@material-ui/core/Paper";
import Divider from "@material-ui/core/Divider";
import FeedbackComment from "../../components/Comment/FeedbackComment";
import List from "@material-ui/core/List";
import { userContext } from "../../pages/Auth/Auth";
import TextField from "@material-ui/core/TextField";
import TextareaAutosize from "@material-ui/core/TextareaAutosize";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import Avatar from "@material-ui/core/Avatar";
import userUnknownImg from "../../assets/icon/user_unknown.png";
import Snackbars from "../../components/Snackbars/Snackbars";
import { FormattedMessage } from "react-intl";

const useStyles = makeStyles((theme) => ({
  video: {
    minWidth: `200px`,
    width: `60vw`,
    [theme.breakpoints.down("md")]: {
      width: `90vw`,
    },
  },
  actionContainer: {
    width: `60vw`,
    minHeight: 100,
    display: `flex`,
    justifyContent: `flex-start`,
    alignItems: `center`,
    overflow: `auto`,
    marginTop: 5,
    [theme.breakpoints.down("md")]: {
      width: `90vw`,
    },
  },
  iconImg: {
    marginLeft: 15,
    width: 40,
    height: 40,
  },
  iconLabel: {
    margin: 5,
  },
  commentContainer: {
    width: `60vw`,
    minHeight: 100,
    marginTop: 5,
    marginBottom: 10,
    justifyContent: `space-evenly`,
    [theme.breakpoints.down("md")]: {
      width: `90vw`,
    },
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
}));

export default function ViewVideo(props) {
  const classes = useStyles();
  const [loaded, setLoaded] = useState(false);
  const [video, setVideo] = useState(null);
  const [currentLike, setCurrentLike] = useState(0);
  const [comments, setComments] = useState([]);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const [formErros, setFormErros] = useState({});
  const uuid = props.match.params.uuid;
  const user = useContext(userContext);
  let name = useRef("");
  let content = useRef("");

  const formValidation = () => {
    let validated = true;
    if (content.value === "") {
      formErros["input"] = <FormattedMessage id="Message can not be empty." />;
      validated = false;
    } else {
      delete formErros["input"];
    }
    return validated;
  };

  useEffect(() => {
    setLoaded(false);
    fetch("/api/videos/" + uuid, {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setVideo(data);
        setCurrentLike(data.liked_number);
        setLoaded(true);
      });
    fetch("/api/comments/video/" + uuid, {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setComments(data);
      });
  }, []);
  const increaseLike = () => {
    fetch("/api/videos/like/" + uuid, {
      method: "post",
    })
      .then((r) => r.json())
      .then((data) => {
        setCurrentLike(data);
        console.log(data);
      });
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    if (formValidation()) {
      var formData = new FormData();
      if (user?.id !== undefined) {
        formData.append("user_id", user.id);
      }
      formData.append("name", user?.user_name || name.value);
      formData.append("category", "video");
      formData.append("video_uuid", uuid);
      formData.append("content", content.value);

      fetch("/api/comments/post-new", {
        method: "POST",
        body: formData,
      }).then((res) =>
        res.json().then((data) => {
          setMsg(data);
          setStatusCode(res.status);
        })
      );
    } else {
      setMsg(
        <FormattedMessage
          id="Please fix the input errors."
          defaultMessage="Please fix the input errors."
        />
      );
      setStatusCode(400);
    }
  };

  return (
    <BodyContainer size="md" noPaper={true}>
      <React.Fragment>
        <Snackbars message={msg} statusCode={statusCode} />
        {!loaded ? (
          <Skeleton variant="rect" className={classes.video} />
        ) : (
          <video controls className={classes.video}>
            <source
              src={"http://" + window.location.host + "/static/" + video?.path}
              type="video/mp4"
            />
          </video>
        )}
        <Paper className={classes.actionContainer}>
          <Typography
            gutterBottom
            variant="h5"
            component="h2"
            className={classes.iconLabel}
            display="inline"
          >
            <FormattedMessage id="Title" defaultMessage="Title" />
            {": "}
            {video?.title}
          </Typography>
          <img src={viewedNumImg} className={classes.iconImg} />
          <label className={classes.iconLabel}>{video?.viewed_number}</label>
          <Button onClick={() => increaseLike(video?.id)}>
            <img src={thumbUpImg} className={classes.iconImg} />
          </Button>
          <label className={classes.iconLabel}>{currentLike}</label>
        </Paper>
        <Paper className={classes.commentContainer}>
          <form noValidate onSubmit={handleSubmit}>
            <List>
              <ListItem alignItems="flex-start">
                <ListItemAvatar>
                  {user?.id ? (
                    <Avatar
                      src={
                        "http://" +
                        window.location.host +
                        "/static/" +
                        user?.avatar
                      }
                    />
                  ) : (
                    <Avatar src={userUnknownImg} />
                  )}
                </ListItemAvatar>
                <ListItemText
                  primary={
                    user?.user_name ? (
                      user.user_name
                    ) : (
                      <TextField
                        variant="outlined"
                        margin="normal"
                        fullWidth
                        id="name"
                        label={
                          <FormattedMessage
                            id="Name (Optional)"
                            defaultMessage="Name (Optional)"
                          />
                        }
                        name="name"
                        autoComplete="name"
                        inputRef={(input) => (name = input)}
                      />
                    )
                  }
                  secondary={
                    <React.Fragment>
                      <FormattedMessage id="Leave a friendly comment here :)">
                        {(msg) => (
                          <TextareaAutosize
                            rowsMax={4}
                            aria-label="maximum height"
                            placeholder={msg[0]}
                            className={classes.textArea}
                            ref={(input) => (content = input)}
                          />
                        )}
                      </FormattedMessage>
                      <label style={{ color: "red" }}>
                        {formErros["input"]}
                      </label>
                      <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.button}
                      >
                        <FormattedMessage id="Post" defaultMessage="Post" />
                      </Button>
                    </React.Fragment>
                  }
                />
              </ListItem>
              <Divider variant="inset" component="li" />
              {comments.map((comment) => (
                <FeedbackComment comment={comment} key={comment.id} />
              ))}
            </List>
          </form>
        </Paper>
      </React.Fragment>
    </BodyContainer>
  );
}
