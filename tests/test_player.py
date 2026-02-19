import pytest
from unittest.mock import MagicMock, Mock, patch
from player import PlaylistPlayer
from modules.utils import format_time
from modules.image_utils import load_image

 
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

    # Mock minimal behavior
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
    player.time_slider.get.return_value = 0  # difference > 500 ms

    player.update_time()

    player.time_slider.set.assert_called_once_with(8000)
    player.current_time_label.config.assert_any_call(text=format_time(8000))

def test_update_time_does_not_update_slider_when_dragging(mock_player):
    player, _ = mock_player

    player.player.is_playing.return_value = True
    player.player.get_time.return_value = 5000  # 5 seconds in ms

    player.slider_dragging = True  # user dragging

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

def test_add_file_adds_to_playlist(mock_player):
    player, _ = mock_player

    fake_path = "C:/music/song.mp3"

    player.add_file(fake_path)

    assert fake_path in player.playlist
    player.listbox.insert.assert_called_once()

def test_play_next_advances_index_and_calls_play_from_selection(mock_player):
    player, _ = mock_player

    # Simulate internal playlist
    player.playlist = [
        "C:/music/track1.mp3",
        "C:/music/track2.mp3",
        "C:/music/track3.mp3",
    ]

    # Initial index
    player.current_index = 0

    # Run
    player.play_next()

    # You must advance to the next index
    assert player.current_index == 1

    player.play_from_selection.assert_called_once()

def test_add_file_updates_ui_listbox(mock_player):
    player, _ = mock_player

    fake_path = "C:/music/song.mp3"
    
    player.add_file(fake_path)

    player.listbox.insert.assert_called_once()

def test_prev_goes_to_previous_track(mock_player):
    player, _ = mock_player

    # Simular playlist interna
    player.playlist = [
        "C:/music/track1.mp3",
        "C:/music/track2.mp3",
        "C:/music/track3.mp3",
    ]

    player.current_index = 1

    player.play_previous()

    assert player.current_index == 0

    player.play_from_selection.assert_called_once()

def test_next_does_not_fail_on_last_track(mock_player):
    player, _ = mock_player

    player.playlist = [
        "C:/music/track1.mp3",
        "C:/music/track2.mp3",
        "C:/music/track3.mp3",
    ]
    
    player.current_index = 2

    player.play_next()

    assert player.current_index == 2

    player.play_from_selection.assert_not_called()

def test_load_image_returns_photoimage(patched_image_utils):
    result = load_image("logo.png")

    assert result is patched_image_utils["fake_photo"]
    patched_image_utils["mock_open"].assert_called_once()
    patched_image_utils["mock_photo"].assert_called_once_with(
        patched_image_utils["fake_image"]
    )

def test_load_image_uses_resource_path(patched_image_utils):

        load_image("graphics/icon.png")

        patched_image_utils["mock_resource"].assert_called_once_with("graphics/icon.png")
        patched_image_utils["mock_open"].assert_called_once_with("fake/path.png")

def test_load_image_resizes_image_when_size_is_given(patched_image_utils):

        result = load_image("graphics/icon.png", size=(50, 50))

        # Verifications
        patched_image_utils["mock_resource"].assert_called_once_with("graphics/icon.png")
        patched_image_utils["mock_open"].assert_called_once_with("fake/path.png")
        patched_image_utils["fake_image"].resize.assert_called_once_with((50, 50))
        patched_image_utils["mock_photo"].assert_called_once_with(patched_image_utils["fake_resized"])
        assert result is patched_image_utils["fake_photo"]

def test_labels_update_on_play_pause(mock_player):
    player, _ = mock_player
    
    player.status_label = MagicMock()
    player.play_button_label = MagicMock()

    player.is_playing = False
    
    player.toggle_play_pause()

    assert player.is_playing is True

    player.status_label.config.assert_called_with(text="Playing…")
    player.play_button_label.config.assert_called_with(text="Pause")

    player.is_playing = True

    player.toggle_play_pause()

    assert player.is_playing is False

    player.status_label.config.assert_called_with(text="Paused")
    player.play_button_label.config.assert_called_with(text="Play")

def test_player_initial_state(mock_player):
    player, _ = mock_player
    assert player.is_playing is False
    assert player.current_index is None
    assert player.playlist == []
    assert player.loop_enabled is False
    assert player.shuffle_enabled is False
    assert player.is_muted is False
    assert player.last_volume == 50
    assert player.duration == 0
    assert player.slider_dragging is False

def test_player_stops_on_end_of_track(mock_player):
    player, _ = mock_player

    player.handle_end_of_track()

    # Ya no se llama a stop() en la nueva lógica
    assert player.is_playing is False


def test_player_handles_invalid_file_gracefully(mock_player_real):
    player = mock_player_real

    player.playlist = ["fake/broken.mp3"]
    player.current_index = 0

    # Simulate failure in media_new
    player.vlc_instance.media_new.side_effect = Exception("Invalid file")

    player.play_from_selection()

    assert player.is_playing is False
    assert player.current_index is None





