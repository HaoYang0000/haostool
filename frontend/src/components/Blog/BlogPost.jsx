import React, { useContext, useState } from "react";
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
  iconWrapper: {},
  iconText: {
    marginLeft: 5,
    marginRight: 5,
  },
  actions: {
    marginLeft: 10,
  },
});

export default function BlogPost(props) {
  const classes = useStyles();
  const { blog } = props;
  const user = useContext(userContext);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
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
            <div className={classes.iconWrapper}>
              <img src={blogViewImg} className={classes.iconImg} />
              <span className={classes.iconText}>{blog.viewed_number}</span>
              <img src={blogLoveImg} className={classes.iconImg} />
              <span className={classes.iconText}>{blog.liked_number}</span>
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
              <Link href={"/blogs/edit/" + blog.uuid}>
                <Button
                  color="primary"
                  variant="contained"
                  className={classes.actions}
                >
                  Edit
                </Button>
              </Link>
            </div>
          </CardContent>
        </div>
      </Card>
    </Grid>
  ) : blog.is_published ? (
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
            <div className={classes.iconWrapper}>
              <img src={blogViewImg} className={classes.iconImg} />
              <span className={classes.iconText}>{blog.viewed_number}</span>
              <img src={blogLoveImg} className={classes.iconImg} />
              <span className={classes.iconText}>{blog.liked_number}</span>
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
