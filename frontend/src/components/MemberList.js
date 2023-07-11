import React from 'react'
import { Link } from 'react-router-dom'
import { useLocation } from 'react-router-dom';
import '../es/css/MemberList.css'

function MemberList(){
  const location = useLocation();
  const users = location.state['users'];
  console.log(users['users']);

  const rows = users.map((user) =>
      <tr key={user}>
        <td>{user}</td>
      </tr>
  );
  return (
    <div>
      <h3 className="title">出席者一覧</h3>
      <table className="tabler">
        <thead>
          <tr>
              <th>Name</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
    </table>
    <Link to='/member'>戻る</Link>
    </div>
  );
}

export default MemberList;