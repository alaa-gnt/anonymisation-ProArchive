---
name: refactoring
description: Improve the internal structure of existing code without changing its external behavior, making it easier to understand, maintain, and extend.
---

# refactoring

## 1. Skill name
Refactoring

## 2. One-line purpose
Improve the internal structure of existing code without changing its external behavior, making it easier to understand, maintain, and extend.

## 3. When to use this skill
- When code is hard to understand or modify
- When you notice code smells (duplicated code, long methods, large classes, etc.)
- Before adding a new feature to existing code (prepare the code for the change)
- During code review when you identify structural problems
- When paying down technical debt in a planned refactoring session

## 4. When not to use this skill
- When the code is working and stable and no changes are planned (if it ain't broke, don't fix it)
- When the code is about to be rewritten or replaced
- When the refactoring would take longer than rewriting the module from scratch
- When tests are not in place to verify behavior is preserved

## 5. Core principles
- **Refactoring changes the structure, not the behavior**: The code must produce exactly the same outputs for the same inputs (Refactoring Ch.1).
- **Refactoring must be done in small, safe steps**: Each step preserves behavior. After each step, run the tests (Refactoring Ch.2, TPP Ch.7).
- **Code smells are the trigger for refactoring**: Common smells include duplicated code, long methods, large classes, long parameter lists, divergent change, shotgun surgery, feature envy, data clumps, primitive obsession, switch statements, lazy class, speculative generality, message chains, middle man, inappropriate intimacy, incomplete library class (Refactoring Ch.3).
- **Tests are the safety net**: Without tests, you are not refactoring—you are just changing code and hoping it works (Refactoring Ch.2, CC Ch.20).
- **Refactoring should be part of the normal development cycle**: Do it continuously, not as a separate phase (Refactoring Ch.1, TPP Ch.7).
- **The rule of three**: The first time you write something, just do it. The second time, you can duplicate. The third time, refactor (TPP Ch.2).
- **Deep modules resist refactoring**: If a module has a clean interface, you can change the implementation without affecting callers (POSD Ch.4).
- **Complexity is incremental**: Each small shortcut adds to the total complexity. Refactoring reverses this trend (POSD Ch.3, CC Ch.24).
- **Don't refactor and add features at the same time**: Separate refactoring from functional changes. Do one or the other in each commit (Refactoring Ch.2, TPP Ch.7).

## 6. Step-by-step method

### Step 1: Identify the code smell
- Run through the catalog of code smells (Refactoring Ch.3):
  - *Mysterious Name*: The method/class name doesn't reveal its purpose
  - *Duplicated Code*: Same expression in multiple places
  - *Long Method*: A method that is too long (heuristic: >10 lines is suspect)
  - *Long Parameter List*: More than 3 parameters
  - *Large Class*: A class with too many responsibilities
  - *Divergent Change*: One class changes for multiple reasons
  - *Shotgun Surgery*: One change requires modifying many classes
  - *Feature Envy*: A method seems more interested in another class than its own
  - *Primitive Obsession*: Using primitives instead of small objects for concepts like money, date range, phone number
  - *Switch Statements*: Repeated switch/case on the same condition
  - *Lazy Class*: A class that doesn't do enough to justify its existence
  - *Message Chains*: A client asks one object for another, then asks that for another...
  - *Middle Man*: A class that delegates everything to another class
  - *Inappropriate Intimacy*: Two classes that know too much about each other's private details
- Prioritize: focus on smells that affect the current development task

### Step 2: Ensure tests are in place
- Before any refactoring, verify there are adequate tests for the code being changed
- If tests don't exist, write characterization tests that capture the current behavior (Refactoring Ch.2, CC Ch.20)
- Run the tests to establish a baseline: they should all pass
- Heuristic: if you can't write a test for it, you can't refactor it safely

### Step 3: Select the refactoring technique
- Match the code smell to the appropriate refactoring (Refactoring Ch.3-12):
  - *Extract Function* (Ch.6): For long methods or duplicated code
  - *Inline Function* (Ch.6): When the function body is as clear as the name
  - *Extract Variable* (Ch.6): For complex expressions
  - *Inline Variable* (Ch.6): When the variable name doesn't add clarity
  - *Rename Variable/Function/Class* (Ch.6): For mysterious names
  - *Extract Class* (Ch.7): For large classes
  - *Inline Class* (Ch.7): For lazy classes
  - *Move Field/Method* (Ch.8): For feature envy or inappropriate intimacy
  - *Replace Primitive with Object* (Ch.9): For primitive obsession
  - *Replace Conditional with Polymorphism* (Ch.10): For switch statements
  - *Introduce Parameter Object* (Ch.11): For long parameter lists
  - *Split Phase* (Ch.12): For methods that do multiple things
  - *Replace Temp with Query* (Ch.11): For temporary variables that can be derived
  - *Separate Query from Modifier* (Ch.11): For methods that both return a value and change state

### Step 4: Perform the refactoring in small steps
- Apply one refactoring technique at a time
- After each atomic change, compile and run tests
- If a test fails, revert the last change and try a different approach (Refactoring Ch.2)
- Commit after each successful refactoring step (or group of small steps)
- The goal is that at any point, the code compiles and all tests pass

### Step 5: Verify behavior is preserved
- All existing tests must pass
- The output for any given input must be identical
- If coverage gaps exist, consider adding tests for the refactored code
- Check for edge cases that the existing tests might miss (CC Ch.20)

### Step 6: Clean up and commit
- Re-run the full test suite
- Review the diff: it should show only structural changes, not behavioral
- Commit with a clear message: describe the smell and the refactoring applied
- If the refactoring was done to prepare for a feature, the next commit adds the feature

## 7. Decision rules
- **If you need to add a feature and the code is a mess, refactor first, then add the feature** (Refactoring Ch.1).
- **If a method is longer than 10 lines, consider extracting sub-methods** (Refactoring Ch.6, CC Ch.7).
- **If a method has more than 3 parameters, use Introduce Parameter Object** (Refactoring Ch.11).
- **If a class has more than 10 methods covering unrelated responsibilities, extract a new class** (Refactoring Ch.7).
- **If you see the same switch statement in more than 2 places, use Replace Conditional with Polymorphism** (Refactoring Ch.10).
- **If you see the same expression in more than 2 places, extract it into a method** (Refactoring Ch.6).
- **If a method name doesn't reveal its purpose, rename it** (Refactoring Ch.6, POSD Ch.4).
- **If a function does both a query and a command, split it** (Refactoring Ch.11).
- **If a test requires extensive setup and testing of intermediate state, the module may be poorly designed** (Refactoring Ch.2, CC Ch.20).
- **If you're tempted to add a comment to explain what the code does, extract a method instead** (Refactoring Ch.6, TPP Ch.2).

## 8. Common mistakes
- Refactoring without tests: you cannot know if behavior was preserved (Refactoring Ch.2).
- Refactoring and adding features in the same commit: makes it impossible to tell what changed (Refactoring Ch.2).
- Taking too-large steps: if a step changes more than one thing at a time, it's too large (Refactoring Ch.2).
- Refactoring code that is about to be rewritten: wasted effort (TPP Ch.7).
- Changing the public API as part of a refactoring: this changes behavior (callers must update). Schedule API changes separately (Refactoring Ch.2).
- Applying refactoring without understanding the domain model: you might break domain invariants (DDD Ch.4).
- Over-refactoring: extracting everything into tiny methods or classes, making the code harder to follow (POSD Ch.4, Refactoring Ch.2).
- Refactoring for performance without profiling: never assume you know where the bottleneck is (TPP Ch.6).
- Refactoring production code without refactoring the tests too: tests should reflect the new structure (Refactoring Ch.2).
- Not committing after each step: if you make 10 changes and the tests fail, you have no idea which change caused it (Refactoring Ch.2).

## 9. Output format
```
## Refactoring Session: [Module/Class Name]

### Code Smell Identified
- Smell:
- Location (file:line):
- Description:

### Refactoring Plans
| Step | Technique | File:Line | Expected Outcome |
|------|-----------|-----------|------------------|
| 1    |           |           |                  |

### Test Coverage
- Existing tests:
- New tests needed:
- Test results after each step:

### Commit History
- Commit 1: [description of refactoring step]
- Commit 2: [next refactoring step]
```

## 10. Quality checklist
- [ ] Tests exist and pass before refactoring begins
- [ ] Each refactoring step preserves behavior
- [ ] Tests pass after each individual step
- [ ] No new features were added in the refactoring commits
- [ ] The code smell is resolved (not just moved elsewhere)
- [ ] The resulting code is simpler than the original
- [ ] No speculative generality (don't add abstractions you don't need yet)
- [ ] Commit messages clearly describe the refactoring applied
- [ ] The refactoring makes the next feature addition easier

## 11. Source books used
- Primary: Refactoring (Fowler)
- Support: A Philosophy of Software Design (Ousterhout), The Pragmatic Programmer (Hunt & Thomas), Code Complete (McConnell)

## 12. Notes on how the books complement each other
Refactoring provides the comprehensive catalog of code smells and refactoring techniques with step-by-step instructions. POSD provides the deeper design philosophy: why deep modules resist refactoring, how complexity accumulates, and what "simple code" really means. TPP adds the pragmatic developer mindset: DRY, orthogonality, the rule of three, and the importance of reversible decisions. CC adds the construction-level rigor: the larger context of software quality, defects, and the role of refactoring in the development process. Together they provide both the "how" (techniques) and the "why" (philosophy) of refactoring.
