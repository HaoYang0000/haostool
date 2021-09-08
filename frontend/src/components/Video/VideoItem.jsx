import React, { useContext, useState, useEffect, useRef } from "react";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Button from "@material-ui/core/Button";
import CameraIcon from "@material-ui/icons/PhotoCamera";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import CssBaseline from "@material-ui/core/CssBaseline";
import Grid from "@material-ui/core/Grid";
import Toolbar from "@material-ui/core/Toolbar";
import Link from "@material-ui/core/Link";
import { userContext, authFetch } from "../../pages/Auth/Auth";
import { ArrowUpward, ArrowDownward, DeleteForever } from "@material-ui/icons";
import thumbUpImg from "../../assets/icon/thumb_up.png";
import viewedNumImg from "../../assets/icon/viewed_num.png";
import straImg from "../../assets/icon/star.png";
import dotaIcon from "../../assets/icon/categories/dota.png";
import fallguysIcon from "../../assets/icon/categories/fallguys.png";
import pianoIcon from "../../assets/icon/categories/piano.png";
import saxIcon from "../../assets/icon/categories/sax.png";
import pubgIcon from "../../assets/icon/categories/pubg.png";
import Rating from "@material-ui/lab/Rating";
import Snackbars from "../../components/Snackbars/Snackbars";
import { FormattedMessage } from "react-intl";
import Avatar from "@material-ui/core/Avatar";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Dialog from "@material-ui/core/Dialog";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import AddCircleIcon from "@material-ui/icons/AddCircle";
import { IconButton } from "@material-ui/core";
import Chip from "@material-ui/core/Chip";
import TextField from "@material-ui/core/TextField";
import InputLabel from "@material-ui/core/InputLabel";
import { videoSourceList } from "../../constants/videoSource";
import Box from "@material-ui/core/Box";
import PlusOneOutlinedIcon from "@material-ui/icons/PlusOneOutlined";
import ExposureNeg1OutlinedIcon from "@material-ui/icons/ExposureNeg1Outlined";

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  iconImg: {
    width: 40,
    height: 40,
  },
  iconStar: {
    width: 20,
    height: 20,
  },
  card: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
  },
  cardMedia: {
    paddingTop: "56.25%", // 16:9
  },
  cardContent: {
    flexGrow: 1,
  },
  labelChip: {
    padding: 2,
    marginRight: 2,
  },
  generalTextMargin: {
    marginBottom: 5,
  },
}));

function LableDialog(props) {
  const classes = useStyles();
  const [labels, setLabels] = useState([]);
  const { open, video } = props;

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
    props.handleUpdate(labelId, video?.id);
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
        {labels.length > 0
          ? labels?.map((label) => (
              <ListItem
                button
                onClick={() => handleListItemClick(label?.id)}
                key={label?.name + label?.id}
              >
                <ListItemText primary={label?.name} />
              </ListItem>
            ))
          : null}
      </List>
    </Dialog>
  );
}

function VideoSourceDialog(props) {
  const classes = useStyles();
  const { open, video } = props;
  const videoUrl = useRef(null);
  const [videoSource, setVideoSource] = useState(videoSourceList[0]);

  const handleChange = (event) => {
    setVideoSource(event.target.value);
  };

  useEffect(() => {}, []);

  const handleClose = () => {
    props.handleClose();
  };

  const handleVideoSourceAdd = () => {
    props.handleUpdate(videoSource, videoUrl.current.value, video?.id);
    props.handleClose();
  };

  return (
    <Dialog
      onClose={handleClose}
      fullWidth={true}
      maxWidth={"md"}
      aria-labelledby="simple-dialog-title"
      open={open}
    >
      <DialogTitle id="simple-dialog-title">Add new source</DialogTitle>
      <TextField
        variant="outlined"
        margin="normal"
        required
        fullWidth
        id="videoUrl"
        label="source url"
        name="videoUrl"
        autoComplete="videoUrl"
        autoFocus
        inputRef={videoUrl}
      />
      <InputLabel id="category-select-outlined-label">Video Source</InputLabel>
      <Select
        labelId="category-select-outlined-label"
        id="category-select-outlined"
        value={videoSource}
        onChange={handleChange}
        label="videoSource"
      >
        <MenuItem value={videoSourceList[0]}>{videoSourceList[0]}</MenuItem>
      </Select>
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        className={classes.submit}
        onClick={() => handleVideoSourceAdd()}
      >
        Upload
      </Button>
    </Dialog>
  );
}

export default function VideoItem(props) {
  const classes = useStyles();
  const { video } = props;
  const user = useContext(userContext);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const [openLabel, setOpenLabel] = useState(false);
  const [openVideoSource, setOpenVideoSource] = useState(false);

  const handleLabelChange = (curLabel) => {
    props.handleLabelChange(curLabel);
  };

  const handleClickOpenLabel = () => {
    setOpenLabel(true);
  };

  const handleCloseLabel = () => {
    setOpenLabel(false);
  };

  const handleClickOpenVideoSource = () => {
    setOpenVideoSource(true);
  };

  const handleCloseVideoSource = () => {
    setOpenVideoSource(false);
  };

  const handleDeleteLabel = (labelId, videoId) => {
    var formData = new FormData();
    formData.append("label_id", labelId);
    formData.append("video_id", videoId);

    authFetch("/api/labels/delete/video-label", {
      method: "DELETE",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const handleUpdateLabel = (labelId, videoId) => {
    setOpenLabel(false);
    var formData = new FormData();
    formData.append("label_id", labelId);
    formData.append("video_id", videoId);
    authFetch("/api/labels/create/video-label", {
      method: "POST",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const handleUpdateVideoSource = (videoSource, videoUrl, videoId) => {
    setOpenVideoSource(false);
    var formData = new FormData();
    formData.append("name", videoSource);
    formData.append("url", videoUrl);
    formData.append("video_id", videoId);
    authFetch("/api/videos/source", {
      method: "POST",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const handleDeleteVideoSource = (videoSourceId) => {
    var formData = new FormData();
    formData.append("source_id", videoSourceId);
    authFetch("/api/videos/source", {
      method: "DELETE",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const increaseStar = (videoId) => {
    authFetch("/api/videos/increase_star", {
      method: "post",
      body: JSON.stringify({ video_id: videoId }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const decreaseStar = (videoId) => {
    authFetch("/api/videos/decrease_star", {
      method: "post",
      body: JSON.stringify({ video_id: videoId }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };
  const generateCategoryIcon = (category) => {
    switch (category) {
      case "pubg":
        return <img src={pubgIcon} className={classes.iconImg} />;
      case "dota":
        return <img src={dotaIcon} className={classes.iconImg} />;
      case "fallguys":
        return <img src={fallguysIcon} className={classes.iconImg} />;
      case "piano":
        return <img src={pianoIcon} className={classes.iconImg} />;
      case "sax":
        return <img src={saxIcon} className={classes.iconImg} />;
      default:
        return <img src={dotaIcon} className={classes.iconImg} />;
    }
  };
  const deleteVideo = (videoId) => {
    authFetch("/api/videos/delete", {
      method: "delete",
      body: JSON.stringify({ video_id: videoId }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
    window.location.reload();
  };
  return (
    <Card className={classes.card}>
      <Snackbars message={msg} statusCode={statusCode} />
      <Link href={"/videos/" + video.uuid}>
        <CardMedia
          className={classes.cardMedia}
          image={
            "http://" + window.location.host + "/static/" + video?.thumb_nail
          }
          title="Image title"
        />
      </Link>
      <CardContent className={classes.cardContent}>
        <Typography gutterBottom variant="h5" component="h2">
          <Link href={"/videos/" + video.uuid}>{video.title}</Link>
          {user.role === "root" || user.role === "admin" ? (
            <Button onClick={() => deleteVideo(video.id)}>
              <DeleteForever />
            </Button>
          ) : null}
        </Typography>
        <Box className={classes.generalTextMargin}>
          <FormattedMessage id="Label: " />
          {user.role === "root" || user.role === "admin" ? (
            <React.Fragment>
              <IconButton onClick={handleClickOpenLabel}>
                <AddCircleIcon color="primary" />
              </IconButton>
              <LableDialog
                open={openLabel}
                handleClose={handleCloseLabel}
                handleUpdate={handleUpdateLabel}
                video={video}
              />
            </React.Fragment>
          ) : null}
          {video?.labels?.length === 0 && (
            <Chip
              label={<FormattedMessage id="None" />}
              disabled
              size="small"
            />
          )}
          {video?.labels?.map((label) => (
            <Chip
              color="primary"
              size="small"
              label={label.name}
              className={classes.labelChip}
              key={label?.name + label?.id}
              onClick={() => handleLabelChange(label?.name)}
              onDelete={
                user.role === "root" || user.role === "admin"
                  ? () => handleDeleteLabel(label?.id, video?.id)
                  : null
              }
            />
          ))}
        </Box>
        {user.role === "root" || user.role === "admin" ? (
          <Box className={classes.generalTextMargin}>
            <FormattedMessage id="Video Source" defaultMessage="Video Source" />
            {": "}
            <IconButton onClick={handleClickOpenVideoSource}>
              <AddCircleIcon color="primary" />
            </IconButton>
            {video?.sources?.length === 0 && (
              <Chip
                label={<FormattedMessage id="None" />}
                disabled
                size="small"
              />
            )}
            {video?.sources.map((videoSource) => (
              <Chip
                color="secondary"
                size="small"
                label={videoSource.name}
                className={classes.labelChip}
                key={videoSource?.name + videoSource?.id}
                onDelete={() => handleDeleteVideoSource(videoSource?.id)}
              />
            ))}
            <VideoSourceDialog
              open={openVideoSource}
              handleClose={handleCloseVideoSource}
              handleUpdate={handleUpdateVideoSource}
              video={video}
            />
          </Box>
        ) : null}
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="center"
        >
          <Grid item>
            <FormattedMessage id="Ratings:" defaultMessage="Ratings:" />
          </Grid>
          <Grid item>
            <Rating value={video.star} readOnly />
          </Grid>
          {user.role === "root" || user.role === "admin" ? (
            <Grid item>
              <IconButton onClick={() => increaseStar(video.id)}>
                <PlusOneOutlinedIcon />
              </IconButton>
              <IconButton onClick={() => decreaseStar(video.id)}>
                <ExposureNeg1OutlinedIcon />
              </IconButton>
            </Grid>
          ) : null}
        </Grid>
      </CardContent>
      <CardActions>
        <img src={viewedNumImg} className={classes.iconImg} />
        {video.viewed_number}
        <img src={thumbUpImg} className={classes.iconImg} />
        {video.liked_number}
        {generateCategoryIcon(video.category)}
      </CardActions>
    </Card>
  );
}
