// eslint-disable-next-line
// import "froala-editor/css/froala_style.min.css";
// import "froala-editor/css/froala_editor.pkgd.min.css";
// eslint-disable-next-line
import FroalaEditorComponent from "react-froala-wysiwyg";
// Include special components if required.
import FroalaEditorView from "react-froala-wysiwyg/FroalaEditorView";
// import FroalaEditorA from "react-froala-wysiwyg/FroalaEditorA";
// import FroalaEditorButton from "react-froala-wysiwyg/FroalaEditorButton";
// import FroalaEditorImg from "react-froala-wysiwyg/FroalaEditorImg";
// import FroalaEditorInput from "react-froala-wysiwyg/FroalaEditorInput";
import "froala-editor/js/plugins.pkgd.min.js";
import "froala-editor/js/languages/de.js";
// eslint-disable-next-line
import FroalaEditor from "react-froala-wysiwyg";
import React, { useRef, useState, useContext, useEffect } from "react";
import Redirect from "react-router-dom";
import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import { login, logout, authFetch, userContext } from "../Auth/Auth";
import Snackbars from "../../components/Snackbars/Snackbars";
import Divider from "@material-ui/core/Divider";
import TextareaAutosize from "@material-ui/core/TextareaAutosize";
import FeedbackComment from "../../components/Comment/FeedbackComment";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import Avatar from "@material-ui/core/Avatar";
import userUnknownImg from "../../assets/icon/user_unknown.png";
import moment from "moment";
import Box from "@material-ui/core/Box";
import { FormattedMessage } from "react-intl";

const useStyles = makeStyles((theme) => ({
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
  commentContainer: {
    width: `100%`,
    minHeight: 100,
    marginTop: 5,
    marginBottom: 10,
    justifyContent: `space-evenly`,
  },
  hr: {
    width: `95%`,
  },
  introBox: {
    marginTop: 10,
    marginLeft: 20,
    marginRight: 20,
    marginBottom: 10,
  },
  generalMargin: {
    marginTop: 10,
    marginBottom: 10,
  },
  frView: {
    width: `95%`,
    "& div": {
      whiteSpace: `normal !important`,
    },
  },
}));

export default function ViewBlog(props) {
  const classes = useStyles();
  const [blog, setBlog] = useState({});
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

  const handleSubmit = (event) => {
    event.preventDefault();
    if (formValidation()) {
      var formData = new FormData();
      if (user?.id !== undefined) {
        formData.append("user_id", user.id);
      }
      formData.append("name", user?.user_name || name.value);
      formData.append("category", "video");
      formData.append("blog_uuid", uuid);
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
  useEffect(() => {
    fetch("/api/blogs/fetch/" + uuid, {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setBlog(data);
      });
    fetch("/api/comments/blog/" + uuid, {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setComments(data);
      });
  }, []);

  return (
    <BodyContainer size="md">
      <Snackbars message={msg} statusCode={statusCode} />
      <Typography component="h2" variant="h5" className={classes.generalMargin}>
        {blog.title}
      </Typography>
      <Typography
        variant="subtitle2"
        color="textSecondary"
        className={classes.generalMargin}
      >
        {moment.utc(blog.created_at).format("lll")}
      </Typography>

      <Divider variant="middle" className={classes.hr} />
      <Typography variant="subtitle1" className={classes.introBox}>
        {blog.blog_intro}
      </Typography>
      <Divider variant="middle" className={classes.hr} />
      <Box className={classes.frView}>
        <FroalaEditorView model={blog?.content} />
      </Box>
      <Divider variant="middle" className={classes.hr} />
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
                    <span style={{ color: "red" }}>{formErros["input"]}</span>
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
    </BodyContainer>
  );
}
