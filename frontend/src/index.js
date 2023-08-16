import React from 'react';
import App from "./App.js";

import ReactDOM from "react-dom/client";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";

import LoginPage from "./components/LoginPage.jsx";
import PrivateRoute from "./utils/PrivateRoute.js";
import {AuthProvider} from './context/AuthContext.js'

const Routing = () => {
  return(
    <Router>
      <AuthProvider>
        <Routes>
          <Route exact path="/login/" element={<LoginPage />}  />
          <Route path="/" element={<PrivateRoute><App/></PrivateRoute>}  />
        </Routes>
      </AuthProvider>
    </Router>
  )
}


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
    <Routing />
  // </React.StrictMode>
);
