######################## IMPORTANT ########################
""" Do not rename the variables or functions.
Do not change the function parameters.
Do not add input() calls inside airport_manager.py.
The file must be importable by the tests. """
###########################################################


airport_info = None
allowed_gates = None
restricted_destinations = None
flights = None


## Logic to find if a flight exists
def find_flight(flights, flight_number):
    pass


## Logic to find if a passenger exists
def passenger_exists(passengers, passenger_name):
    pass


## Logic to check in a passenger
def check_in_passenger(
    flights,
    flight_number,
    passenger_name,
    restricted_destinations
):
    pass


## Logic to remove a passenger from a flight
def remove_passenger(
    flights,
    flight_number,
    passenger_name
):
    pass


# Logic to change the gate of a flight
def change_gate(
    flights,
    flight_number,
    new_gate,
    allowed_gates
):
    pass


# Logic to get the status of a flight
def flight_status(flight):
    pass



# Logic to get the sorted manifest of a flight
def sorted_manifest(
    flights,
    flight_number
):
    pass


# Logic to get the total number of passengers across all flights
def total_passengers(flights):
    pass


# Logic to check if any flight is full
def any_full_flight(flights):
    pass



# Logic to check if all flights have at least one passenger
def all_flights_have_passengers(flights):
    pass
######################## IMPORTANT ########################
""" Do not rename the variables or functions.
Do not change the function parameters.
Do not add input() calls inside airport_manager.py.
The file must be importable by the tests. """
###########################################################
# 模块顶层全局变量初始化
airport_info = ("OUL", "1", "14-09-2026")   # tuple
allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}  # set
restricted_destinations = {"Moscow", "Pyongyang"}  # set
flights = dict()  # 空字典


## Logic to find if a flight exists
def find_flight(flights, flight_number):
    if not isinstance(flights, dict):
        return None
    norm_flight = flight_number.strip().upper()
    for key in flights.keys():
        if key.upper() == norm_flight:
            return key
    return None


## Logic to find if a passenger exists
def passenger_exists(passengers, passenger_name):
    """passengers: 乘客原始名称可迭代对象；大小写不敏感，忽略首尾空格"""
    target = passenger_name.strip().lower()
    for p in passengers:
        if p.strip().lower() == target:
            return True
    return False


## Logic to check in a passenger
def check_in_passenger(
    flights,
    flight_number,
    passenger_name,
    restricted_destinations
):
    # 1. 检查航班是否存在
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    flight = flights[flight_key]
    name_stripped = passenger_name.strip()

    # 2. 空名字：去除空白后为空就拒绝
    if len(name_stripped) == 0:
        return "EMPTY_NAME"

    # 3. 检查目的地是否受限
    dest = flight.get("destination", "").strip()
    restricted_set = set(restricted_destinations)
    if dest in restricted_set:
        return "RESTRICTED"

    # 4. 检查重复乘客（大小写不敏感，忽略首尾空格）
    passenger_list = flight.get("passengers", [])
    if passenger_exists(passenger_list, passenger_name):
        return "DUPLICATE"

    # 5. 检查航班是否已满
    capacity = flight.get("capacity", 0)
    current_count = len(passenger_list)
    if current_count >= capacity:
        return "FULL"

    # 修复：去除首尾空格 + title格式化存储
    name_formatted = name_stripped.title()
    flight["passengers"].append(name_formatted)
    return "OK"


## Logic to remove a passenger from a flight
def remove_passenger(
    flights,
    flight_number,
    passenger_name
):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    flight = flights[flight_key]
    passenger_list = flight.get("passengers", [])

    if not passenger_exists(passenger_list, passenger_name):
        return "PASSENGER_NOT_FOUND"

    # 找到大小写匹配的名字并删除
    for idx, p in enumerate(passenger_list):
        if p.strip().lower() == passenger_name.strip().lower():
            del passenger_list[idx]
            break
    return "OK"


# Logic to change the gate of a flight
def change_gate(
    flights,
    flight_number,
    new_gate,
    allowed_gates
):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    # 登机口标准化大写：用于比对+存储
    new_gate_norm = new_gate.strip().upper()
    allowed_normalized = {g.strip().upper() for g in allowed_gates}
    if new_gate_norm not in allowed_normalized:
        return "INVALID_GATE"

    # 存储标准化大写登机口
    flights[flight_key]["gate"] = new_gate_norm
    return "OK"


# Logic to get the status of a flight
def flight_status(flight):
    """
    老师测试规则：百分比75%阈值
    100% → FULL
    >=75% → ALMOST FULL
    else → AVAILABLE
    """
    passengers = flight.get("passengers", [])
    capacity = flight.get("capacity", 0)
    count = len(passengers)

    if capacity <= 0:
        return "AVAILABLE"

    percentage = (count / capacity) * 100
    if percentage >= 100:
        return "FULL"
    elif percentage >= 75:
        return "ALMOST FULL"
    else:
        return "AVAILABLE"


# Logic to get the sorted manifest of a flight
def sorted_manifest(
    flights,
    flight_number
):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return None
    passenger_list = flights[flight_key].get("passengers", [])
    # 返回排序后的拷贝，不修改原始数据
    return sorted(passenger_list)


# Logic to get the total number of passengers across all flights
def total_passengers(flights):
    total = 0
    for flight in flights.values():
        passengers = flight.get("passengers", [])
        total += len(passengers)
    return total


# Logic to check if any flight is full
def any_full_flight(flights):
    for flight in flights.values():
        if flight_status(flight) == "FULL":
            return True
    return False


# Logic to check if all flights have at least one passenger
def all_flights_have_passengers(flights):
    for flight in flights.values():
        passengers = flight.get("passengers", [])
        if len(passengers) == 0:
            return False
    return True


# ---------------- 样例初始化（仅用于本地自测！测试框架不会执行这部分） ----------------
if __name__ == "__main__":
    flights = {
        "AY450": {
            "destination": "Helsinki",
            "departure": "08:30",
            "gate": "A2",
            "capacity": 5,
            "passengers": ["Alice Wong", "David Kim", "Fatima Ali"]
        },
        "SK271": {
            "destination": "Stockholm",
            "departure": "10:15",
            "gate": "B1",
            "capacity": 4,
            "passengers": ["Chen Wei", "George Smith"]
        },
        "LH2491": {
            "destination": "Munich",
            "departure": "12:40",
            "gate": "A4",
            "capacity": 5,
            "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"]
        }
    }

    print("find_flight AY450:", find_flight(flights, "ay450"))
    print("passenger exists alice wong:", passenger_exists(flights["AY450"]["passengers"], "alice wong"))
    print("total passengers:", total_passengers(flights))
    print("any full flight:", any_full_flight(flights))
    print("all flights have passengers:", all_flights_have_passengers(flights))
    print("sorted manifest AY450:", sorted_manifest(flights, "AY450"))
