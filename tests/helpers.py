def simulate_vlc_stopped(vlc_player):
    """Configure the VLC mock to behave as if playback is stopped."""
    vlc_player.is_playing.return_value = False
    vlc_player.play.reset_mock()
    vlc_player.pause.reset_mock()


def simulate_vlc_playing(vlc_player):
    """Configure the VLC mock to behave as if playback is currently active."""
    vlc_player.is_playing.return_value = True
    vlc_player.play.reset_mock()
    vlc_player.pause.reset_mock()


