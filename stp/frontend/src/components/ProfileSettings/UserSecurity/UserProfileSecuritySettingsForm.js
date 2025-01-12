import React from "react";
import {displayDate} from "../../../utils/dateUtils";


export default function UserProfileSettingsForm({ user }) {
  return (
    <form>
      <div className="mb-1 row align-items-center">
        <span className="fw-bold col-sm-4 col-form-label">Последний вход</span>
        <div className="col-sm-8">
          <span>{displayDate(user.last_login)}</span>
        </div>
      </div>
      <div className="mb-4 row align-items-center">
        <span className="fw-bold col-sm-4 col-form-label">Дата регистрации</span>
        <div className="col-sm-8">
          <span>{displayDate(user.date_joined)}</span>
        </div>
      </div>
      <form method="post">
        {/* TODO: place form errors here */}
        <div className="mb-3 row">
          <label htmlFor="id_old_password" className="fw-bold col-sm-4 col-form-label">Старый пароль</label>
          <div className="col-sm-8">
            <div>
              <input
                type="password"
                name="old_password"
                autoComplete="new-password"
                className="form-control rounded-4"
                required
                id="id_old_password"
                placeholder="Старый пароль"/>
            </div>
          </div>
        </div>
        <div className="mb-3 row">
          <label htmlFor="id_new_password1" className="fw-bold col-sm-4 col-form-label">Новый пароль</label>
          <div className="col-sm-8">
            <div className="mb-2">
              <div>
                <input
                  type="password"
                  name="new_password1"
                  autoComplete="new-password"
                  className="form-control rounded-4"
                  required
                  id="id_new_password1"
                  placeholder="Новый пароль"
                />
              </div>
            </div>
            <div>
              <input
                type="password"
                name="new_password2"
                autoComplete="new-password"
                required
                id="id_new_password2"
                className="form-control rounded-4"
                placeholder="Повторите новый пароль"
              />
            </div>
          </div>
        </div>

        <button type="submit" className="btn btn-primary rounded-pill">Сохранить</button>
      </form>
    </form>
  )
}