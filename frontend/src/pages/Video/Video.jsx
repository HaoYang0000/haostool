import React, { useEffect, useState, useContext, Suspense } from "react";
import Grid from "@material-ui/core/Grid";
import Skeleton from "@material-ui/lab/Skeleton";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import { userContext } from "../../pages/Auth/Auth";
import SearchAndFilterBar from "../../components/SearchBar/SearchAndFilterBar";
import { categoryList } from "../../constants/category";
import { sortByList } from "../../constants/sortBy";
import Pagination from "@material-ui/lab/Pagination";
import Divider from "@material-ui/core/Divider";

const VideoItem = React.lazy(() => import("../../components/Video/VideoItem"));
const useStyles = makeStyles((theme) => ({
  fallback: {
    width: 280,
    height: 380,
  },
  container: {
    width: `100%`,
  },
  pagenation: {
    display: `flex`,
    marginTop: 20,
    flexDirection: "column",
    alignItems: "center",
  },
  divider: {
    marginBottom: 10,
  },
}));
export default function Video() {
  const classes = useStyles();
  const [videos, setVideos] = useState([]);
  const user = useContext(userContext);
  const [category, setCategory] = useState("all");
  const [sortBy, setSortBy] = useState(sortByList[0]);
  const [order, setOrder] = useState("desc");
  const [page, setPage] = useState(1);
  const [totalPage, setTotalPage] = useState(5);

  const handleChange = (event, value) => {
    setPage(value);
  };

  const handleCategoryUpdate = (curCagetory) => {
    setCategory(curCagetory);
  };

  const handleOrderChange = (event) => {
    if (event.target.checked) {
      setOrder("desc");
    } else {
      setOrder("asc");
    }
  };
  const handleSortByChange = (newValue) => {
    setSortBy(newValue);
  };
  useEffect(() => {
    fetch(
      "/api/videos?" +
        new URLSearchParams({
          category: category,
          sortBy: sortBy,
          order: order,
          page: page,
        }),
      {
        method: "get",
      }
    )
      .then((r) => r.json())
      .then((data) => {
        setVideos(data.videos);
        setTotalPage(data.count);
      });
  }, [category, sortBy, order, page]);

  return (
    <BodyContainer size="md">
      <main className={classes.container}>
        <SearchAndFilterBar
          category={category}
          sortBy={sortBy}
          order={order}
          handleCategoryUpdate={handleCategoryUpdate}
          handleOrderChange={handleOrderChange}
          handleSortByChange={handleSortByChange}
        />
        <Divider className={classes.divider} />
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
        <Pagination
          count={totalPage}
          shape="rounded"
          page={page}
          onChange={handleChange}
          className={classes.pagenation}
        />
      </main>
    </BodyContainer>
  );
}
