import axios from "axios";
import { useState,useEffect } from "react";

function Login(){
    const [validLogin, setValidLogin]=useState(false)
    const[email,setEmail]=useState("")
    const[password,setPassword]=useState("")
    const [inputError,setInputError]=useState("")
    const handleLogin=(e)=>{
        e.preventDefault();
        if (email.trim()==""){
            setInputError("Invalid Username or password!!");
            setValidLogin(false)
        }
    };
    return(
        <div>
            <div className="Login">
            <div className="LoginHeader"><h1>User Login</h1> </div>
            <form className="LoginForm">
                <div>Email:<input type="email" placeholder="xyz@domain.com" required value={email} onChange={(e)=>setEmail(e.target.value)}/></div>
                <div>Password:<input type="password" value={password} onChange={(e)=>setPassword(e.target.value)}/></div>
                <div><input type="button" value="Login" onClick={(e)=>handleLogin(e)}/></div>
            </form>
            </div>
        </div>
    )
}

export default Login;