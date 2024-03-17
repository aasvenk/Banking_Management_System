import {useState} from "react";
import axios from "axios";

function SignUp(){
    const [accountCreated, setAccountCreated]=useState(false)
    const [firstName,setFirstName]=useState("")
    const[lastName,setLastName]=useState("")
    const[dob,setDOB]=useState("")
    const[emailId,setEmailId]=useState("")
    const[password,setPassowrd]=useState("")
    const[address,setAddress]=useState("")

    const handleSignUpButton=()=>{
        axios.post("/auth/register",{
            firstName:firstName,
            lastName:lastName,
            emailId:emailId,
            password:password,
            dob:dob,
            address:address
        })
        .then((response)=>{
            if (response.status===200){
                setAccountCreated(true)
            }
        })
        .catch((error)=>{
            console.error(error)
        });
    };
    return(
        <div>
           {!accountCreated && (
            <div className="SignUp">
            <div className="SignUpFormHeader"><h1>User Registration</h1></div>
            <form className="SignUpForm"> 
                <div>First Name:<input type="text" value={firstName} required onChange={(e)=>setFirstName(e.target.value)}/></div>
                <div>Last Name:<input type="text" value={lastName} required onChange={(e)=>setLastName(e.target.value)}/></div>
                <div>Date Of Birth:<input type="date" value={dob} required onChange={(e)=>setDOB(e.target.value)}/></div>
                <div>Email Id:<input type="email" placeholder="xyz@domain.com" value={emailId} required onChange={(e)=>setEmailId(e.target.value)}/></div>
                <div>Password:<input type="password" value={password} required onChange={(e)=>setPassowrd(e.target.value)}/></div>
                <div>Address:<input type="text" value={address} required onChange={(e)=>setAddress(e.target.value)}/></div>
                <div><input type="submit" value="Submit" onClick={handleSignUpButton}/></div>
            </form>
            </div> )}
        {accountCreated &&(
            <div className="SignUp">
                <h1>Account created Successfully</h1> 
            </div>
        )
        }
        </div>
          
    )
}

export default SignUp;