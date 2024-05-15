import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const [newName, setNewName] = useState("");
  const [newEmail, setNewEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleNewNameChange = (e) => {
    setNewName(e.target.value);
  };

  const handleNewEmailChange = (e) => {
    setNewEmail(e.target.value);
  };

  const handleNewPasswordChange = (e) => {
    setNewPassword(e.target.value);
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSignUpSubmit = (e) => {
    e.preventDefault();

    const userDetails = {
      username: newName,
      email: newEmail,
      password: newPassword,
    };

    fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userDetails),
    })
      .then((response) => {
        console.log("Server response status:", response.status);
        if (!response.ok) {
          console.error("Sign Up failed");
          throw new Error("Sign Up failed");
        }
        return response.json();
      })
      .then((result) => {
        console.log(result);
        return "Successfully signed up. You can now Log in.";
      });
  };

  const handleLogInSubmit = (e) => {
    e.preventDefault();

    // console.log("inside the login handler");

    const userDetails = {
      username: name,
      password: password,
    };

    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userDetails),
    };

    console.log("inside the userDetails, before fetch");

    fetch("http://127.0.0.1:5000/login", requestOptions)
      .then((response) => {
        console.log(response);
        if (response.ok) {
          return response.json();
        } else {
          console.log("Server response status:", response.status);
          console.error("Login failed");
          throw new Error("Login failed");
        }
      })
      .then((result) => {
        const accessToken = result.access_token;
        // Associate token with user by storing it securely
        localStorage.setItem("accessToken", JSON.stringify(accessToken));
        console.log("Login Successful");
        // Redirect user
        navigate("/");
      })
      .catch((error) => {
        setLoading(false);
        console.error("There was a problem with the login:", error);
      });
  };

  return (
    <div className="main">
      <input type="checkbox" id="chk"/>

      <div className="signup">
        <form onSubmit={handleSignUpSubmit}>
          <label htmlFor="chk" aria-hidden="true">
            Sign up
          </label>
          <input
            type="text"
            name="txt"
            placeholder="Name"
            required=""
            value={newName}
            onChange={handleNewNameChange}
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            required=""
            value={newEmail}
            onChange={handleNewEmailChange}
          />
          <input
            type="password"
            name="pswd"
            placeholder="Password"
            required=""
            value={newPassword}
            onChange={handleNewPasswordChange}
          />
          <button type="submit">Sign up</button>
        </form>
      </div>

      <div className="login">
        <form onSubmit={handleLogInSubmit}>
          <label htmlFor="chk" aria-hidden="true">
            Login
          </label>
          <input
            type="text"
            name="txt"
            placeholder="Name"
            required=""
            value={name}
            onChange={handleNameChange}
          />

          <input
            type="password"
            name="pswd"
            placeholder="Password"
            required=""
            value={password}
            onChange={handlePasswordChange}
          />
          <button type="submit" style={{color: 'black'}}>{loading ? "Loading..." : "Login"}</button>
          <div className="foot-lnk">
					<a href="/login/forgot-password"><small>Forgot Password?</small></a>
				</div>
        </form>
      </div>
    </div>
  );
}

export default Login;
