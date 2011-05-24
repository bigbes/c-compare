CC=gcc
PYTHON=/usr/bin/env python3
CFLAGS=-Wall -std=c99

all: 
	$(CC) $(CFLAGS) main_dt.c -o main_dt.out
	$(CC) $(CFLAGS) main1_1.c -o main1_1.out
	$(CC) $(CFLAGS) main1_2.c -o main1_2.out
	$(CC) $(CFLAGS) main1_3.c -o main1_3.out
	$(CC) $(CFLAGS) main2_1.c -o main2_1.out
	$(CC) $(CFLAGS) main2_2.c -o main2_2.out
	$(CC) $(CFLAGS) main2_3.c -o main2_3.out

python:
	$(PYTHON) ../main.py -f main1_1.c -s main2_1.c -o main1.o
	$(PYTHON) ../main.py -f main1_2.c -s main2_2.c -o main2.o
	$(PYTHON) ../main.py -f main1_3.c -s main2_3.c -o main3.o
	$(PYTHON) ../main.py --dt -f main_dt.c -o main_dt.o
clean:
	rm -rf *.out

default: all
