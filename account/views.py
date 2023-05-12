import asyncio
import json
import os
import time

import requests
import websockets
from datetime import datetime
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
from channels.layers import get_channel_layer
from django.http import Http404, JsonResponse
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from account.models import User, UserConnection, Scan, ScanData
from rest_framework.views import APIView
from machine_learning import *

from account.models import ScanData
from django.views.decorators.http import require_http_methods
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, \
    UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UpdateRegisterUserSerializer, \
    UserConnectionSerializer, IsScanSerializer, ScanDataSerializer, SysInfoSerializer, ItgnirSerializer, \
    PredictSerializer, ModelTrainingSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserRegistrationSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserLoginSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_201_CREATED)


class SendPasswordResetEmailView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = SendPasswordResetEmailSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_201_CREATED)


class UserPasswordResetView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserPasswordResetSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_201_CREATED)


class UpdateRegisterUserView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UpdateRegisterUserSerializer
    allowed_methods = ('PUT',)
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, format=None):
        serializer = UpdateRegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'User type update successfully'}, status=status.HTTP_200_OK)


def lobby(request):
    return render(request, 'account/lobby.html')


class UserConnectionView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = UserConnectionSerializer
    allowed_methods = ('POST', 'PUT')
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserConnectionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'User Connection Established Successfully'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        try:
            machine_name = request.data['machine_name']
            user_id = request.data['user_id']
            user_conn = self.get_object(machine_name, user_id)
        except Http404:
            return Response({"error": "UserConnection not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserConnectionSerializer(user_conn, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'User Connection Updated Successfully'}, status=status.HTTP_200_OK)

    def get_object(self, machine_name, user_id):
        user_conn = UserConnection.objects.get(machine_name=machine_name, user_id=user_id)
        return user_conn


async def send_and_receive(request_data):
    try:
        user_id = request_data['user_id']
        from .consumers import connections
        await connections[user_id].receive(json.dumps(request_data))
    except Exception as e:
        print("error", e)
        return print({f'Error: {e}'})


class IsScanView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = IsScanSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        try:
            if len(request.data) == 0:
                return Response({f'Error': 'invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
            is_scan = dict(request.data)['is_scan'][0]
            if is_scan == 'yes':
                scan_instance = Scan.objects.create()
                user_id = request.user.id
                scan_id = str(scan_instance.scan_id)
                async_to_sync(send_and_receive)(
                    request_data={'is_scan_data': 'yes', 'user_id': user_id, 'scan_id': scan_id})
                return Response({'message': 'data Scanning is in progress'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'Error': 'select is_scan yes for scanning the data'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error", e)
            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class ScanDataView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = ScanDataSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        machine_name = request.data['machine_name']
        user_id = request.data['user_id']
        scan_id = request.data['scan_id']
        new_scan_id = scan_id.replace("-", "").replace("_", "")
        # user_connection_obj = UserConnection.objects.get(machine_name=machine_name, user_id=user_id)
        user_connection_obj = UserConnection.objects.get(machine_name=machine_name)
        scan_obj = Scan.objects.get(scan_id=scan_id)
        # energy_wavelength_data = request.data.getlist('energy_wavelength_data')
        energy_wavelength_data = [(1100, 69), (1102, 9), (1104, 81), (1106, 73), (1108, 34), (1110, 50), (1112, 93), (1114, 44), (1116, 57), (1118, 24), (1120, 48), (1122, 47), (1124, 10), (1126, 53), (1128, 32), (1130, 7), (1132, 82), (1134, 60), (1136, 6), (1138, 21), (1140, 38), (1142, 1), (1144, 63), (1146, 37), (1148, 86), (1150, 90), (1152, 94), (1154, 48), (1156, 96), (1158, 58), (1160, 9), (1162, 16), (1164, 98), (1166, 84), (1168, 79), (1170, 48), (1172, 93), (1174, 82), (1176, 45), (1178, 92), (1180, 15), (1182, 35), (1184, 3), (1186, 10), (1188, 11), (1190, 76), (1192, 56), (1194, 20), (1196, 44), (1198, 33), (1200, 34), (1202, 18), (1204, 81), (1206, 39), (1208, 60), (1210, 27), (1212, 31), (1214, 63), (1216, 26), (1218, 12), (1220, 76), (1222, 78), (1224, 100), (1226, 57), (1228, 80), (1230, 10), (1232, 69), (1234, 60), (1236, 20), (1238, 50), (1240, 92), (1242, 58), (1244, 48), (1246, 34), (1248, 18), (1250, 85), (1252, 49), (1254, 89), (1256, 87), (1258, 32), (1260, 64), (1262, 34), (1264, 21), (1266, 5), (1268, 43), (1270, 48), (1272, 87), (1274, 89), (1276, 84), (1278, 39), (1280, 5), (1282, 23), (1284, 54), (1286, 31), (1288, 7), (1290, 75), (1292, 33), (1294, 3), (1296, 61), (1298, 72), (1300, 2), (1302, 17), (1304, 98), (1306, 19), (1308, 39), (1310, 50), (1312, 30), (1314, 32), (1316, 4), (1318, 54), (1320, 54), (1322, 31), (1324, 69), (1326, 18), (1328, 44), (1330, 28), (1332, 19), (1334, 3), (1336, 65), (1338, 16), (1340, 30), (1342, 63), (1344, 61), (1346, 53), (1348, 52), (1350, 28), (1352, 78), (1354, 97), (1356, 70), (1358, 23), (1360, 17), (1362, 30), (1364, 99), (1366, 19), (1368, 84), (1370, 39), (1372, 56), (1374, 32), (1376, 49), (1378, 93), (1380, 27), (1382, 98), (1384, 49), (1386, 60), (1388, 9), (1390, 9), (1392, 92), (1394, 73), (1396, 60), (1398, 93), (1400, 54), (1402, 57), (1404, 90), (1406, 83), (1408, 75), (1410, 74), (1412, 64), (1414, 98), (1416, 71), (1418, 92), (1420, 61), (1422, 62), (1424, 82), (1426, 99), (1428, 60), (1430, 22), (1432, 77), (1434, 74), (1436, 22), (1438, 85), (1440, 51), (1442, 52), (1444, 68), (1446, 92), (1448, 55), (1450, 61), (1452, 4), (1454, 88), (1456, 68), (1458, 76), (1460, 20), (1462, 44), (1464, 9), (1466, 74), (1468, 7), (1470, 82), (1472, 80), (1474, 2), (1476, 71), (1478, 25), (1480, 71), (1482, 8), (1484, 3), (1486, 92), (1488, 12), (1490, 71), (1492, 70), (1494, 67), (1496, 46), (1498, 100), (1500, 72), (1502, 84), (1504, 50), (1506, 40), (1508, 25), (1510, 94), (1512, 82), (1514, 50), (1516, 10), (1518, 21), (1520, 7), (1522, 42), (1524, 25), (1526, 14), (1528, 95), (1530, 20), (1532, 52), (1534, 47), (1536, 85), (1538, 87), (1540, 5), (1542, 26), (1544, 83), (1546, 15), (1548, 50), (1550, 13), (1552, 5), (1554, 25), (1556, 75), (1558, 65), (1560, 81), (1562, 35), (1564, 22), (1566, 39), (1568, 18), (1570, 89), (1572, 50), (1574, 56), (1576, 16), (1578, 18), (1580, 74), (1582, 39), (1584, 66), (1586, 8), (1588, 45), (1590, 8), (1592, 77), (1594, 50), (1596, 55), (1598, 90), (1600, 56), (1602, 11), (1604, 29), (1606, 74), (1608, 70), (1610, 15), (1612, 2), (1614, 66), (1616, 77), (1618, 4), (1620, 37), (1622, 99), (1624, 33), (1626, 21), (1628, 5), (1630, 21), (1632, 68), (1634, 87), (1636, 46), (1638, 21), (1640, 66), (1642, 18), (1644, 70), (1646, 44), (1648, 44), (1650, 53), (1652, 27), (1654, 79), (1656, 41), (1658, 31), (1660, 7), (1662, 94), (1664, 29), (1666, 17), (1668, 84), (1670, 75), (1672, 24), (1674, 46), (1676, 27), (1678, 41), (1680, 9), (1682, 83), (1684, 51), (1686, 61), (1688, 99), (1690, 55), (1692, 78), (1694, 97), (1696, 17), (1698, 49), (1700, 90), (1702, 32), (1704, 42), (1706, 46), (1708, 34), (1710, 91), (1712, 89), (1714, 40), (1716, 63), (1718, 52), (1720, 3), (1722, 19), (1724, 38), (1726, 57), (1728, 9), (1730, 28), (1732, 4), (1734, 73), (1736, 48), (1738, 23), (1740, 41), (1742, 23), (1744, 42), (1746, 45), (1748, 15), (1750, 62), (1752, 56), (1754, 9), (1756, 97), (1758, 4), (1760, 72), (1762, 11), (1764, 49), (1766, 79), (1768, 15), (1770, 12), (1772, 22), (1774, 66), (1776, 2), (1778, 62), (1780, 32), (1782, 59), (1784, 18), (1786, 55), (1788, 28), (1790, 47), (1792, 10), (1794, 6), (1796, 99), (1798, 14), (1800, 29), (1802, 66), (1804, 3), (1806, 62), (1808, 76), (1810, 75), (1812, 51), (1814, 41), (1816, 52), (1818, 73), (1820, 4), (1822, 95), (1824, 93), (1826, 93), (1828, 80), (1830, 17), (1832, 2), (1834, 9), (1836, 39), (1838, 50), (1840, 11), (1842, 67), (1844, 99), (1846, 58), (1848, 94), (1850, 69), (1852, 44), (1854, 20), (1856, 19), (1858, 51), (1860, 37), (1862, 10), (1864, 62), (1866, 16), (1868, 20), (1870, 63), (1872, 80), (1874, 32), (1876, 67), (1878, 43), (1880, 45), (1882, 22), (1884, 33), (1886, 40), (1888, 43), (1890, 45), (1892, 84), (1894, 91), (1896, 88), (1898, 86), (1900, 5), (1902, 94), (1904, 93), (1906, 9), (1908, 75), (1910, 89), (1912, 10), (1914, 37), (1916, 63), (1918, 48), (1920, 84), (1922, 12), (1924, 16), (1926, 25), (1928, 6), (1930, 57), (1932, 46), (1934, 1), (1936, 51), (1938, 39), (1940, 25), (1942, 24), (1944, 40), (1946, 17), (1948, 6), (1950, 67), (1952, 67), (1954, 4), (1956, 24), (1958, 11), (1960, 69), (1962, 80), (1964, 83), (1966, 12), (1968, 22), (1970, 50), (1972, 86), (1974, 68), (1976, 18), (1978, 92), (1980, 14), (1982, 67), (1984, 28), (1986, 19), (1988, 86), (1990, 50), (1992, 3), (1994, 5), (1996, 58), (1998, 74), (2000, 53), (2002, 72), (2004, 12), (2006, 31), (2008, 66), (2010, 81), (2012, 12), (2014, 21), (2016, 11), (2018, 69), (2020, 2), (2022, 92), (2024, 7), (2026, 15), (2028, 40), (2030, 17), (2032, 13), (2034, 79), (2036, 74), (2038, 62), (2040, 35), (2042, 71), (2044, 88), (2046, 61), (2048, 29), (2050, 72), (2052, 44), (2054, 58), (2056, 40), (2058, 65), (2060, 38), (2062, 100), (2064, 35), (2066, 3), (2068, 10), (2070, 50), (2072, 44), (2074, 7), (2076, 90), (2078, 27), (2080, 94), (2082, 98), (2084, 98), (2086, 11), (2088, 6), (2090, 96), (2092, 21), (2094, 12), (2096, 33), (2098, 37), (2100, 98), (2102, 31), (2104, 40), (2106, 58), (2108, 17), (2110, 91), (2112, 100), (2114, 46), (2116, 59), (2118, 78), (2120, 71), (2122, 13), (2124, 60), (2126, 73), (2128, 77), (2130, 51), (2132, 36), (2134, 84), (2136, 36), (2138, 76), (2140, 36), (2142, 56), (2144, 50), (2146, 78), (2148, 25), (2150, 27), (2152, 83), (2154, 74), (2156, 5), (2158, 31), (2160, 63), (2162, 76), (2164, 16), (2166, 67), (2168, 91), (2170, 54), (2172, 38), (2174, 12), (2176, 36), (2178, 25), (2180, 38), (2182, 48), (2184, 88), (2186, 74), (2188, 50), (2190, 84), (2192, 29), (2194, 56), (2196, 83), (2198, 41), (2200, 83), (2202, 5), (2204, 45), (2206, 48), (2208, 77), (2210, 48), (2212, 74), (2214, 6), (2216, 23), (2218, 96), (2220, 89), (2222, 42), (2224, 40), (2226, 63), (2228, 31), (2230, 75), (2232, 20), (2234, 38), (2236, 24), (2238, 88), (2240, 70), (2242, 84), (2244, 10), (2246, 54), (2248, 13), (2250, 32), (2252, 61), (2254, 56), (2256, 23), (2258, 61), (2260, 88), (2262, 21), (2264, 16), (2266, 6), (2268, 7), (2270, 47), (2272, 97), (2274, 20), (2276, 87), (2278, 18), (2280, 92), (2282, 85), (2284, 54), (2286, 41), (2288, 94), (2290, 7), (2292, 55), (2294, 39), (2296, 75), (2298, 21), (2300, 80), (2302, 50), (2304, 57), (2306, 100), (2308, 38), (2310, 58), (2312, 53), (2314, 98), (2316, 93), (2318, 34), (2320, 86), (2322, 12), (2324, 11), (2326, 75), (2328, 34), (2330, 3), (2332, 65), (2334, 93), (2336, 87), (2338, 55), (2340, 40), (2342, 87), (2344, 81), (2346, 2), (2348, 43), (2350, 84), (2352, 25), (2354, 92), (2356, 75), (2358, 7), (2360, 89), (2362, 33), (2364, 31), (2366, 97), (2368, 24), (2370, 79), (2372, 56), (2374, 21), (2376, 98), (2378, 13), (2380, 49), (2382, 62), (2384, 5), (2386, 86), (2388, 54), (2390, 98), (2392, 56), (2394, 25), (2396, 69), (2398, 93), (2400, 34), (2402, 58), (2404, 94), (2406, 82), (2408, 85), (2410, 51), (2412, 30), (2414, 84), (2416, 63), (2418, 85), (2420, 73), (2422, 25), (2424, 41), (2426, 68), (2428, 80), (2430, 68), (2432, 25), (2434, 67), (2436, 15), (2438, 90), (2440, 49), (2442, 81), (2444, 47), (2446, 16), (2448, 23), (2450, 20), (2452, 99), (2454, 29), (2456, 25), (2458, 68), (2460, 8), (2462, 43), (2464, 14), (2466, 65), (2468, 27), (2470, 62), (2472, 91), (2474, 41), (2476, 1), (2478, 41), (2480, 54), (2482, 4), (2484, 79), (2486, 58), (2488, 46), (2490, 95), (2492, 49), (2494, 28), (2496, 3), (2498, 40)]
        scan_data_list = []
        for data in energy_wavelength_data:
            # energy, wavelength = eval(data)
            energy, wavelength = data[0], data[1]
            scan_data_list.append(
                ScanData(
                    user_connection=user_connection_obj,
                    scan_connection=scan_obj,
                    energy=energy,
                    wavelength=wavelength
                )
            )
        ScanData.objects.bulk_create(scan_data_list)

        try:
            # create instance of DataProcessor class
            data_processor = DataProcessor(username='root', password='U$er123',
                                           host='localhost', database='qtdb')

            # connect to database and retrieve data
            cnx, cursor = data_processor.connect_to_database()
            db_rows = data_processor.retrieve_data_for_prediction(cursor, new_scan_id)

            # preprocess data
            latest_energy_sample = data_processor.sample_data(db_rows)
            latest_energy_sample = latest_energy_sample[0]

            # close database connection
            cnx.close()

            # create instance of ModelTrainer class
            processor = SavGolFilter(unprocessed_energy_data=latest_energy_sample)
            pred = processor.process_data()

            print('Successfully getting the prediction')

            scan_instance = Scan.objects.get(scan_id=scan_id)
            scan_instance.predict_value = pred
            scan_instance.save()

            print('Data Scanned Successfully')
            return Response({'msg': 'Data Scanned Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("error", e)
            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class SysInfoView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = SysInfoSerializer

    def get(self, request, format=None):
        try:
            user_id = request.user.id
            userconnection_objects = UserConnection.objects.filter(user_id=user_id)
            connected_user_list = []
            for obj in userconnection_objects:
                data = {
                    'machine_name': obj.machine_name,
                    'mac_address': obj.mac_address
                }
                connected_user_list.append(data)
            message = {
                'message': 'machine names and mac addresses for login user',
                'connected_user_info': connected_user_list
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class ItgnirDataView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = ItgnirSerializer

    def post(self, request, format=None):
        try:
            if len(request.data) == 0:
                return Response({f'Error': 'invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
            machine_name = request.data['machine_name']
            userconnection_obj = UserConnection.objects.get(machine_name=machine_name)
            userconnection_id = userconnection_obj.id
            current_time = timezone.now()
            time_10_mints_ago = current_time - timezone.timedelta(minutes=10)
            scan_objects_list = ScanData.objects.filter(
                user_connection_id=userconnection_id,
                created_at__gte=time_10_mints_ago
            )
            itgnir_data = []
            for obj in scan_objects_list:
                energy = obj.energy
                wavelength = obj.wavelength
                data = {
                    'energy': energy,
                    'wavelength': wavelength
                }
                itgnir_data.append(data)
            message = {
                'message': 'energy and wavelength data between the last 2 days',
                'itgnir_data': itgnir_data
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = PredictSerializer

    def post(self, request, format=None):
        try:
            scan_id = request.data['scan_id']
            scan_instance = Scan.objects.get(scan_id=scan_id)
            predict_value = scan_instance.predict_value
            if not predict_value:
                message = {
                    'message': 'Prediction is in progress',
                }
                return Response(message, status=status.HTTP_200_OK)
            message = {
                'message': 'Prediction completed successfully',
                'predict_value': predict_value
            }
            return Response(message, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("error", e)
            error_message = f'{",".join(e)}'
            return Response({'Error': error_message}, status=status.HTTP_400_BAD_REQUEST)


class ModelTrainingView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = ModelTrainingSerializer

    def get(self, request, format=None):
        try:
            # create instance of DataProcessor class
            data_processor = DataProcessor(username='root', password='U$er123',
                                           host='localhost', database='qtdb')

            # connect to database and retrieve data
            cnx, cursor = data_processor.connect_to_database()
            db_rows = data_processor.retrieve_data(cursor)

            # preprocess data
            X_train_scaled, y_train, X_test_scaled, = data_processor.preprocess_data(db_rows)

            # close database connection
            cnx.close()

            # create instance of ModelTrainer class
            model_trainer = ModelTrainer(X_train_scaled=X_train_scaled, y_train=y_train)

            # train the model
            grid, train_score = model_trainer.train_model()

            # save the model
            model_trainer.save_model(grid)

            # load the model
            model_trainer.load_model()

            # format predictions as a JSON response
            response_data = {
                'message': 'Successfully trained the SVR model and saved it as gs_object.pkl file'
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print("error", e)
            error_message = str(e)
            return Response({'Error': error_message}, status=status.HTTP_400_BAD_REQUEST)
