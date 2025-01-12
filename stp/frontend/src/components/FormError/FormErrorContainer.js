import React from 'react';

export default function FormErrorContainer({ errorMessage }) {
  return (
    <div className="alert alert-danger alert-dismissible fade show" role="alert">
      <ul className="fa-ul mb-0 ms-4">
        <li>
          <span className="fa-li text-danger"><i className="fa-solid fa-circle-exclamation fa-shake"></i></span>
          <span className="small lh-sm">{errorMessage}</span>
        </li>
      </ul>
      <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button>
    </div>
  );
}
