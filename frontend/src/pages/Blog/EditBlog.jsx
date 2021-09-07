// eslint-disable-next-line
import "froala-editor/css/froala_style.min.css";
import "froala-editor/css/froala_editor.pkgd.min.css";
// eslint-disable-next-line
import FroalaEditorComponent from "react-froala-wysiwyg";
// Include special components if required.
// import FroalaEditorView from "react-froala-wysiwyg/FroalaEditorView";
// import FroalaEditorA from "react-froala-wysiwyg/FroalaEditorA";
// import FroalaEditorButton from "react-froala-wysiwyg/FroalaEditorButton";
// import FroalaEditorImg from "react-froala-wysiwyg/FroalaEditorImg";
// import FroalaEditorInput from "react-froala-wysiwyg/FroalaEditorInput";
import "froala-editor/js/plugins.pkgd.min.js";
import "froala-editor/js/languages/de.js";
// eslint-disable-next-line
import FroalaEditor from "react-froala-wysiwyg";
import React, { useRef, useState, useEffect } from "react";
import Redirect from "react-router-dom";
import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import { login, logout, authFetch, userContext } from "../Auth/Auth";
import Snackbars from "../../components/Snackbars/Snackbars";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";

const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: `100%`,
    height: `100%`,
  },
  profileImg: {
    height: 200,
    width: 200,
  },
}));
export default function EditBlog(props) {
  const classes = useStyles();
  const config = {
    // Set the language code.
    language: "zh_cn",
    dragInline: true,
    charCounterCount: true, //默认 显示字数
    theme: "gray", //主题：dark，red，gray，royal，注意需要引入对应主题的css
    width: 900,
    editorClass: "editor-class",
    toolbarInline: false, //true选中设置样式,默认false
    imageUploadMethod: "POST",
    heightMin: 450,
    imageUploadURL: "/api/blogs/file_upload", //上传到本地服务器
    videoUploadURL: "/api/blogs/file_upload",
    fileUploadURL: "/api/blogs/file_upload",
    toolbarButtons: {
      moreText: {
        buttons: [
          "bold",
          "italic",
          "underline",
          "strikeThrough",
          "subscript",
          "superscript",
          "fontFamily",
          "fontSize",
          "textColor",
          "backgroundColor",
          "inlineClass",
          "inlineStyle",
          "clearFormatting",
        ],
      },
      moreParagraph: {
        buttons: [
          "alignLeft",
          "alignCenter",
          "formatOLSimple",
          "alignRight",
          "alignJustify",
          "formatOL",
          "formatUL",
          "paragraphFormat",
          "paragraphStyle",
          "lineHeight",
          "outdent",
          "indent",
          "quote",
        ],
      },
      moreRich: {
        buttons: [
          "insertLink",
          "insertImage",
          "insertVideo",
          "insertTable",
          "emoticons",
          "fontAwesome",
          "specialCharacters",
          "embedly",
          "insertFile",
          "insertHR",
        ],
      },
      moreMisc: {
        buttons: [
          "undo",
          "redo",
          "fullscreen",
          "print",
          "getPDF",
          "spellChecker",
          "selectAll",
          "html",
          "help",
        ],
        align: "right",
        buttonsVisible: 2,
      },
    },
  };
  const uuid = props.match.params.uuid;

  const [file, setFile] = useState(null);
  let title = useRef("");
  let intro = useRef("");
  const [isHidden, setIsHidden] = React.useState(true);
  const [coverImg, setCoverImg] = useState("");
  const [content, setContent] = useState("");
  const [msg, setMsg] = useState("");
  const [statusCode, setStatusCode] = useState(null);
  useEffect(() => {
    fetch("/api/blogs/fetch/" + uuid, {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        title.value = data.title;
        intro.value = data.blog_intro;
        setIsHidden(data.is_hidden == true);
        setCoverImg(data.cover_img);
        setContent(data.content);
      });
  }, []);

  const handleChange = (event) => {
    setIsHidden(event.target.checked);
  };
  const handleContentChange = (model) => {
    setContent(model);
  };
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    var formData = new FormData();
    formData.append("title", title.value);
    formData.append("intro", intro.value);
    formData.append("is_hidden", isHidden);
    formData.append("content", content);
    if (file !== null) {
      formData.append("file", file);
    }

    authFetch("/api/blogs/edit/" + uuid, {
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
    <BodyContainer>
      <Snackbars message={msg} statusCode={statusCode} />
      <div className={classes.paper}>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <img
            src={"http://" + window.location.host + "/static/" + coverImg}
            className={classes.profileImg}
          />
          <br />
          <Button variant="contained">
            <input name="file" type="file" onChange={handleFileChange} />
          </Button>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="title"
            helperText="Title"
            name="title"
            autoComplete="title"
            inputRef={(input) => (title = input)}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="intro"
            helperText="Intro"
            name="intro"
            autoComplete="intro"
            inputRef={(input) => (intro = input)}
          />
          <FormControlLabel
            control={
              <Checkbox
                value="is_hidden"
                color="primary"
                id="is_hidden"
                name="is_hidden"
                checked={isHidden}
                onChange={handleChange}
              />
            }
            label={"Is hiddedn content: "}
            labelPlacement="start"
          />
          <FroalaEditorComponent
            tag="textarea"
            config={config}
            model={content}
            onModelChange={handleContentChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Post
          </Button>
        </form>
      </div>
    </BodyContainer>
  );
}
