export default function UserProfileDescription({ user }) {
  return (
    <>
      <p className="fw-bold fs-5 mb-0">{user.first_name} {user.last_name}</p>
      {user.site_url &&
        <div className="mt-1 mb-1">
          <i className="fa-solid fa-link text-muted small me-2"></i>
          <a href={user.site_url} target="_blank">{user.site_url}</a>
        </div>
      }
      {/* TODO: Add user color support */}
      {user.description &&
        <p>{user.description}</p>
      }
    </>
  );
}