import React, { useEffect, useState, useContext, Suspense } from "react";
import Grid from "@material-ui/core/Grid";
import Skeleton from "@material-ui/lab/Skeleton";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import { userContext } from "../../pages/Auth/Auth";
const VideoItem = React.lazy(() => import("../../components/Video/VideoItem"));
const useStyles = makeStyles((theme) => ({
  fallback: {
    width: 280,
    height: 380,
  },
}));
export default function Video() {
  const classes = useStyles();
  const [videos, setVideos] = useState([]);
  const user = useContext(userContext);
  useEffect(() => {
    fetch("/videos", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setVideos(data);
      });
  }, []);
  return (
    <BodyContainer size="md">
      <main>
        <Grid container spacing={4}>
          {videos.map((video) => (
            <Grid item key={video.uuid} xs={12} sm={6} md={4}>
              <Suspense
                fallback={
                  <Skeleton variant="rect" className={classes.fallback} />
                }
              >
                <VideoItem video={video} />
              </Suspense>
            </Grid>
          ))}
        </Grid>
      </main>
    </BodyContainer>
  );
}
