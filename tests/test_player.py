import pytest
from unittest.mock import MagicMock, patch
from player import PlaylistPlayer
from unittest.mock import patch
from modules.utils import format_time

@pytest.fixture
def mock_player():
    mock_root = MagicMock()
    mock_root.bind = MagicMock()

    mock_media_player = MagicMock()

    with (
        patch("player.vlc.Instance") as mock_vlc_instance,
        patch("player.setup_ui"),
        patch("player.PlaylistPlayer.bind_events"),
        patch("player.PlaylistPlayer.update_time", return_value=None),
        patch("player.PlaylistPlayer.init_eq", return_value=None),
        patch("player.PlaylistPlayer.play_from_selection", return_value=None),
        patch("player.PlaylistPlayer.set_duration", return_value=None),
        patch("player.PlaylistPlayer.exit_fullscreen_video", return_value=None),
        patch("player.PlaylistPlayer.start_eq_light_loop", return_value=None),
        patch("player.PlaylistPlayer.force_layout_refresh", return_value=None),
        patch("player.PlaylistPlayer.track_mouse", return_value=None),
        patch("player.PlaylistPlayer.breathe_hal", return_value=None),
    ):
        instance = MagicMock()
        instance.media_player_new.return_value = mock_media_player
        mock_vlc_instance.return_value = instance

        player = PlaylistPlayer(mock_root)
        player.is_playing = False
        player.pause = player.pause.__func__.__get__(player, type(player))
        player.root.after = lambda *args, **kwargs: None

        # UI mocks
        player.style = MagicMock()
        player.mp6_label_left = MagicMock()
        player.mp6_label_right = MagicMock()
        player.time_slider = MagicMock()
        player.current_time_label = MagicMock()
        player.total_time_label = MagicMock()
        player.volume_label = MagicMock()
        player.play_pause_button = MagicMock()
        player.stop_button = MagicMock()
        player.mute_button = MagicMock()
        player.volume_label_frame = MagicMock()

        # Images
        player.mp6 = MagicMock()
        player.mp6_off = MagicMock()
        player.pause_big = MagicMock()
        player.play_off = MagicMock()
        player.stop_on = MagicMock()

        # VLC methods
        player.player.get_time = MagicMock()
        # player.player.is_playing = MagicMock()  

        # Flags
        player.slider_dragging = False
        player.updating_slider = False

        # after()
        player.root.after = MagicMock()

    return player, player.player   
 
def test_play_calls_vlc_play(mock_player):
    player, mock_vlc = mock_player
    
    player.play()
    mock_vlc.play.assert_called_once()
    
def test_pause_calls_vlc_pause(mock_player):
    player, mock_vlc = mock_player
    player.pause()
    mock_vlc.pause.assert_called_once()
    
def test_stop_calls_vlc_stop(mock_player):
    player, mock_vlc = mock_player
    player.stop()
    mock_vlc.stop.assert_called_once()
    
def test_load_calls_set_media(mock_player):
    player, mock_vlc = mock_player

    fake_path = "song.mp3"

    # Pretend that media_new returns a fake media object
    fake_media = MagicMock()
    player.vlc_instance.media_new.return_value = fake_media

    player.load_media_file(fake_path)

    # Verify that media_new was called with the correct path
    player.vlc_instance.media_new.assert_called_once_with(fake_path)

    # Verify that set_media was called with the fake media
    mock_vlc.set_media.assert_called_once_with(fake_media)

def test_set_volume_calls_vlc_volume(mock_player):
    player, mock_vlc = mock_player

    volume_value = 0
    player.set_volume(volume_value)

    mock_vlc.audio_set_volume.assert_called_once_with(volume_value)

def test_set_volume_unmutes_when_volume_above_one(mock_player):
    player, mock_vlc = mock_player

    player.is_muted = True 

    fake_volume = 50
    player.set_volume(fake_volume)

    mock_vlc.audio_set_volume.assert_called_once_with(fake_volume)

    # UI changes to "unmuted" state
    player.volume_label.config.assert_any_call(fg="#CAFFFE")
    player.mute_button.config.assert_called_once_with(bg="#3E3838")
    player.volume_label_frame.config.assert_called_once_with(fg="green")
    player.style.configure.assert_called_with('TScale', troughcolor="#AC8433")

    #  Updated internal flag
    assert player.is_muted is False
    
def test_set_volume_mutes_when_volume_zero(mock_player):
    player, mock_vlc = mock_player

    player.is_muted = False  

    fake_volume = 0
    player.set_volume(fake_volume)

    # VLC receives the volume
    mock_vlc.audio_set_volume.assert_called_once_with(fake_volume)

    # UI changes to "muted" state
    player.mute_button.config.assert_called_once_with(bg="#D21A1A")
    player.style.configure.assert_called_with('TScale', troughcolor="#D21A1A")

    # Updated internal flag
    assert player.is_muted is True

def test_seek_on_release_sets_vlc_time_from_slider(mock_player):
    player, mock_vlc = mock_player

    player.time_slider.get.return_value = 30000

    fake_event = object()  
    player.seek_on_release(fake_event)

    mock_vlc.set_time.assert_called_once_with(30000)
    
def test_seek_to_time_converts_seconds_to_ms(mock_player):
    player, mock_vlc = mock_player

    player.seek_to_time(42)

    mock_vlc.set_time.assert_called_once_with(42000)

def test_on_slider_move_updates_label_when_dragging(mock_player):
    player, mock_vlc = mock_player

    player.slider_dragging = True

    player.on_slider_move("15")

    # We just check that the time tag is updated
    player.current_time_label.config.assert_called_once()
   
    mock_vlc.set_time.assert_not_called()
    
def test_on_slider_move_does_nothing_when_not_dragging(mock_player):
    player, mock_vlc = mock_player

    player.slider_dragging = False

    player.on_slider_move("20")

    player.current_time_label.config.assert_not_called()
    mock_vlc.set_time.assert_not_called()
    
def test_on_slider_press_sets_dragging_true(mock_player):
    player, _ = mock_player

    player.slider_dragging = False
    fake_event = object()

    player.on_slider_press(fake_event)

    assert player.slider_dragging is True

def test_on_slider_release_calls_seek_and_unsets_flag(mock_player):
    player, _ = mock_player

    player.slider_dragging = True
    fake_event = object()

    with patch.object(player, "seek_on_release") as mock_seek:
        player.on_slider_release(fake_event)

    assert player.slider_dragging is False
    mock_seek.assert_called_once_with(fake_event)

def test_update_time_calls_after(mock_player):
    player, _ = mock_player

    # Mockear comportamiento mínimo
    player.player.get_time.return_value = 0
    player.player.is_playing.return_value = False

    player.update_time()

    player.root.after.assert_called_once()
    args, kwargs = player.root.after.call_args

    assert args[0] == 1000
    assert args[1] == player.update_time

def test_update_time_updates_ui_when_playing(mock_player):
    player, _ = mock_player

    player.player.get_time.return_value = 5000
    player.player.is_playing.return_value = True
    player.slider_dragging = False
    player.time_slider.get.return_value = 0

    player.update_time()

    player.mp6_label_left.config.assert_called_with(image=player.mp6)
    player.mp6_label_right.config.assert_called_with(image=player.mp6)
    player.style.configure.assert_any_call('Custom.Horizontal.TScale', troughcolor="#8A4A06")
    player.current_time_label.config.assert_any_call(fg="#F4BF22")
    player.total_time_label.config.assert_any_call(fg="#F4BF22")
    player.play_pause_button.config.assert_called_with(image=player.pause_big)

def test_update_time_updates_ui_when_stopped(mock_player):
    player, _ = mock_player

    player.player.get_time.return_value = 5000
    player.player.is_playing.return_value = False

    player.update_time()

    player.mp6_label_left.config.assert_called_with(image=player.mp6_off)
    player.mp6_label_right.config.assert_called_with(image=player.mp6_off)
    player.style.configure.assert_any_call('Custom.Horizontal.TScale', troughcolor="black")
    player.current_time_label.config.assert_any_call(fg="#ADADAD")
    player.total_time_label.config.assert_any_call(fg="#ADADAD")
    player.play_pause_button.config.assert_called_with(image=player.play_off)

def test_update_time_calls_play_from_selection_when_loop_enabled(mock_player):
    player, _ = mock_player

    player.duration = 10000
    player.loop_enabled = True
    player.player.get_time.return_value = 9500
    player.player.is_playing.return_value = False

    player.play_from_selection = MagicMock()

    player.update_time()

    player.play_from_selection.assert_called_once()
    
def test_update_time_calls_play_next_when_not_looping(mock_player):
    player, _ = mock_player

    player.duration = 10000
    player.loop_enabled = False
    player.player.get_time.return_value = 9500
    player.player.is_playing.return_value = False

    player.play_next = MagicMock()

    player.update_time()

    player.play_next.assert_called_once()

def test_play_does_not_call_vlc_play_if_already_playing(mock_player):
    player, mock_vlc = mock_player
    player.is_playing = True  # We pretend that it is already playing

    player.play()

    mock_vlc.play.assert_not_called()

def test_play_sets_is_playing_to_true(mock_player):
    player, _ = mock_player
    player.is_playing = False

    player.play()

    assert player.is_playing is True

def test_play_does_not_change_is_playing_if_already_playing(mock_player):
    player, _= mock_player
    player.is_playing = True

    player.play()

    assert player.is_playing is True

def test_pause_calls_player_pause_when_playing(mock_player):
    player, mock_vlc = mock_player

    player.is_playing = True
    print("DEBUG test: is_playing justo después de poner True =", player.is_playing)
    assert player.is_playing is True  # ← esto es CLAVE

    player.pause()

    assert player.is_playing is False
    mock_vlc.pause.assert_called_once()

def test_update_time_updates_slider_position(mock_player):
    player, _ = mock_player

    # Simulate that VLC is playing
    player.player.is_playing.return_value = True

    # Simulate current time in milliseconds
    player.player.get_time.return_value = 5000

    # Simulate that the user is NOT dragging the slider
    player.slider_dragging = False

    player.update_time()

    player.time_slider.set.assert_called_with(5000)
    
def test_update_time_moves_slider_when_not_dragging(mock_player):
    player, _ = mock_player

    player.player.get_time.return_value = 8000
    player.player.is_playing.return_value = True
    player.slider_dragging = False
    player.time_slider.get.return_value = 0  # diferencia > 500 ms

    player.update_time()

    player.time_slider.set.assert_called_once_with(8000)
    player.current_time_label.config.assert_any_call(text=format_time(8000))

def test_update_time_does_not_update_slider_when_dragging(mock_player):
    player, _ = mock_player

    player.player.is_playing.return_value = True
    player.player.get_time.return_value = 5000  # 5 seconds in ms

    player.slider_dragging = True  # usuario arrastrando

    player.update_time()

    player.time_slider.set.assert_not_called()

def test_slider_change_updates_player_time(mock_player):
    player, _ = mock_player

    # Simulate that the user is dragging the slider
    player.slider_dragging = True

    # Simulate that the slider returns a new value (in ms)
    player.time_slider.get.return_value = 7000  # 7 seconds in ms

    # Call the method that handles the slider change
    player.on_time_slider_change("event")

    # You must call VLC to update the time
    player.player.set_time.assert_called_once_with(7000)

def test_slider_change_ignores_updates_when_not_playing(mock_player):
    player, _ = mock_player

    # Pretend it is NOT playing
    player.player.is_playing.return_value = False

    # Simulate that the user is dragging the slider
    player.slider_dragging = True

    # Simulate a slider value
    player.time_slider.get.return_value = 9000  

    # Call the method that the tests use for the seek
    player.on_time_slider_change("event")

    
    player.player.set_time.assert_not_called()

