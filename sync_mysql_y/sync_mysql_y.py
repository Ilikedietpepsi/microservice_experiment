from nameko.rpc import rpc, RpcProxy

class SyncServiceY:
    name = "sync_mysql_y"

    service_x = RpcProxy("sync_mysql_x")

    @rpc
    def enhance_data(self, ACTION):

        processed_data = self.service_x.process_data(ACTION)


        return processed_data
