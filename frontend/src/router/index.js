import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import Nav from "../components/Navigation/Nav";
import Home from "../pages/Home/Home";
import Login from "../pages/Auth/Login";
import Register from "../pages/Auth/Register";
import Settings from "../pages/Auth/Settings";
import AWS from "../pages/AWS/AWS";
import Blog from "../pages/Blog/Blog";
import CreateBlog from "../pages/Blog/CreateBlog";
import ViewBlog from "../pages/Blog/ViewBlog";
import EditBlog from "../pages/Blog/EditBlog";
import Donate from "../pages/Contact/Donate";
import Wechat from "../pages/Contact/Wechat";
import Game from "../pages/Game/Game";
import Comment from "../pages/Comment/Comment";
import Label from "../pages/Label/Labels";
import ViewHiddenContent from "../pages/HiddenContent/ViewHiddenContent";
import HiddenContent from "../pages/HiddenContent/HiddenContent";
import HiddenContentManagement from "../pages/HiddenContent/HiddenContentManagement";
import Backups from "../pages/Backup/Backups";
import TimelinePage from "../pages/Timeline/Timeline";
import Video from "../pages/Video/Video";
import ViewVideo from "../pages/Video/ViewVideo";
import UploadVideo from "../pages/Video/UploadVideo";
import NotFound from "../pages/Error/NotFound";

export default function RouterMap(props) {
  return (
    <Router>
      <Nav handleLangChange={props.handleLangChange} />
      <Switch>
        <Route path="/" exact component={Blog} />
        <Route path="/auth/login" exact component={Login} />
        <Route path="/auth/register" exact component={Register} />
        <Route path="/auth/settings" exact component={Settings} />
        <Route path="/aws" exact component={AWS} />
        <Route path="/blogs" exact component={Blog} />
        <Route path="/blogs/create-post" exact component={CreateBlog} />
        <Route path="/blogs/view/:uuid" component={ViewBlog} />
        <Route path="/blogs/edit/:uuid" component={EditBlog} />
        <Route path="/games" exact component={Game} />
        <Route path="/contacts/donate" exact component={Donate} />
        <Route path="/contacts/wechat" exact component={Wechat} />
        <Route path="/comments" exact component={Comment} />
        <Route path="/timelines" exact component={TimelinePage} />
        <Route path="/videos" exact component={Video} />
        <Route path="/videos/upload" exact component={UploadVideo} />
        <Route path="/videos/:uuid" component={ViewVideo} />
        <Route path="/labels" exact component={Label} />
        <Route path="/backups" exact component={Backups} />
        <Route path="/hidden-content" exact component={HiddenContent} />
        <Route path="/hidden-content/management" exact component={HiddenContentManagement} />
        <Route path="/hidden-content/:uuid" exact component={ViewHiddenContent} />
        <Route component={NotFound} />
      </Switch>
    </Router>
  );
}
