from . import db
from flask_login import UserMixin


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String(150))

    doAutoSync = db.Column(db.Boolean, default=True)
    # type of sync (change, x time, if change persistent after x time)

    doVideo = db.Column(db.Boolean, default=True)
    doAudio = db.Column(db.Boolean, default=True)
    doThumbnail = db.Column(db.Boolean, default=False)
    doCaption = db.Column(db.Boolean, default=False)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String(150))

    doThumbnail = db.Column(db.Boolean, default=False)
    doVideo = db.Column(db.Boolean, default=True)
    doAudio = db.Column(db.Boolean, default=True)
    doCaption = db.Column(db.Boolean, default=False)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    nickName = db.Column(db.String(150))

    playlists = db.relationship('Playlist')
