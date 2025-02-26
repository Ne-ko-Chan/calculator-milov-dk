#include <cstdio>
#include <cstdlib>
#include <gtest/gtest.h>
#include <string>
#include <unistd.h>

extern "C" {
typedef enum EType { INTEGER,
    DOUBLE,
    OPERATOR } EType;

typedef struct Node {
    void* value;
    EType type;
    struct Node* next;
} Node;

typedef struct Stack {
    Node* top;
} Stack;

Stack* newStack();
void stackPush(Stack*, void*, EType);
void stackPushNode(Stack*, Node*);
Node* stackPop(Stack*);
void nodeFree(Node*);
void stackPrint(Stack* s);
}

class StackQueuePrintTest : public ::testing::Test {
protected:
    int saved_stdout;
    void SetUp() override
    {
        saved_stdout = dup(STDOUT_FILENO);
    }
    void TearDown() override
    {
        dup2(saved_stdout, STDOUT_FILENO);
        close(saved_stdout);
    }

    std::string captureOutput(Stack* s)
    {
        int pipefd[2];
        pipe(pipefd);

        dup2(pipefd[1], STDOUT_FILENO);
        close(pipefd[1]);

        stackPrint(s);
        fflush(stdout);

        char buffer[1024];
        ssize_t bytes = read(pipefd[0], buffer, sizeof(buffer) - 1);
        close(pipefd[0]);

        // Restore stdout
        dup2(saved_stdout, STDOUT_FILENO);

        if (bytes > 0) {
            buffer[bytes] = '\0';
            return std::string(buffer);
        }
        return "";
    }
};

TEST_F(StackQueuePrintTest, PrintValues) {
  auto s = newStack();
  long* v1 = (long*)malloc(sizeof(long));
  *v1 = 10;
  double* v2 = (double*)malloc(sizeof(double));
  *v2 = 12;
  char* v3 = (char*)malloc(sizeof(char));
  *v3 = '+';
  stackPush(s, v1, INTEGER);
  stackPush(s, v2, DOUBLE);
  stackPush(s, v3, OPERATOR);
  auto str = captureOutput(s);
  std::cout<<str;
  nodeFree(stackPop(s));
  nodeFree(stackPop(s));
  nodeFree(stackPop(s));
  free(s);
}
