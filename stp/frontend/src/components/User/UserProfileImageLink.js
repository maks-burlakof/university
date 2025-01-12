import {userProfilePicUrl} from "../../utils/userProfilePicUrl";

export default function UserProfileImageLink({ user }) {
  return (
    <>
      {user ? (
        <a className="nav-link" href="/user">
          <img src={userProfilePicUrl(user)} className="profile-photo" style={{width: '22px', height: '22px'}}/>
        </a>
      ) : (
        <a className="nav-link fs-5 text-dark" href="/login">
          <i className="fa-solid fa-right-to-bracket"></i>
        </a>
      )}
    </>
  );
}