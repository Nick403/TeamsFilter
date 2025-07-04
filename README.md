# Teams Filter App (Kivy + Pyjnius)

This project silences Microsoft Teams calls on Android **unless** the caller
matches a user‑defined allow‑list (names, phone numbers, etc.).

## Files

| File | Purpose |
|------|---------|
| `main.py` | Kivy GUI to edit the allow‑list. |
| `filter_service.py` | Background `NotificationListenerService` running in Python. |
| `buildozer.spec` | Buildozer configuration to generate the APK. |
| `android_manifest_snippets.xml` | Extra manifest declaring the notification listener. |
| `allow_list.json` | Created at runtime inside the app’s private storage. |

## Build Instructions

1. **Install prerequisites** (Ubuntu example):

   ```bash
   sudo apt update && sudo apt install -y python3-pip openjdk-17-jdk git             build-essential libssl-dev libffi-dev
   pip install --upgrade buildozer cython
   ```

2. **Initialize buildozer** (first time):

   ```bash
   cd teams_filter_app
   buildozer -v android debug
   ```

   > The first run is heavy (downloads SDK, NDK). Subsequent builds are
   > incremental.

3. **Deploy to device** (USB debugging ON):

   ```bash
   buildozer android deploy run
   ```

4. **Enable the listener**  
   After first launch Android will show a *“Notification access”* prompt.
   Toggle **Teams Filter** ON so it can receive Teams call notifications.

## Usage

* Open the app → add caller strings in the textbox → **Add** → **Save**.
* Remove an entry by tapping on it in the list.
* Close the app; the background service continues to run.
* If a Teams call comes from someone **not** on the list, ringer + vibration
  are suppressed until the call notification disappears, then original
  ringer mode is restored.

## Notes / Caveats

* Works only for Microsoft Teams (`com.microsoft.teams`) calls marked with
  `Notification.CATEGORY_CALL`.
* No answering or rejecting is performed; we only toggle ringer mode.
* Tested on Android 14; permission model may vary on older versions.
* Google Play policies disallow auto‑answer; this app complies by merely
  muting.


---

## 🔧 How to Build APK via GitHub Actions

1. Push this repo to GitHub (you already did!)
2. Go to the **Actions** tab
3. Click **Build Teams Filter APK**
4. Hit **Run workflow**
5. After 5–10 min, download the APK under the **Artifacts** section (e.g., `teamsfilter-1.0-debug.apk.zip`)

You can then install the APK directly on your Android device.
