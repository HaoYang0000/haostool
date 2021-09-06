import React, { useEffect, useState, useRef } from "react";
import Typography from "@material-ui/core/Typography";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import { userContext, authFetch } from "../Auth/Auth";
import Button from "@material-ui/core/Button";
import Snackbars from "../../components/Snackbars/Snackbars";
import { FormattedMessage } from "react-intl";
import TextField from "@material-ui/core/TextField";
import List from "@material-ui/core/List";
import Chip from "@material-ui/core/Chip";
import Divider from "@material-ui/core/Divider";
import DoneIcon from "@material-ui/icons/Done";
import { Link } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `95%`,
  },
  container: {
    display: `block`,
    width: `100%`,
  },
  textArea: {
    marginTop: 15,
    borderRadius: 5,
    background: `#f7f7f7`,
    padding: 2,
    boxShadow: `inset 2px 2px 6px rgba(0,0,0,.08)`,
    minHeight: 100,
    width: `99%`,
    backgroundAttachment: `scroll`,
    resize: `none`,
    borderColor: `#c4c4c4`,
  },
  button: {
    marginTop: 15,
  },
  hr: {
    width: `100%`,
    marginTop: 15,
    marginBottom: 15,
  },
}));
export default function Backup() {
  const classes = useStyles();
  const [backups, setBackups] = useState([]);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const [file, setFile] = useState(null);
  let name = useRef("");

  useEffect(() => {
    authFetch("/api/backup-restore/backups", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setBackups(data?.backups);
      });
  }, []);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const deleteBackupRecord = (id) => {
    var formData = new FormData();
    formData.append("id", id);

    authFetch("/api/backup-restore/backups/record", {
      method: "DELETE",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  const handleBackupFileUpload = (event) => {
    event.preventDefault();
    var formData = new FormData();
    formData.append("file", file);
    authFetch("/api/backup-restore/backups/upload", {
      method: "post",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
        window.location.reload();
      })
    );
  };

  const downloadBackupFiles = (name) => {
    var formData = new FormData();
    formData.append("name", name.split(".")[0]);

    authFetch("/api/backup-restore/backups/download", {
      method: "POST",
      body: formData,
    })
      .then((resp) => resp.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        // the filename you want
        a.download = name.split(".")[0] + ".zip";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        setMsg("Download starts");
        setStatusCode(200);
      })
      .catch(() => {
        setMsg("Failed to download...");
      });
  };

  const deleteBackupFiles = (name) => {
    var formData = new FormData();
    formData.append("name", name.split(".")[0]);
    authFetch("/api/backup-restore/backups/record-and-files", {
      method: "DELETE",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
        window.location.reload();
      })
    );
  };

  const restoreBackupFiles = (name) => {
    var formData = new FormData();
    formData.append("name", name);
    authFetch("/api/backup-restore/restore/record-and-files", {
      method: "POST",
      body: formData,
    });
  };

  const createBackup = (event) => {
    event.preventDefault();
    authFetch("/api/backup-restore/backups", {
      method: "POST",
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
        window.location.reload();
      })
    );
  };

  return (
    <BodyContainer size="md">
      <Snackbars message={msg} statusCode={statusCode} />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          Create a new Backup
        </Typography>
        <form noValidate onSubmit={createBackup}>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.button}
          >
            <FormattedMessage id="Submit" defaultMessage="Submit" />
          </Button>
        </form>
        <Divider variant="middle" className={classes.hr} />
        <Typography component="h1" variant="h5">
          Upload a Backup
        </Typography>
        <form noValidate onSubmit={handleBackupFileUpload}>
          <Button variant="contained">
            <input name="file" type="file" onChange={handleFileChange} />
          </Button>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            <FormattedMessage id="Upload" defaultMessage="Upload" />
          </Button>
        </form>
        <Divider variant="middle" className={classes.hr} />
        <List className={classes.container}>
          {backups.map((backup) => (
            <React.Fragment key={backup?.file_name}>
              <Typography component="h1" variant="h5">
                Backup File: {backup?.file_name}
                <Chip
                  color="primary"
                  size="medium"
                  label={"Download " + backup.file_name}
                  onClick={() => downloadBackupFiles(backup?.file_name)}
                  key={backup?.file_name + "download"}
                />
                <Chip
                  color="primary"
                  size="medium"
                  label={"Restore backup: " + backup.file_name}
                  deleteIcon={<DoneIcon />}
                  onClick={() => restoreBackupFiles(backup?.file_name)}
                  key={backup?.file_name + "restore"}
                />
                <Chip
                  color="secondary"
                  size="medium"
                  label={"Delete Record and Files of " + backup.file_name}
                  onDelete={() => deleteBackupFiles(backup?.file_name)}
                  key={backup?.file_name + "backup"}
                />
              </Typography>
              {backup?.records.map((record) => (
                <React.Fragment key={record?.id + "record"}>
                  <Chip
                    color="secondary"
                    size="medium"
                    label={"Delete record"}
                    onDelete={() => deleteBackupRecord(record?.id)}
                    key={record?.name + record?.id}
                  />
                  <p>{record?.job_status}</p>
                  <br />
                </React.Fragment>
              ))}
            </React.Fragment>
          ))}
        </List>
      </div>
    </BodyContainer>
  );
}
