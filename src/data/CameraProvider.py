from faker.providers import BaseProvider

class CameraProvider(BaseProvider):
    __provider__= "camera"
    __lang__ = "en_US"

    cameras = [
        ('Canon','EOS 80D'),
        ('Canon','EOS 6D'),
        ('Fujifilm','FinePix A150'),
        ('Fujifilm','X100F'),
        ('Kodak','EasyShare Z981'),
        ('Kodak','Pixipro S-1'),
        ('Nikon','Coolpix A10'),
        ('Nikon','D90'),
        ('Olympus','FE-45'),
        ('Olympus','XZ-1'),
        ('Pentax','KP'),
        ('Pentax','X90'),
        ('Sony','Alpha QX1'),
        ('Sony','SLT-A33')
    ]

    @classmethod
    def camera(cls):
        return cls.random_element(cls.cameras)
