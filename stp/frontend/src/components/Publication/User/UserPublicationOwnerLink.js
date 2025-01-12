import BasePublicationOwnerLink from "../Base/BasePublicationOwnerLink";
import {userProfilePicUrl} from "../../../utils/userProfilePicUrl";

export default function UserPublicationOwnerLink({publication}) {
  return (
    <BasePublicationOwnerLink
      ownerLink={`/user/${publication.user.username}`}
      ownerName={publication.user.username}
      ownerProfilePic={userProfilePicUrl(publication.user)}
    />
  )
}