import React, {useState} from "react";
import {useNavigate} from "react-router-dom";

import FormErrorContainer from "../FormError/FormErrorContainer";

export default function SignUpForm() {
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const form = event.target.closest('form');
    const email = form.querySelector('#id_email').value;
    const phone_number = form.querySelector('#id_phone_number').value;
    const username = form.querySelector('#id_username').value;
    const first_name = form.querySelector('#id_first_name').value;
    const last_name = form.querySelector('#id_last_name').value;
    const password1 = form.querySelector('#id_password1').value;
    const password2 = form.querySelector('#id_password2').value;

    // Validation
    if (!email) {
      setErrorMessage('Email обязателен');
      return;
    }
    if (!username) {
      setErrorMessage('Имя пользователя обязательно');
      return;
    }
    if (!first_name) {
      setErrorMessage('Имя обязательно');
      return;
    }
    if (!last_name) {
      setErrorMessage('Фамилия обязательна');
      return;
    }
    if (!password1) {
      setErrorMessage('Поле пароля обязательно');
      return;
    }
    if (!password2) {
      setErrorMessage('Повторите пароль');
      return;
    }
    if (password1 !== password2) {
      setErrorMessage('Пароли не совпадают');
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          username: username,
          password: password1,
          phone_number: phone_number,
          first_name: first_name,
          last_name: last_name,
        }),
      });

      if (!response.ok) {
        setErrorMessage(await response.text());
        return;
      }

      //const data = await response.json();
      navigate('/login');
    } catch (error) {
      setErrorMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div className="card-body p-md-4">
      <img className="d-block mx-auto mb-2" src={`${process.env.PUBLIC_URL}/img/babushka-logo.png`} width="300"/>
      <p className="fw-semibold text-primary-emphasis text-center px-md-4">Зарегистрируйтесь, чтобы стать частью
        сообщества!</p>
      {errorMessage && <FormErrorContainer errorMessage={errorMessage}/>}
      <form>
        <div className="mb-3">
          <div className="form-floating">
            <input id="id_email" className="form-control rounded-4" name="email" placeholder="Email"/>
            <label htmlFor="id_email">Электронная почта</label>
          </div>
        </div>
        <div className="row g-3 mb-3">
          <div className="col">
            <div className="form-floating">
              <input id="id_first_name" className="form-control rounded-4" name="first_name" placeholder="First name"/>
              <label htmlFor="id_first_name">Имя</label>
            </div>
          </div>
          <div className="col">
            <div className="form-floating">
              <input id="id_last_name" className="form-control rounded-4" name="last_name" placeholder="Last name"/>
              <label htmlFor="id_last_name">Фамилия</label>
            </div>
          </div>
        </div>
        <div className="mb-3">
          <div className="form-floating">
            <input id="id_username" className="form-control rounded-4" name="username" placeholder="Username"/>
            <label htmlFor="id_username">Имя пользователя</label>
          </div>
        </div>
        <div className="mb-3">
          <div className="form-floating">
            <input id="id_phone_number" className="form-control rounded-4" name="phone_number" placeholder="Phone number"/>
            <label htmlFor="id_phone_number">Номер телефона</label>
          </div>
        </div>
        <div className="mb-3">
          <div className="form-floating">
            <input id="id_password1" type="password" className="form-control rounded-4" name="password1"
                   placeholder="Password"/>
            <label htmlFor="id_password1"><i className="fa-solid fa-unlock-keyhole me-2"></i> Пароль</label>
          </div>
        </div>
        <div className="mb-3">
          <div className="form-floating">
            <input id="id_password2" type="password" className="form-control rounded-4" name="password2"
                   placeholder="Repeat password"/>
            <label htmlFor="id_password2"><i className="fa-solid fa-unlock-keyhole me-2"></i> Повторите
              пароль</label>
          </div>
        </div>
        <div className="d-flex align-items-center mb-3">
          <span className="me-2 text-primary fs-4"><i className="fa-solid fa-shield-halved"></i></span>
          <p className="small lh-sm text-muted mb-0">Регистрируясь, вы принимаете наши Условия, Политику
            конфиденциальности и Политику в отношении файлов cookie.</p>
        </div>
        <button onClick={handleSubmit} className="btn btn-primary rounded-pill w-100">Регистрация</button>
      </form>
    </div>
  )
}