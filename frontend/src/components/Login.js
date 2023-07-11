import React from 'react'
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import '../es/css/Login.css';

function Login(){
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const URL = 'http://localhost:5001/login'
  const navigate = useNavigate();

  const Submit = async() => {
    const formdata = new FormData();
    formdata.append('email', email);
    formdata.append('password', password);
    const requestOptions = {
        method:"POST",
        body:formdata,
    }

    const response = await fetch(URL, requestOptions);
    const data = await response.json()
    console.log(data["is_success"]);
    if(data["is_success"]){
      navigate("/member")
    }
  }
  const handleSubmit = (event) => {
    event.preventDefault();
    Submit();
  };
  const handleChangeEmail = (event) => {
    setEmail(event.currentTarget.value);
  };
  const handleChangePassword = (event) => {
    setPassword(event.currentTarget.value);
  };

  return (
    <div>
      <h3 className="title">ログイン</h3>
      <form onSubmit={handleSubmit} className="container">
        <div>
          <label>メールアドレス</label>
          <input
            className="form-input"
            name="email"
            type="email"
            placeholder="email"
            onChange={(event) => handleChangeEmail(event)}
          />
        </div>
        <div>
          <label>パスワード</label>
          <input
            className="form-input"
            name="password"
            type="password"
            placeholder="password"
            onChange={(event) => handleChangePassword(event)}
          />
        </div>
        <div>
          <button className="form-btn">ログイン</button>
        </div>
        <Link to='/signup'>新規登録はこちら</Link>
      </form>
    </div>
  );
}


export default Login;