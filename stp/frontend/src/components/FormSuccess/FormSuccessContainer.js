import React from 'react';

export default function FormSuccessContainer({ successMessage }) {
  return (
    <div className="alert alert-success alert-dismissible fade show" role="alert">
      <ul className="fa-ul mb-0 ms-4">
        <li>
          <span className="fa-li text-success"><i className="fa-solid fa-circle-check fa-shake"></i></span>
          <span className="small lh-sm">{successMessage}</span>
        </li>
      </ul>
      <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button>
    </div>
  );
}
