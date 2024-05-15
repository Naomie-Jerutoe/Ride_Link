import { Routes, Route } from "react-router-dom"
import Home from "./components/Home/Home"
import Login from "./components/Sign_up_In/Login"
import ForgotPassword from "./components/Sign_up_In/ForgotPassword"
import ResetPassword from "./components/Sign_up_In/ResetPassword"

function App() {
  

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={ <Home/> } />
        <Route path="/login" element={ <Login/> } />
        <Route path="/login/forgot-password" element={ <ForgotPassword/> } />
        <Route path="/login/reset-password/:token" element={ <ResetPassword/> } />
      </Routes>
    </div>
  )
}

export default App
