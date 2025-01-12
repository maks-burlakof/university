import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import FormErrorContainer from "../FormError/FormErrorContainer";

export default function SignInForm() {
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const form = event.target.closest('form');
    const username = form.querySelector('#id_username').value;
    const password = form.querySelector('#id_password').value;

    // Validation
    if (!username) {
      setErrorMessage('Имя пользователя обязательно');
      return;
    }
    if (!password) {
      setErrorMessage('Пароль обязателен');
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (!response.ok) {
        if ([401, 403].includes(response.status)) {
          setErrorMessage('Неверное имя пользователя или пароль.');
        } else {
          setErrorMessage('Произошла ошибка. Перезагрузите страницу и попробуйте снова.');
        }
        return;
      }

      const data = await response.json();
      localStorage.setItem('access_token', data['access']);
      localStorage.setItem('refresh_token', data['refresh']);
      navigate('/');
      window.location.reload();
    } catch (error) {
      setErrorMessage('Произошла ошибка. Перезагрузите страницу и попробуйте снова.');
    }
  };

  return (
    <>
      <div className="col-md-8 col-lg-6 col-xl-5 offset-md-2 offset-lg-0">
        <div className="square twitter">
          <span></span>
          <span></span>
          <span></span>
          <div className="content">
            <img className="d-block mx-auto mb-3 mt-2" src={`${process.env.PUBLIC_URL}/img/babushka-logo.png`}
                 width="260" alt="Babushka"/>
            <form>
              <div className="mb-3">
                <div className="form-floating">
                  <input id="id_username" className="form-control rounded-4" name="username" placeholder="Username"/>
                  <label htmlFor="id_username">Имя пользователя</label>
                </div>
              </div>
              <div className="mb-3">
                <div className="form-floating">
                  <input id="id_password" type="password" className="form-control rounded-4" name="password" placeholder="Password"/>
                  <label htmlFor="id_password">Пароль</label>
                </div>
              </div>
              <div className="mb-3">
                <div className="form-check form-switch">
                  <input id="id_remember_me" type="checkbox" role="switch" className="form-check-input" name="remember-me"/>
                  <label htmlFor="id_remember_me" className="ms-1">Запомнить меня</label>
                </div>
              </div>
              <button onClick={handleSubmit} className="btn btn-primary rounded-pill w-100 mb-5">Войти</button>
            </form>
          </div>
        </div>
        <div className="card shadow rounded-5 mt-3 mx-sm-4">
          <div className="card-body p-4">
            {errorMessage && <FormErrorContainer errorMessage={errorMessage}/>}
            <p className="text-center mb-2">
              Нет аккаунта?
              <a href="/signup"
                 className="btn btn-primary btn-sm rounded-pill ms-2 px-3">Зарегистрируйтесь!</a>
            </p>
            <p className="text-center mb-0">
              <a href="#" className="small">Забыли пароль?</a>
            </p>
          </div>
        </div>
      </div>
    </>
  );
}