import subprocess
import time
import chardet

def clearstd(std, num):
	for _ in range(num):
		std.readline()

def readstd(process):
	process.stdin.write(b'test\n')
	on = True
	data = []
	while on:
		r = process.stdout.readline()
		print(r)
		if r != b'\r\n':
			data.append(r)
		else:
			on = False
	return data

def listdisk(stdin, stdout):
	stdin.write(b"LIST DISK\n")
	stdin.flush()
	time.sleep(0.5)
	on=True
	data=[]
	clearstd(stdout, 3)
	while on:
		line = stdout.readline()
		if line != b'\r\n':
			data.append(line.decode('utf-8').split(' '))
		else:
			on=False
	processed = []
	for i in data:
		for _ in range(i.count('')):
			i.remove('')
		processed.append([i[1], f"{i[4]}{i[5]}"])
	return processed

def rempart(stdin, stdout, disk):
	stdin.write(f"SELECT DISK {disk}\n".encode('utf-8'))
	stdin.flush()

	stdin.write(b"LIST PART\n")
	stdin.flush()

	time.sleep(0.5)
	on=True
	data=0
	clearstd(stdout, 6)
	while on:
		line = stdout.readline()
		if line != b'\r\n':
			data += 1
		else:
			on=False

	for i in range(data):
		stdin.write(f"SELECT PART {i+1}\n".encode('utf-8'))
		stdin.flush()
		stdin.write(b"DEL PART OVERRIDE\n")
		stdin.flush()

	stdin.write(b"CREATE PART PRIM\n")
	stdin.flush()


def main(stdin, stdout):
	disklist = listdisk(p.stdin, p.stdout)
	for i in disklist:
		print(f"Disk {i[0]}: {i[1]}")
	choosen = int(input('Choose the disk to clear!\n -> '))
	time.sleep(0.5)
	rempart(stdin, stdout, choosen)



p = subprocess.Popen(['diskpart'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
clearstd(p.stdout, 6)
time.sleep(0.5)
main(p.stdin, p.stdout)


