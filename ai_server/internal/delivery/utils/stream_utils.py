from socket import CAN_EFF_FLAG
from ...handler.rtsp_stream.utils.rtsp_stream import RTSPStream

from ....pkg.config.config import config

EVENT = config["event"]
CAMERA_EVENT = EVENT["camera"]

class StreamUtils:
    def parse_stream_info(self, camera_stream_detail):
        camera_id = camera_stream_detail._id
        rtsp_url = camera_stream_detail.sfu_rtsp_stream_url
        event_key = camera_stream_detail.event_key
        is_set_line = camera_stream_detail.is_set_line

        iot_event_zone_coords = camera_stream_detail.iot_event_zone_coords
        camera_event_zone_coords = camera_stream_detail.camera_event_zone_coords

        stream_info = RTSPStream(camera_id, rtsp_url, event_key, iot_event_zone_coords, camera_event_zone_coords)
        if is_set_line:
            line_coords = [camera_stream_detail.offset_x_begin, camera_stream_detail.offset_y_begin, camera_stream_detail.offset_x_end, camera_stream_detail.offset_y_end]
            stream_info.set_line_coords(line_coords)

        return stream_info

    def valid_event_info(self, stream_info):
        if stream_info.event_key == CAMERA_EVENT["line_crossing"]["key"]:
            if stream_info.line_coords == None:
                return False
        return True
