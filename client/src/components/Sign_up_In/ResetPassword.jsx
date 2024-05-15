import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [token, setToken] = useState('');
  const navigate = useNavigate()

  useEffect(() => {
    // Extract token from URL
    const path = window.location.pathname;
    const tokenFromUrl = path.split('/').pop();
    setToken(tokenFromUrl);
  }, []);

  const handleResetPassword = (e) =>{
    e.preventDefault()

    fetch(`http://127.0.0.1:5000/reset_token/${token}`, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        new_password: newPassword,
      })
    })
    .then(response => {
      console.log(response);
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("An error has occurred!!");
      }
    })
    .then(data => {
      setMessage(data.message);
      alert("Password reset successfully.")
      // Redirect user to login page
      navigate("/login");
    })
    .catch(error => {
      setMessage(error.message);
    });
  }

  return (
    <div>
      <h2 style={{color:'white'}}>Reset Password</h2>
      <form onSubmit={handleResetPassword}>
        <input
          type="password"
          placeholder="Enter your new password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
        <button type="submit">Reset</button>
      </form>
      {message && <p style={{color:'white'}}>{message}</p>}
    </div>
  );
};

export default ResetPassword;
