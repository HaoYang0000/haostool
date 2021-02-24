import React from "react";
import Redirect from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from '@material-ui/core/styles';
import BodyContainer from '../../components/Layout/Layout';
const useStyles = makeStyles({
    container: {
        marginTop: 65
    }
});

export default function Home() {
    const classes = useStyles();
    return (
        <BodyContainer>
            home.
        </BodyContainer>
    )
}