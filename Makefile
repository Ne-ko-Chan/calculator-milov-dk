CC:=gcc
CFLAGS:=-Wall -Wextra -Wpedantic
GTEST_DIR ?= googletest/googletest
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h $(GTEST_DIR)/include/gtest/internal/*.h

clean:
	rm -rf build/

run-int: build/main.exe
	build/main.exe

run-float: build/main.exe
	build/main.exe --float

run-unit-tests: build/unit-tests.exe
	build/unit-tests.exe

build/main.exe: build/main.o
	@$(CC) -o build/main.exe -c build/main.o

build/main.o: src/main.c
	@$(CC) $(CFLAGS) -o build/main.o src/main.c

# Google Test object files
build/gtest/gtest-all.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	g++ -isystem $(GTEST_DIR)/include -I$(GTEST_DIR) -c $(GTEST_DIR)/src/gtest-all.cc -o $@

build/gtest/gtest_main.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	g++ -isystem $(GTEST_DIR)/include -I$(GTEST_DIR) -c $(GTEST_DIR)/src/gtest_main.cc -o $@

# Google Test static libraries
build/gtest/gtest_main.a: build/gtest/gtest-all.o build/gtest/gtest_main.o
	ar rv $@ $^ -o $@
