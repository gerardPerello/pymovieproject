from client.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different


class Event:
    def __init__(self, event_id, type_event, content_event, percentage_or_total, percentage_change, total_change):
        self.event_id = event_id
        self.type_event = type_event
        self.content_event = content_event
        self.percentage_or_total = percentage_or_total
        self.percentage_change = percentage_change
        self.total_change = total_change

