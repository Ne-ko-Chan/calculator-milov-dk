#include <cstdio>
#include <cstring>
#include <gtest/gtest.h>
#include <stdlib.h>

extern "C" {
typedef enum EErrors {
    ERR_UNEXPECTED_CHAR = -1,
    ERR_MISMATCHED_PARANTHESES = -2,
    ERR_STACK_FUCKED = -3,
    ERR_EMPTY_INPUT = -4
} EErrors;

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

typedef struct Queue {
    Node* first;
    Node* last;
} Queue;
int parseStdin(Queue* q);
Queue* newQueue();
Node* queuePop(Queue* q);
void nodeFree(Node*);
void pushIfNumberEnded(int* wasNum, long* number, Queue* q);
}

TEST(ParseTest,UtilityTestPushNumber) {
  Queue *q = newQueue();
  int wasNum = 0;
  long number = 100;
  pushIfNumberEnded(&wasNum, &number, q);
  EXPECT_EQ(q->first, (void*)0);

  wasNum = 1;
  pushIfNumberEnded(&wasNum, &number, q);
  EXPECT_EQ(*(long*)q->first->value, 100);
  nodeFree(queuePop(q));
  free(q);
}

TEST(ParseTest, SimpleTest1)
{
    auto q = newQueue();
    const char* input = "1+2-3*4/5";
    FILE* stream = fmemopen((void*)input, strlen(input), "r");
    FILE* tmp = stdin;
    stdin = stream;
    int err = parseStdin(q);
    fclose(stream);
    stdin = tmp;

    Node *n = NULL, *tmpn = NULL;
    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 1);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 2);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '+');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 3);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 4);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '*');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 5);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '/');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '-');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    EXPECT_EQ(n, (void*)0);
    free(q);
}

TEST(ParseTest, SimpleTest2)
{
    auto q = newQueue();
    const char* input = "(1+2 -\t \n\n\r3)*4/5";
    FILE* stream = fmemopen((void*)input, strlen(input), "r");
    FILE* tmp = stdin;
    stdin = stream;
    int err = parseStdin(q);
    fclose(stream);
    stdin = tmp;

    Node *n = NULL, *tmpn = NULL;
    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 1);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 2);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '+');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 3);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '-');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 4);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '*');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(long*)n->value, 5);
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    n = queuePop(q);
    ASSERT_NE(n, (void*)0);
    EXPECT_EQ(*(char*)n->value, '/');
    tmpn = n;
    n = n->next;
    nodeFree(tmpn);

    EXPECT_EQ(n, (void*)0);
    free(q);
}
