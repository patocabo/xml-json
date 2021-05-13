import json
import sys
import xml.dom.minidom

# Open XML document using minidom parser

# inFile = sys.argv[1]
inFile = "seatmap1.xml"
xmlFile = xml.dom.minidom.parse(inFile)


def set_amount(element_to_analyze):
    if element_to_analyze.getAttribute('AvailableInd') == 'true':
        return seat.getElementsByTagName('ns:Service')[0].getElementsByTagName(
            'ns:Fee')[0].getAttribute('Amount')
    else:
        return None


def str_to_bool(s):
    if s == 'true':
        return True
    else:
        return False


if xmlFile.getElementsByTagName('Document').length == 0:
    plane_data = xmlFile.getElementsByTagName('ns:FlightSegmentInfo')[0]

    flight_data = {'FlightNumber': plane_data.getAttribute('FlightNumber'),
                   'DepartureDateTime': plane_data.getAttribute('DepartureDateTime'),
                   'DepartureAirport': plane_data.getElementsByTagName('ns:DepartureAirport')[0].getAttribute(
                       'LocationCode'),
                   'ArrivalAirport': plane_data.getElementsByTagName('ns:ArrivalAirport')[0].getAttribute(
                       'LocationCode')}
    plane = xmlFile.getElementsByTagName('ns:CabinClass')
    cabin_object = {}  # NS CABIN CLASS
    for cabin_class in plane:
        cabin = cabin_class.getElementsByTagName('ns:RowInfo')
        cabin_type = cabin[0].getAttribute('CabinType')
        for row_group in cabin:
            row_object = {}  # NS ROW INFO
            seat_group = row_group.getElementsByTagName('ns:SeatInfo')
            for seat in seat_group:
                seat_details = {}
                details = seat.getElementsByTagName('ns:Summary')[0]
                column = details.getAttribute('SeatNumber')[-1]
                print column
                row_object[column] = {'seat': seat.getElementsByTagName('ns:'),
                                      'seat_id': details.getAttribute('SeatNumber'),
                                      'cabin_class': cabin_type,
                                      'availability': str_to_bool(details.getAttribute('AvailableInd')),
                                      'seat_price': set_amount(details)}
                row_object[details.getAttribute('SeatNumber')[-1]] = seat_details
            cabin_object[row_group.getAttribute('RowNumber')] = row_object
    flight_data['Rows'] = cabin_object
    with open(inFile + '_parsed.json', 'w') as outfile:
        outfile.write(json.dumps(flight_data))
else:
    seatMap_list = xmlFile.getElementsByTagName('SeatMap')
    plane_object = {}
    for seatMap in seatMap_list:
        rowMap_list = seatMap.getElementsByTagName('Row')
        for individual_row in rowMap_list:
            seat_list = individual_row.getElementsByTagName('Seat')
            row_object = {}
            for individual_seat in seat_list:
                seat = {'seat': "Seat",
                        'seat_id': individual_row.getElementsByTagName('Number')[0].firstChild.nodeValue +
                                   individual_seat.getElementsByTagName('Column')[0].firstChild.nodeValue,
                        'cabin_class': "asd"}
                available = False
                for elemento in individual_seat.getElementsByTagName('SeatDefinitionRef'):

                    if elemento.firstChild.nodeValue == 'SD4':
                        available = True
                seat['availability'] = available
                seat['position'] = None
                seat['seat_price'] = None
                row_object[individual_seat.getElementsByTagName('Column')[0].firstChild.nodeValue] = seat
            plane_object[int(individual_row.getElementsByTagName('Number')[0].firstChild.nodeValue)] = row_object
            items = plane_object.items()
    sorted_rows = dict(sorted(items))
    flight_data = {"Rows": sorted_rows}

    with open(inFile + '_parsed.json', 'w') as outfile:
        outfile.write(json.dumps(total))
