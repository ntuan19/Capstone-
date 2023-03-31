import React from "react";
import PaymentForm from "./CardPayment";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";


function App() {
  return (
    <Router>
      <div>
        <ul>
        <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/payment">Payment</Link>
          </li>
        </ul>

        <hr />
        <Routes>
        <Route exact path="/" element={<Home/>} />
        <Route path="/payment" element={<PaymentForm/>} />
        </Routes>
        
      </div>
    </Router>
  );
}
function Home() {
  return (
    <div>
      <h2>Home</h2>
    </div>
  );
}

export default App;
