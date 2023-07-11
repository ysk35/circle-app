import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../es/css/Member.css';

function Member(){

  const [date, setDate] = useState(new Date());
  const URL = 'http://localhost:5001/getmember';
  const navigate = useNavigate();

  const Submit = async() => {
    const formdata = new FormData();
    formdata.append('date', date);
    const requestOptions = {
      method: "POST",
      body: formdata,
    }

    const response = await fetch(URL, requestOptions);
    const data = await response.json()
    // console.log(data['users'])
    navigate('/memberlist', {state: {users: data['users']}})
  }
  const handleSubmit = (event) => {
    event.preventDefault();
    Submit();
  };
  const handleChangeDate = (event) => {
    setDate(event.currentTarget.value);
  };

  return (
    <div>
      <h3 className="title">日付を指定してください</h3>
      <form onSubmit={handleSubmit} className="container">
        <div>
          <label>日付</label>
          <input
            name="date"
            type="date"
            onChange={(event) => handleChangeDate(event)}
          />
        </div>
        <div>
          <button className="form-btn">確定</button>
        </div>
      </form>
    </div>
  );
}

export default Member;