import React from "react";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import beian from "../../assets/beian.png";
const useStyles = makeStyles({
  footer: {
    backgroundColor: `#3e3e3e`,
    width: `100%`,
    textAlign: `center`,
    color: `white`,
    padding: 2,
  },
  text: {
    textDecoration: `none`,
    color: `white`,
  },
});
export default function Footer() {
  const classes = useStyles();
  return (
    <div className={classes.footer}>
      <p>
        Copyright ©
        <a href="http://ydaxian.top/" target="_blank" className={classes.text}>
          www.ydaxian.top
        </a>
        All Rights Reserved.
        <br />
        备案号：
        <a
          href="http://www.beian.miit.gov.cn/"
          target="_blank"
          className={classes.text}
        >
          京ICP备20021404号
        </a>
        <a
          target="_blank"
          href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010502041362"
          className={classes.text}
        >
          <img src={beian} />
          京公网安备 11010502041362号
        </a>
      </p>
    </div>
  );
}
