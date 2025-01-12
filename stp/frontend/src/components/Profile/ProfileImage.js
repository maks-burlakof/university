export default function ProfileImage({ imageUrl }) {
  return (
    <>
      <img src={imageUrl} className="profile-photo w-100" alt={"Profile"}/>
    </>
  );
}