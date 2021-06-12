class TaiKhoan:
    def __init__(self, parent=None):
        super(TaiKhoan, self).__init__(parent)
        self.MNV = ""
        self.Hoten = ''
        self.GioiTinh = 1
        self.NgaySinh = '1990/12/5'
        self.ChucVu = 2
        self.TienNgay = 0

    def getMaNV(self):
        return self.MNV
    def setMaNV(self, MNV):
        self.MNV = MNV

    def Logout(self):
        self.MNV = ""
        self.Hoten = ''
        self.GioiTinh = 1
        self.NgaySinh = '1990/01/01'
        self.ChucVu = 2
        self.TienNgay = 0