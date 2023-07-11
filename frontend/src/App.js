import React from 'react'
import './es/css/App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import SignUp from './components/SignUp';
import Member from './components/Member';
import MemberList from './components/MemberList';

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path='/login' element={<Login />} />
                <Route path='/signup' element={<SignUp />} />
                <Route path='/member' element={<Member />} />
                <Route path='/memberlist' element={<MemberList/>} />
            </Routes>
        </BrowserRouter>
    )
}

export default App;