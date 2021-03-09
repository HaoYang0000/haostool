import React, { useEffect, useState } from "react";
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import IconButton from "@material-ui/core/IconButton";
import DeleteIcon from "@material-ui/icons/Delete";
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

const useStyles = makeStyles((theme) => ({
  buttonGroup: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
  },
  iconImg: {
    width: 40,
    height: 40,
    marginLeft: 10,
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
}));

export default function SearchAndFilterBar(props) {
  const classes = useStyles();
  const { category, sortBy, order } = props;

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
    <Grid container direction="row" justify="space-between" alignItems="center">
      <Grid item>
        <div className={classes.buttonGroup}>
          <Typography variant="button" display="block" className={classes.text}>
            <FormattedMessage id="Filter:" />
          </Typography>
          <ButtonGroup
            variant="text"
            color="primary"
            aria-label="text primary button group"
          >
            <Button
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
              aria-label="fallguys"
              variant="contained"
              className={
                category === categoryList[1]
                  ? classes.buttonSelected
                  : classes.buttonDefault
              }
              onClick={() => handleCategoryUpdate(categoryList[1])}
              startIcon={<img src={fallguysIcon} className={classes.iconImg} />}
            ></Button>
            <Button
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
      </Grid>
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
            <Button
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
            </Button>
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
          size="middle"
          inputProps={{ "aria-label": "primary checkbox" }}
        />
        <Typography variant="button" display="inline">
          <FormattedMessage id="DESC" />
        </Typography>
      </Grid>
    </Grid>
  );
}
