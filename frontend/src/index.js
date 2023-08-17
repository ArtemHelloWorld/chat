import React from 'react';
import App from "./App.js";

import ReactDOM from "react-dom/client";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";

import LoginPage from "./components/auth/LoginPage.jsx";
import PrivateRoute from "./utils/PrivateRoute.js";
import {AuthProvider} from './context/AuthContext.js'




const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
    <App />
  // </React.StrictMode>
);
