export default function BaseProfileSettings({ settingsInfo, settingsTabs, settingsForm }) {
  return (
    <div className="row justify-content-center">
      <div className="col-12 col-md-8 col-lg-7 col-xl-5">
        {settingsInfo}
        {settingsTabs}
        {settingsForm}
      </div>
    </div>
  )
}