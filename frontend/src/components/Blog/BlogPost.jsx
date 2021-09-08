import React, { useContext, useState, useEffect } from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Hidden from "@material-ui/core/Hidden";
import blogViewImg from "../../assets/icon/blog_view.png";
import blogLoveImg from "../../assets/icon/love.png";
import moment from "moment";
import { userContext, authFetch } from "../../pages/Auth/Auth";
import Chip from "@material-ui/core/Chip";
import Button from "@material-ui/core/Button";
import Link from "@material-ui/core/Link";
import Snackbars from "../../components/Snackbars/Snackbars";
import { FormattedMessage } from "react-intl";
import Avatar from "@material-ui/core/Avatar";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Dialog from "@material-ui/core/Dialog";
import PersonIcon from "@material-ui/icons/Person";
import AddIcon from "@material-ui/icons/Add";
import AddCircleIcon from "@material-ui/icons/AddCircle";
import { IconButton } from "@material-ui/core";

const useStyles = makeStyles({
  card: {
    display: "flex",
  },
  cardDetails: {
    flex: 1,
  },
  cardMedia: {
    width: 160,
  },
  iconImg: {
    width: 40,
    height: 40,
  },
  iconWrapper: {
    marginTop: 5,
  },
  iconText: {
    marginLeft: 5,
    marginRight: 5,
  },
  actions: {
    marginLeft: 10,
    marginTop: 5,
  },
  labelChip: {
    padding: 2,
    marginRight: 2,
  },
});

function SimpleDialog(props) {
  const classes = useStyles();
  const [labels, setLabels] = useState([]);
  const { open, blog } = props;

  useEffect(() => {
    authFetch("/api/labels", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setLabels(data);
      });
  }, []);

  const handleClose = () => {
    props.handleClose();
  };

  const handleListItemClick = (labelId) => {
    props.handleUpdate(labelId, blog?.id);
    props.handleClose();
  };

  return (
    <Dialog
      onClose={handleClose}
      aria-labelledby="simple-dialog-title"
      open={open}
    >
      <DialogTitle id="simple-dialog-title">Add New Labels</DialogTitle>
      <List>
        {labels.map((label) => (
          <ListItem
            button
            onClick={() => handleListItemClick(label?.id)}
            key={label?.name + label?.id}
          >
            <ListItemText primary={label?.name} />
          </ListItem>
        ))}
      </List>
    </Dialog>
  );
}

export default function BlogPost(props) {
  const classes = useStyles();
  const { blog, allowHidden } = props;
  const user = useContext(userContext);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleLabelChange = (curLabel) => {
    props.handleLabelChange(curLabel);
  };

  const handleDelete = (labelId, blogId) => {
    var formData = new FormData();
    formData.append("label_id", labelId);
    formData.append("blog_id", blogId);

    authFetch("/api/labels/delete/blog-label", {
      method: "DELETE",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const handleUpdate = (labelId, blogId) => {
    setOpen(false);
    var formData = new FormData();
    formData.append("label_id", labelId);
    formData.append("blog_id", blogId);
    authFetch("/api/labels/create/blog-label", {
      method: "POST",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const publishBlog = (blogId) => {
    authFetch("/api/blogs/publish", {
      method: "POST",
      body: JSON.stringify({ blog_id: blogId }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };
  const unpublishBlog = (blogId) => {
    authFetch("/api/blogs/unpublish", {
      method: "POST",
      body: JSON.stringify({ blog_id: blogId }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const makeBlogHidden = (blog_id) => {
    authFetch("/api/blogs/hidden", {
      method: "POST",
      body: JSON.stringify({ blog_id: blog_id }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const makeBlogUnHidden = (blog_id) => {
    authFetch("/api/blogs/unhidden", {
      method: "POST",
      body: JSON.stringify({ blog_id: blog_id }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  return user.role === "root" || user.role === "admin" ? (
    <Grid item xs={12} md={12}>
      <Snackbars message={msg} statusCode={statusCode} />
      <Card className={classes.card} key={blog.uuid}>
        <Hidden xsDown>
          <CardMedia
            component="a"
            href={"/blogs/view/" + blog.uuid}
            className={classes.cardMedia}
            image={
              "http://" + window.location.host + "/static/" + blog.cover_img
            }
            title={blog.title}
          />
        </Hidden>
        <div className={classes.cardDetails}>
          <CardContent>
            <Typography component="h2" variant="h5">
              <Link href={"/blogs/view/" + blog.uuid}>{blog.title}</Link>
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              {moment.utc(blog.created_at).format("lll")}
            </Typography>
            <Typography variant="subtitle2" paragraph>
              {blog.blog_intro}
            </Typography>
            <FormattedMessage id="Label: " />
            <IconButton onClick={handleClickOpen}>
              <AddCircleIcon color="primary" />
            </IconButton>
            {blog?.labels?.length === 0 && (
              <Chip
                label={<FormattedMessage id="None" />}
                disabled
                size="small"
              />
            )}
            {blog?.labels.map((label) => (
              <Chip
                color="primary"
                size="small"
                label={label.name}
                className={classes.labelChip}
                onClick={() => handleLabelChange(label?.name)}
                key={label?.name + label?.id}
                onDelete={() => handleDelete(label?.id, blog?.id)}
              />
            ))}
            <SimpleDialog
              open={open}
              handleClose={handleClose}
              handleUpdate={handleUpdate}
              blog={blog}
            />
            <div className={classes.iconWrapper}>
              <Grid
                container
                direction="column"
                justify="flex-start"
                alignItems="center"
              >
                <Grid
                  container
                  direction="row"
                  justify="flex-start"
                  alignItems="center"
                >
                  <img src={blogViewImg} className={classes.iconImg} />
                  <span className={classes.iconText}>{blog.viewed_number}</span>
                  <img src={blogLoveImg} className={classes.iconImg} />
                  <span className={classes.iconText}>{blog.liked_number}</span>
                  <Link href={"/blogs/edit/" + blog.uuid}>
                    <Button
                      color="primary"
                      variant="contained"
                      className={classes.actions}
                    >
                      Edit
                    </Button>
                  </Link>
                </Grid>
                <Grid
                  container
                  direction="row"
                  justify="flex-start"
                  alignItems="center"
                >
                  {blog?.is_published ? (
                    <Chip color="primary" size="small" label="Published" />
                  ) : (
                    <Chip
                      color="secondary"
                      size="small"
                      label="Not Published Yet"
                    />
                  )}
                  <Button
                    onClick={() => publishBlog(blog.id)}
                    color="primary"
                    variant="contained"
                    className={classes.actions}
                  >
                    Publish
                  </Button>
                  <Button
                    onClick={() => unpublishBlog(blog.id)}
                    color="primary"
                    variant="contained"
                    className={classes.actions}
                  >
                    Unpublish
                  </Button>
                </Grid>
                <Grid
                  container
                  direction="row"
                  justify="flex-start"
                  alignItems="center"
                >
                  {blog?.is_hidden ? (
                    <Chip
                      color="secondary"
                      size="small"
                      label="Hidden content"
                    />
                  ) : (
                    <Chip color="primary" size="small" label="Not hidden" />
                  )}
                  <Button
                    onClick={() => makeBlogHidden(blog.id)}
                    color="primary"
                    variant="contained"
                    className={classes.actions}
                  >
                    Make Hidden
                  </Button>
                  <Button
                    onClick={() => makeBlogUnHidden(blog.id)}
                    color="primary"
                    variant="contained"
                    className={classes.actions}
                  >
                    unhidden
                  </Button>
                </Grid>
              </Grid>
            </div>
          </CardContent>
        </div>
      </Card>
    </Grid>
  ) : blog.is_published && !blog?.is_hidden ? (
    <Grid item xs={12} md={12}>
      <Snackbars message={msg} statusCode={statusCode} />
      <Card className={classes.card} key={blog.uuid}>
        <Hidden xsDown>
          <CardMedia
            component="a"
            href={"/blogs/view/" + blog.uuid}
            className={classes.cardMedia}
            image={
              "http://" + window.location.host + "/static/" + blog.cover_img
            }
            title={blog.title}
          />
        </Hidden>
        <div className={classes.cardDetails}>
          <CardContent>
            <Typography component="h2" variant="h5">
              <Link href={"/blogs/view/" + blog.uuid}>{blog.title}</Link>
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              {moment.utc(blog.created_at).format("lll")}
            </Typography>
            <Typography variant="subtitle2" paragraph>
              {blog.blog_intro}
            </Typography>
            <FormattedMessage id="Label: " />
            {blog?.labels?.length === 0 && (
              <Chip
                label={<FormattedMessage id="None" />}
                disabled
                size="small"
              />
            )}
            {blog?.labels.map((label) => (
              <Chip
                color="primary"
                size="small"
                label={label?.name}
                className={classes.labelChip}
                onClick={() => handleLabelChange(label?.name)}
                key={label?.name + label?.id}
              />
            ))}
            <div className={classes.iconWrapper}>
              <Grid
                container
                direction="row"
                justify="flex-start"
                alignItems="center"
              >
                <img src={blogViewImg} className={classes.iconImg} />
                <span className={classes.iconText}>{blog.viewed_number}</span>
                <img src={blogLoveImg} className={classes.iconImg} />
                <span className={classes.iconText}>{blog.liked_number}</span>
              </Grid>
            </div>
          </CardContent>
        </div>
      </Card>
    </Grid>
  ) : blog.is_published && allowHidden && blog?.is_hidden ? (
    <Grid item xs={12} md={12}>
      <Snackbars message={msg} statusCode={statusCode} />
      <Card className={classes.card} key={blog.uuid}>
        <Hidden xsDown>
          <CardMedia
            component="a"
            href={"/blogs/view/" + blog.uuid}
            className={classes.cardMedia}
            image={
              "http://" + window.location.host + "/static/" + blog.cover_img
            }
            title={blog.title}
          />
        </Hidden>
        <div className={classes.cardDetails}>
          <CardContent>
            <Typography component="h2" variant="h5">
              <Link href={"/blogs/view/" + blog.uuid}>{blog.title}</Link>
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              {moment.utc(blog.created_at).format("lll")}
            </Typography>
            <Typography variant="subtitle2" paragraph>
              {blog.blog_intro}
            </Typography>
            <FormattedMessage id="Label: " />
            {blog?.labels?.length === 0 && (
              <Chip
                label={<FormattedMessage id="None" />}
                disabled
                size="small"
              />
            )}
            {blog?.labels.map((label) => (
              <Chip
                color="primary"
                size="small"
                label={label?.name}
                className={classes.labelChip}
                onClick={() => handleLabelChange(label?.name)}
                key={label?.name + label?.id}
              />
            ))}
            <div className={classes.iconWrapper}>
              <Grid
                container
                direction="row"
                justify="flex-start"
                alignItems="center"
              >
                <img src={blogViewImg} className={classes.iconImg} />
                <span className={classes.iconText}>{blog.viewed_number}</span>
                <img src={blogLoveImg} className={classes.iconImg} />
                <span className={classes.iconText}>{blog.liked_number}</span>
              </Grid>
            </div>
          </CardContent>
        </div>
      </Card>
    </Grid>
  ) : null;
}

BlogPost.propTypes = {
  post: PropTypes.object,
};
