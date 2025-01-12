export default function BasePublicationOwnerLink({ ownerLink, ownerName, ownerProfilePic }) {
  return (
    <a href={ownerLink}>
      <img src={ownerProfilePic} className="profile-photo me-2" alt={ownerName}/>
      <span className="fw-bold">{ownerName}</span>
    </a>
  )
}