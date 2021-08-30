import React, { useEffect, useRef, useState, useContext } from "react";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import BodyContainer from "../../components/Layout/Layout";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import { makeStyles } from "@material-ui/core/styles";
import { categoryList } from "../../constants/category";
import { authFetch, userContext } from "../../pages/Auth/Auth";
import Snackbars from "../../components/Snackbars/Snackbars";
// import { login, useAuth, logout } from "./Auth";

const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `100%`,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  select: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function UploadVideo() {
  const classes = useStyles();
  const title = useRef(null);
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState(categoryList[0]);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const user = useContext(userContext);

  const handleChange = (event) => {
    setCategory(event.target.value);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    var formData = new FormData();
    formData.append("title", title.current.value);
    formData.append("category", category);
    formData.append("file", file);
    authFetch("/api/videos/upload", {
      method: "POST",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
      })
    );
  };

  return (
    <BodyContainer size="sm">
      <Snackbars message={msg} statusCode={statusCode} />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          Upload Video
        </Typography>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="title"
            label="Video Title"
            name="title"
            autoComplete="title"
            autoFocus
            inputRef={title}
          />
          <InputLabel id="category-select-outlined-label">Category</InputLabel>
          <Select
            labelId="category-select-outlined-label"
            id="category-select-outlined"
            value={category}
            onChange={handleChange}
            label="category"
            className={classes.select}
          >
            <MenuItem value={categoryList[0]}>{categoryList[0]}</MenuItem>
            <MenuItem value={categoryList[1]}>{categoryList[1]}</MenuItem>
            <MenuItem value={categoryList[2]}>{categoryList[2]}</MenuItem>
            <MenuItem value={categoryList[3]}>{categoryList[3]}</MenuItem>
            <MenuItem value={categoryList[4]}>{categoryList[4]}</MenuItem>
          </Select>
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
            Upload
          </Button>
        </form>
        <Snackbars message={msg} statusCode={statusCode} />
      </div>
    </BodyContainer>
  );
}
