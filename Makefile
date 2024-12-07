CROSS_COMPILE ?=
CC      = $(CROSS_COMPILE)gcc
CFLAGS  = -Wall -g -pthread
LDFLAGS   = -pthread 
LOADLIBES = -lrt -lm

EXERCISES=		\
daemon			\

.PHONY: all
all : ${EXERCISES}

.PHONY: clean
clean : 
	@rm -f core *.o *.out *.bb *.bbg *.gcov *.da *~
	@rm -f ${EXERCISES}

CXX = g++
CXXFLAGS = -std=c++11 -pthread

all: daemon

daemon: deamon.cpp
	$(CXX) $(CXXFLAGS) -o daemon deamon.cpp

clean:
	rm -f daemon

