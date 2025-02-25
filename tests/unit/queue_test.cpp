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

typedef struct Queue {
    Node* first;
    Node* last;
} Queue;

Queue* newQueue();
void queuePush(Queue*, void*, EType);
void queuePushNode(Queue*, Node*);
Node* queuePop(Queue*);
void nodeFree(Node*);
}

TEST(QueueTest, QueueInit)
{
    Queue* s = newQueue();
    EXPECT_EQ(s->first, (void*)0);
    EXPECT_EQ(s->last, (void*)0);
}

TEST(QueueTest, QueuePushPop)
{
    void *v1 = malloc(sizeof(long)), *v2 = malloc(sizeof(char)), *v3 = malloc(sizeof(double));
    *(long*)v1 = 1;
    *(char*)v2 = 'c';
    *(double*)v3 = 3.0;
    auto q = newQueue();
    queuePush(q, v1, INTEGER);
    queuePush(q, v2, OPERATOR);
    queuePush(q, v3, DOUBLE);
    auto n1 = queuePop(q);
    auto n2 = queuePop(q);
    auto n3 = queuePop(q);
    queuePushNode(q, n3);
    n3 = queuePop(q);
    EXPECT_EQ(n1->value, v1);
    EXPECT_EQ(n2->value, v2);
    EXPECT_EQ(n3->value, v3);
    free(q);
    nodeFree(n1);
    nodeFree(n2);
    nodeFree(n3);
}
