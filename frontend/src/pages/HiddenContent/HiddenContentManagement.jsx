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
import AddCircleIcon from "@material-ui/icons/AddCircle";
import { IconButton } from "@material-ui/core";
import SettingsIcon from "@material-ui/icons/Settings";
import DialogTitle from "@material-ui/core/DialogTitle";
import Dialog from "@material-ui/core/Dialog";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

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
  listItem: {
    marginTop: 15,
  },
  hr: {
    width: `100%`,
  },
}));

function SimpleDialog(props) {
  const classes = useStyles();
  const [blogs, setBlogs] = useState([]);
  const { open } = props;

  useEffect(() => {
    authFetch("/api/hidden-content/blogs", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setBlogs(data);
      });
  }, []);

  const handleClose = () => {
    props.handleClose();
  };

  const handleListItemClick = (blogId) => {
    props.handleLinkBlog(blogId);
    props.handleClose();
  };

  return (
    <Dialog
      onClose={handleClose}
      aria-labelledby="simple-dialog-title"
      open={open}
    >
      <DialogTitle id="simple-dialog-title">Add blogs</DialogTitle>
      <List>
        {blogs.map((blog) => (
          <ListItem
            button
            onClick={() => handleListItemClick(blog?.id)}
            key={blog?.title + blog?.id}
          >
            <ListItemText primary={blog?.title} />
          </ListItem>
        ))}
      </List>
    </Dialog>
  );
}

function UpdateDialog(props) {
  const classes = useStyles();
  const { open, curCategory } = props;
  const name = useRef(null);
  const uuid = useRef(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    var formData = new FormData();
    formData.append("id", curCategory.id);
    formData.append("name", name.current.value);
    formData.append("uuid", uuid.current.value);

    authFetch("/api/hidden-content/config/update", {
      method: "POST",
      body: formData,
    })
      .then((r) => r.json())
      .then((data) => {
        window.location.reload();
      });
  };

  const handleClose = () => {
    props.handleClose();
  };

  const handleListItemClick = (blogId) => {
    props.handleLinkBlog(blogId);
    props.handleClose();
  };

  return (
    <Dialog
      onClose={handleClose}
      aria-labelledby="simple-dialog-title"
      open={open}
    >
      <DialogTitle id="simple-dialog-title">
        Update hidden content config
      </DialogTitle>
      <form noValidate onSubmit={handleSubmit}>
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="email"
          label={"name"}
          name="name"
          autoComplete="name"
          defaultValue={curCategory?.name}
          inputRef={name}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="uuid"
          label={"uuid"}
          name="uuid"
          autoComplete="uuid"
          defaultValue={curCategory?.uuid}
          inputRef={uuid}
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          className={classes.submit}
        >
          <FormattedMessage id="Update" defaultMessage="Update" />
        </Button>
      </form>
    </Dialog>
  );
}

export default function HiddenContentManagement() {
  const classes = useStyles();
  const [categories, setCategories] = useState([]);
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  const [open, setOpen] = useState(false);
  const [openUpdate, setOpenUpdate] = useState(false);
  const [curCategory, setCurCategory] = useState(null);
  let name = useRef("");

  const handleClickOpen = (curCategory) => {
    setCurCategory(curCategory);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleLinkBlog = (blogId) => {
    setOpen(false);
    var formData = new FormData();
    formData.append("blog_id", blogId);
    formData.append("hidden_content_id", curCategory.id);
    authFetch("/api/hidden-content/link-blogs", {
      method: "POST",
      body: formData,
    }).then((res) =>
      res.json().then((data) => {
        setMsg(data);
        setStatusCode(res.status);
        window.location.reload();
      })
    );
  };

  const handleUnlinkBlog = (blogId, hiddenContnetId) => {
    var formData = new FormData();
    formData.append("blog_id", blogId);
    formData.append("hidden_content_id", hiddenContnetId);

    authFetch("/api/hidden-content/link-blogs", {
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

  useEffect(() => {
    authFetch("/api/hidden-content/categories", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setCategories(data);
      });
  }, []);

  const handleDelete = (id) => {
    var formData = new FormData();
    formData.append("id", id);

    authFetch("/api/hidden-content/categories", {
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

  const handleUpdateOpen = (category) => {
    setCurCategory(category);
    setOpenUpdate(true);
  };

  const handleUpdateClose = () => {
    setOpenUpdate(false);
  };

  const handleCreateHiddenContent = (event) => {
    event.preventDefault();
    var formData = new FormData();
    formData.append("name", name.value);

    authFetch("/api/hidden-content/categories", {
      method: "POST",
      body: formData,
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
          Create new hidden content category
        </Typography>
        <form noValidate onSubmit={handleCreateHiddenContent}>
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            id="name"
            label="name"
            name="name"
            autoComplete="name"
            required
            inputRef={(input) => (name = input)}
          />
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
        <List className={classes.container}>
          {categories.map((category) => (
            <React.Fragment key={category?.name + category?.id}>
              <Chip
                color="secondary"
                size="small"
                label={category.name}
                onDelete={() => handleDelete(category.id)}
                key={category?.name + category?.id}
                className={classes.listItem}
              />
              <Typography component="h3" variant="h5">
                name: {category.name}
              </Typography>
              <Typography component="h3" variant="h5">
                uuid: {category.uuid}
              </Typography>
              <Typography component="h3" variant="h5">
                blogs:
              </Typography>
              <IconButton onClick={() => handleUpdateOpen(category)}>
                <SettingsIcon color="primary" />
              </IconButton>
              <IconButton onClick={() => handleClickOpen(category)}>
                <AddCircleIcon color="primary" />
              </IconButton>
              {category?.blogs?.length === 0 && (
                <Chip
                  label={<FormattedMessage id="None" />}
                  disabled
                  size="small"
                />
              )}
              {category?.blogs.map((blog) => (
                <Chip
                  color="secondary"
                  size="small"
                  label={blog.title}
                  key={blog?.title + blog?.id}
                  onDelete={() => handleUnlinkBlog(blog?.id, category?.id)}
                />
              ))}
              <SimpleDialog
                open={open}
                handleClose={handleClose}
                handleLinkBlog={handleLinkBlog}
                curCategory={curCategory}
              />
              <UpdateDialog
                open={openUpdate}
                handleClose={handleUpdateClose}
                curCategory={curCategory}
              />
              <br />
            </React.Fragment>
          ))}
        </List>
      </div>
    </BodyContainer>
  );
}
