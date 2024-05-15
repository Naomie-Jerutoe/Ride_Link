import { useState } from 'react'

function Register() {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const credentials = {
    username: username,
    email: email,
    password: password
  }

  const reqOptions = {
    method: 'POST',
    headers : {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  }

  const handleRegisterSubmit = (e) =>{
    e.preventDefault();

      fetch('http://127.0.0.1:5000/register', reqOptions)
      .then(res => {
        if(!res.ok){
          throw new Error(`An error has occured: ${res.status}`)
        }
        return res.json()
      })
      .then(data => {
        console.log(data)
        alert ("User created successfully, You can now Log in.")
        setUsername("");
        setEmail("");
        setPassword("")
      })
      .catch(error => {
        console.log("Invalid credentials. Try again!!")
        alert(`${error}`)
      });
  }

  return (
    <div className="signup">
				<form onSubmit={handleRegisterSubmit}>
					<label htmlFor="chk" aria-hidden="true">Sign up</label>
					<input 
            type="text" 
            name="txt" 
            placeholder="Name" 
            required
            value={username}
            onChange={(e)=>setUsername(e.target.value)} 
          />
					<input 
            type="email" 
            name="email" 
            placeholder="Email" 
            required
            value={email}
            onChange={(e)=>setEmail(e.target.value)} 
          />
					<input 
            type="password" 
            name="pswd" 
            placeholder="Password" 
            required
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            />
					<button type="submit">Sign up</button>
				</form>
			</div>
    
  )
}

export default Register