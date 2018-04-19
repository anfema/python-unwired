import argparse
import unwiredlabs

parser = argparse.ArgumentParser(description='Make a location request against the unwiredlabs location API')
parser.add_argument(
	'-k', '--key',
	dest='key',
	action='store',
	nargs=1,
	type=str,
	required=True,
    help='API key from Unwired API panel'
)

parser.add_argument(
	'-w', '--wifi',
	dest='wifi',
	action='append',
	nargs=1,
	type=str,
    help='WIFI BSSID and signal strength (format: XX:XX:XX:XX:XX:XX@RSSI)'
)

parser.add_argument(
	'-g', '--gps',
	dest='gps',
	action='store',
	nargs=1,
	type=str,
    help='GPS coordinate (format: lattitude,longitude@num_satelites)'
)

parser.add_argument(
	'-c', '--cell', '--celltower',
	dest='cell',
	action='append',
	nargs=1,
	type=str,
    help='Celltower information (format: MCC,MNC,LAC,CellID@RSSI)'
)

parser.add_argument(
	'-l', '--lte',
	dest='lte',
	action='append',
	nargs=1,
	type=str,
    help='LTE Celltower information (format: MCC,MNC,LAC,CellID@RSSI)'
)

parser.add_argument(
	'-u', '--umts',
	dest='umts',
	action='append',
	nargs=1,
	type=str,
    help='UMTS (3G) Celltower information (format: MCC,MNC,LAC,CellID@RSSI)'
)

parser.add_argument(
	'-m', '--cdma',
	dest='cdma',
	action='append',
	nargs=1,
	type=str,
    help='CDMA/EVDO Celltower information (format: MCC,MNC,LAC,CellID@RSSI)'
)

parser.add_argument(
	'-a', '--address',
	dest='address',
	action='store_const',
	const=True,
	default=False,
    help='Fetch address info in addition to coordinates'
)
args = parser.parse_args()

request = unwiredlabs.UnwiredRequest(fetch_address=args.address)

if args.wifi:
	for wifi in args.wifi:
		bssid, rssi = wifi[0].split('@')
		request.addAccessPoint(bssid, int(rssi))

if args.gps:
	coordinate, numSat = args.gps.split('@')
	lat, lon = coordinate.split(',')
	request.setGPSCoordinate(float(lat), float(lon), int(numSat))

if args.cell:
	for cell in args.cell:
		tower, rssi = cell[0].split('@')
		mcc, mnc, lac, cellID = tower.split(',')
		request.addGSMCellTower(int(lac), int(cellID), int(rssi), mcc=int(mcc), mnc=int(mnc))

if args.lte:
	for cell in args.lte:
		tower, rssi = cell[0].split('@')
		mcc, mnc, lac, cellID = tower.split(',')
		request.addLTECellTower(int(lac), int(cellID), int(rssi), mcc=int(mcc), mnc=int(mnc))

if args.umts:
	for cell in args.umts:
		tower, rssi = cell[0].split('@')
		mcc, mnc, lac, cellID = tower.split(',')
		request.addUMTSCellTower(int(lac), int(cellID), int(rssi), mcc=int(mcc), mnc=int(mnc))

if args.cdma:
	for cell in args.cdma:
		tower, rssi = cell[0].split('@')
		mcc, mnc, lac, cellID = tower.split(',')
		request.addCDMACellTower(int(lac), int(cellID), int(rssi), mcc=int(mcc), mnc=int(mnc))

print('Performing request:', str(request))

connection = unwiredlabs.UnwiredConnection(key=args.key[0])
response = connection.performRequest(request)
if response.status != 'Ok':
	print('Error:', response.status)
else:
	print('Response: ', response.coordinate, 'deviation', response.hpe, 'meters')
	if args.address:
		print('Address: ', response.address)
