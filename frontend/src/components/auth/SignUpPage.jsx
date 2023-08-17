import React, { useState, useContext } from 'react';
import { useNavigate } from "react-router-dom";

import AuthContext from '../../context/AuthContext.js';
import AuthLayout from './AuthLayout.jsx';





function SignUpPage() {
  let navigate = useNavigate();
  const {signUpUser} = useContext(AuthContext);


  const [formError, setformError] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');


  const handleSignUpUser = (event) => {
    event.preventDefault();

    signUpUser(event).then(response => {
      if (response === 200){
        navigate('/login/');
      }
      else{
        setformError(response['detail'])
        setUsernameError(response['username'])
        setPasswordError(response['password'])
      }
    });
  }


  

  return (
    <AuthLayout>
      <div className="mt-md-4">
        <h1 className="fw-bold mb-2">Регистрация</h1>
        <p className="text-white-50 mb-5">Придумайте логин и пароль</p>
      </div>
      <div>
        <p id='form_error'>{formError}</p>
        <form onSubmit={handleSignUpUser}>
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
          <div className="form-outline form-white mb-4">
            <input
              type="password"
              name="passwordRepeat"
              placeholder="Повторите пароль"
              className="form-control form-control-lg"
            />
          </div>
          <button type="submit" className="btn btn-primary btn-lg px-5 mb-5">Зарегистрироваться</button>
        </form>
        <div>
          {/* <p className="small mb-5 pb-lg-2"><a className="text-white-50" href="/password_reset">Забыли пароль?</a></p> */}
          <p className="mb-0">Уже есть аккаунт? <a href="/login" className="text-white-50 fw-bold">Войти</a></p>
        </div>
      </div>
    </AuthLayout>

  );
}

export default SignUpPage;
