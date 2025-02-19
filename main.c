#include <stdio.h>
#include <stdlib.h>
// #define DEBUG

/////////////////// STRUCTS, ENUMS ////////////////////
typedef enum EErrors {
  ERR_UNEXPECTED_CHAR = -1,
  ERR_MISMATCHED_PARANTHESES = -2,
  ERR_STACK_FUCKED = -3,
  ERR_EMPTY_INPUT = -4
} EErrors;

typedef enum EType { NUMBER, OPERATOR } EType;

typedef struct Node {
  int value;
  EType type;
  struct Node *next;
} Node;

typedef struct Stack {
  Node *top;
} Stack;

typedef struct Queue {
  Node *first;
  Node *last;
} Queue;

/////////////////// STACK ////////////////////
Stack *newStack() {
  Stack *s = (Stack *)malloc(sizeof(Stack));
  if (s == NULL) {
    printf("ERROR allocating memory for Stack");
    return NULL;
  }
  s->top = NULL;
  return s;
}

void stackPush(Stack *s, int value, EType type) {
  Node *new = (Node *)malloc(sizeof(Node));
  new->value = value;
  new->next = s->top;
  new->type = type;
  s->top = new;
}

void stackPushNode(Stack *s, Node *new) {
  new->next = s->top;
  s->top = new;
}

Node *stackPop(Stack *s) {
  if (s->top == NULL) {
    return NULL;
  }

  Node *res = s->top;
  s->top = s->top->next;
  return res;
}

void stackPrint(Stack *s) {
  Node *tmp = s->top;
  while (tmp != NULL) {
    printf("%d(%c)\n", tmp->value, tmp->value);
    tmp = tmp->next;
  }
}

/////////////////// QUEUE ////////////////////
Queue *newQueue() {
  Queue *q = (Queue *)malloc(sizeof(Queue));
  if (q == NULL) {
    printf("ERROR allocating memory for Stack");
    return NULL;
  }
  q->first = NULL;
  q->last = NULL;
  return q;
}

void queuePush(Queue *q, int value, EType type) {
  Node *new = (Node *)malloc(sizeof(Node));
  new->value = value;
  new->type = type;
  new->next = NULL;
  if (q->first == NULL) {
    q->first = new;
    q->last = new;
  } else {
    q->last->next = new;
    q->last = new;
  }
}

void queuePushNode(Queue *q, Node *new) {
  new->next = NULL;
  if (q->first == NULL) {
    q->first = new;
    q->last = new;
  } else {
    q->last->next = new;
    q->last = new;
  }
}

Node *queuePop(Queue *q) {
  if (q->first == NULL) {
    return NULL;
  }

  Node *res = q->first;
  q->first = q->first->next;
  return res;
}

void queuePrint(Queue *q) {
  Node *tmp = q->first;
  while (tmp != NULL) {
    if (tmp->type == OPERATOR) {
      printf("%c\n", tmp->value);
    } else {
      printf("%d\n", tmp->value);
    }
    tmp = tmp->next;
  }
}

/////////////////// PARSING ////////////////////

int precedence(char op1, char op2) {
  if (op1 == '+' || op1 == '-') {
    if (op2 == '+' || op2 == '-') {
      return 0;
    } else { // op2 == '*' || '/'
      return -1;
    }
  } else { // op1 == '*' || '/'
    if (op2 == '+' || op2 == '-') {
      return 1;
    } else {
      return 0;
    }
  }
}

void pushIfNumberEnded(int *wasNum, int *number, Queue *q) {
  if (*wasNum) {
    queuePush(q, *number, NUMBER);
    *number = 0;
    *wasNum = 0;
  }
}

int parseStdin(Queue *q) {
  Node *tmp = NULL;
  int number = 0;
  int wasNum = 0;
  char ch;
  Stack *s = newStack();

  do {
    switch (ch = getchar()) {
    case '(':
      stackPush(s, '(', OPERATOR);
      break;
    case ')':
      pushIfNumberEnded(&wasNum, &number, q);
      while (s->top != NULL && s->top->value != '(') {
        tmp = stackPop(s);
        queuePushNode(q, tmp);
      }
      if (s->top == NULL) {
        return ERR_MISMATCHED_PARANTHESES;
      }
      if (s->top->value == '(') {
        free(stackPop(s));
      }
      break;
    case '+':
    case '-':
    case '*':
    case '/':
      pushIfNumberEnded(&wasNum, &number, q);
      while (s->top != NULL && s->top->value != '(' &&
             precedence(s->top->value, ch) != -1) {
        tmp = stackPop(s);
        queuePushNode(q, tmp);
      }
      stackPush(s, ch, OPERATOR);
      break;
    case '\n':
    case EOF:
      pushIfNumberEnded(&wasNum, &number, q);
      while (s->top != NULL) {
        tmp = stackPop(s);
        queuePushNode(q, tmp);
      }
    case ' ':
      pushIfNumberEnded(&wasNum, &number, q);
      break;
    default:
      if (ch >= '0' && ch <= '9') {
        wasNum = 1;
        number = number * 10 + ch - '0';
      } else {
        return ERR_UNEXPECTED_CHAR;
      }
    }
#ifdef DEBUG
    printf("\nQUEUE FRAME:\n");
    queuePrint(q);
    printf("STACK FRAME:\n");
    stackPrint(s);
#endif /* ifdef DEBUG */
  } while (ch != EOF);
  return 0;
}

int count(int opcode, int arg1, int arg2) {
  int res = 0;
  switch (opcode) {
  case '+':
    res = arg1 + arg2;
    break;
  case '-':
    res = arg1 - arg2;
    break;
  case '*':
    res = arg1 * arg2;
    break;
  case '/':
    res = arg1 / arg2;
    break;
  }
  return res;
}

int calculate(Queue *q, int *res) {
  Stack *s = newStack();

  while (q->first != NULL) {
    Node *nextToken = queuePop(q);
    if (nextToken->type == NUMBER) {
      stackPushNode(s, nextToken);
    } else {
      if (s->top == NULL || s->top->next == NULL) {
        return ERR_STACK_FUCKED;
      }
      Node *arg2 = stackPop(s);
      Node *arg1 = stackPop(s);
      int value = count(nextToken->value, arg1->value, arg2->value);
      free(arg2);
      free(arg1);
      stackPush(s, value, NUMBER);
    }
  }
  *res = s->top->value;
  free(s);
  return 0;
}

int calculateStdin() {
  int res;
  Queue *resultQueue = newQueue();

  int err = parseStdin(resultQueue);
  switch (err) {
  case ERR_MISMATCHED_PARANTHESES:
    printf("ERROR: mismatched parantheses in expression");
    return ERR_MISMATCHED_PARANTHESES;
    break;
  case ERR_EMPTY_INPUT:
    printf("ERROR: no meaningfull characters in input");
    return ERR_EMPTY_INPUT;
  case ERR_UNEXPECTED_CHAR:
    printf("ERROR: unexpected character");
    return ERR_UNEXPECTED_CHAR;
  }
#ifdef DEBUG
  queuePrint(resultQueue);
#endif /* ifdef DEBUG */

  err = calculate(resultQueue, &res);
  if (err == ERR_STACK_FUCKED) {
    printf("ERROR: stack corrupted during evaluation. Expression must be "
           "incorrect");
    return ERR_STACK_FUCKED;
  }

  printf("%d", res);

  return 0;
}

int main() { return calculateStdin(); }
