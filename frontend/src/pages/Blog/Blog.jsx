import React, { useEffect, useState, useContext, Suspense } from "react";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import BlogPost from "../../components/Blog/BlogPost";
const useStyles = makeStyles((theme) => ({
  container: {
    display: `block`,
    width: `100%`,
  },
}));
export default function Blog() {
  const classes = useStyles();
  const [blogs, setBlogs] = useState([]);
  useEffect(() => {
    fetch("/api/blogs", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setBlogs(data);
      });
  }, []);
  return (
    <BodyContainer size="md">
      <div className={classes.container}>
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
          spacing={2}
        >
          {blogs.map((blog) => (
            <BlogPost blog={blog} key={blog.uuid} />
          ))}
        </Grid>
      </div>
    </BodyContainer>
  );
}
