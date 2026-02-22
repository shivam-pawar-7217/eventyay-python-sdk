import unittest
from unittest.mock import Mock, patch
from eventyay.client import EventyayClient
from eventyay.models import Track, TrackList


class TestTracksAPI(unittest.TestCase):
    def setUp(self):
        self.client = EventyayClient(api_key="test_key")
        self.mock_track_data = {
            "id": 1,
            "name": "AI & Machine Learning",
            "description": "Sessions about artificial intelligence.",
            "color": "#FF5733",
            "font_color": "#FFFFFF"
        }

    @patch('eventyay.client.requests.Session.get')
    def test_get_event_tracks(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                self.mock_track_data,
                {
                    "id": 2,
                    "name": "Web Development",
                    "description": "Frontend and backend talks.",
                    "color": "#3366FF",
                    "font_color": "#FFFFFF"
                }
            ],
            "meta": {"total": 2}
        }
        mock_get.return_value = mock_response

        track_list = self.client.get_event_tracks(
            "test-event", page=1, page_size=10
        )

        self.assertIsInstance(track_list, TrackList)
        self.assertEqual(len(track_list.data), 2)

        first_track = track_list.data[0]
        self.assertIsInstance(first_track, Track)
        self.assertEqual(first_track.id, 1)
        self.assertEqual(first_track.name, "AI & Machine Learning")
        self.assertEqual(first_track.color, "#FF5733")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/tracks",
            params={'page': 1, 'page_size': 10}
        )

    @patch('eventyay.client.requests.Session.get')
    def test_get_track(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_track_data
        mock_get.return_value = mock_response

        track = self.client.get_track("test-event", "1")

        self.assertIsInstance(track, Track)
        self.assertEqual(track.id, 1)
        self.assertEqual(track.name, "AI & Machine Learning")

        mock_get.assert_called_once_with(
            "https://dev.eventyay.com/api/v1/events/test-event/tracks/1",
            params=None
        )


if __name__ == '__main__':
    unittest.main()
