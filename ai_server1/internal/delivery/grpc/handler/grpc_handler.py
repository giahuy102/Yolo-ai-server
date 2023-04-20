
class GrpcHandler:

    def success(self, response):
        response.code = "0"
        response.message = "Success"
        return response

    def failure(self, response):
        response.code = "13"
        response.message = "Failed"
        return response
