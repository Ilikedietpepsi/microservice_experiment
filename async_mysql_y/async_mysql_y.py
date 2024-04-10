from nameko.events import event_handler




class AsyncServiceY:
    name = "async_mysql_y"

    @event_handler("async_mysql_x", "processed_data_event")
    def handle_processed_data(self, processed_data):
        return processed_data


