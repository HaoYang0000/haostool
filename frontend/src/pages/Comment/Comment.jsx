import React, { useState, useRef, useContext, useEffect } from "react";
import TextareaAutosize from "@material-ui/core/TextareaAutosize";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import Snackbars from "../../components/Snackbars/Snackbars";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import { userContext } from "../../pages/Auth/Auth";
import FeedbackComment from "../../components/Comment/FeedbackComment";
import List from "@material-ui/core/List";
import { FormattedMessage } from "react-intl";
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
export default function Comment() {
  const classes = useStyles();
  const [comments, setComments] = useState([]);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const user = useContext(userContext);
  let name = useRef("");
  let email = useRef("");
  let content = useRef("");

  const handleSubmit = (event) => {
    event.preventDefault();
    var formData = new FormData();
    if (user?.id !== undefined) {
      formData.append("user_id", user.id);
    }
    formData.append("name", name.value);
    formData.append("email", email.value);
    formData.append("category", "feedback");
    formData.append("content", content.value);

    fetch("/comments/post-new", {
      method: "POST",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };
  useEffect(() => {
    fetch("/comments/feedback", {
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
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          <FormattedMessage
            id="Leave a Comments"
            defaultMessage="Leave a Comments"
          />
        </Typography>
        <form noValidate onSubmit={handleSubmit}>
          <FormattedMessage id="feedback, please let me know">
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
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            id="email"
            label={
              <FormattedMessage
                id="Email Address (Optional)"
                defaultMessage="Email Address (Optional)"
              />
            }
            name="email"
            autoComplete="email"
            inputRef={(input) => (email = input)}
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
        <hr className={classes.hr} />
        <List className={classes.container}>
          {comments.map((comment) => (
            <FeedbackComment comment={comment} key={comment.id} />
          ))}
        </List>
      </div>
    </BodyContainer>
  );
}
