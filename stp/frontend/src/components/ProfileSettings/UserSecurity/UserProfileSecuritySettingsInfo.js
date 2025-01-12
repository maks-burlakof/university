import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";

export default function UserProfileSecuritySettingsInfo({ user }) {
  return (
    <>
      <h3 className="fw-bold mb-4">Редактировать профиль</h3>
      <div className="d-flex align-items-center mb-4">
        <img src={userProfilePicUrl(user)} className="profile-photo me-3" style={{width: '55px', height: '55px'}}/>
        <p className="mb-0">{user.username}</p>
      </div>
    </>
  )
}