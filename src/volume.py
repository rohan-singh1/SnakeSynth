class Volume():
    def __init__(self, setting=9, offset=0):
        self._setting = setting
        self._offset = offset
        self._volume = gain(self._setting, self._offset)

    def gain(setting, offset):
        if setting < 0.1:
            return 0
        db = 3.0 * (setting - offset)
        return pow(10.0 , db / 20.0)