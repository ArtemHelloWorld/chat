import React, {useContext, useState} from 'react';

import AuthContext from '../../context/AuthContext.js';
import AuthLayout from './AuthLayout.jsx';



function SignUpPage() {
  const {signUpUser} = useContext(AuthContext);

  const [signUpSuccess, setSignUpSuccess] = useState(false);

  const [formError, setFormError] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordErrors, setPasswordErrors] = useState([]);

  function clearErrors() {
    setFormError('');
    setUsernameError('');
    setPasswordErrors([]);

  }
  const handleSignUpUser = (event) => {
    event.preventDefault();

    let username = event.target.username.value;
    let password = event.target.password.value;
    let passwordRepeat = event.target.passwordRepeat.value;

    clearErrors()

    if (!username.length) {
          setUsernameError('Придумайте логин');
    }
    else if (!password.length) {
        setPasswordErrors(['Придумайте пароль']);
    }

    else if (passwordRepeat !== password) {
        setPasswordErrors(['Пароли не совпадают']);
    }

    else {
      signUpUser(username, password).then(([response_status, response_data]) => {
        if (response_status === 200){
          setSignUpSuccess(true)
        }
        else{
          setFormError(response_data['detail'])
          setUsernameError(response_data['username'])
          setPasswordErrors(response_data['password'])
        }
      });
    }
  }

  if (!signUpSuccess){
    return (
    <AuthLayout>
      <div className="mt-md-4">
        <h1 className="fw-bold mb-2">Регистрация</h1>
        <p className="text-white-50 mb-5">Придумайте логин и пароль</p>
      </div>
      <div>
        <p id='form_error'>{formError}</p>
        <form onSubmit={handleSignUpUser}>
          <p id='username_errors'>{usernameError}</p>
          <div className="form-outline form-white mb-4">
            <input
                type="text"
                name="username"
                placeholder="Логин"
                className="form-control form-control-lg"
              />
          </div>
          {
            passwordErrors &&
            <ul id='password_errors' className='list-unstyled'>
              {passwordErrors.map((error, index) =>
                  <li key={index}>
                    {error}
                  </li>
                )
              }
            </ul>
          }

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
          <p className="mb-0">Уже есть аккаунт? <a href="/login" className="text-white-50 fw-bold">Войти</a></p>
        </div>
      </div>
    </AuthLayout>
    );
  }
  else{
    return (
      <AuthLayout>
        <div className="mt-md-4">
          <h1 className="fw-bold mb-2">Вы зарегистрировались</h1>
          <button type="submit" className="btn btn-primary btn-lg px-5 mb-5"><a className="text-decoration-none text-white" href="/login" >Войти</a></button>
        </div>
      </AuthLayout>
    )
  }
}

export default SignUpPage;
