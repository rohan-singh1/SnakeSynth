class Volume():
    def __init__(self, setting=9, offset=9):
        self._setting = setting
        self._offset = offset
        self._volume = self.gain()

    def set_setting(self,setting):
        self._setting = setting

    def gain(self):
        if self._setting < 0.1:
            return 0
        db = 3.0 * (self._setting - self._offset)
        return pow(10.0 , db / 20.0)
