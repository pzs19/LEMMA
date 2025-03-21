### Instruction

You are a careless student. I will provide you with a problem and the ground-truth solution. Your goal is to propose a new solution that contains specific errors. Specifically, you should:

1. **Understand the Problem and Solution:** Carefully read the problem statement and the ground-truth solution provided. Ensure you fully understand the question and the solution.
2. **Introduce Specific Errors:**  Intentionally introduce a **{error_type} error** into the reasoning steps. {error_description} Try to make these errors **plausible** and **reasonable** that even an intelligent student will make, not blatant or superficial. Don't mention the {error_type} error explicitly. Your output should be as natural as a student's realistic reasoning process, in which he/she makes mistakes.
3. **Continue Reasoning:** Continue reasoning after the error-injected step until you reach a wrong answer that is **inconsistent** with the final answer of the ground-truth solution. Leave the previous error as it is. Do NOT try to correct the error in the following steps.
4. **Format Answer:** Give your final number in the format of 'The answer is [your answer]'. Stop at the wrong answer, do not try to correct it.
5. **Explain the Error:** Explain why the proposed solution is incorrect and why it is a {error_type} error. Your explanation should be wrapped in <explanation> tags.

### Examples
{examples}

### Examples end. Now, introduce a {error_type} error into the solution of the following problem.

[Question]
{question}

[Ground-truth Solution]
{gt_solution}

[Error-Injected Solution]
