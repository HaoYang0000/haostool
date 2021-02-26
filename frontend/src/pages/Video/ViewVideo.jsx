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
import Footer from "../../components/Footer/Footer";
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

// import { login, useAuth, logout } from "./Auth";

const useStyles = makeStyles((theme) => ({
  body: {
    width: `46vw`,
    marginTop: 75,
    marginBottom: 15,
    minHeight: "78vh",
  },
  container: {},
  video: {
    minWidth: `200px`,
    width: `40vw`,
  },
  actionContainer: {
    width: `40vw`,
    display: `inline-flex`,
    minHeight: 100,
    justifyContent: `flex-start`,
    alignItems: `center`,
    backgroundColor: `#ffffff`,
    boxShadow: `0px 0px 5px 0px rgb(162, 162, 162)`,
    borderRadius: 5,
    overflow: `auto`,
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
    width: `40vw`,
    minHeight: 100,
    backgroundColor: `#ffffff`,
    marginTop: 5,
    marginBottom: 10,
    borderRadius: 5,
    boxShadow: `0px 0px 5px 0px rgb(162, 162, 162)`,
    justifyContent: `space-evenly`,
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
  const uuid = props.match.params.uuid;
  const user = useContext(userContext);
  let name = useRef("");
  let content = useRef("");
  useEffect(() => {
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
  };

  return (
    <BodyContainer container={classes.body} noPaper={true}>
      {!loaded ? (
        <Skeleton variant="rect" width={210} height={118} />
      ) : (
        <React.Fragment>
          <Snackbars message={msg} statusCode={statusCode} />
          <video controls className={classes.video}>
            <source
              src={"http://" + window.location.host + "/static/" + video.path}
              type="video/mp4"
            />
          </video>
          <div className={classes.actionContainer}>
            <Typography
              gutterBottom
              variant="h5"
              component="h2"
              className={classes.iconLabel}
            >
              <FormattedMessage id="Title" defaultMessage="Title" />
              {": "}
              {video.title}
            </Typography>
            <img src={viewedNumImg} className={classes.iconImg} />
            <label className={classes.iconLabel}>{video.viewed_number}</label>
            <Button onClick={() => increaseLike(video.id)}>
              <img src={thumbUpImg} className={classes.iconImg} />
            </Button>
            <label className={classes.iconLabel}>{currentLike}</label>
          </div>
          <div className={classes.commentContainer}>
            <form noValidate onSubmit={handleSubmit}>
              <List>
                <ListItem alignItems="flex-start">
                  <ListItemAvatar>
                    {user ? (
                      <Avatar
                        src={
                          "http://" +
                          window.location.host +
                          "/static/" +
                          user.avatar
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
          </div>
        </React.Fragment>
      )}
    </BodyContainer>
  );
}
