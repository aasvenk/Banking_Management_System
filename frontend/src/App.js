import logo from './logo.svg';
import './App.css';
import SignUp from './components/SignUp';
import Login from './components/Login';
import axios from "axios"
import React from 'react';
import {BrowserRouter as Router, Routes, Route } from 'react-router-dom';

axios.defaults.baseURL=process.env.REACT_APP_BASE_URL
axios.defaults.headers.post['Content-Type'] = 'application/json';


function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<SignUp />}/>
      </Routes>
    </Router>
  );
}

export default App;
