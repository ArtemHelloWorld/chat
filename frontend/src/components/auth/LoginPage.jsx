import React, { useContext, useState } from 'react'
import { useNavigate } from "react-router-dom"

import AuthContext from '../../context/AuthContext.js'
import AuthLayout from './AuthLayout.jsx'


function LoginPage() {
  let navigate = useNavigate()
  const {loginUser} = useContext(AuthContext)

  const [formError, setFormError] = useState('')
  const [usernameError, setUsernameError] = useState('')
  const [passwordErrors, setPasswordErrors] = useState([])

  function clearErrors() {
    setFormError('')
    setUsernameError('')
    setPasswordErrors([])
  }
  const handleLoginSubmit = async (event) => {
    event.preventDefault()

    let username = event.target.username.value
    let password = event.target.password.value

    clearErrors()

    if (!username.length){
      setUsernameError('Введите логин')
    }
    else if (!password.length){
      setPasswordErrors(['Введите пароль'])
    }
    else {
      const [response_status, response_data] = await loginUser(username, password)
      if (response_status === 200) {
        navigate('/')
      } else {
        setFormError(response_data['detail'])
        setUsernameError(response_data['username'])
        setPasswordErrors(response_data['password'])
      }
    }
  }
  
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
          {
            passwordErrors &&
            <ul id='password_errors' className='list-unstyled'>
              {
                passwordErrors.map((error, index) =>
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
          <button type="submit" className="btn btn-primary btn-lg px-5 mb-5">Войти</button>
        </form>
        <div>
          <p className="mb-0">Ещё нет аккаунта? <a href="/signup" className="text-white-50 fw-bold">Регистрация</a></p>
        </div>
      </div>
    </AuthLayout>       
  )
}

export default LoginPage
