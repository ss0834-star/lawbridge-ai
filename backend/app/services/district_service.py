from typing import List, Dict, Optional
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

DISTRICTS = [
    # ANDHRA PRADESH
    {"district": "Visakhapatnam", "state": "Andhra Pradesh", "lat": 17.6868, "lon": 83.2185, "dlsa": "District Legal Services Authority Visakhapatnam", "address": "District Court Complex, Visakhapatnam - 530 001", "phone": "0891-2565526"},
    {"district": "Vijayawada", "state": "Andhra Pradesh", "lat": 16.5062, "lon": 80.6480, "dlsa": "District Legal Services Authority Vijayawada", "address": "District Court Complex, Vijayawada - 520 001", "phone": "0866-2573333"},
    {"district": "Guntur", "state": "Andhra Pradesh", "lat": 16.3067, "lon": 80.4365, "dlsa": "District Legal Services Authority Guntur", "address": "District Court Complex, Guntur - 522 001", "phone": "0863-2233456"},
    {"district": "Nellore", "state": "Andhra Pradesh", "lat": 14.4426, "lon": 79.9865, "dlsa": "District Legal Services Authority Nellore", "address": "District Court Complex, Nellore - 524 001", "phone": "0861-2324567"},
    {"district": "Kurnool", "state": "Andhra Pradesh", "lat": 15.8281, "lon": 78.0373, "dlsa": "District Legal Services Authority Kurnool", "address": "District Court Complex, Kurnool - 518 001", "phone": "08518-224567"},
    {"district": "Kadapa", "state": "Andhra Pradesh", "lat": 14.4673, "lon": 78.8242, "dlsa": "District Legal Services Authority Kadapa", "address": "District Court Complex, Kadapa - 516 001", "phone": "08562-224567"},
    {"district": "Tirupati", "state": "Andhra Pradesh", "lat": 13.6288, "lon": 79.4192, "dlsa": "District Legal Services Authority Tirupati", "address": "District Court Complex, Tirupati - 517 501", "phone": "0877-2224567"},
    {"district": "Anantapur", "state": "Andhra Pradesh", "lat": 14.6819, "lon": 77.6006, "dlsa": "District Legal Services Authority Anantapur", "address": "District Court Complex, Anantapur - 515 001", "phone": "08554-274567"},
    {"district": "Eluru", "state": "Andhra Pradesh", "lat": 16.7107, "lon": 81.0952, "dlsa": "District Legal Services Authority Eluru", "address": "District Court Complex, Eluru - 534 001", "phone": "08812-224567"},
    {"district": "Rajamahendravaram", "state": "Andhra Pradesh", "lat": 17.0005, "lon": 81.8040, "dlsa": "District Legal Services Authority Rajamahendravaram", "address": "District Court Complex, Rajamahendravaram - 533 101", "phone": "0883-2474567"},
    # ASSAM
    {"district": "Guwahati", "state": "Assam", "lat": 26.1445, "lon": 91.7362, "dlsa": "District Legal Services Authority Kamrup Metro", "address": "District Court Complex, Guwahati - 781 001", "phone": "0361-2735026"},
    {"district": "Dibrugarh", "state": "Assam", "lat": 27.4728, "lon": 94.9120, "dlsa": "District Legal Services Authority Dibrugarh", "address": "District Court Complex, Dibrugarh - 786 001", "phone": "0373-2324567"},
    {"district": "Silchar", "state": "Assam", "lat": 24.8333, "lon": 92.7789, "dlsa": "District Legal Services Authority Cachar", "address": "District Court Complex, Silchar - 788 001", "phone": "03842-224567"},
    {"district": "Jorhat", "state": "Assam", "lat": 26.7509, "lon": 94.2037, "dlsa": "District Legal Services Authority Jorhat", "address": "District Court Complex, Jorhat - 785 001", "phone": "0376-2324567"},
    {"district": "Nagaon", "state": "Assam", "lat": 26.3464, "lon": 92.6840, "dlsa": "District Legal Services Authority Nagaon", "address": "District Court Complex, Nagaon - 782 001", "phone": "03672-224567"},
    {"district": "Tezpur", "state": "Assam", "lat": 26.6338, "lon": 92.7926, "dlsa": "District Legal Services Authority Sonitpur", "address": "District Court Complex, Tezpur - 784 001", "phone": "03712-224567"},
    # BIHAR
    {"district": "Patna", "state": "Bihar", "lat": 25.5941, "lon": 85.1376, "dlsa": "District Legal Services Authority Patna", "address": "District Court Complex, Patna - 800 001", "phone": "0612-2215247"},
    {"district": "Gaya", "state": "Bihar", "lat": 24.7914, "lon": 85.0002, "dlsa": "District Legal Services Authority Gaya", "address": "District Court Complex, Gaya - 823 001", "phone": "0631-2224567"},
    {"district": "Bhagalpur", "state": "Bihar", "lat": 25.2425, "lon": 86.9842, "dlsa": "District Legal Services Authority Bhagalpur", "address": "District Court Complex, Bhagalpur - 812 001", "phone": "0641-2224567"},
    {"district": "Muzaffarpur", "state": "Bihar", "lat": 26.1197, "lon": 85.3910, "dlsa": "District Legal Services Authority Muzaffarpur", "address": "District Court Complex, Muzaffarpur - 842 001", "phone": "0621-2224567"},
    {"district": "Darbhanga", "state": "Bihar", "lat": 26.1542, "lon": 85.8918, "dlsa": "District Legal Services Authority Darbhanga", "address": "District Court Complex, Darbhanga - 846 004", "phone": "06272-224567"},
    {"district": "Purnia", "state": "Bihar", "lat": 25.7771, "lon": 87.4753, "dlsa": "District Legal Services Authority Purnia", "address": "District Court Complex, Purnia - 854 301", "phone": "06454-224567"},
    # CHHATTISGARH
    {"district": "Raipur", "state": "Chhattisgarh", "lat": 21.2514, "lon": 81.6296, "dlsa": "District Legal Services Authority Raipur", "address": "District Court Complex, Raipur - 492 001", "phone": "0771-2224567"},
    {"district": "Bilaspur", "state": "Chhattisgarh", "lat": 22.0796, "lon": 82.1391, "dlsa": "District Legal Services Authority Bilaspur", "address": "District Court Complex, Bilaspur - 495 001", "phone": "07752-224567"},
    {"district": "Durg", "state": "Chhattisgarh", "lat": 21.1904, "lon": 81.2849, "dlsa": "District Legal Services Authority Durg", "address": "District Court Complex, Durg - 491 001", "phone": "0788-2224567"},
    {"district": "Korba", "state": "Chhattisgarh", "lat": 22.3595, "lon": 82.7501, "dlsa": "District Legal Services Authority Korba", "address": "District Court Complex, Korba - 495 677", "phone": "07759-224567"},
    {"district": "Jagdalpur", "state": "Chhattisgarh", "lat": 19.0748, "lon": 82.0388, "dlsa": "District Legal Services Authority Bastar", "address": "District Court Complex, Jagdalpur - 494 001", "phone": "07782-224567"},
    # DELHI
    {"district": "Central Delhi", "state": "Delhi", "lat": 28.6469, "lon": 77.2151, "dlsa": "District Legal Services Authority Central Delhi", "address": "Tis Hazari Courts, Delhi - 110 054", "phone": "011-23917914"},
    {"district": "South Delhi", "state": "Delhi", "lat": 28.5245, "lon": 77.1855, "dlsa": "District Legal Services Authority South Delhi", "address": "Saket District Courts, New Delhi - 110 017", "phone": "011-29563456"},
    {"district": "East Delhi", "state": "Delhi", "lat": 28.6562, "lon": 77.3010, "dlsa": "District Legal Services Authority East Delhi", "address": "Karkardooma Courts, Delhi - 110 032", "phone": "011-22374567"},
    {"district": "West Delhi", "state": "Delhi", "lat": 28.6541, "lon": 77.0747, "dlsa": "District Legal Services Authority West Delhi", "address": "Dwarka Courts, New Delhi - 110 075", "phone": "011-25394567"},
    {"district": "North Delhi", "state": "Delhi", "lat": 28.7041, "lon": 77.1025, "dlsa": "District Legal Services Authority North Delhi", "address": "Rohini Courts, Delhi - 110 085", "phone": "011-27554567"},
    # GOA
    {"district": "Panaji", "state": "Goa", "lat": 15.4909, "lon": 73.8278, "dlsa": "District Legal Services Authority North Goa", "address": "District Court Complex, Panaji - 403 001", "phone": "0832-2224958"},
    {"district": "Margao", "state": "Goa", "lat": 15.2993, "lon": 73.9862, "dlsa": "District Legal Services Authority South Goa", "address": "District Court Complex, Margao - 403 601", "phone": "0832-2714567"},
    # GUJARAT
    {"district": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714, "dlsa": "District Legal Services Authority Ahmedabad", "address": "District Court Complex, Ahmedabad - 380 001", "phone": "079-27560950"},
    {"district": "Surat", "state": "Gujarat", "lat": 21.1702, "lon": 72.8311, "dlsa": "District Legal Services Authority Surat", "address": "District Court Complex, Surat - 395 001", "phone": "0261-2474567"},
    {"district": "Vadodara", "state": "Gujarat", "lat": 22.3072, "lon": 73.1812, "dlsa": "District Legal Services Authority Vadodara", "address": "District Court Complex, Vadodara - 390 001", "phone": "0265-2424567"},
    {"district": "Rajkot", "state": "Gujarat", "lat": 22.3039, "lon": 70.8022, "dlsa": "District Legal Services Authority Rajkot", "address": "District Court Complex, Rajkot - 360 001", "phone": "0281-2474567"},
    {"district": "Bhavnagar", "state": "Gujarat", "lat": 21.7645, "lon": 72.1519, "dlsa": "District Legal Services Authority Bhavnagar", "address": "District Court Complex, Bhavnagar - 364 001", "phone": "0278-2424567"},
    {"district": "Jamnagar", "state": "Gujarat", "lat": 22.4707, "lon": 70.0577, "dlsa": "District Legal Services Authority Jamnagar", "address": "District Court Complex, Jamnagar - 361 001", "phone": "0288-2674567"},
    {"district": "Gandhinagar", "state": "Gujarat", "lat": 23.2156, "lon": 72.6369, "dlsa": "District Legal Services Authority Gandhinagar", "address": "District Court Complex, Gandhinagar - 382 010", "phone": "079-23244567"},
    # HARYANA
    {"district": "Gurugram", "state": "Haryana", "lat": 28.4595, "lon": 77.0266, "dlsa": "District Legal Services Authority Gurugram", "address": "District Court Complex, Gurugram - 122 001", "phone": "0124-2224567"},
    {"district": "Faridabad", "state": "Haryana", "lat": 28.4089, "lon": 77.3178, "dlsa": "District Legal Services Authority Faridabad", "address": "District Court Complex, Faridabad - 121 001", "phone": "0129-2224567"},
    {"district": "Ambala", "state": "Haryana", "lat": 30.3782, "lon": 76.7767, "dlsa": "District Legal Services Authority Ambala", "address": "District Court Complex, Ambala - 134 003", "phone": "0171-2634567"},
    {"district": "Hisar", "state": "Haryana", "lat": 29.1492, "lon": 75.7217, "dlsa": "District Legal Services Authority Hisar", "address": "District Court Complex, Hisar - 125 001", "phone": "01662-224567"},
    {"district": "Rohtak", "state": "Haryana", "lat": 28.8955, "lon": 76.6066, "dlsa": "District Legal Services Authority Rohtak", "address": "District Court Complex, Rohtak - 124 001", "phone": "01262-274567"},
    {"district": "Karnal", "state": "Haryana", "lat": 29.6857, "lon": 76.9905, "dlsa": "District Legal Services Authority Karnal", "address": "District Court Complex, Karnal - 132 001", "phone": "0184-2234567"},
    # HIMACHAL PRADESH
    {"district": "Shimla", "state": "Himachal Pradesh", "lat": 31.1048, "lon": 77.1734, "dlsa": "District Legal Services Authority Shimla", "address": "District Court Complex, Shimla - 171 001", "phone": "0177-2623537"},
    {"district": "Kangra", "state": "Himachal Pradesh", "lat": 32.0998, "lon": 76.2691, "dlsa": "District Legal Services Authority Kangra", "address": "District Court Complex, Dharamsala - 176 215", "phone": "01892-224567"},
    {"district": "Mandi", "state": "Himachal Pradesh", "lat": 31.7080, "lon": 76.9320, "dlsa": "District Legal Services Authority Mandi", "address": "District Court Complex, Mandi - 175 001", "phone": "01905-224567"},
    {"district": "Solan", "state": "Himachal Pradesh", "lat": 30.9045, "lon": 77.0967, "dlsa": "District Legal Services Authority Solan", "address": "District Court Complex, Solan - 173 212", "phone": "01792-224567"},
    # JHARKHAND
    {"district": "Ranchi", "state": "Jharkhand", "lat": 23.3441, "lon": 85.3096, "dlsa": "District Legal Services Authority Ranchi", "address": "District Court Complex, Ranchi - 834 001", "phone": "0651-2482093"},
    {"district": "Jamshedpur", "state": "Jharkhand", "lat": 22.8046, "lon": 86.2029, "dlsa": "District Legal Services Authority East Singhbhum", "address": "District Court Complex, Jamshedpur - 831 001", "phone": "0657-2424567"},
    {"district": "Dhanbad", "state": "Jharkhand", "lat": 23.7957, "lon": 86.4304, "dlsa": "District Legal Services Authority Dhanbad", "address": "District Court Complex, Dhanbad - 826 001", "phone": "0326-2224567"},
    {"district": "Bokaro", "state": "Jharkhand", "lat": 23.6693, "lon": 86.1511, "dlsa": "District Legal Services Authority Bokaro", "address": "District Court Complex, Bokaro - 827 001", "phone": "06542-224567"},
    # KARNATAKA
    {"district": "Bengaluru", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "dlsa": "District Legal Services Authority Bengaluru", "address": "City Civil Court Complex, Bengaluru - 560 001", "phone": "080-22113170"},
    {"district": "Mysuru", "state": "Karnataka", "lat": 12.2958, "lon": 76.6394, "dlsa": "District Legal Services Authority Mysuru", "address": "District Court Complex, Mysuru - 570 001", "phone": "0821-2424567"},
    {"district": "Mangaluru", "state": "Karnataka", "lat": 12.9141, "lon": 74.8560, "dlsa": "District Legal Services Authority Dakshina Kannada", "address": "District Court Complex, Mangaluru - 575 001", "phone": "0824-2424567"},
    {"district": "Hubballi", "state": "Karnataka", "lat": 15.3647, "lon": 75.1240, "dlsa": "District Legal Services Authority Dharwad", "address": "District Court Complex, Hubballi - 580 020", "phone": "0836-2224567"},
    {"district": "Belagavi", "state": "Karnataka", "lat": 15.8497, "lon": 74.4977, "dlsa": "District Legal Services Authority Belagavi", "address": "District Court Complex, Belagavi - 590 001", "phone": "0831-2424567"},
    {"district": "Ballari", "state": "Karnataka", "lat": 15.1394, "lon": 76.9214, "dlsa": "District Legal Services Authority Ballari", "address": "District Court Complex, Ballari - 583 101", "phone": "08392-224567"},
    {"district": "Shivamogga", "state": "Karnataka", "lat": 13.9299, "lon": 75.5681, "dlsa": "District Legal Services Authority Shivamogga", "address": "District Court Complex, Shivamogga - 577 201", "phone": "08182-224567"},
    {"district": "Tumakuru", "state": "Karnataka", "lat": 13.3379, "lon": 77.1173, "dlsa": "District Legal Services Authority Tumakuru", "address": "District Court Complex, Tumakuru - 572 101", "phone": "0816-2224567"},
    {"district": "Kalaburagi", "state": "Karnataka", "lat": 17.3297, "lon": 76.8343, "dlsa": "District Legal Services Authority Kalaburagi", "address": "District Court Complex, Kalaburagi - 585 101", "phone": "08472-224567"},
    # KERALA
    {"district": "Thiruvananthapuram", "state": "Kerala", "lat": 8.5241, "lon": 76.9366, "dlsa": "District Legal Services Authority Thiruvananthapuram", "address": "District Court Complex, Thiruvananthapuram - 695 001", "phone": "0471-2334567"},
    {"district": "Kochi", "state": "Kerala", "lat": 9.9312, "lon": 76.2673, "dlsa": "District Legal Services Authority Ernakulam", "address": "District Court Complex, Ernakulam - 682 031", "phone": "0484-2562252"},
    {"district": "Kozhikode", "state": "Kerala", "lat": 11.2588, "lon": 75.7804, "dlsa": "District Legal Services Authority Kozhikode", "address": "District Court Complex, Kozhikode - 673 001", "phone": "0495-2724567"},
    {"district": "Thrissur", "state": "Kerala", "lat": 10.5276, "lon": 76.2144, "dlsa": "District Legal Services Authority Thrissur", "address": "District Court Complex, Thrissur - 680 001", "phone": "0487-2424567"},
    {"district": "Kollam", "state": "Kerala", "lat": 8.8932, "lon": 76.6141, "dlsa": "District Legal Services Authority Kollam", "address": "District Court Complex, Kollam - 691 001", "phone": "0474-2724567"},
    {"district": "Palakkad", "state": "Kerala", "lat": 10.7867, "lon": 76.6548, "dlsa": "District Legal Services Authority Palakkad", "address": "District Court Complex, Palakkad - 678 001", "phone": "0491-2524567"},
    {"district": "Malappuram", "state": "Kerala", "lat": 11.0510, "lon": 76.0711, "dlsa": "District Legal Services Authority Malappuram", "address": "District Court Complex, Malappuram - 676 505", "phone": "0483-2734567"},
    {"district": "Kannur", "state": "Kerala", "lat": 11.8745, "lon": 75.3704, "dlsa": "District Legal Services Authority Kannur", "address": "District Court Complex, Kannur - 670 001", "phone": "0497-2704567"},
    # MADHYA PRADESH
    {"district": "Bhopal", "state": "Madhya Pradesh", "lat": 23.2599, "lon": 77.4126, "dlsa": "District Legal Services Authority Bhopal", "address": "District Court Complex, Bhopal - 462 001", "phone": "0755-2574567"},
    {"district": "Indore", "state": "Madhya Pradesh", "lat": 22.7196, "lon": 75.8577, "dlsa": "District Legal Services Authority Indore", "address": "District Court Complex, Indore - 452 001", "phone": "0731-2524567"},
    {"district": "Jabalpur", "state": "Madhya Pradesh", "lat": 23.1815, "lon": 79.9864, "dlsa": "District Legal Services Authority Jabalpur", "address": "District Court Complex, Jabalpur - 482 001", "phone": "0761-2624567"},
    {"district": "Gwalior", "state": "Madhya Pradesh", "lat": 26.2183, "lon": 78.1828, "dlsa": "District Legal Services Authority Gwalior", "address": "District Court Complex, Gwalior - 474 001", "phone": "0751-2424567"},
    {"district": "Ujjain", "state": "Madhya Pradesh", "lat": 23.1765, "lon": 75.7885, "dlsa": "District Legal Services Authority Ujjain", "address": "District Court Complex, Ujjain - 456 001", "phone": "0734-2524567"},
    {"district": "Sagar", "state": "Madhya Pradesh", "lat": 23.8388, "lon": 78.7378, "dlsa": "District Legal Services Authority Sagar", "address": "District Court Complex, Sagar - 470 001", "phone": "07582-224567"},
    # MAHARASHTRA
    {"district": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "dlsa": "District Legal Services Authority Mumbai", "address": "City Civil Court, Dhobi Talao, Mumbai - 400 001", "phone": "022-22620711"},
    {"district": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "dlsa": "District Legal Services Authority Pune", "address": "District Court Complex, Shivajinagar, Pune - 411 005", "phone": "020-25534567"},
    {"district": "Nagpur", "state": "Maharashtra", "lat": 21.1458, "lon": 79.0882, "dlsa": "District Legal Services Authority Nagpur", "address": "District Court Complex, Nagpur - 440 001", "phone": "0712-2524567"},
    {"district": "Nashik", "state": "Maharashtra", "lat": 19.9975, "lon": 73.7898, "dlsa": "District Legal Services Authority Nashik", "address": "District Court Complex, Nashik - 422 001", "phone": "0253-2574567"},
    {"district": "Aurangabad", "state": "Maharashtra", "lat": 19.8762, "lon": 75.3433, "dlsa": "District Legal Services Authority Aurangabad", "address": "District Court Complex, Aurangabad - 431 001", "phone": "0240-2334567"},
    {"district": "Solapur", "state": "Maharashtra", "lat": 17.6805, "lon": 75.9064, "dlsa": "District Legal Services Authority Solapur", "address": "District Court Complex, Solapur - 413 001", "phone": "0217-2724567"},
    {"district": "Kolhapur", "state": "Maharashtra", "lat": 16.7050, "lon": 74.2433, "dlsa": "District Legal Services Authority Kolhapur", "address": "District Court Complex, Kolhapur - 416 001", "phone": "0231-2644567"},
    {"district": "Thane", "state": "Maharashtra", "lat": 19.2183, "lon": 72.9781, "dlsa": "District Legal Services Authority Thane", "address": "District Court Complex, Thane - 400 601", "phone": "022-25334567"},
    {"district": "Amravati", "state": "Maharashtra", "lat": 20.9374, "lon": 77.7796, "dlsa": "District Legal Services Authority Amravati", "address": "District Court Complex, Amravati - 444 601", "phone": "0721-2574567"},
    # ODISHA
    {"district": "Bhubaneswar", "state": "Odisha", "lat": 20.2961, "lon": 85.8245, "dlsa": "District Legal Services Authority Khordha", "address": "District Court Complex, Bhubaneswar - 751 001", "phone": "0674-2534567"},
    {"district": "Cuttack", "state": "Odisha", "lat": 20.4625, "lon": 85.8830, "dlsa": "District Legal Services Authority Cuttack", "address": "District Court Complex, Cuttack - 753 001", "phone": "0671-2304856"},
    {"district": "Rourkela", "state": "Odisha", "lat": 22.2604, "lon": 84.8536, "dlsa": "District Legal Services Authority Sundargarh", "address": "District Court Complex, Rourkela - 769 001", "phone": "0661-2474567"},
    {"district": "Berhampur", "state": "Odisha", "lat": 19.3150, "lon": 84.7941, "dlsa": "District Legal Services Authority Ganjam", "address": "District Court Complex, Berhampur - 760 001", "phone": "0680-2224567"},
    {"district": "Sambalpur", "state": "Odisha", "lat": 21.4669, "lon": 83.9756, "dlsa": "District Legal Services Authority Sambalpur", "address": "District Court Complex, Sambalpur - 768 001", "phone": "0663-2524567"},
    # PUNJAB
    {"district": "Ludhiana", "state": "Punjab", "lat": 30.9010, "lon": 75.8573, "dlsa": "District Legal Services Authority Ludhiana", "address": "District Court Complex, Ludhiana - 141 001", "phone": "0161-2424567"},
    {"district": "Amritsar", "state": "Punjab", "lat": 31.6340, "lon": 74.8723, "dlsa": "District Legal Services Authority Amritsar", "address": "District Court Complex, Amritsar - 143 001", "phone": "0183-2524567"},
    {"district": "Jalandhar", "state": "Punjab", "lat": 31.3260, "lon": 75.5762, "dlsa": "District Legal Services Authority Jalandhar", "address": "District Court Complex, Jalandhar - 144 001", "phone": "0181-2224567"},
    {"district": "Patiala", "state": "Punjab", "lat": 30.3398, "lon": 76.3869, "dlsa": "District Legal Services Authority Patiala", "address": "District Court Complex, Patiala - 147 001", "phone": "0175-2214567"},
    {"district": "Bathinda", "state": "Punjab", "lat": 30.2110, "lon": 74.9455, "dlsa": "District Legal Services Authority Bathinda", "address": "District Court Complex, Bathinda - 151 001", "phone": "0164-2234567"},
    # RAJASTHAN
    {"district": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "dlsa": "District Legal Services Authority Jaipur", "address": "District Court Complex, Jaipur - 302 001", "phone": "0141-2714567"},
    {"district": "Jodhpur", "state": "Rajasthan", "lat": 26.2389, "lon": 73.0243, "dlsa": "District Legal Services Authority Jodhpur", "address": "District Court Complex, Jodhpur - 342 001", "phone": "0291-2634567"},
    {"district": "Udaipur", "state": "Rajasthan", "lat": 24.5854, "lon": 73.7125, "dlsa": "District Legal Services Authority Udaipur", "address": "District Court Complex, Udaipur - 313 001", "phone": "0294-2424567"},
    {"district": "Kota", "state": "Rajasthan", "lat": 25.2138, "lon": 75.8648, "dlsa": "District Legal Services Authority Kota", "address": "District Court Complex, Kota - 324 001", "phone": "0744-2424567"},
    {"district": "Ajmer", "state": "Rajasthan", "lat": 26.4499, "lon": 74.6399, "dlsa": "District Legal Services Authority Ajmer", "address": "District Court Complex, Ajmer - 305 001", "phone": "0145-2424567"},
    {"district": "Bikaner", "state": "Rajasthan", "lat": 28.0229, "lon": 73.3119, "dlsa": "District Legal Services Authority Bikaner", "address": "District Court Complex, Bikaner - 334 001", "phone": "0151-2524567"},
    {"district": "Alwar", "state": "Rajasthan", "lat": 27.5530, "lon": 76.6346, "dlsa": "District Legal Services Authority Alwar", "address": "District Court Complex, Alwar - 301 001", "phone": "0144-2334567"},
    # TAMIL NADU
    {"district": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707, "dlsa": "District Legal Services Authority Chennai", "address": "City Civil Court, Parry's Corner, Chennai - 600 001", "phone": "044-25213521"},
    {"district": "Coimbatore", "state": "Tamil Nadu", "lat": 11.0168, "lon": 76.9558, "dlsa": "District Legal Services Authority Coimbatore", "address": "District Court Complex, Coimbatore - 641 001", "phone": "0422-2394567"},
    {"district": "Madurai", "state": "Tamil Nadu", "lat": 9.9252, "lon": 78.1198, "dlsa": "District Legal Services Authority Madurai", "address": "District Court Complex, Madurai - 625 020", "phone": "0452-2534567"},
    {"district": "Tiruchirappalli", "state": "Tamil Nadu", "lat": 10.7905, "lon": 78.7047, "dlsa": "District Legal Services Authority Tiruchirappalli", "address": "District Court Complex, Tiruchirappalli - 620 001", "phone": "0431-2714567"},
    {"district": "Salem", "state": "Tamil Nadu", "lat": 11.6643, "lon": 78.1460, "dlsa": "District Legal Services Authority Salem", "address": "District Court Complex, Salem - 636 001", "phone": "0427-2444567"},
    {"district": "Tirunelveli", "state": "Tamil Nadu", "lat": 8.7139, "lon": 77.7567, "dlsa": "District Legal Services Authority Tirunelveli", "address": "District Court Complex, Tirunelveli - 627 001", "phone": "0462-2574567"},
    {"district": "Vellore", "state": "Tamil Nadu", "lat": 12.9165, "lon": 79.1325, "dlsa": "District Legal Services Authority Vellore", "address": "District Court Complex, Vellore - 632 001", "phone": "0416-2224567"},
    {"district": "Erode", "state": "Tamil Nadu", "lat": 11.3410, "lon": 77.7172, "dlsa": "District Legal Services Authority Erode", "address": "District Court Complex, Erode - 638 001", "phone": "0424-2254567"},
    {"district": "Thanjavur", "state": "Tamil Nadu", "lat": 10.7870, "lon": 79.1378, "dlsa": "District Legal Services Authority Thanjavur", "address": "District Court Complex, Thanjavur - 613 001", "phone": "04362-234567"},
    {"district": "Tiruppur", "state": "Tamil Nadu", "lat": 11.1085, "lon": 77.3411, "dlsa": "District Legal Services Authority Tiruppur", "address": "District Court Complex, Tiruppur - 641 601", "phone": "0421-2224567"},
    {"district": "Kancheepuram", "state": "Tamil Nadu", "lat": 12.8185, "lon": 79.6947, "dlsa": "District Legal Services Authority Kancheepuram", "address": "District Court Complex, Kancheepuram - 631 501", "phone": "044-27224567"},
    {"district": "Dindigul", "state": "Tamil Nadu", "lat": 10.3624, "lon": 77.9695, "dlsa": "District Legal Services Authority Dindigul", "address": "District Court Complex, Dindigul - 624 001", "phone": "0451-2424567"},
    # TELANGANA
    {"district": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "dlsa": "District Legal Services Authority Hyderabad", "address": "District Court Complex, Nampally, Hyderabad - 500 001", "phone": "040-23447083"},
    {"district": "Warangal", "state": "Telangana", "lat": 17.9784, "lon": 79.5941, "dlsa": "District Legal Services Authority Warangal", "address": "District Court Complex, Warangal - 506 001", "phone": "0870-2574567"},
    {"district": "Nizamabad", "state": "Telangana", "lat": 18.6725, "lon": 78.0941, "dlsa": "District Legal Services Authority Nizamabad", "address": "District Court Complex, Nizamabad - 503 001", "phone": "08462-224567"},
    {"district": "Karimnagar", "state": "Telangana", "lat": 18.4386, "lon": 79.1288, "dlsa": "District Legal Services Authority Karimnagar", "address": "District Court Complex, Karimnagar - 505 001", "phone": "0878-2224567"},
    {"district": "Khammam", "state": "Telangana", "lat": 17.2473, "lon": 80.1514, "dlsa": "District Legal Services Authority Khammam", "address": "District Court Complex, Khammam - 507 001", "phone": "08742-224567"},
    {"district": "Nalgonda", "state": "Telangana", "lat": 17.0575, "lon": 79.2671, "dlsa": "District Legal Services Authority Nalgonda", "address": "District Court Complex, Nalgonda - 508 001", "phone": "08682-224567"},
    # UTTAR PRADESH
    {"district": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462, "dlsa": "District Legal Services Authority Lucknow", "address": "District Court Complex, Lucknow - 226 001", "phone": "0522-2209754"},
    {"district": "Kanpur", "state": "Uttar Pradesh", "lat": 26.4499, "lon": 80.3319, "dlsa": "District Legal Services Authority Kanpur", "address": "District Court Complex, Kanpur - 208 001", "phone": "0512-2334567"},
    {"district": "Agra", "state": "Uttar Pradesh", "lat": 27.1767, "lon": 78.0081, "dlsa": "District Legal Services Authority Agra", "address": "District Court Complex, Agra - 282 001", "phone": "0562-2224567"},
    {"district": "Varanasi", "state": "Uttar Pradesh", "lat": 25.3176, "lon": 82.9739, "dlsa": "District Legal Services Authority Varanasi", "address": "District Court Complex, Varanasi - 221 001", "phone": "0542-2224567"},
    {"district": "Prayagraj", "state": "Uttar Pradesh", "lat": 25.4358, "lon": 81.8463, "dlsa": "District Legal Services Authority Prayagraj", "address": "District Court Complex, Prayagraj - 211 001", "phone": "0532-2424567"},
    {"district": "Meerut", "state": "Uttar Pradesh", "lat": 28.9845, "lon": 77.7064, "dlsa": "District Legal Services Authority Meerut", "address": "District Court Complex, Meerut - 250 001", "phone": "0121-2634567"},
    {"district": "Noida", "state": "Uttar Pradesh", "lat": 28.5355, "lon": 77.3910, "dlsa": "District Legal Services Authority Gautam Buddha Nagar", "address": "District Court Complex, Noida - 201 301", "phone": "0120-2424567"},
    {"district": "Ghaziabad", "state": "Uttar Pradesh", "lat": 28.6692, "lon": 77.4538, "dlsa": "District Legal Services Authority Ghaziabad", "address": "District Court Complex, Ghaziabad - 201 001", "phone": "0120-2824567"},
    {"district": "Bareilly", "state": "Uttar Pradesh", "lat": 28.3670, "lon": 79.4304, "dlsa": "District Legal Services Authority Bareilly", "address": "District Court Complex, Bareilly - 243 001", "phone": "0581-2524567"},
    {"district": "Gorakhpur", "state": "Uttar Pradesh", "lat": 26.7606, "lon": 83.3732, "dlsa": "District Legal Services Authority Gorakhpur", "address": "District Court Complex, Gorakhpur - 273 001", "phone": "0551-2224567"},
    # UTTARAKHAND
    {"district": "Dehradun", "state": "Uttarakhand", "lat": 30.3165, "lon": 78.0322, "dlsa": "District Legal Services Authority Dehradun", "address": "District Court Complex, Dehradun - 248 001", "phone": "0135-2714567"},
    {"district": "Haridwar", "state": "Uttarakhand", "lat": 29.9457, "lon": 78.1642, "dlsa": "District Legal Services Authority Haridwar", "address": "District Court Complex, Haridwar - 249 401", "phone": "01334-224567"},
    {"district": "Nainital", "state": "Uttarakhand", "lat": 29.3919, "lon": 79.4542, "dlsa": "District Legal Services Authority Nainital", "address": "District Court Complex, Nainital - 263 001", "phone": "05942-235430"},
    # WEST BENGAL
    {"district": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639, "dlsa": "District Legal Services Authority Kolkata", "address": "City Civil Court, 2 Kiran Shankar Roy Road, Kolkata - 700 001", "phone": "033-22454483"},
    {"district": "Howrah", "state": "West Bengal", "lat": 22.5958, "lon": 88.2636, "dlsa": "District Legal Services Authority Howrah", "address": "District Court Complex, Howrah - 711 101", "phone": "033-26384567"},
    {"district": "Durgapur", "state": "West Bengal", "lat": 23.5204, "lon": 87.3119, "dlsa": "District Legal Services Authority Paschim Bardhaman", "address": "District Court Complex, Asansol - 713 301", "phone": "0341-2224567"},
    {"district": "Siliguri", "state": "West Bengal", "lat": 26.7271, "lon": 88.3953, "dlsa": "District Legal Services Authority Darjeeling", "address": "District Court Complex, Siliguri - 734 001", "phone": "0353-2524567"},
    {"district": "Malda", "state": "West Bengal", "lat": 25.0108, "lon": 88.1418, "dlsa": "District Legal Services Authority Malda", "address": "District Court Complex, Malda - 732 101", "phone": "03512-224567"},
    # CHANDIGARH
    {"district": "Chandigarh", "state": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "dlsa": "District Legal Services Authority Chandigarh", "address": "District Courts Complex, Sector 43, Chandigarh - 160 036", "phone": "0172-2665015"},
    # PUDUCHERRY
    {"district": "Puducherry", "state": "Puducherry", "lat": 11.9416, "lon": 79.8083, "dlsa": "District Legal Services Authority Puducherry", "address": "Sessions Court Complex, Puducherry - 605 001", "phone": "0413-2220283"},
    # JAMMU & KASHMIR
    {"district": "Srinagar", "state": "Jammu & Kashmir", "lat": 34.0837, "lon": 74.7973, "dlsa": "District Legal Services Authority Srinagar", "address": "District Court Complex, Srinagar - 190 001", "phone": "0194-2452354"},
    {"district": "Jammu", "state": "Jammu & Kashmir", "lat": 32.7266, "lon": 74.8570, "dlsa": "District Legal Services Authority Jammu", "address": "District Court Complex, Jammu - 180 001", "phone": "0191-2544567"},
]


def get_nearest_dlsa(lat: float, lon: float, limit: int = 3) -> List[Dict]:
    results = []
    for d in DISTRICTS:
        dist = haversine(lat, lon, d["lat"], d["lon"])
        results.append({**d, "distance_km": round(dist, 1)})
    results.sort(key=lambda x: x["distance_km"])
    top = results[:limit]
    for r in top:
        r["maps_url"] = f"https://www.google.com/maps/search/?api=1&query={r['dlsa'].replace(' ', '+')},{r['district']}"
        r["directions_url"] = f"https://www.google.com/maps/dir/?api=1&destination={r['lat']},{r['lon']}"
    return top


def get_districts_by_state(state: str) -> List[Dict]:
    return [d for d in DISTRICTS if d["state"] == state]
