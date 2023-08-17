import React  from 'react'
import 'bootstrap/dist/css/bootstrap.css';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";

import {AuthProvider} from './context/AuthContext.js'
import PrivateRoute from "./utils/PrivateRoute.js";

import ChatApp from './components/chat/ChatApp.jsx';
import LoginPage from "./components/auth/LoginPage.jsx";
import SignUpPage from "./components/auth/SignUpPage.jsx";


function App() {

  return (
    <Router>
      <AuthProvider>
        <Routes >
          <Route exact path="/login/" element={<LoginPage />}  />
          <Route exact path="/signup/" element={<SignUpPage />}  />
          <Route path="/" element={<PrivateRoute><ChatApp/></PrivateRoute>}/>
        </Routes>
      </AuthProvider>
    </Router>
  );

}

export default App;
