import React, { useContext, useState } from "react";
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
}));
export default function VideoItem(props) {
  const classes = useStyles();
  const { video } = props;
  const user = useContext(userContext);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
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
        break;
      case "dota":
        return <img src={dotaIcon} className={classes.iconImg} />;
        break;
      case "fallguys":
        return <img src={fallguysIcon} className={classes.iconImg} />;
        break;
      case "piano":
        return <img src={pianoIcon} className={classes.iconImg} />;
        break;
      default:
        return <img src={dotaIcon} className={classes.iconImg} />;
        break;
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
        <Typography variant="h6" component="h6">
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
