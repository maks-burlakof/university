import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";

export default function UserProfileSettingsInfo({ user }) {
  return (
    <>
      <h3 className="fw-bold mb-4">Редактировать профиль</h3>
      <div className="d-flex align-items-center mb-4">
        <img src={userProfilePicUrl(user)} className="profile-photo me-3" style={{width: '55px', height: '55px'}}/>
        <div>
          <p className="mb-0">{user.username}</p>
          <a type="button" data-bs-toggle="modal" data-bs-target="#upload-photo-modal" className="link-primary">
            Изменить фото профиля
          </a>
        </div>
      </div>
    </>
  )
}