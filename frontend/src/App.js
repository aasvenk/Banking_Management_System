import logo from './logo.svg';
import './App.css';
import SignUp from './components/SignUp';
import axios from "axios"
import React from 'react';

axios.defaults.baseURL=process.env.REACT_APP_BASE_URL


function App() {

  return (
    <div className="App">
      <SignUp/>
    </div>
  );
}

export default App;
