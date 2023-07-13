import React from 'react'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import '../es/css/SignUp.css';

function SignUp(){
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const URL = 'http://localhost:5001/signup'
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
      navigate("/login")
    }else{
      alert(data["error"]);
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
      <h3 className="title">新規登録</h3>
      <form onSubmit={handleSubmit} className="container">
        <div>
          <label>メールアドレス</label>
          <input
            className="form-input"
            name="email"
            type="email"
            placeholder="email"
            onChange={(event) => handleChangeEmail(event)}
            value={email}
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
            value={password}
          />
        </div>
        <div>
          <button disabled={!email | !password} className="form-btn">登録</button>
        </div>
        <Link to='/login'>ログインはこちら</Link>
      </form>
    </div>
  );
}

export default SignUp;