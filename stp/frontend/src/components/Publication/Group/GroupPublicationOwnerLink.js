import BasePublicationOwnerLink from "../Base/BasePublicationOwnerLink";

export default function GroupPublicationOwnerLink({publication}) {
  return (
    <BasePublicationOwnerLink
      ownerLink={`/group/${publication.group.groupname}`}
      ownerName={publication.group.groupname}
      ownerProfilePic={publication.group.profile_pic}
    />
  )
}