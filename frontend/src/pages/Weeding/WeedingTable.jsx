import React, { useState, useRef, useContext, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import BodyContainer from "../../components/Layout/Layout";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import { FormattedMessage } from "react-intl";
import Divider from "@material-ui/core/Divider";

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
    marginBottom: 15,
  },
  hr: {
    width: `95%`,
  },
}));
export default function Comment() {
  const classes = useStyles();
  const [tables, setTables] = useState([]);
  const [error, setError] = useState("");
  let name = useRef("");

  const formValidation = () => {
    let validated = true;
    if (name.value === "") {
      setError(<FormattedMessage id="Message can not be empty." />);
      validated = false;
    } else {
      setError(<FormattedMessage id="Table not found." />);
    }
    return validated;
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (formValidation()) {
      for (let index = 0; index < tables?.length; index++) {
        if (tables[index].pinyin.includes(name.value ) || tables[index].pinyin_full.includes(name.value) || tables[index].people.includes(name.value)){
          setError(tables[index].name);
        }
      }
    };
  }
  useEffect(() => {
    fetch("/api/comments/weeding/table-check", {
      method: "get",
    })
      .then((r) => r.json())
      .then((data) => {
        setTables(data);
      });
  }, []);

  return (
    <BodyContainer size="md">
      <div className={classes.paper}>
        <Typography component="h3" variant="h3">
          <FormattedMessage
            id="Weeding Table Check"
            defaultMessage="Weeding Table Check"
          />
        </Typography>
        <Typography component="h5" variant="h5">
          <FormattedMessage
            id="e.g: search for 阳皓, use 阳皓, yh or yanghao."
            defaultMessage="e.g: search for 阳皓, use 阳皓, yh or yanghao."
          />
        </Typography>
        <form noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            id="name"
            label={
              <FormattedMessage
                id="Name (Optional)"
                defaultMessage="Name (Optional)"
              />
            }
            name="name"
            autoComplete="name"
            inputRef={(input) => (name = input)}
          />
          <div style={{ color: "red" }}>
            <Typography component="h5" variant="h5">
            {error}
            </Typography>
          </div>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.button}
          >
            <FormattedMessage id="Check" defaultMessage="Check" />
          </Button>
        </form>
        <Divider variant="middle" className={classes.hr} />
        {<div >
            <ul>
                {
                tables?.map((table) => 
                <li key={table?.name}>
                  {table?.name}: {table?.people}
                </li>
                )}
            </ul>
        </div>}

      </div>
    </BodyContainer>
  );
}

