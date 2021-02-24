import React from "react";
import { useHistory } from "react-router-dom";
import { FormattedMessage } from "react-intl";
import { makeStyles } from "@material-ui/core/styles";
import SpeedDial from "@material-ui/lab/SpeedDial";
import SpeedDialIcon from "@material-ui/lab/SpeedDialIcon";
import SpeedDialAction from "@material-ui/lab/SpeedDialAction";
import blogImg from "../../assets/speedDials/blog.png";
import commentImg from "../../assets/speedDials/comment.png";
import donateImg from "../../assets/speedDials/donate.png";
import movieImg from "../../assets/speedDials/movie.png";
import settingsImg from "../../assets/speedDials/settings.png";
import wechatImg from "../../assets/speedDials/wechat.png";

const useStyles = makeStyles((theme) => ({
  wrapper: {
    zIndex: 5,
    position: `fixed`,
    bottom: 100,
    right: 30,
  },
  radioGroup: {
    margin: theme.spacing(1, 0),
  },
  iconImg: {
    width: 40,
    height: 40,
  },
  actionWarpper: {
    backgroundColor: `transparent`,
  },
  speedDial: {
    position: "absolute",
    "&.MuiSpeedDial-directionUp, &.MuiSpeedDial-directionLeft": {
      bottom: theme.spacing(2),
      right: theme.spacing(2),
    },
    "&.MuiSpeedDial-directionDown, &.MuiSpeedDial-directionRight": {
      top: theme.spacing(2),
      left: theme.spacing(2),
    },
  },
}));

export default function SpeedDials(props) {
  const classes = useStyles();
  const history = useHistory();
  const actions = [
    {
      icon: <img src={settingsImg} className={classes.iconImg} />,
      name: <FormattedMessage id="Settings" defaultMessage="Settings" />,
      url: "/auth/settings",
    },
    {
      icon: <img src={donateImg} className={classes.iconImg} />,
      name: <FormattedMessage id="Donate" defaultMessage="Donate" />,
      url: "/contacts/donate",
    },
    {
      icon: <img src={wechatImg} className={classes.iconImg} />,
      name: <FormattedMessage id="Wechat" defaultMessage="Wechat" />,
      url: "/contacts/wechat",
    },
    {
      icon: <img src={commentImg} className={classes.iconImg} />,
      name: <FormattedMessage id="Comment" defaultMessage="Comment" />,
      url: "/comments",
    },
    {
      icon: <img src={movieImg} className={classes.iconImg} />,
      name: <FormattedMessage id="Videos" defaultMessage="Videos" />,
      url: "/videos",
    },
    {
      icon: <img src={blogImg} className={classes.iconImg} />,
      name: <FormattedMessage id="Blogs" defaultMessage="Blogs" />,
      url: "/blogs",
    },
  ];
  const [open, setOpen] = React.useState(false);

  const handleClick = (url) => {
    history.push(url);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  return (
    <div className={classes.wrapper}>
      <SpeedDial
        ariaLabel="SpeedDial example"
        className={classes.speedDial}
        icon={<SpeedDialIcon />}
        onClose={handleClose}
        onOpen={handleOpen}
        open={open}
        direction="up"
      >
        {actions.map((action) => (
          <SpeedDialAction
            key={action.url}
            icon={action.icon}
            tooltipTitle={action.name}
            onClick={() => handleClick(action.url)}
            className={classes.actionWarpper}
          />
        ))}
      </SpeedDial>
    </div>
  );
}
