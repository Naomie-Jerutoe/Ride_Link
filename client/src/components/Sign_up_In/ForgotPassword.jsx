import { useState } from "react"
import { useNavigate } from "react-router-dom"


function ForgotPassword() {
  const[username, setUsername] = useState("")
  const[message, setMessage] = useState("")
  const navigate = useNavigate()

  const reqOptions = {
    method: 'POST',
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({username:username})
  }
  const handleSubmit = (e) => {
    e.preventDefault()

    fetch('http://127.0.0.1:5000/forgot_password', reqOptions)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to submit username');
      }
      return response.json();
    })
    .then(data => {
      console.log(data.message)
      setMessage(data.message);
      
      // Redirect to reset password page with token
      navigate(`/login/reset-password/${data.token}`);
    })
    .catch(error => {
      setMessage(error.message);
    });
  }

  return (
    <div>
      <p style={{color:'white'}}>Fill in your username in the form below</p>
      <form onSubmit={handleSubmit}>
      <input
            type="text"
            name="txt"
            placeholder="username"
            required=""
            value={username}
            onChange={(e)=>setUsername(e.target.value)}
          />
      <button type="submit" style={{color: 'black'}} >Submit</button>
      </form>
      <div className="msg">
      {message && <p style={{color:'white'}}>{message}</p>}
      </div>
      
    </div>
  )
}

export default ForgotPassword