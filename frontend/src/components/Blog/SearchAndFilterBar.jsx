import React, { useEffect, useState, useRef } from "react";
import { useHistory } from "react-router-dom";
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import dotaIcon from "../../assets/icon/categories/dota.png";
import fallguysIcon from "../../assets/icon/categories/fallguys.png";
import pianoIcon from "../../assets/icon/categories/piano.png";
import pubgIcon from "../../assets/icon/categories/pubg.png";
import Typography from "@material-ui/core/Typography";
import { categoryList } from "../../constants/category";
import { sortByList } from "../../constants/sortBy";
import { makeStyles } from "@material-ui/core/styles";
import { blue } from "@material-ui/core/colors";
import Grid from "@material-ui/core/Grid";
import Switch from "@material-ui/core/Switch";
import { FormattedMessage } from "react-intl";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import Chip from "@material-ui/core/Chip";

const useStyles = makeStyles((theme) => ({
  buttonGroup: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
  },
  iconImg: {
    maxWidth: 32,
    maxHeight: 32,
    marginLeft: 6,
  },
  buttonGroup: {
    color: "black",
  },
  text: {
    marginRight: 10,
  },
  buttonDefault: {
    color: "black",
    backgroundColor: blue[50],
    "&:hover": {
      backgroundColor: blue[400],
    },
  },
  buttonSelected: {
    color: blue[50],
    backgroundColor: blue[400],
  },
  searchBar: {
    display: "flex",
    alignItems: "center",
    marginLeft: -8,
    marginBottom: 10,
  },
  input: {
    marginLeft: theme.spacing(1),
    flex: 1,
  },
  iconButton: {
    padding: 10,
  },
  divider: {
    height: 28,
    margin: 4,
  },
}));

export default function SearchAndFilterBar(props) {
  const classes = useStyles();
  const history = useHistory();
  const { category, sortBy, order, items, type } = props;
  const search = useRef(null);

  const handleCategoryUpdate = (curCagetory) => {
    props.handleCategoryUpdate(curCagetory);
  };

  const handleOrderChange = (event) => {
    props.handleOrderChange(event);
  };
  const handleSortByChange = (newValue) => {
    props.handleSortByChange(newValue);
  };

  return (
    <React.Fragment>
      <Grid container direction="row" justify="flex-start" alignItems="center">
        {/* <Grid item>
          <div className={classes.buttonGroup}>
            <Typography
              variant="button"
              display="block"
              className={classes.text}
            >
              <FormattedMessage id="Filter:" />
            </Typography>
            <ButtonGroup
              variant="text"
              color="primary"
              aria-label="text primary button group"
            >
              <Button
                size="small"
                variant="contained"
                className={
                  category === "all"
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleCategoryUpdate("all")}
              >
                <FormattedMessage id="All" />
              </Button>
              <Button
                size="small"
                aria-label="dota"
                variant="contained"
                className={
                  category === categoryList[0]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleCategoryUpdate(categoryList[0])}
                startIcon={<img src={dotaIcon} className={classes.iconImg} />}
              ></Button>
              <Button
                size="small"
                aria-label="fallguys"
                variant="contained"
                className={
                  category === categoryList[1]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleCategoryUpdate(categoryList[1])}
                startIcon={
                  <img src={fallguysIcon} className={classes.iconImg} />
                }
              ></Button>
              <Button
                size="small"
                aria-label="pubg"
                variant="contained"
                className={
                  category === categoryList[2]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleCategoryUpdate(categoryList[2])}
                startIcon={<img src={pubgIcon} className={classes.iconImg} />}
              ></Button>
              <Button
                size="small"
                aria-label="piano"
                variant="contained"
                className={
                  category === categoryList[3]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleCategoryUpdate(categoryList[3])}
                startIcon={<img src={pianoIcon} className={classes.iconImg} />}
              ></Button>
            </ButtonGroup>
          </div>
        </Grid> */}
        <Grid item>
          <Typography variant="button" display="block" className={classes.text}>
            <FormattedMessage id="Sort By:" />
          </Typography>
          <div className={classes.buttonGroup}>
            <ButtonGroup
              variant="text"
              color="primary"
              aria-label="text primary button group"
            >
              <Button
                aria-label={sortByList[0]}
                variant="contained"
                size="small"
                className={
                  sortBy === sortByList[0]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleSortByChange(sortByList[0])}
              >
                <FormattedMessage id={sortByList[0]} />
              </Button>
              {/* <Button
                aria-label={sortByList[1]}
                variant="contained"
                size="small"
                className={
                  sortBy === sortByList[1]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleSortByChange(sortByList[1])}
              >
                <FormattedMessage id={sortByList[1]} />
              </Button> */}
              <Button
                aria-label={sortByList[2]}
                variant="contained"
                size="small"
                className={
                  sortBy === sortByList[2]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleSortByChange(sortByList[2])}
              >
                <FormattedMessage id={sortByList[2]} />
              </Button>
              <Button
                aria-label={sortByList[3]}
                variant="contained"
                size="small"
                className={
                  sortBy === sortByList[3]
                    ? classes.buttonSelected
                    : classes.buttonDefault
                }
                onClick={() => handleSortByChange(sortByList[3])}
              >
                <FormattedMessage id={sortByList[3]} />
              </Button>
            </ButtonGroup>
          </div>
          <Typography variant="button" display="inline">
            <FormattedMessage id="ASC" />
          </Typography>
          <Switch
            checked={order === "desc"}
            onChange={handleOrderChange}
            color="primary"
            name="sortOrder"
            size="medium"
            inputProps={{ "aria-label": "primary checkbox" }}
          />
          <Typography variant="button" display="inline">
            <FormattedMessage id="DESC" />
          </Typography>
        </Grid>
      </Grid>
      <Grid item xs={11} sm={12}>
        <Autocomplete
          id="search-bar"
          className={classes.searchBar}
          freeSolo
          options={items}
          getOptionLabel={(option) => option?.title}
          renderOption={(option) => (
            <div
              style={{ width: `100%`, cursor: `pointer` }}
              onClick={() => {
                history.push("/" + type + "/" + option?.uuid);
              }}
            >
              <div style={{ flexGrow: 1 }}>
                <FormattedMessage id="Title" defaultMessage="Title" />
                {": " + option?.title}
                <br />
                <Chip
                  color="primary"
                  size="small"
                  label={
                    <FormattedMessage
                      id="blog intro"
                      values={{ intro: option.blog_intro }}
                    />
                  }
                />
                {option?.labels.map((label) => (
                  <Chip
                    color="secondary"
                    size="small"
                    label={label.name}
                    className={classes.labelChip}
                  />
                ))}
              </div>
            </div>
          )}
          renderInput={(params) => (
            <TextField
              {...params}
              className={classes.input}
              label="Search"
              margin="normal"
              variant="outlined"
              inputRef={search}
            />
          )}
        />
      </Grid>
    </React.Fragment>
  );
}
