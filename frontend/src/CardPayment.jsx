import React, { useState, useEffect } from "react";

function PaymentForm() {
//   useState is used to create a variable name as empty string 
//   and later update it using setName
  const [name, setName] = useState("");
  const [cardNumber, setCardNumber] = useState("");
  const [csvCode, setCsvCode] = useState("");
  const [expMonth, setExpMonth] = useState("");
  const [expYear, setExpYear] = useState("");

  // define a new function that would wait for an event. 
  const handleSubmit = async (event) => {
    //normally Javascript would reload but it is being prevented
    event.preventDefault();

    const csrf_code = await fetch("/get_csrf_token");
    const content_data = await csrf_code.json();
    const csrfToken = content_data.csrf_token;
    console.log(csrfToken)

    const response = await fetch("/accountinfo/v/paymentinfo",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken,
      },
      body: new URLSearchParams({
          user_name: name,
          card_number: cardNumber,
          csv_code: csvCode,
          epx_month: expMonth,
          epx_year: expYear
      }),
    });
    const data = await response.text();
    };
    return (
        <form onSubmit={handleSubmit}>
            <input 
            type ="text"
            placeholder="Name"
            value={name}
            onChange={(event) =>
            setName(event.target.value)}
            />
             <input 
            type ="text"
            placeholder="Card Number"
            value={cardNumber}
            onChange={(event) =>
            setCardNumber(event.target.value)}
            />
            <input 
            type ="text"
            placeholder="CSV Code"
            value={csvCode}
            onChange={(event) =>
            setCsvCode(event.target.value)}
            />
            <input
            type="text"
            placeholder="Expiration Month"
            value={expMonth}
            onChange={(event) => setExpMonth(event.target.value)}
            />
      <input
        type="text"
        placeholder="Expiration Year"
        value={expYear}
        onChange={(event) => setExpYear(event.target.value)}
      />
      <button type="submit">Submit</button>    
        </form>

    )

  };

export default PaymentForm;
