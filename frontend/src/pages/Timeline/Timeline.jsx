import React, { useEffect, useState, useContext, useRef } from "react";
import Timeline from "@material-ui/lab/Timeline";
import TimelineItem from "@material-ui/lab/TimelineItem";
import TimelineSeparator from "@material-ui/lab/TimelineSeparator";
import TimelineConnector from "@material-ui/lab/TimelineConnector";
import TimelineContent from "@material-ui/lab/TimelineContent";
import TimelineOppositeContent from "@material-ui/lab/TimelineOppositeContent";
import TimelineDot from "@material-ui/lab/TimelineDot";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import moment from "moment";
import { authFetch, userContext } from "../../pages/Auth/Auth";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import { DeleteForever } from "@material-ui/icons";
import Snackbars from "../../components/Snackbars/Snackbars";
const useStyles = makeStyles((theme) => ({
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `100%`,
  },
  dot: {
    background: `rgb(227, 80, 62)`,
  },
  line: {
    background: `linear-gradient(to bottom, rgba(80,80,80,0) 0%, rgb(18, 40, 73) 20%, rgb(18, 40, 73) 80%, rgba(80,80,80,0) 100%)`,
    width: 2,
  },
  timestamp: {
    padding: `4px 6px`,
    color: `rgb(227, 80, 62)`,
  },
  paper: {
    padding: "6px 16px",
  },
  secondaryTail: {
    backgroundColor: theme.palette.secondary.main,
  },
}));
export default function TimelinePage() {
  const classes = useStyles();
  const [timelines, setTimelines] = useState([]);
  const title = useRef(null);
  const content = useRef(null);
  const user = useContext(userContext);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  useEffect(() => {
    fetch("/api/timelines", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setTimelines(data);
      });
  }, []);
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = {
      title: title.current.value,
      content: content.current.value,
    };

    authFetch("/api/timelines/add", {
      method: "post",
      body: JSON.stringify(data),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
    window.location.reload();
  };
  const deleteTimeline = (timeline_id) => {
    authFetch("/api/timelines/disable", {
      method: "delete",
      body: JSON.stringify({ timeline_id: timeline_id }),
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
    window.location.reload();
  };
  return (
    <BodyContainer size="md">
      <Snackbars message={msg} statusCode={statusCode} />
      <div className={classes.container}>
        {user.role === "root" ? (
          <form className={classes.form} noValidate onSubmit={handleSubmit}>
            <Typography component="h1" variant="h5">
              Create New Timeline
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="title"
              label="Title"
              name="title"
              autoComplete="title"
              autoFocus
              inputRef={title}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="content"
              label="Content"
              type="content"
              id="content"
              inputRef={content}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
            >
              Create
            </Button>
          </form>
        ) : null}
        <Timeline>
          {timelines.map((timeline) => (
            <TimelineItem key={timeline.id}>
              <TimelineOppositeContent>
                <Typography className={classes.timestamp}>
                  {moment.utc(timeline.created_at).format("lll")}
                </Typography>
                {user.role === "root" ? (
                  <React.Fragment>
                    <Button onClick={() => deleteTimeline(timeline.id)}>
                      <DeleteForever />
                    </Button>
                  </React.Fragment>
                ) : null}
              </TimelineOppositeContent>
              <TimelineSeparator>
                <TimelineDot className={classes.dot} />
                <TimelineConnector className={classes.line} />
              </TimelineSeparator>
              <TimelineContent>
                <Paper elevation={3} className={classes.paper}>
                  <Typography variant="h6" component="h1">
                    {timeline.title}
                  </Typography>

                  <Typography>{timeline.content}</Typography>
                </Paper>
              </TimelineContent>
            </TimelineItem>
          ))}
        </Timeline>
      </div>
    </BodyContainer>
  );
}
