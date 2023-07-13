import React from 'react'
import { Link } from 'react-router-dom'
import { useLocation } from 'react-router-dom';
import { CSVLink } from "react-csv";
import '../es/css/MemberList.css'

function MemberList(){
  const location = useLocation();
  const users = location.state['users'];
  const headers = [
    { label: "名前", key: "name" },
    { label: "学籍番号", key: "student_number" }
  ];
  const date = new Date();
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  console.log(year);
  console.log(users['users']);

  const rows = users.map((user) =>
      <tr key={user}>
        <td>{user.name}</td>
        <td>{user.student_number}</td>
      </tr>
  );
  return (
    <div>
      <h3 className="title">出席者一覧</h3>
      <table className="table">
        <thead>
          <tr>
              <th>名前</th>
              <th>学籍番号</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
    </table>
    <div className='btn-box'>
      <CSVLink className="csv-btn" filename={year + "-" + month + "-" + day + "-attendees.csv"} data={users} headers={headers}>CSV出力</CSVLink>
      <Link to='/member' className="back-btn">戻る</Link>
    </div>

    </div>
  );
}

export default MemberList;