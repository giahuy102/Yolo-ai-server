from ...handler.rtsp_stream.utils.rtsp_stream import RTSPStream

class StreamUtils:
    def parse_stream_info(self, camera_stream_detail):
        camera_id = camera_stream_detail._id
        rtsp_url = camera_stream_detail.sfu_rtsp_stream_url
        event_key = camera_stream_detail.event_key
        is_set_line = camera_stream_detail.is_set_line
        stream_info = RTSPStream(camera_id, rtsp_url, event_key)
        if is_set_line:
            line_coords = [camera_stream_detail.offset_x_begin, camera_stream_detail.offset_y_begin, camera_stream_detail.offset_x_end, camera_stream_detail.offset_y_end]
            stream_info.set_line_coords(line_coords)

        return stream_info
