import React, { useEffect, useState, useContext, Suspense } from "react";
import Grid from "@material-ui/core/Grid";
import Skeleton from "@material-ui/lab/Skeleton";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import { userContext } from "../../pages/Auth/Auth";
import SearchAndFilterBar from "../../components/Video/SearchAndFilterBar";
import { sortByList } from "../../constants/sortBy";
import Pagination from "@material-ui/lab/Pagination";
import LinearProgress from "@material-ui/core/LinearProgress";

const VideoItem = React.lazy(() => import("../../components/Video/VideoItem"));
const useStyles = makeStyles((theme) => ({
  fallback: {
    width: 280,
    height: 380,
  },
  container: {},
  pagenation: {
    display: `flex`,
    marginTop: 20,
    flexDirection: "column",
    alignItems: "center",
  },
}));
export default function Video() {
  const classes = useStyles();
  const [videos, setVideos] = useState([]);
  const user = useContext(userContext);
  const [category, setCategory] = useState("all");
  const [label, setLabel] = useState("");
  const [sortBy, setSortBy] = useState(sortByList[0]);
  const [order, setOrder] = useState("desc");
  const [page, setPage] = useState(1);
  const [totalPage, setTotalPage] = useState(5);
  const [loading, setIsLoading] = useState(false);
  const [searchItems, setSearchItems] = useState([]);

  const handleChange = (event, value) => {
    setPage(value);
  };

  const handleCategoryUpdate = (curCagetory) => {
    setCategory(curCagetory);
  };

  const handleLabelChange = (curLabel) => {
    let tmpLabel = label;
    if (!tmpLabel.includes(curLabel)) {
      if (tmpLabel === "") {
        tmpLabel = curLabel;
      } else {
        tmpLabel = tmpLabel + "," + curLabel;
      }

      setLabel(tmpLabel);
    }
  };

  const handleLabelDelete = (dropLabel) => {
    let tmpLabelList = label.split(",");
    let outputList = [];
    for (let index = 0; index < tmpLabelList.length; index++) {
      if (tmpLabelList[index] !== dropLabel) {
        outputList.push(tmpLabelList[index]);
      }
    }
    setLabel(outputList.join(","));
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
    setIsLoading(true);
    fetch(
      "/api/videos?" +
        new URLSearchParams({
          category: category,
          label: label,
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
        setIsLoading(false);
      });
    fetch("/api/videos/get-all", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setSearchItems(data);
      });
  }, [category, label, sortBy, order, page]);

  return (
    <BodyContainer size="md">
      <SearchAndFilterBar
        category={category}
        sortBy={sortBy}
        order={order}
        label={label}
        handleCategoryUpdate={handleCategoryUpdate}
        handleOrderChange={handleOrderChange}
        handleSortByChange={handleSortByChange}
        handleLabelDelete={handleLabelDelete}
        type={"videos"}
        items={searchItems}
      />

      {loading ? (
        <LinearProgress />
      ) : (
        <Grid container spacing={1}>
          {videos.map((video) => (
            <Grid item key={video.uuid} xs={12} sm={6} md={4}>
              <Suspense
                fallback={
                  <Skeleton variant="rect" className={classes.fallback} />
                }
              >
                <VideoItem
                  video={video}
                  handleLabelChange={handleLabelChange}
                />
              </Suspense>
            </Grid>
          ))}
        </Grid>
      )}
      <Pagination
        count={totalPage}
        shape="rounded"
        page={page}
        onChange={handleChange}
        className={classes.pagenation}
      />
    </BodyContainer>
  );
}
