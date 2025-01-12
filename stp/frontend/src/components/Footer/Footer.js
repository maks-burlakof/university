export default function Footer() {
  return (
    <footer className="mb-4">
      <ul className="d-flex flex-row list-unstyled justify-content-center flex-wrap small opacity-50">
        <li className="mx-3">
          <a href="/docs" target="_blank" className="text-decoration-none text-muted">Информация</a>
        </li>
        <li className="mx-4">
          <a href="#" target="_blank" className="text-decoration-none text-muted">Рейтинг аккаунтов</a>
        </li>
        <li className="mx-4">
          <a href="#" target="_blank" className="text-decoration-none text-muted">Хэштэги</a>
        </li>
        <li className="mx-4">
          <a href="#" target="_blank" className="text-decoration-none text-muted">Места</a>
        </li>
        <li className="mx-4 text-secondary">
          <i className="fa-regular fa-copyright"></i> 2024 <a href="/" className="common-link">Babushka</a> from BSUIR
        </li>
      </ul>
    </footer>
  )
}