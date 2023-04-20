

from .....pkg.grpc import camera_stream_info_pb2_grpc
from .....pkg.grpc import camera_stream_info_pb2 
from .grpc_handler import GrpcHandler
from ....handler.rtsp_stream.stream_loader import StreamLoader
from ....handler.rtsp_stream.utils.rtsp_stream import RTSPStream

class CameraStreamInfoHandler(camera_stream_info_pb2_grpc.CameraStreamInfoServiceServicer, GrpcHandler):

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


    def CreateCameraStream(self, request, context):
        stream_loader = StreamLoader.get_instance()
        camera_stream_detail = request.camera_stream_detail
        stream_info = self.parse_stream_info(camera_stream_detail)
        stream_loader.add_stream(stream_info.camera_id, stream_info)

        response = camera_stream_info_pb2.CameraStreamResponse()
        response._id = camera_stream_detail._id
        return self.success(response)

    def UpdateCameraStreamById(self, request, context):
        stream_loader = StreamLoader.get_instance()
        old_camera_id = request._id
        camera_stream_detail = request.camera_stream_detail
        stream_info = self.parse_stream_info(camera_stream_detail)
        stream_loader.update_stream(old_camera_id, stream_info)

        response = camera_stream_info_pb2.CameraStreamResponse()
        response._id = camera_stream_detail._id
        return self.success(response)


    def DeleteCameraStreamById(self, request, context):
        stream_loader = StreamLoader.get_instance()
        camera_id = request._id
        stream_loader.remove_stream(camera_id)

        response = camera_stream_info_pb2.CameraStreamResponse()
        response._id = request._id
        return self.success(response)
