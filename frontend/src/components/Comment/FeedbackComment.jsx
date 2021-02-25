import React, { useContext, useState, useEffect } from "react";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Button from "@material-ui/core/Button";
import { userContext, authFetch } from "../../pages/Auth/Auth";
import { DeleteForever } from "@material-ui/icons";
import Snackbars from "../../components/Snackbars/Snackbars";
import userUnknownImg from "../../assets/icon/user_unknown.png";
import moment from "moment";
import ListItem from "@material-ui/core/ListItem";
import Divider from "@material-ui/core/Divider";
import ListItemText from "@material-ui/core/ListItemText";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import Avatar from "@material-ui/core/Avatar";

const useStyles = makeStyles((theme) => ({
  commentText: {
    wordWrap: `break-word`,
  },
}));
export default function FeedbackComment(props) {
  const classes = useStyles();
  const { comment } = props;
  const user = useContext(userContext);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);

  const deleteComment = (commentId) => {
    authFetch("/api/comments/deactivate-comment", {
      method: "POST",
      body: JSON.stringify({ comment_id: commentId }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };
  return (
    <div>
      <Snackbars message={msg} statusCode={statusCode} />
      <ListItem alignItems="flex-start">
        <ListItemAvatar>
          {comment?.user ? (
            <Avatar
              src={
                "http://" +
                window.location.host +
                "/static/" +
                comment.user.avatar
              }
            />
          ) : (
            <Avatar src={userUnknownImg} />
          )}
        </ListItemAvatar>
        <ListItemText
          primary={
            comment?.unknown_user_name
              ? comment.unknown_user_name
              : "Secret User"
          }
          secondary={
            <React.Fragment>
              <Typography
                component="span"
                variant="body2"
                color="textSecondary"
              >
                {moment(comment.created_at).format("lll")}
                {user.role === "root" || user.role === "admin" ? (
                  <Button onClick={() => deleteComment(comment.id)}>
                    <DeleteForever />
                  </Button>
                ) : null}
              </Typography>
              <br />
              <Typography
                component="span"
                variant="body2"
                className={classes.commentText}
                color="textPrimary"
              >
                {comment.content}
              </Typography>
            </React.Fragment>
          }
        />
      </ListItem>
      <Divider variant="inset" component="li" />
    </div>
  );
}
