import React, { useEffect, useState, useContext, Suspense } from "react";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import BlogPost from "../../components/Blog/BlogPost";
import SearchAndFilterBar from "../../components/Blog/SearchAndFilterBar";
import { sortByList } from "../../constants/sortBy";
import Pagination from "@material-ui/lab/Pagination";
import LinearProgress from "@material-ui/core/LinearProgress";

const useStyles = makeStyles((theme) => ({
  container: {
    display: `block`,
    width: `100%`,
  },
  pagenation: {
    display: `flex`,
    marginTop: 20,
    flexDirection: "column",
    alignItems: "center",
  },
}));

export default function Blog() {
  const classes = useStyles();
  const [blogs, setBlogs] = useState([]);
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
      "/api/blogs?" +
        new URLSearchParams({
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
        setBlogs(data.blogs);
        setTotalPage(data.count);
        setIsLoading(false);
      });

    fetch("/api/blogs/get-all", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setSearchItems(data);
      });
  }, [category, label, sortBy, order, page]);
  return (
    <BodyContainer size="md">
      <div className={classes.container}>
        <SearchAndFilterBar
          category={category}
          label={label}
          sortBy={sortBy}
          order={order}
          handleCategoryUpdate={handleCategoryUpdate}
          handleOrderChange={handleOrderChange}
          handleSortByChange={handleSortByChange}
          handleLabelDelete={handleLabelDelete}
          type={"blogs"}
          items={searchItems}
        />
        {loading ? (
          <LinearProgress />
        ) : (
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
            spacing={1}
          >
            {blogs.map((blog) => (
              <BlogPost
                blog={blog}
                key={blog.uuid}
                handleLabelChange={handleLabelChange}
                allowHidden={false}
              />
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
      </div>
    </BodyContainer>
  );
}
