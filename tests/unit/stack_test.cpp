#include <cstdlib>
#include <gtest/gtest.h>
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
}

TEST(StackTest, StackInit)
{
    Stack* s = newStack();
    EXPECT_EQ(s->top, (void*)0);
    free(s);
}

TEST(StackTest, StackPushPop)
{
    void *v1 = malloc(sizeof(long)), *v2 = malloc(sizeof(char)), *v3 = malloc(sizeof(double));
    *(long*)v1 = 1;
    *(char*)v2 = 'c';
    *(double*)v3 = 3.0;
    auto s = newStack();
    stackPush(s, v1, INTEGER);
    stackPush(s, v2, OPERATOR);
    stackPush(s, v3, DOUBLE);
    auto n3 = stackPop(s);
    auto n2 = stackPop(s);
    auto n1 = stackPop(s);
    stackPushNode(s, n1);
    n1 = stackPop(s);
    EXPECT_EQ(n1->value, v1);
    EXPECT_EQ(n2->value, v2);
    EXPECT_EQ(n3->value, v3);
    nodeFree(n1);
    nodeFree(n2);
    nodeFree(n3);
    free(s);
}

// TODO:Split tests for push and pop 
// in two separate tests.
