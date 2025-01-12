import {useUser} from '../../context/UserContext';
import {userProfilePicUrl} from "../../utils/userProfilePicUrl";
import LoaderInlineBlock from "../Loaders/LoaderInlineBlock";

export default function UserProfileCard() {
  const user = useUser();

  if (!user) {
    return <LoaderInlineBlock />;
  }

  return (
    <div className="d-flex justify-content-between align-items-center mb-4">
      <div className="d-flex align-items-center">
        <a href={"/user/"}>
          <img src={userProfilePicUrl(user)} className="profile-photo me-3" style={{ width: '45px', height: '45px' }} />
        </a>
        <div>
          <a href={"/user/"} className="fw-bold common-link mb-0">
            {user.username}
          </a>
          <p className="text-muted small limit-str mb-0" style={{ '--num-lines': 1 }}>
            {user.first_name} {user.last_name}
          </p>
        </div>
      </div>
      <div className="d-flex">
        <a href="/logout" title="Switch Account" className="text-muted">
          <i className="fa-solid fa-arrows-rotate"></i>
        </a>
      </div>
    </div>
  );
}