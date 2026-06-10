import logging

class MonitoringService:
    """
    Placeholder untuk integrasi Prometheus/Grafana atau Datadog.
    Saat ini hanya mencatat ke console/file log.
    """
    @staticmethod
    def log_event(event_name: str, details: dict = None):
        logging.info(f"[MONITORING] Event: {event_name} | Details: {details}")
        
    @staticmethod
    def log_error(error_msg: str):
        logging.error(f"[MONITORING] Error: {error_msg}")
