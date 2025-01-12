import BaseProfileSettings from "../Base/BaseProfileSettings";
import UserProfileSecuritySettingsInfo from "./UserProfileSecuritySettingsInfo";
import UserProfileSecuritySettingsTabs from "./UserProfileSecuritySettingsTabs";
import UserProfileSecuritySettingsForm from "./UserProfileSecuritySettingsForm";


export default function UserProfileSecuritySettings({ user }) {
  return (
    <BaseProfileSettings
      settingsInfo={<UserProfileSecuritySettingsInfo user={user} />}
      settingsTabs={<UserProfileSecuritySettingsTabs />}
      settingsForm={<UserProfileSecuritySettingsForm user={user} />}
    />
  )
}