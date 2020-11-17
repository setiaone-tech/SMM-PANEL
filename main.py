import requests
import json
from prettytable import PrettyTable
from bs4 import BeautifulSoup as BS
from data import akun
ses = requests.session()

cekauth = {
        'username':akun[0],
        'password':akun[1],
        'tombol':''
       }
cek = ses.post("https://borneopanel.com/auth/masuk/",data=cekauth)
if "Terjadi kesalahan" in cek.text:
    exit("Password/Username salah")
auth2 = {
    'status':'On',
    'ip':'',
    'generate':'on',
    'tombol':''
    }
generateapi = ses.post("https://borneopanel.com/pengaturan-api/", data=auth2)
API = (BS(generateapi.text, "html.parser").findAll("input")[1]['value'])
auth3 = {
    "api_key" : API
}
cekapi = ses.post("https://borneopanel.com/api/v2/profile/", data = auth3)
pesan = cekapi.json()['message']
spl = pesan.split(":")
ip = spl[1]
auth4 = {
    'status':'On',
    'ip':ip,
    'tombol':''
    }
simpansesi = ses.post("https://borneopanel.com/pengaturan-api/", data=auth4)
url = "https://borneopanel.com/api/v2/"
auth = {
            "api_key" : API
        }
while True:
    print("[---------------------------------]")
    print("[===========BORNEO PANEL==========]")
    print("[---------------------------------]")
    print()
    print("1. Cek Status Akun")
    print("2. Daftar Layanan")
    print("3. Pemesanan")
    print("4. Riwayat Saldo")
    print("99. Keluar")
    pilihan = int(input("Masukan Pilihan(1/2/3/99)? "))

    if pilihan == 1:
        print("[---------------------------------]")
        print("[=====Login Akun Borneo Panel=====]")
        print("[---------------------------------]")
        print()
        profil = url+"profile/"
        login = ses.post(profil, data = auth)
        res = login.json()
        print()
        username = res['response']['username']
        saldo = res['response']['balance']
        status = res['response']['status']
        print("USERNAME : "+username)
        print("SALDO : "+saldo)
        print("STATUS : "+status)
        print()
        menu = input("Ingin kembali Ke Menu(ya/tidak)? ")
        if menu == "tidak" or menu == "t":
            break
    if pilihan == 2:
        service = url+"service/"
        login = ses.post(service, data = auth)
        res = login.json()
        x = PrettyTable()
        x.field_names = ["ID","Service","Price","Min. Pemeblian"]
        for i in res["response"]:
            x.add_row([i["id"],i["service"],i["price"],i["min"]])
        print(x)
        print()
        menu = input("Ingin kembali Ke Menu(ya/tidak)? ")
        if menu == "tidak" or menu == "t":
            break
    if pilihan == 3:
        print("[---------------------------------]")
        print("[=============Pemesanan===========]")
        print("[---------------------------------]")
        print()
        print("+------------------------------------------------------------------------------------------------+")
        print("| note : + Sebelum melakukan pembelian, harap cek halaman 2 karena terdapat data yang diperlukan |")
        print("|        + Harap ingat id service sebelum melakukan pembelian                                    |")
        print("|        + Harap perhitungkan antara sisa saldo dengan jumlah pembelian                          |")
        print("|        + Karena setiap service memiliki minimal pembelian yang berbeda-beda                    |")
        print("|        + Untuk pembelian followers instagram gunakan username tanpa tanda @                    |")
        print("|        + Selain pembelian tersebut, gunakan link target                                        |")
        print("+------------------------------------------------------------------------------------------------+")
        service = input("Masukan ID service(bisa cek di halaman 2) : ")
        target = input("Masukan target(username/link) : ")
        jumlah = input("Masukan banyak jumlah : ")
        print()
        url = "https://borneopanel.com/api/v2/"
        pesan = url+"buy/"
        authbuy = {
            "api_key" : API,
            "service" : service,
            "target" : target,
            "quantity" : jumlah
        }
        beli = ses.post(pesan, data = authbuy)
        res = beli.json()
        mess = res['message']
        if res['result'] == 'success':
            print(mess)
            menu = input("Ingin kembali Ke Menu(ya/tidak)? ")
            if menu == "tidak" or menu == "t":
                break
        else:
            if mess == "Service not found":
                print("X- Gagal melakukan pembelian karena ID service tidak ditemukan -X")
                print()
                menu = input("Ingin kembali Ke Menu(ya/tidak)? ")
                if menu == "tidak" or menu == "t":
                    break
            elif mess == "Insufficient balance":
                print("$- Gagal melakukan pembelian karena saldo tidak cukup -$")
                menu = input("Ingin kembali Ke Menu(ya/tidak)? ")
                if menu == "tidak" or menu == "t":
                    break
    if pilihan == 4:
        masuk = ses.post("https://borneopanel.com/auth/masuk/",data=cekauth)
        if "Terjadi kesalahan" in masuk.text:
            exit("Password/Username salah")
        else:
            table = PrettyTable()
            label = []
            get = ses.get("https://borneopanel.com/riwayat/saldo/")
            tr = (BS(get.text, "html.parser").findAll("tr"))
            for i in tr[0].findAll("th"):
                label.append(i.text)
            table.field_names = label
            tr.pop(0)
            for i in tr:
                isian = []
                for isi in i.findAll("td"):
                    isian.append(isi.text)
                table.add_row(isian)
            print (table)
            print()
            menu = input("Ingin kembali Ke Menu(ya/tidak)? ")
            if menu == "tidak" or menu == "t":
                break
    if pilihan == 99:
        exit("Terima Kasih Sudah Menggunakan Tool Ini:)")

        
        