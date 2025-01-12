import BaseProfileSettings from "../Base/BaseProfileSettings";
import UserProfileSettingsInfo from "./UserProfileSettingsInfo";
import UserProfileSettingsTabs from "./UserProfileSettingsTabs";
import UserProfileSettingsForm from "./UserProfileSettingsForm";


export default function UserProfileSettings({ user }) {
  return (
    <BaseProfileSettings
      settingsInfo={<UserProfileSettingsInfo user={user} />}
      settingsTabs={<UserProfileSettingsTabs />}
      settingsForm={<UserProfileSettingsForm user={user} />}
    />
  )
}