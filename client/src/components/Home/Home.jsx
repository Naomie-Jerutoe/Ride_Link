import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [rides, setRides] = useState([]);

  useEffect(() => {
      fetch("http://127.0.0.1:5000/rides")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch rides");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setRides(data);
      })
      .catch((error) => {
        console.log(`Error fetching rides: ${error.message}`);
      });
  }, []);

  return (
    <div>
      <div>
      <h1 style={{color: "white"}}>Welcome to Ride Link!!!</h1>
      <p style={{color: "white"}}>Your ultimate link to the most affordable rides</p>
      <Link to="/login">Login</Link>
      </div>
      <div>
      {Array.isArray(rides) && rides.map(ride => (
        <div key={ride.id}>
          <h3>Rides</h3>
          <h4>{ride.departure_location}</h4>
          <h4>{ride.destination}</h4>
          <h4>{ride.departure_time}</h4>
          <h4>{ride.available_seats}</h4>
          <h4>{ride.price}</h4>
          <h4>{ride.driver_id}</h4>
        </div>
      ))}
      </div>

    </div>
  );
}

export default Home;
