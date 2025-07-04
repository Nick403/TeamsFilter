import os, json
from jnius import autoclass, PythonJavaClass, java_method

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
AudioManager = autoclass('android.media.AudioManager')
Notification = autoclass('android.app.Notification')

class TeamsFilterService(PythonJavaClass):
    """
    Silences Microsoft Teams calls unless caller matches allow‑list.
    Register this class as NotificationListenerService via manifest.
    """
    __javainterfaces__ = ['android/service/notification/NotificationListenerService']
    __javacontext__ = 'app'

    def __init__(self):
        super().__init__()
        self.prev_modes = {}
        self.activity = PythonActivity.mActivity
        self.audio = self.activity.getSystemService(Context.AUDIO_SERVICE)
        self.data_dir = self.activity.getFilesDir().getAbsolutePath()

    # --- helpers --------------------------------------------------------
    def _allow_list(self):
        path = os.path.join(self.data_dir, 'allow_list.json')
        try:
            with open(path, encoding='utf-8') as f:
                return [s.lower() for s in json.load(f)]
        except Exception:
            return []

    # --- NotificationListenerService API --------------------------------
    @java_method('(Landroid/service/notification/StatusBarNotification;)V')
    def onNotificationPosted(self, sbn):
        if sbn.getPackageName() != 'com.microsoft.teams':
            return
        n = sbn.getNotification()
        if n.category != Notification.CATEGORY_CALL:
            return
        extras = n.extras
        title = str(extras.getString('android.title') or '')
        text = str(extras.getCharSequence('android.text') or '')
        body = (title + ' ' + text).lower()
        if any(term in body for term in self._allow_list()):
            return  # allow normal ringing
        key = sbn.getKey()
        self.prev_modes[key] = self.audio.getRingerMode()
        self.audio.setRingerMode(AudioManager.RINGER_MODE_SILENT)

    @java_method('(Landroid/service/notification/StatusBarNotification;)V')
    def onNotificationRemoved(self, sbn):
        key = sbn.getKey()
        prev = self.prev_modes.pop(key, None)
        if prev is not None:
            self.audio.setRingerMode(prev)
