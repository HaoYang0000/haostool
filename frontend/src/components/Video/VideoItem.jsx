import React, { useContext, useState, useEffect } from "react";
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
import PersonIcon from "@material-ui/icons/Person";
import AddIcon from "@material-ui/icons/Add";
import AddCircleIcon from "@material-ui/icons/AddCircle";
import { IconButton } from "@material-ui/core";
import Chip from "@material-ui/core/Chip";

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
}));

function SimpleDialog(props) {
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

export default function VideoItem(props) {
  const classes = useStyles();
  const { video } = props;
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

  const handleDelete = (labelId, videoId) => {
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

  const handleUpdate = (labelId, videoId) => {
    setOpen(false);
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
            "http://" + window.location.host + "/static/" + video.thumb_nail
          }
          title="Image title"
        />
      </Link>
      <CardContent className={classes.cardContent}>
        <Typography gutterBottom variant="h5" component="h2">
          <Link href={"/videos/" + video.uuid}>{video.title}</Link>
          {user.role === "root" || user.role === "admin" ? (
            <React.Fragment>
              <Button onClick={() => deleteVideo(video.id)}>
                <DeleteForever />
              </Button>
            </React.Fragment>
          ) : null}
        </Typography>
        {user.role === "root" || user.role === "admin" ? (
          <React.Fragment>
            <FormattedMessage id="Label: " />
            <IconButton onClick={handleClickOpen}>
              <AddCircleIcon color="primary" />
            </IconButton>
            {video?.labels?.length === 0 && (
              <Chip
                label={<FormattedMessage id="None" />}
                disabled
                size="small"
              />
            )}
            {video?.labels.map((label) => (
              <Chip
                color="secondary"
                size="small"
                label={label.name}
                className={classes.labelChip}
                key={label?.name + label?.id}
                onDelete={() => handleDelete(label?.id, video?.id)}
              />
            ))}
            <SimpleDialog
              open={open}
              handleClose={handleClose}
              handleUpdate={handleUpdate}
              video={video}
            />
          </React.Fragment>
        ) : (
          <React.Fragment>
            <FormattedMessage id="Label: " />
            {video?.labels?.length === 0 && (
              <Chip
                label={<FormattedMessage id="None" />}
                disabled
                size="small"
              />
            )}
            {video?.labels.map((label) => (
              <Chip
                color="secondary"
                size="small"
                label={label?.name}
                className={classes.labelChip}
                key={label?.name + label?.id}
              />
            ))}
          </React.Fragment>
        )}
        <Typography variant="body1" display="block">
          <FormattedMessage id="Ratings:" defaultMessage="Ratings:" />
          <Rating value={video.star} readOnly />
          {user.role === "root" || user.role === "admin" ? (
            <React.Fragment>
              <Button onClick={() => increaseStar(video.id)}>
                <ArrowUpward />
              </Button>
              <Button onClick={() => decreaseStar(video.id)}>
                <ArrowDownward />
              </Button>
            </React.Fragment>
          ) : null}
        </Typography>
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
