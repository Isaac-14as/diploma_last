import asyncio
import random
from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp, Float, Integer


class ValueDevice(Table):
    full_power = Float()
    active_power = Float()
    reactive_power = Float()
    voltage = Float()
    amperage = Float()
    power_factor = Float()
    date_of_origin = Timestamp()
    device_id = Integer()

class AccidentLog(Table):
    info = Varchar()
    date_of_origin = Timestamp()
    device_id = Integer()



async def print_numbers():
    accident_count = [i * 10 for i in range(4)]
    while True:
        amperage = [round(random.uniform(5.2, 5.4), 1) for _ in range(4)]
        voltage = [random.randint(209, 231) * 1000 for _ in range(4)]
        power_factor = [round(random.uniform(0.8, 0.95), 2) for _ in range(4)]
  
        for i in range(4):
            accident_count[i] += 1
            if accident_count[i] > 60:
                voltage[i] = random.randint(195, 245) * 1000
            data = {
                'full_power': round(amperage[i] * voltage[i] / 10**6, 2),
                'active_power': round((amperage[i] * voltage[i] * power_factor[i]) / 10**6, 2),
                'reactive_power': round((amperage[i] * voltage[i] * (1 - (power_factor[i] ** 2)) ** (1/2)) / 10**6, 2),
                'voltage': voltage[i] // 1000,
                'amperage': amperage[i],
                'power_factor': power_factor[i],
                'device_id': i + 1
            }
            if voltage[i] // 1000 < 200:
                data_accident = {
                    'info': f"Зафиксировано напряжение меньше 200 кВ (S = {data['full_power']} МВА, P = {data['active_power']} МВт, Q = {data['reactive_power']} МВар, U = {data['voltage']} А, I = {data['amperage']} А, cos(φ) = {data['power_factor']})",
                    'device_id': i + 1
                }
                accident_count[i] = 0
                await AccidentLog(**data_accident).save()
            elif voltage[i] // 1000 > 240:
                data_accident = {
                    'info': f"Зафиксировано напряжение больше 240 кВ (S = {data['full_power']} МВА, P = {data['active_power']} МВт, Q = {data['reactive_power']} МВар, U = {data['voltage']} А, I = {data['amperage']} А, cos(φ) = {data['power_factor']})",
                    'device_id': i + 1
                }
                await AccidentLog(**data_accident).save()
                accident_count[i] = 0

            await ValueDevice(**data).save()
        await asyncio.sleep(3)

async def main():
    task = asyncio.create_task(print_numbers())
    await task

asyncio.run(main())