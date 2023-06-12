import grpc

class GrpcHandler:

    def success(self, response, message="Success"):
        response.code = "0"
        response.message = message
        return response

    def failure(self, context, response, message="Failed"):
        context.set_code(grpc.StatusCode.ABORTED)
        context.set_details(str(message))
        return response
