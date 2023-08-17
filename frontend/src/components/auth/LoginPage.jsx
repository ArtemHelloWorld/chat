import React, { useContext, useState } from 'react';
import { useNavigate } from "react-router-dom";

import AuthContext from '../../context/AuthContext.js';
import AuthLayout from './AuthLayout.jsx';


function LoginPage() {
  let navigate = useNavigate();
  const {loginUser} = useContext(AuthContext);

  const [formError, setformError] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  

  const handleLoginSubmit = (event) => {
    event.preventDefault();

    loginUser(event).then(response => {
      if (response === 200){
        navigate('/');
      }
      else{
        setformError(response['detail'])
        setUsernameError(response['username'])
        setPasswordError(response['password'])
      }
    });
  };
  
  return (
    <AuthLayout>
      <div className="mt-md-4">
        <h1 className="fw-bold mb-2">Вход</h1>
        <p className="text-white-50 mb-5">Введите свой логин и пароль</p>
      </div>
      <div>
        <p id='form_error'>{formError}</p>
        <form onSubmit={handleLoginSubmit}>
          <p id='username_error'>{usernameError}</p>
          <div className="form-outline form-white mb-4">
              <input
                type="text"
                name="username"
                placeholder="Логин"
                className="form-control form-control-lg"
              />
              </div>
          <p id='password_error'>{passwordError}</p>
          <div className="form-outline form-white mb-4">
              <input
                type="password"
                name="password"
                placeholder="Пароль"
                className="form-control form-control-lg"
              />
            </div>
          <button type="submit" className="btn btn-primary btn-lg px-5 mb-5">Войти</button>
        </form>
        <div>
          {/* <p className="small mb-5 pb-lg-2"><a className="text-white-50" href="/password_reset">Забыли пароль?</a></p> */}
          <p className="mb-0">Ещё нет аккаунта? <a href="/signup" className="text-white-50 fw-bold">Регистрация</a></p>
        </div>
      </div>
    </AuthLayout>       
  );
}

export default LoginPage;
