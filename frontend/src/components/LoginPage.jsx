import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';

function LoginPage() {
  let {loginUser} = useContext(AuthContext);

  return (
    <main className="main gradient-custom overflow-auto">
      <div className="container content ">
        <section className="vh-100">
          <div className="container py-5 h-100">
            <div className="row d-flex justify-content-center align-items-center h-100">
              <div className="col-12 col-md-8 col-lg-6 col-xl-5">
                <div className="card bg-dark text-white" style={{borderRadius: '1rem'}}>
                  <div className="card-body p-5 text-center">
                    <div className=" mt-md-4">
                      <h1 className="fw-bold mb-2">Вход</h1>
                      <p className="text-white-50 mb-5">Введите свой логин и пароль</p>
                    </div>
                    <div>
                      <form onSubmit={loginUser}>
                        <div className="form-outline form-white mb-4">
                            <input
                              type="text"
                              name="username"
                              placeholder="Username"
                              className="form-control form-control-lg"
                            />
                            </div>
                        <div className="form-outline form-white mb-4">

                            <input
                              type="password"
                              name="password"
                              placeholder="Password"
                              className="form-control form-control-lg"
                            />
                          </div>
                        <button type="submit" className="btn btn-primary btn-lg px-5 mb-5">Login</button>
                      </form>
                      <div>
                        <p className="small mb-5 pb-lg-2"><a className="text-white-50" href="/password_reset">Забыли пароль?</a></p>
                        <p className="mb-0">Ещё нет аккаунта? <a href="/signup" className="text-white-50 fw-bold">Регистрация</a></p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>

  );
}

export default LoginPage;
