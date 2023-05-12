import React, { useState } from 'react';
import { useCookies } from 'react-cookie';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import "./App.css"

function App() {

  // --------------------- CONST --------------------- //
  const [name, setName] = useState('');
  const [pass, setPass] = useState('');
  const [cookies, setCookie] = useCookies(['user']);

  // When submit button is clicked
  const handle = () => {
     setCookie('Name', name, { path: '/' }); // Sets username
     setCookie('Password', pass, { path: '/' }); // Sets password
     window.location.reload(); // Refreshes page
  }
    
  return (
    <div className="App">
      <h1>Set a Cookie!</h1>
      <h3> Please enter the following information: </h3>

      <div>
        <TextField 
          id="outlined-basic"
          label="Username"
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <br/>

      <div>
        <TextField 
          id="outlined-basic"
          label="Password"
          variant="outlined"
          value={pass}
          onChange={(e) => setPass(e.target.value)}
        />
      </div>

      <br/>

      <div>
        <Button
          variant="contained"
          onClick={handle}
        >
        Submit Cookie
        </Button>
      </div>  

      <br/>
      <br/>
      <br/>

      <div>
        <h3>Last Set Cookie:</h3>
        {cookies.Name && (
          <div>
            <p>Name: {cookies.Name}</p>
          </div>
        )}

        {cookies.Password && (
          <div>
            <p>Password: {cookies.Password}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
