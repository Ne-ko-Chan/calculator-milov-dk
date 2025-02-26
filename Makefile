CC := gcc
CFLAGS := -Wall -Wextra -Wpedantic
GTEST_DIR ?= googletest/googletest
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h $(GTEST_DIR)/include/gtest/internal/*.h
VENV_DIR := venv
PYTEST = $(VENV_DIR)/bin/pytest

$(shell mkdir -p build/gtest)

.PHONY: all clean run-int run-float run-unit-tests run-integration-tests build/unit-tests

all: build/app.exe build/unit-tests

venv:
	@echo "Creating virtual environment"
	@python -m venv $(VENV_DIR)
	@source $(VENV_DIR)/bin/activate; pip install -U pytest

clean:
	@echo "Cleaning"
	@rm -rf build/
	@rm -rf $(VENV_DIR)
	@rm -rf tests/integration/__pycache__
	@rm -rf .pytest_cache

run-integration-tests: build/app.exe venv tests/integration/test_math.py
	@echo "Running integration tests..."
	@source $(VENV_DIR)/bin/activate; $(PYTEST) tests/integration/test_math.py

run-int: build/app.exe
	@echo "Running in integer mode"
	@build/app.exe

run-float: build/app.exe
	@echo "Running in float mode"
	@build/app.exe --float

run-unit-test: build/unit-tests
	@echo "Running unit-tests"
	@build/node_test.exe
	@build/stack_test.exe
	@build/queue_test.exe
	@build/precedence_test.exe
	@build/parse_test.exe
	@build/calculate_test.exe
	@build/cli_test.exe
	@build/print_test.exe

build/app.exe: src/main.c
	@echo "Building app.exe"
	@$(CC) $(CFLAGS) -o build/app.exe src/main.c

build/app-test.o: src/main.c
	@echo "Building app-test.o"
	@$(CC) $(CFLAGS) -DGTEST -c src/main.c -o build/app-test.o -g

build/unit-tests: build/precedence_test.exe build/stack_test.exe build/queue_test.exe build/parse_test.exe build/calculate_test.exe build/cli_test.exe build/node_test.exe build/print_test.exe

build/precedence_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/precedence_test.cpp
	@echo "Building precedence unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/precedence_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/precedence_test.exe

build/stack_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/stack_test.cpp
	@echo "Building stack unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/stack_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/stack_test.exe

build/node_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/node_test.cpp
	@echo "Building node unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/node_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/node_test.exe

build/cli_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/cli_test.cpp
	@echo "Building cli unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/cli_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/cli_test.exe

build/calculate_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/calculate_test.cpp
	@echo "Building calculate unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/calculate_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/calculate_test.exe

build/parse_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/parse_test.cpp
	@echo "Building parse unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/parse_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/parse_test.exe -g

build/queue_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/queue_test.cpp
	@echo "Building queue unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/queue_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/queue_test.exe

build/print_test.exe: build/gtest/gtest_main.a build/app-test.o tests/unit/print_test.cpp
	@echo "Building print unit-tests"
	@g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/print_test.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-fsanitize=address \
		-o build/print_test.exe


# Google Test object files
build/gtest/gtest-all.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	@echo "Building gtest libraries"
	@g++ -isystem $(GTEST_DIR)/include -I$(GTEST_DIR) -c $(GTEST_DIR)/src/gtest-all.cc -o $@

build/gtest/gtest_main.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	@echo "Building gtest libraries"
	@g++ -isystem $(GTEST_DIR)/include -I$(GTEST_DIR) -c $(GTEST_DIR)/src/gtest_main.cc -o $@

# Google Test static libraries
build/gtest/gtest_main.a: build/gtest/gtest-all.o build/gtest/gtest_main.o
	@echo "Unpacking gtest libraries"
	@ar rv $@ $^ -o $@
