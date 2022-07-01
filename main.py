import openpyxl
import json
import requests

inn = "87349639"
uit_list = open("testUitList.txt").readlines()
cert_date_list = open("testCertDate.txt").readlines()
cert_numb_list = open("testCertNumb.txt").readlines()
low_line = 1
high_line = 5000
step = 5000
total_lines = (len(uit_list))


def create_json_raw(low, high):
    json_raw_positions = ""
    for line in range(low, high):
        # print(line)
        if line < high - 1:
            json_raw_positions = json_raw_positions + """
            {"code": """ + "\"" + uit_list[line].replace("\n", "") + "\"," + """
            "permitDocDate": """ + "\"" + cert_date_list[line].replace("\n", "") + """",
            "permitDocNumb": """ + "\"" + cert_numb_list[line].replace("\n", "") + """",
            "permitDocType": "CERTIFICATE" },"""
        else:
            json_raw_positions = json_raw_positions + """
            {"code": """ + "\"" + uit_list[line].replace("\n", "") + """",
             "permitDocDate": """ + "\"" + cert_date_list[line].replace("\n", "") + """",
             "permitDocNumb": """ + "\"" + cert_numb_list[line].replace("\n", "") + """",
             "permitDocType": "CERTIFICATE" }"""

    json_raw_body = """
    {"participantInn": """ + "\"" + inn + """",
    "positions": [ """ + json_raw_positions + """ ] }
    """
    return json_raw_body


def send_request():
    request_header = {
        "X-Auth-Token": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0dzhJVmw1XzcxTGo1UnZ5dHdWdFEwLXZVX3lQdjZOZGl5OUtXOVczdzJnIn0.eyJleHAiOjE2NTY1MjMzMzMsImlhdCI6MTY1NjUxNjEzMywianRpIjoiOTA4ZDA4OWYtODQwZC00ZDg2LTgxODQtODhkOTU1OTU3NDQ1IiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LW1hcmtpbmctMDEua29ydXNjb25zdWx0aW5nLnJ1L2F1dGgvcmVhbG1zL21hcmtpbmciLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNThkNTJjMGItMDBkMy00ODcwLThlMDctNjkyZTIwOWYwYjVhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibWFya2luZyIsInNlc3Npb25fc3RhdGUiOiIzNGE3YTBlNC01NzZlLTQzNzMtOGQ0Ny1hNTM3ZTZiOTIxNjMiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vdWktbWFya2luZy0wMS5rb3J1c2NvbnN1bHRpbmcucnUiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6InRlc3RpbmdhZG1pbiJ9.T3tg72yl5zCbP83-HZY_P12g7mnxCNhPNGno5ZbGVJdJBZmqYmyRY0iXlaEWIAPRaDt7AAgkrXb7Ks4VjlaF_bisDpbpjJ7JDk7OH3jW9Hia9PINZHahVUCfOcVM5eQinFEBuwVs5ychhiQVbshFyDY5ByL1d3dFT-4wRFQkL7USdhAC-iCba7cWU1ApXE4QIb_PkudLoqZkXo52SDvbyxy8Si9BtGgOkOBtEFd1JzRU0QW7Pkr7Wp9mcRCR5U08BRIqxaOMdIPHNzHjDvtardw9ADSbqmn27BTCkf9zd6fhLm-vuJpbxohz-DU8kcHiDUlRV7ZaeW4t6puQSyxEOw",
        "Content-Type": "application/json"
    }
    response = requests.post("https://api-marking-01.korusconsulting.ru/marking/admin/pd_information_h/full",
                             headers=request_header,
                             data=json_raw)
    # print(response.request.body)
    # print(response.text)
    print(response.status_code)


while high_line < total_lines:
    print("Нижняя граница: " + str(low_line) + " верхняя граница: " + str(high_line))
    json_raw = create_json_raw(low_line, high_line)
    send_request()
    if high_line + step <= total_lines:
        low_line = high_line
        high_line += step
    else:
        low_line = high_line
        high_line = total_lines
        print("Нижняя граница: " + str(low_line) + " верхняя граница: " + str(high_line))
        json_raw = create_json_raw(low_line, high_line)
        send_request()
