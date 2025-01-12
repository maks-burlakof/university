export function userProfilePicUrl(user) {
  return (user && user.profile_pic) ? user.profile_pic : `${process.env.PUBLIC_URL}/img/profile_default.jpg`;
}