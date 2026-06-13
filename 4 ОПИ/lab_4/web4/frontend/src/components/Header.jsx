import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../store/authSlice';
import { useNavigate } from 'react-router-dom';
import './Components.css';

const Header = () => {
  const { token } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <header className="app-header">
      <div className="student-info">
        <h3>Караганов Павел</h3>
        <p>Группа: P3210 | Вариант: 1723</p>
      </div>
      {token && (
        <button className="btn-logout" onClick={handleLogout}>
          Выйти
        </button>
      )}
    </header>
  );
};

export default Header;