from nameko.rpc import rpc, RpcProxy
from datetime import datetime
import subprocess

# Define the curl command
curl_command = "curl -i localhost:8000/query"


class Request:
    name = "request"

    # http_service = RpcProxy("http_service")

    @rpc
    def send_request(self):
        try:
            process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            return stdout

            # Print any error messages
            if stderr:
                return stderr
        except Exception as e:
            return e

