export default function UserProfileSecuritySettingsTabs() {
  return (
    <div className="mb-4">
      <span>
        <a href="/user/edit/" className="btn btn-sm text-bg-gray rounded-pill me-2 mb-1">
          <i className="fa-solid fa-user mx-1"></i> Основная информация
        </a>
      </span>
      <span>
        <a href="/user/edit/security/" className="btn btn-sm text-bg-gray border border-secondary rounded-pill mb-1">
          <i className="fa-solid fa-lock mx-1"></i> Безопасность
        </a>
      </span>
    </div>
  )
}