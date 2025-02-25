#include <gtest/gtest.h>

extern "C" {
int precedence(char op1, char op2);
}

TEST(PrecedenceTest, PlusAndMinus)
{
    EXPECT_EQ(0, precedence('+', '-'));
}
