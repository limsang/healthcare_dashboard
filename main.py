from preprocess.health_data_parser import HealthDataExtractor
from preprocess.route_data_parser import RouteDataExtractor

def main():
    # health_data parsing
    # data = HealthDataExtractor()
    # data.report_stats()
    # data.extract()

    # route_data parsing
    handler = RouteDataExtractor()
    handler.loop_genDF()

if __name__ == '__main__':
    main()