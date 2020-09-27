import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Header from "./components/Header";
import Aside from "./components/Aside";
import Footer from "./components/Footer";
import Home from "./components/pages/Home";
import "./styles.css";

export default function App() {
  return (
    <>
      <Header />
      <Aside />
      <main className="main">
        <Router>
          <Switch>
            <Route path="/" exact component={Home} />
          </Switch>
        </Router>
      </main>
      <Footer />
    </>
  );
}
