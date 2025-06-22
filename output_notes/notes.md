# Notes for Chunk 1
```markdown
## Chapter 18: Concurrency Control

### Outline
*   Lock-Based Protocols
*   Timestamp-Based Protocols
*   Validation-Based Protocols
*   Multiple Granularity
*   Multiversion Schemes
*   Insert and Delete Operations
*   Concurrency in Index Structures

### Lock-Based Protocols

*   A lock is a mechanism to control concurrent access to a data item.

*   **Lock Modes:** Data items can be locked in two modes:
    1.  **Exclusive (X) Mode:**
        *   Data item can be both read and written.
        *   X-lock is requested using `lock-X` instruction.
    2.  **Shared (S) Mode:**
        *   Data item can only be read.
        *   S-lock is requested using `lock-S` instruction.

*   Lock requests are made to the concurrency-control manager. A transaction can proceed only after the request is granted.

*   **Lock Compatibility Matrix:**

    |             | S     | X     |
    | :---------- | :---- | :---- |
    | **S**       | True  | False |
    | **X**       | False | False |

    *   A transaction may be granted a lock on an item if the requested lock is compatible with locks already held on the item by other transactions.
    *   Any number of transactions can hold shared locks on an item.
    *   If any transaction holds an exclusive lock on the item, no other transaction may hold any lock on the item.

*   **Example:**

    ```
    T2: lock-S(A);
        read (A);
        unlock(A);

        lock-S(B);
        read (B);
        unlock(B);
        display(A+B)
    ```

    *   Locking as shown above is not sufficient to guarantee serializability.

*   **Schedule With Lock Grants:**

    *Grants are omitted in the remaining sections.*
    *Assume grant happens just before the next instruction following the lock request.*
    *   The schedule may not be serializable.

*   **Locking Protocol:** A locking protocol is a set of rules followed by all transactions while requesting and releasing locks.

*   Locking protocols enforce serializability by restricting the set of possible schedules.

*   **Deadlock:**

    *Consider the partial schedule (the actual schedule is not provided in the content, so this is just to indicate where a deadlock example would be).*
```

# Notes for Chunk 2
# Relational Database Design Exam Notes

## Desirable Properties of Decompositions

*   **Lossless-join decomposition:**
    *   Enables the reconstruction of any instance of the original relation from instances of the smaller relations.
*   **Dependency preservation:**
    *   Enables the enforcement of any constraint on the original relation by enforcing constraints on each of the smaller relations.
*   **Repetition of information is avoided**

## Functional Dependencies (FDs)

*   **Definition:**
    *   Let R be a relation schema.
    *   α ⊆ R and β ⊆ R
    *   The functional dependency α → β holds on R if and only if for any legal relations r(R), whenever any two tuples t1 and t2 in r agree on the attributes α, they also agree on the attributes β.
    *   That is, t1\[α] = t2\[α] → t1\[β] = t2\[β]
*   **Example:**
    *   Consider a relation schema: Loan-schema = (loan\_number, branch\_name, amount)
    *   The functional dependency loan\_number → amount holds on Loan-schema if for any legal loan relation r, the value of loan\_number uniquely determines the value of amount.
    *   Given a loan number there is only one amount associated with that loan number.

## FD (Cont.)

*   **Superkey:**
    *   K is a superkey for relation schema R if and only if K → R
*   **Candidate Key:**
    *   K is a candidate key for R if and only if
        *   K → R, and
        *   for no α ⊂ K, α → R
*   **Constraints:**
    *   Functional dependencies allow us to express constraints that cannot be expressed using superkeys.
    *   Consider the schema Loan-schema = (loan\_number, branch\_name, amount)
    *   We might want to say that branch\_name → amount
        *   This means that the amount of the loan is determined by the branch the loan belongs to.
        *   If we change the branch\_name of loan number L-300 from “Perryridge” to “Round Hill”, we also need to change the amount to the amount at the Round Hill branch.

## Use of Functional Dependencies

*   We use functional dependencies to:
    *   Test relations to see if they are legal under a given set of functional dependencies.
        *   If a relation r is legal under a set F of functional dependencies, we say that r satisfies F.
    *   Specify constraints on the set of legal relations.
        *   We say that F specifies the constraints on legal relations.
    *   Design a database schema such that it enforces a given set of functional dependencies.

## Example

*   Relation schema: Loan-schema = (loan\_number, branch\_name, amount)
*   Functional dependencies:
    *   loan\_number → amount
    *   branch\_name → amount
*   The amount depends on the loan\_number
*   The amount of the loan depends on the branch
*   This suggests that the Loan-schema should be decomposed into:
    *   Loan-number-schema = (loan\_number, amount)
    *   Branch-schema = (branch\_name, amount)

## Closure of a Set of Functional Dependencies

*   Given a set F of functional dependencies, the closure of F is the set of all functional dependencies logically implied by F.
*   We denote the closure of F by F+.
*   **Example:**
    *   A → B
    *   B → C
    *   A → C is in F+
*   We can find all of F+ by applying Armstrong’s Axioms:
    *   if β ⊆ α, then α → β (reflexivity)
    *   if α → β, then γα → γβ (augmentation)
    *   if α → β, and β → γ, then α → γ (transitivity)

## Closure of a Set of Functional Dependencies (Cont.)

*   Additional rules (can be derived from Armstrong’s axioms)
    *   If α → β and α → γ, then α → βγ (union)
    *   If α → βγ, then α → β and α → γ (decomposition)
    *   If α → β and γβ → δ, then αγ → δ (pseudotransitivity)
*   The above rules are sound and complete.
*   **Computation of F+:**
    *   For each α ⊆ R we find α+, the attribute closure of α, the set of all attributes functionally determined by α
    *   Use α+ to find all dependencies in F+ involving α
*   **Example:**
    *   R = (A, B, C, G, H, I) and F is { A → B, A → C, CG → H, CG → I, B → H}
        *   (AG)+ = AG
        *   (CG)+ = CGHI
        *   (AB)+ = ABCH
        *   (AGH)+ = ABCHGI

## Uses of Attribute Closure

*   There are several uses of the attribute closure algorithm:
    *   **Testing for superkey:**
        *   To test if α is a superkey, we compute α+, and check if α+ contains all attributes of R.
    *   **Testing functional dependencies**
        *   To check if a functional dependency α → β holds (that is, is in F+), we compute α+ and check if it contains β.
    *   **Computing closure of F**
        *   We can use the attribute closure algorithm to compute the closure F+ of a set of functional dependencies F :
        *   For each α ⊆ R, we find α+, and for each β ⊆ α+, we output α → β.

## Example of Attribute Closure

*   R = (A, B, C, G, H, I)
    F: A → B
    A → C
    CG → H
    CG → I
    B → H
*   Is AG a superkey?
    *   (AG)+ = AG
    *   (AG)+ = ABCG (A → B and A → C)
    *   (AG)+ = ABCGH (CG → H and CG ⊆ (AG)+)
    *   (AG)+ = ABCGHI (CG → I and CG ⊆ (AG)+)
    *   Thus, (AG)+ = ABCGHI
*   AG is a superkey

## Example of Attribute Closure (Cont.)

*   R = (A, B, C, G, H, I)
    F: A → B
    A → C
    CG → H
    CG → I
    B → H
*   Is CG → H in F+?
    *   (CG)+ = CG
    *   (CG)+ = CGH (CG → H)
    *   (CG)+ = CGHI (CG → I)
*   Thus, yes, CG → H is in F+

## Decomposition

*   Goal: decompose a relation schema R into a set of relation schemas {R1, R2, ..., Rn} such that:
    *   Each relation schema Ri is in BCNF
    *   Lossless-join decomposition
    *   Dependency preservation

## Lossless-Join Decomposition

*   A decomposition of R into R1 and R2 is lossless-join if and only if at least one of the following dependencies is in F+:
    *   R1 ∩ R2 → R1
    *   R1 ∩ R2 → R2
*   **Example:**
    *   R = (A, B, C)
    *   F = {A → B, B → C}
    *   R1 = (A, B)
    *   R2 = (B, C)
    *   The decomposition is lossless-join since R1 ∩ R2 = {B} and B → BC

## Dependency Preservation

*   Let Fi be the set of dependencies F+ that include only attributes in Ri
*   A decomposition is dependency preserving if
    (F1 ∪ F2 ∪ ... ∪ Fn)+ = F+
*   Dependency preservation is important because it allows us to enforce functional dependencies by examining individual relations rather than having to perform a join.
*   **Example:**
    *   R = (A, B, C)
    *   F = {A → B, B → C}
    *   R1 = (A, B)
    *   R2 = (B, C)
    *   F1 = {A → B}
    *   F2 = {B → C}
    *   (F1 ∪ F2)+ = {A → B, B → C, A → C} = F+

## Testing for Dependency Preservation

*   To check if a decomposition R1, R2, ..., Rn is dependency preserving, we apply the following algorithm:

```
result = F;
for each Ri in the decomposition
 t = (Ri ∩ result)+ ∩ R;
 result = result ∪ {t → Ri ∩ result};
if result+ = F+ then the decomposition is dependency preserving
else it is not
```

## Normalization

*   Normalization is a process of analyzing the relations schemas to minimize redundancy and avoid update anomalies.
*   First Normal Form (1NF)
*   Second Normal Form (2NF)
*   Third Normal Form (3NF)
*   Boyce-Codd Normal Form (BCNF)
*   Fourth Normal Form (4NF)
*   Fifth Normal Form (5NF)

## First Normal Form

*   Domain is atomic if all its elements are considered to be indivisible
*   A relation schema R is in first normal form (1NF) if the domains of all attributes of R are atomic
*   **Example:**
    *   The relation schema Loan-schema = (loan\_number, branch\_name, amount) is in 1NF if the domains of loan\_number, branch\_name, and amount are atomic.
    *   If the domain of branch\_name is not atomic, then the Loan-schema is not in 1NF. For example, branch\_name could be a composite attribute consisting of branch\_street, branch\_city, and branch\_state.

## Second Normal Form

*   A relation schema R is in second normal form (2NF) if it is in 1NF and every non-prime attribute is fully functionally dependent on the primary key.
*   A non-prime attribute is an attribute that is not part of the primary key.
*   **Example:**
    *   Consider a relation schema R = (A, B, C, D) with primary key (A, B) and functional dependencies A → C and B → D.
    *   R is in 1NF, but it is not in 2NF because C is dependent on only part of the primary key (A), and D is dependent on only part of the primary key (B).
    *   To put R in 2NF, we decompose it into R1 = (A, C), R2 = (B, D), and R3 = (A, B).

## Third Normal Form

*   A relation schema R is in third normal form (3NF) if it is in 2NF and every non-prime attribute is non-transitively dependent on the primary key.
*   A transitive dependency is a functional dependency X → Z that can be derived from functional dependencies X → Y and Y → Z.
*   **Example:**
    *   Consider a relation schema R = (A, B, C, D) with primary key A and functional dependencies A → B, B → C, and C → D.
    *   R is in 2NF, but it is not in 3NF because D is transitively dependent on A (A → B → C → D).
    *   To put R in 3NF, we decompose it into R1 = (A, B), R2 = (B, C), and R3 = (C, D).

## Boyce-Codd Normal Form

*   A relation schema R is in Boyce-Codd Normal Form (BCNF) if and only if for every functional dependency X → A, X is a superkey.
*   **Example:**
    *   Consider a relation schema R = (A, B, C) with functional dependencies A → B and B → C.
    *   R is not in BCNF because B → C is a functional dependency, but B is not a superkey.
    *   To put R in BCNF, we decompose it into R1 = (A, B) and R2 = (B, C).

## Fourth Normal Form

*   A relation schema R is in fourth normal form (4NF) if it is in BCNF and there are no non-trivial multi-valued dependencies.
*   A multi-valued dependency is a dependency of the form X →→ Y, which means that for each value of X there is a set of values for Y.
*   **Example:**
    *   Consider a relation schema R = (A, B, C) with multi-valued dependencies A →→ B and A →→ C.
    *   R is not in 4NF because A →→ B and A →→ C are multi-valued dependencies.
    *   To put R in 4NF, we decompose it into R1 = (A, B) and R2 = (A, C).

## Fifth Normal Form

*   A relation schema R is in fifth normal form (5NF) if it is in 4NF and there are no non-trivial join dependencies.
*   A join dependency is a dependency of the form JD(R1, R2, ..., Rn), which means that R can be reconstructed by joining R1, R2, ..., Rn.
*   **Example:**
    *   Consider a relation schema R = (A, B, C) with join dependency JD(R1, R2, R3), where R1 = (A, B), R2 = (B, C), and R3 = (A, C).
    *   R is not in 5NF because JD(R1, R2, R3) is a join dependency.
    *   To put R in 5NF, we decompose it into R1 = (A, B), R2 = (B, C), and R3 = (A, C).

## Index Design

*   An index on an attribute of a relation allows us to find tuples with a specific value for that attribute quickly.
*   **Example:**
    *   If we want to find all loans with loan\_number = 123, we can create an index on the loan\_number attribute.
*   Indexes can be created on multiple attributes.
*   **Example:**
    *   If we want to find all loans with loan\_number = 123 and branch\_name = “Perryridge”, we can create an index on the (loan\_number, branch\_name) attributes.
*   Indexes can be clustered or unclustered.
*   A clustered index is an index in which the order of the tuples in the relation is the same as the order of the index.
*   An unclustered index is an index in which the order of the tuples in the relation is different from the order of the index.

# Notes for Chunk 3
# Exam Notes: Database Transactions

## Locking Protocols

*   **Locking Protocol Definition:** A set of rules that transactions must follow when acquiring and releasing locks on data items.

*   **Legal Schedule:** Given a locking protocol (e.g., 2PL), a schedule S is considered legal if it can be generated by a set of transactions adhering to that specific protocol.

*   **Ensuring Serializability:** A locking protocol *ensures serializability* if all schedules that are legal under that protocol are also serializable. This means that any concurrent execution permitted by the protocol is equivalent to some serial execution of those same transactions.

## Transaction Concept

*   **Definition:** A transaction is a single, logical unit of work that accesses and potentially updates various data items.

*   **Example:** Transferring $50 from account A to account B involves multiple steps:
    1.  `read(A)`
    2.  `A := A - 50`
    3.  `write(A)`
    4.  `read(B)`
    5.  `B := B + 50`
    6.  `write(B)`

*   **Challenges:**
    *   Failures (hardware, system crashes).
    *   Concurrent execution of multiple transactions.

## ACID Properties

To ensure data integrity, database systems must maintain the ACID properties:

*   **Atomicity:** "All or nothing." Either all operations within the transaction are reflected in the database, or none are.

*   **Consistency:** A transaction executed in isolation (without concurrent transactions) preserves the consistency of the database.

*   **Isolation:** Concurrent transactions should not be aware of each other; each transaction should execute as if it were the only one running. Intermediate results should be hidden.

*   **Durability:** Once a transaction completes successfully (commits), the changes persist, even in the event of system failures.

### Atomicity (Detailed)

*   **Example (Funds Transfer):** If the funds transfer transaction fails after writing the updated balance of account A but before updating account B, the money is "lost," violating consistency. The system must undo partial transactions.

### Consistency (Detailed)

*   **Example (Funds Transfer):** The sum of account A and account B should remain constant before and after the transaction. The transaction code must ensure this.

*   **Integrity Constraints:** Rules that the database must satisfy (e.g., every account balance >= $1000).

### Isolation (Detailed)

*   **Example (Funds Transfer):** Concurrent transactions can interfere:
    *   Overwriting updates from one transaction with another.
    *   "Dirty read": Reading a value written by another transaction that has not yet committed (and might be rolled back).

### Durability (Detailed)

*   **Example (Funds Transfer):** After the transaction commits, the updated balances of A and B *must* persist in the database, even if a crash occurs immediately afterward.

## Transaction State

During its lifetime, a transaction passes through several states:

*   **Active:** The initial state; the transaction is executing.

*   **Partially Committed:** After the final statement has been executed, but before changes are finalized.

*   **Failed:** Normal execution can no longer proceed (due to an error or exception).

*   **Aborted:** The transaction has been rolled back, and the database is restored to its state prior to the transaction's start.

*   **Committed:** Successful completion of the transaction.

## Implementation of Atomicity and Durability

*   The *recovery-management component* of the DBMS handles atomicity and durability.

*   **Approaches:**
    *   **Logging (Write-Ahead Logging):** All database changes are reliably recorded in a log before being applied to the database itself.
    *   **Shadow Paging:** Two page tables are maintained:
        *   Current page table: Reflects ongoing changes.
        *   Shadow page table: Represents the consistent state before the transaction began. It remains unchanged during the transaction. Changes are made only to the current page table.

## Isolation (Concurrency Control)

*   Concurrent execution can lead to database inconsistency.

*   **Concurrency Control Schemes:** Mechanisms to manage concurrent execution and avoid inconsistency.

*   The goal is to allow concurrency while maintaining database consistency.

## Serializability

*   **Basic Assumption:** Each transaction preserves database consistency.

*   **Serial Execution:** Serial execution of transactions preserves database consistency.

*   **Serializable Execution:** An execution (possibly concurrent) is serializable if its outcome is equivalent to that of some serial execution of the same transactions.

    *   **Result Equivalence:** The final value of each database item after the concurrent execution must be the same as after the serial execution.
    *   **Conflict Equivalence:** A concurrent schedule is conflict serializable if non-conflicting operations can be swapped to transform it into a serial schedule.

### Conflict Serializable (Detailed)

*   `Oi(X)`: Operation O performed by transaction Ti on data item X.

*   **Conflicting Operations:** Two operations `Oi(X)` and `Oj(X)` conflict if:
    1.  They access the *same* database element X.
    2.  *At least one* of the operations is a write operation.

*   **Examples:**
    *   `r1(A); w1(A)`: Conflict (read and write on A by T1).
    *   `r1(A); r2(A)`: No conflict (both are reads).
    *   `r1(A); w2(A)`: Conflict (read by T1, write by T2 on A).
    *   `w1(A); w2(A)`: Conflict (write by T1, write by T2 on A).

*   **Non-Conflict Serializable Example:**

    *   Schedule: `r1(Q), r2(Q), w1(Q), w2(Q)`
    *   Possible Serial Schedules:
        1.  T1 followed by T2: `r1(Q), w1(Q), r2(Q), w2(Q)`
        2.  T2 followed by T1: `r2(Q), w2(Q), r1(Q), w1(Q)`
    *   The original schedule is NOT conflict serializable because the order of operations cannot be swapped to match either serial schedule without swapping conflicting operations (w1(Q) and w2(Q) must be swapped which are conflicting).

## Transaction Isolation and Atomicity (Tradeoff)

*   **Isolation:** The degree to which a transaction is shielded from other concurrent transactions.

*   **Atomicity:** The "all or nothing" property.

*   **Tradeoff:**
    *   Higher isolation reduces concurrency-related anomalies but increases overhead and reduces concurrency.
    *   Lower isolation improves concurrency but increases the risk of anomalies.

## Transaction as a Code

*   SQL transaction blocks group SQL statements into a single logical unit.

*   **Example:**

    ```sql
    START TRANSACTION;
    -- SQL statements to transfer $50 from account A to account B
    UPDATE Accounts SET balance = balance - 50 WHERE account_number = A;
    UPDATE Accounts SET balance = balance + 50 WHERE account_number = B;
    COMMIT;
    ```

*   If any statement fails, the entire transaction can be rolled back.

## Concurrency Control (General)

*   Managing the concurrent execution of transactions.

*   Goal: Ensure database consistency despite concurrent access.

*   **Types:**
    *   Locking-based
    *   Timestamp-based

### Locking-Based Concurrency Control

*   Uses locks to prevent concurrent access to the same data.

*   **Lock Types:**
    *   Shared locks: Allow multiple transactions to read the same data concurrently.
    *   Exclusive locks: Allow only one transaction to write to the data.

*   A transaction must acquire a lock before accessing a data item. If the lock is held by another transaction, the requesting transaction waits.

### Timestamp-Based Concurrency Control

*   Uses timestamps to order transactions.

*   Each transaction gets a unique timestamp at the start.

*   A transaction checks the timestamp of a data item before accessing it, ensuring it's not accessing data modified by a more recent transaction. If it is, the transaction is rolled back and restarted.

## Recoverability

*   The ability of a database system to recover from failures while preserving consistency.

*   **Failure Types:**
    *   Transaction failures: A transaction cannot complete.
    *   System failures: The entire database system crashes.

*   **Techniques:**
    *   Logging: Recording changes in a log file.
    *   Checkpointing: Periodically creating a snapshot of the database.
    *   Shadow paging: Maintaining two copies of each page.

# Notes for Chunk 4
```markdown
# Exam Notes: Concurrency Control - Lock Conversions, Automatic Locks, Graph-Based Protocols & Deadlock Handling

## Lock Conversions

Two-phase locking protocol with lock conversions involves a growing phase and a shrinking phase.

*   **Growing Phase:**
    *   Can acquire a lock-S (shared lock) on a data item.
    *   Can acquire a lock-X (exclusive lock) on a data item.
    *   Can convert a lock-S to a lock-X (upgrade).
*   **Shrinking Phase:**
    *   Can release a lock-S.
    *   Can release a lock-X.
    *   Can convert a lock-X to a lock-S (downgrade).

This protocol ensures serializability.

## Automatic Acquisition of Locks

Transactions automatically acquire locks when read or write operations are issued, without explicit locking calls.

*   **Read(D) Operation:**
    *   If transaction Ti has a lock on data item D, then read(D).
    *   Otherwise:
        *   Wait if another transaction has a lock-X on D.
        *   Grant Ti a lock-S on D.
        *   read(D).
*   **Write(D) Operation:**
    *   If Ti has a lock-X on D, then write(D).
    *   Otherwise:
        *   Wait if another transaction has any lock on D.
        *   If Ti has a lock-S on D, then upgrade the lock on D to lock-X.
        *   Otherwise, grant Ti a lock-X on D.
        *   write(D).

All locks are released after commit or abort.

## Implementation of Locking

A lock manager is often implemented as a separate process.

*   Transactions send lock and unlock requests as messages to the lock manager.
*   The lock manager replies with lock grant messages or rollback requests (in case of a deadlock).
*   The requesting transaction waits until its request is answered.
*   The lock manager maintains a lock table to record granted locks and pending requests.

## Lock Table

*   The lock table is an in-memory data structure.
*   Dark rectangles indicate granted locks, light colored ones indicate waiting requests.
*   The lock table records the type of lock (S or X) granted or requested.
*   New requests are added to the end of the queue for the data item.
*   A request is granted if it is compatible with all earlier locks.
*   Unlock requests result in the request being deleted, and later requests are checked to see if they can now be granted.
*   If a transaction aborts, all waiting or granted requests of the transaction are deleted.
*   The lock manager may keep a list of locks held by each transaction for efficient abort processing.

## Graph-Based Protocols

Graph-based protocols offer an alternative to two-phase locking.

*   Impose a partial ordering () on the set of data items D = {d1, d2, ..., dh}.
*   If di  dj, then any transaction accessing both di and dj must access di before accessing dj.
*   The set D can be viewed as a directed acyclic graph, called a database graph.

## Tree Protocol

A simple kind of graph protocol.

*   Only exclusive locks are allowed.
*   The first lock by Ti may be on any data item.
*   Subsequently, a data item Q can be locked by Ti only if the parent of Q is currently locked by Ti.
*   Data items may be unlocked at any time.
*   A data item that has been locked and unlocked by Ti cannot subsequently be relocked by Ti.

*   **Advantages:**
    *   Ensures conflict serializability and freedom from deadlock.
    *   Unlocking may occur earlier than in two-phase locking, potentially reducing waiting times and increasing concurrency.
    *   Deadlock-free, no rollbacks required.
*   **Drawbacks:**
    *   Does not guarantee recoverability or cascade freedom. Commit dependencies may be needed.
    *   Transactions may have to lock data items that they do not access, leading to increased locking overhead, additional waiting time, and potential decrease in concurrency.
    *   Schedules possible under two-phase locking might not be possible under the tree protocol, and vice versa.

## Deadlock Handling

A system is deadlocked if there is a set of transactions such that every transaction in the set is waiting for another transaction in the set.

## Deadlock Prevention

Deadlock prevention protocols ensure that the system will never enter a deadlock state.

*   **Pre-declaration:** Require that each transaction locks all its data items before it begins execution.
*   **Partial Ordering:** Impose a partial ordering of all data items and require that a transaction can lock data items only in the order specified by the partial order (graph-based protocol).

## More Deadlock Prevention Strategies

*   **wait-die scheme:** (non-preemptive)
    *   Older transactions may wait for younger ones to release data items.
    *   Younger transactions never wait for older ones; they are rolled back instead (die).
    *   A transaction may "die" several times before acquiring a lock.
*   **wound-wait scheme:** (preemptive)
    *   Older transactions "wound" (force rollback) younger transactions instead of waiting for them.
    *   Younger transactions may wait for older ones.
    *   Fewer rollbacks than wait-die scheme.
*   **Timestamp Considerations:**
    *   In both schemes, a rolled-back transaction is restarted with its original timestamp.
    *   This ensures that older transactions have precedence over newer ones, avoiding starvation.
```

# Notes for Chunk 5
```markdown
# Module 6: Database System Concepts - Exam Notes

## Chapter 6: Formal Relational Query Languages

### Relational Query Languages
*   **Relational Algebra:**
    *   Procedural language.
*   **Relational Calculus:**
    *   Non-procedural, or declarative, language.
    *   Specifies *what* to retrieve, not *how* to retrieve it.
*   **Importance of Relational Algebra:**
    *   Fundamental basis for query languages (e.g., SQL).
    *   Basis for query implementation (query processing and optimization).

### Relational Algebra
*   A procedural language with operations that take one or two relations as input and produce a new relation.
*   **Six Fundamental Operations:**
    *   Selection
    *   Projection
    *   Union
    *   Set Difference
    *   Cartesian Product
    *   Rename
*   Other operations are defined using these six.
*   **Additional Operations:**
    *   Set intersection
    *   Natural join
    *   Division

### Select Operation
*   **Notation:** 𝜎𝑝(r)
    *   `p` is the selection predicate.
*   Defines a relation containing tuples in `r` that satisfy predicate `p`.
*   **Example:**
    *   Relation `r`:

        A B
        --- ---
        α 10
        β 10
        γ 20
        δ 30
    *   𝜎A=B (r):

        A B
        --- ---
        α 10
        β 10

### Select Operation (Cont.)
*   **Comparison Operators:** =, ≠, >, <, ≥, ≤
*   **Connectives:** ∧ (and), ∨ (or), ¬ (not)
*   **Example:**
    *   𝜎A=B∧D > 5 (r):

        A B C D
        --- --- --- ---
        α 10 1 7
        β 10 3 4
        β 10 2 10
        β 10 2 9

### Project Operation
*   **Notation:** ∏A1, A2, …, Ak (r)
    *   `A1`, `A2`, …, `Ak` are attribute names, and `r` is a relation name.
*   Result: A new relation of `k` columns, retaining only the values for attributes `A1`, `A2`, …, `Ak` from each tuple in `r`.
*   Duplicate rows are eliminated.

### Project Operation (Cont.)
*   **Example:**
    *   Relation `r`:

        A B C
        --- --- ---
        α 10 1
        α 20 1
        β 30 1
        β 40 2
    *   ∏A,C (r):

        A C
        --- ---
        α 1
        β 1
        β 2

### Union Operation
*   **Notation:** r ∪ s
*   Defined on two relations `r` and `s` that must have the same schema.
    *   Same number of attributes, and corresponding attributes have the same type.
*   Result: All tuples that are in `r` or `s` or both.
*   Duplicate tuples are eliminated.
*   **Example:**
    *   Relation `r`:

        A B
        --- ---
        α 1
        α 2
        β 1
    *   Relation `s`:

        A B
        --- ---
        α 2
        β 3
    *   r ∪ s:

        A B
        --- ---
        α 1
        α 2
        β 1
        β 3

### Set-Difference Operation
*   **Notation:** r – s
*   Defined on two relations `r` and `s` that must have the same schema.
    *   Same number of attributes, and corresponding attributes have the same type.
*   Result: All tuples that are in `r` but not in `s`.
*   **Example:**
    *   Relation `r`:

        A B
        --- ---
        α 1
        α 2
        β 1
    *   Relation `s`:

        A B
        --- ---
        α 2
        β 3
    *   r – s:

        A B
        --- ---
        α 1
        β 1

### Cartesian-Product Operation
*   **Notation:** r x s
*   Defines a relation that is the concatenation of every tuple of relation `r` with every tuple of relation `s`.
*   Assume that relations `r` and `s` have no attributes in common.  (If they do, the renaming operation can be used).

### Cartesian-Product Operation (Cont.)
*   **Example:**
    *   Relation `r`:

        A B
        --- ---
        α 1
        β 2
    *   Relation `s`:

        C D
        --- ---
        α 5
        β 12
        γ 10
    *   r x s:

        A B C D
        --- --- --- ---
        α 1 α 5
        α 1 β 12
        α 1 γ 10
        β 2 α 5
        β 2 β 12
        β 2 γ 10

### Rename Operation
*   **Notation:** ρx(r)
    *   Returns the result of relation `r` under the name `x`.
*   **Notation:** ρx(A1, A2, …, An)(r)
    *   Returns the result of relation `r` under the name `x`, and renames the attributes to `A1`, `A2`, …, `An`.

### Example Queries
*   Relation `student` (ID, name, dept_name, tot_cred)
*   Relation `takes` (ID, course_id, sec_id, semester, year, grade)

    1.  Find the names of all students who have taken course ‘CS-101’

        ∏name (𝜎course_id=“CS-101” (takes student))

### Additional Operations
*   These operations do not add any power to the relational algebra, but simplify common queries.
    *   Set intersection
    *   Natural join
    *   Division

### Set-Intersection Operation
*   **Notation:** r ∩ s
*   Defined on two relations `r` and `s` that must have the same schema.
    *   Same number of attributes, and corresponding attributes have the same type
*   Result: All tuples that are in both `r` and `s`.
*   **Example:**
    *   Relation `r`:

        A B
        --- ---
        α 1
        α 2
        β 1
    *   Relation `s`:

        A B
        --- ---
        α 2
        β 3
    *   r ∩ s:

        A B
        --- ---
        α 2

### Natural-Join Operation
*   **Notation:** r ⋈ s
*   Let `r` and `s` be relations on schemas `R` and `S` respectively.
*   Then `r ⋈ s` is a relation on schema `R ∪ S` whose tuples are obtained as follows:
    *   Consider each pair of tuples `tr` from `r` and `ts` from `s`.
    *   If `tr` and `ts` have the same value on each of the attributes in `R ∩ S`, add a tuple `t` to the result, where
        *   `t` has the same value as `tr` on `r`
        *   `t` has the same value as `ts` on `s`

### Natural-Join Operation (Cont.)
*   **Example:**
    *   Relation `r`:

        A B C D
        --- --- --- ---
        α 1 10 a
        β 2 20 b
        γ 1 10 c
    *   Relation `s`:

        B D E
        --- --- ---
        1 a α
        2 b β
        3 c γ
    *   r ⋈ s:

        A B C D E
        --- --- --- --- ---
        α 1 10 a α
        β 2 20 b β

### Division Operation
*   **Notation:** r ÷ s
*   Suited to queries that include the phrase “for all”.
*   Let `r` and `s` be relations on schemas `R` and `S` respectively
    *   where `S ⊆ R`
*   `r ÷ s` is a relation on schema `R – S` consisting of the set of tuples `tr` such that for every tuple `ts` in `s`, there is a tuple `t` in `r` satisfying
    *   `t[S] = ts[S]`
    *   `t[R – S] = tr`

### Division Operation (Cont.)
*   **Example:**
    *   Relation `r`:

        A B
        --- ---
        a 1
        a 2
        a 3
        b 1
        c 1
        d 1
        d 3
        e 2
    *   Relation `s`:

        B
        ---
        1
        2
    *   r ÷ s:

        A
        ---
        a
        d

### Relational Algebra Summary
*   The relational algebra is a procedural query language.
*   It consists of a set of operations that take one or two relations as input and produce a new relation as their result.
*   Six basic operations: Selection, Projection, Union, Set Difference, Cartesian Product, and Rename.
*   Other operations like Set Intersection, Natural Join, and Division can be defined in terms of the six basic operations.
*   Relational algebra forms the basis for query languages like SQL and is used in query processing and optimization.
```

# Notes for Chunk 6
# Exam Notes: Concurrency Control and Recovery

## Deadlock Prevention (Cont.)

### Timeout-Based Schemes

*   **Concept:** A transaction waits for a lock for a specified amount of time. If the wait exceeds this time, the transaction is rolled back.
*   **Advantage:** Ensures deadlocks are resolved by timeout if they occur. Simple to implement.
*   **Disadvantages:**
    *   May roll back transactions unnecessarily even when no deadlock exists.
    *   Difficult to determine a good timeout interval.
    *   Starvation is possible.

## Deadlock Detection

### Wait-For Graph

*   **Vertices:** Transactions.
*   **Edges:** An edge from Ti -> Tj indicates that transaction Ti is waiting for a lock held by transaction Tj in conflicting mode.
*   **Deadlock Condition:** The system is in a deadlock state if and only if the wait-for graph contains a cycle.
*   **Process:** A deadlock-detection algorithm is invoked periodically to check for cycles in the wait-for graph.
*   **Example:**
    *   Wait-for graph *without* a cycle indicates no deadlock.
    *   Wait-for graph *with* a cycle indicates a deadlock.

## Deadlock Recovery

*   **Process:** When a deadlock is detected, one or more transactions must be rolled back (chosen as victims) to break the deadlock cycle.
*   **Victim Selection:** Choose the transaction that will incur the minimum cost when rolled back.
*   **Rollback:**
    *   **Total Rollback:** Abort the transaction and restart it.
    *   **Partial Rollback:** Roll back the transaction only far enough to release the locks that another transaction in the cycle is waiting for.
*   **Starvation:** Can occur if the same transaction is repeatedly chosen as the victim.
*   **Solution:** The oldest transaction in the deadlock set should never be chosen as the victim.

## Multiple Granularity

*   **Concept:** Allow data items to be of various sizes and define a hierarchy of data granularities, where smaller granularities are nested within larger ones.
*   **Representation:** Can be represented as a tree structure.
*   **Locking Implication:** When a transaction explicitly locks a node in the tree, it implicitly locks all the node's descendants in the same mode.
*   **Granularity of Locking:**
    *   **Fine Granularity (lower in the tree):** High concurrency, high locking overhead.
    *   **Coarse Granularity (higher in the tree):** Low locking overhead, low concurrency.
*   **Example of Granularity Hierarchy:**
    *   Levels: Database -> Area -> File -> Record.

### Intention Lock Modes

*   **Additional Lock Modes:** Besides Shared (S) and Exclusive (X) locks, there are three intention lock modes:
    *   **Intention-Shared (IS):** Indicates explicit locking at a lower level of the tree with shared locks.
    *   **Intention-Exclusive (IX):** Indicates explicit locking at a lower level with exclusive or shared locks.
    *   **Shared and Intention-Exclusive (SIX):** The subtree rooted by that node is locked explicitly in shared mode, and explicit locking is being done at a lower level with exclusive-mode locks.
*   **Purpose:** Intention locks allow a higher-level node to be locked in S or X mode without checking all descendent nodes.
*   **Compatibility Matrix:** The compatibility matrix defines which lock modes can be held concurrently. (The specific matrix was mentioned as existing, but not provided).

### Multiple Granularity Locking Scheme

*   **Rules:** Transaction Ti can lock a node Q, subject to the lock compatibility matrix. (Again, the specific matrix was not provided).

## Recovery

### Failure Classification

*   **Failures are unavoidable:** Due to software errors, hardware malfunctions, or power failures.
*   **Types of Failure:**
    *   **Transaction Failure:**
        *   Logical errors: Data accessed by the transaction does not conform to expectations.
        *   Internal state error: The transaction encounters a state from which it cannot proceed.
    *   **System Failure:**
        *   The system reaches a state where normal operation cannot proceed.
        *   Hardware or software error causes loss of main memory.
        *   May leave the database in an inconsistent state.
    *   **Media Failure:**
        *   Failure of the storage medium (disk or tape).
        *   Loss of all or part of persistent storage.

### Transaction Recovery

*   **Goal:** Preserve atomicity, consistency, isolation, and durability (ACID properties).
*   **Recovery Algorithms:**
    *   Actions during normal transaction processing to ensure enough information exists to recover from failures.
    *   Actions taken after a failure to recover the database to a consistent state.
*   **Key Concept:** Redundancy – store extra information to recover from failure.
*   **Methods:**
    *   Log-based recovery
    *   Shadow paging

### Recovery and Atomicity

*   **Transaction Begin:** `<Ti start>` is written to the log.
*   **Transaction End:**
    *   `<Ti commit>` is written to the log if the transaction commits.
    *   `<Ti abort>` is written to the log if the transaction aborts.
*   **Transaction Rollback:** Use the log to undo the updates performed by the transaction. If the log contains `<Ti start>` but no `<Ti commit>`, transaction Ti needs to be rolled back.

### Recovery and Durability

*   **Durability Requirement:** If a transaction reports successful completion, the changes it made must persist.
*   **Approaches to Ensure Durability:**
    *   Defer database modifications.
    *   Immediate database modifications.

### Recovery with Deferred Update

*   **Concept:** Do not physically update the database on disk until after the transaction commits.
*   **Process:** During execution, transaction updates are recorded only in the log. When the transaction commits, the log records are used to update the database. If the transaction aborts before commit, the log records are ignored.
*   **Recovery Procedure:**
    *   Scan the log from the end.
    *   For each transaction Ti, if the log contains both `<Ti start>` and `<Ti commit>`, then redo(Ti).
    *   Redo(Ti): Sets the value of all data items updated by Ti to the new values.

### Recovery with Immediate Update

*   **Concept:** Database modifications are written to disk before the transaction commits.
*   **Write Ahead Logging (WAL) Protocol:**
    *   Before a data item is modified in the database, both the old and new values (`Viold` and `Vinew`) are recorded in the log as `<Ti, Xi, Viold, Vinew>`.
    *   Also, `<Ti start>` and `<Ti commit>` are recorded in the log.
*   **Recovery Procedure:**
    *   Scan the log from the end.
    *   For each transaction Ti, if the log contains both `<Ti start>` and `<Ti commit>`, then redo(Ti).
    *   For each transaction Ti, if the log contains `<Ti start>` but no `<Ti commit>`, then undo(Ti).
    *   Undo(Ti): Sets the value of all data items updated by Ti to the old values.

### Checkpoints

*   **Purpose:** To reduce recovery time by avoiding scanning the entire log.
*   **Process:**
    *   Output all log records currently residing in main memory to disk.
    *   Output all modified data residing in main memory to disk.
    *   Output a log record `<checkpoint>` to disk.
*   **Recovery Procedure:**
    *   Find the most recent `<checkpoint>` record.
    *   Scan the log backward from that point. For each transaction Ti, if the log contains `<Ti start>` but no `<Ti commit>`, then undo(Ti).
    *   Scan the log forward from that point. For each transaction Ti, if the log contains both `<Ti start>` and `<Ti commit>`, then redo(Ti).
*   **Example:**
    1.  T1 starts and writes P1
    2.  T2 starts and writes P2
    3.  Checkpoint
    4.  T1 commits
    5.  T3 starts and writes P3
    6.  T3 commits

### Buffer Management

*   **Impact:** The replacement policy can substantially impact the time it takes to recover from a system crash.
*   **Policies:**
    *   Steal/No-Steal
    *   Force/No-Force
*   **Steal/No-Steal:**
    *   **Steal:** A block of data in memory can be written to disk even though the transaction that performed the write has not yet committed. Steal requires Undo logging and is easier to implement.
    *   **No-Steal:** The buffer cannot be overwritten by a new transaction until the transaction that performed the write has committed.
*   **Force/No-Force:**
    *   **Force:** All updates are immediately written to disk as soon as the transaction commits. Force requires Redo logging and is easier to implement.
    *   **No-Force:** Database modifications are written to disk only when the buffer block is replaced. No-force reduces the amount of disk I/O and is preferable.
*   **Interaction:**
    *   Steal, No-Force is most commonly implemented.
    *   Steal/Force is possible, but less common.
    *   No-Steal/Force is possible, but requires complex implementation.
    *   No-Steal/No-Force is not practical.

### Failure with Loss of Nonvolatile Storage (Media Failure)

*   **Definition:** Failure of the storage medium (disk or tape). Loss of all or part of persistent storage.
*   **Recovery:**
    *   Periodically dump the entire database to tape.
    *   Archive the log to tape.
    *   When the disk is repaired, restore the most recent dump.
    *   Consult the log to identify transactions that need to be redone. May lose some transactions executed since the last dump.

# Notes for Chunk 7
# Database Locking and Concurrency Control

## Tree Locking Protocol

*   **Root Lock:** The root of the tree must be locked first. It can be locked in any mode.
*   **Locking in S or IS Mode:** A node Q can be locked by transaction Ti in S (Shared) or IS (Intent Shared) mode only if the parent of Q is currently locked by Ti in either IX (Intent Exclusive) or IS mode.
*   **Locking in X, SIX, or IX Mode:** A node Q can be locked by transaction Ti in X (Exclusive), SIX (Shared Intent Exclusive), or IX mode only if the parent of Q is currently locked by Ti in either IX or SIX mode.
*   **Two-Phase Locking:** A transaction Ti can lock a node only if it has not previously unlocked any node (Ti is two-phase).
*   **Unlocking:** Ti can unlock a node Q only if none of the children of Q are currently locked by Ti.
*   **Lock/Unlock Order:** Locks are acquired in root-to-leaf order, and they are released in leaf-to-root order.
*   **Lock Granularity Escalation:** If there are too many locks at a particular level, switch to a higher granularity S or X lock.

## Insert/Delete Operations and Predicate Reads

### Locking Rules for Insert/Delete Operations

*   **Exclusive Lock for Deletion:** An exclusive lock must be obtained on an item before it is deleted.
*   **Exclusive Lock for Insertion:** A transaction that inserts a new tuple into the database is automatically given an X-mode lock on the tuple.

    *   Ensures that reads/writes conflict with deletes.
    *   The inserted tuple is not accessible by other transactions until the inserting transaction commits.

### Phantom Phenomenon

*   **Definition:** A situation where a transaction reads data that satisfies a search condition, and another transaction inserts new data that also satisfies the same condition. The first transaction, if repeated, might see different results, violating serializability.

*   **Example:**

    *   Transaction T1 performs a predicate read (scan) of a relation:

        ```sql
        select count(*)
        from instructor
        where dept_name = 'Physics'
        ```

    *   Transaction T2 inserts a tuple while T1 is active but after T1's predicate read:

        ```sql
        insert into instructor values ('11111', 'Feynman', 'Physics', 94000)
        ```

    *   This represents a conceptual conflict, even though T1 and T2 do not access any tuple in common initially.

*   **Problem with Tuple Locks:** If only tuple locks are used, non-serializable schedules can result. The scan transaction might not see the new instructor but may read some other tuple written by the update transaction.

*   **Occurrence with Updates:** The phantom phenomenon can also occur with updates.

    *   Example: Updating Wu's department from Finance to Physics.

*   **Another Example:** T1 and T2 both find the maximum instructor ID in parallel and create new instructors with ID = maximum ID + 1. Both instructors may get the same ID, which is not possible in a serializable schedule.

### Addressing the Phantom Phenomenon

*   The provided text doesn't contain resolution strategies, but it highlights the issue arising from concurrent operations, emphasizing the need for mechanisms beyond simple tuple locks to ensure serializability, especially when dealing with predicate reads and insert/delete operations.

# Notes for Chunk 8
```markdown
# Concurrency Exam Notes

## Handling Phantoms

### The Phantom Problem
*   Occurs when a transaction performing a predicate read (scanning a relation) reads information about the tuples a relation contains.
*   A conflicting transaction inserts, deletes, or updates tuples, changing the same information.
*   This conflict needs to be detected, typically by locking the relevant information.

### Basic Solution
*   Associate a data item with the relation to represent information about its tuples.
*   **Scanning Transactions:** Acquire a shared lock on this data item.
*   **Inserting/Deleting Transactions:** Acquire an exclusive lock on the data item.
*   **Important:** Locks on the data item do **not** conflict with locks on individual tuples.
*   **Drawback:** This approach leads to very low concurrency for insertions and deletions.

## Index Locking to Prevent Phantoms

### Protocol Requirements
*   **Mandatory Index:** Every relation must have at least one index.
*   **Index-Based Access:** Transactions can only access tuples by finding them through indices.

### Locking Rules
1.  **Lookup Locking:**
    *   A transaction *Ti* performing a lookup must lock *all* accessed index leaf nodes in S-mode (shared lock).
    *   This applies even if a leaf node contains no tuple satisfying the lookup (e.g., in a range query).
2.  **Update Locking:**
    *   A transaction *Ti* that inserts, updates, or deletes a tuple *ti* in a relation *r* must:
        *   Update all indices to *r*.
        *   Obtain exclusive locks on *all* affected index leaf nodes.
3.  **Two-Phase Locking:**
    *   The rules of the two-phase locking protocol must be observed.

### Guarantees
*   This protocol guarantees that the phantom phenomenon will not occur.

## Next-Key Locking to Prevent Phantoms

### Motivation
*   Index locking, while preventing phantoms, can result in poor concurrency, especially with frequent inserts.

### Protocol
*   **Locking Strategy:**
    *   Lock all values that satisfy the index lookup (matching the lookup value or falling within the lookup range).
    *   Also, lock the *next* key value in the index.
*   **Lock Modes:**
    *   S-mode (shared) for lookups.
    *   X-mode (exclusive) for insert/delete/update.
*   **Benefit:** Provides higher concurrency compared to basic index locking.
*   **Ensures:** Detection of query conflicts with inserts, deletes, and updates.

## Timestamp Based Concurrency Control

### Basic Principles
*   **Timestamp Assignment:** Each transaction *Ti* is assigned a unique timestamp *TS(Ti)* upon entering the system.
*   **Timestamp Uniqueness:** Newer transactions receive strictly greater timestamps than older ones.
*   **Timestamp Basis:**
    *   Can be based on a logical counter.
    *   Real time alone might not be unique enough.
    *   A combination like `(wall-clock time, logical counter)` ensures uniqueness.
*   **Goal:** Manage concurrent execution to ensure `timestamp order = serializability order`.

### Timestamp-Ordering Protocol (TSO)

#### Data Item Timestamps
*   For each data item *Q*, maintain two timestamp values:
    *   **W-timestamp(Q):** The largest timestamp of any transaction that successfully executed `write(Q)`.
    *   **R-timestamp(Q):** The largest timestamp of any transaction that successfully executed `read(Q)`.

#### Protocol Operation
*   Imposes rules on `read` and `write` operations to ensure conflicting operations are executed in timestamp order.
*   Out-of-order operations cause transaction rollback.

#### Read Operation Rule (Transaction *Ti* issues `read(Q)`)
Based on the provided content, there are no rules listed for how the read operation happens, nor are there rules for the write operation.
```

# Notes for Chunk 9
```markdown
## Timestamp-Based Protocols

### Read Operation

Suppose transaction T<sub>i</sub> issues read(Q).

1.  **If TS(T<sub>i</sub>) < W-timestamp(Q):**
    *   T<sub>i</sub> needs to read a value of Q that has already been overwritten.
    *   This means T<sub>i</sub> is trying to read an outdated value.
    *   The read operation is rejected.
    *   T<sub>i</sub> is rolled back.

2.  **If TS(T<sub>i</sub>) >= W-timestamp(Q):**
    *   The read operation is executed.
    *   The R-timestamp(Q) is updated to the maximum of its current value and TS(T<sub>i</sub>):
        *   R-timestamp(Q) = max(R-timestamp(Q), TS(T<sub>i</sub>))

### Write Operation

Suppose transaction T<sub>i</sub> issues write(Q).

1.  **If TS(T<sub>i</sub>) < R-timestamp(Q):**
    *   The value of Q that T<sub>i</sub> is producing was needed previously.
    *   The system assumed that this value would never be produced.
    *   The write operation is rejected.
    *   T<sub>i</sub> is rolled back.

2.  **If TS(T<sub>i</sub>) < W-timestamp(Q):**
    *   T<sub>i</sub> is attempting to write an obsolete value of Q.
    *   The write operation is rejected.
    *   T<sub>i</sub> is rolled back.

3.  **Otherwise (TS(T<sub>i</sub>) >= R-timestamp(Q) and TS(T<sub>i</sub>) >= W-timestamp(Q)):**
    *   The write operation is executed.
    *   The W-timestamp(Q) is set to TS(T<sub>i</sub>).

### Example of Schedule Under TSO

Initial condition: R-TS(Q) = W-TS(Q) = 0

Consider an example with:
*   R-TS(A) = W-TS(A) = 0
*   R-TS(B) = W-TS(B) = 0
*   TS(T25) = 25
*   TS(T26) = 26

The content does not provide the schedule itself, so it's impossible to determine if the schedule is valid under TSO. To determine the validity, we would need the specific sequence of read and write operations performed by T25 and T26 on data items A and B.

### Another Example Under TSO

A partial schedule is given for several data items for transactions with timestamps 1, 2, 3, 4, and 5. Initially, all R-TS and W-TS values are 0.

Again, the content does not provide the schedule itself, so it's impossible to determine if the schedule is valid under TSO.

### Correctness of Timestamp-Ordering Protocol

The timestamp-ordering protocol guarantees serializability.  All arcs in the precedence graph are of the form:
(Ti -> Tj) or (Tj -> Ti), ensuring that the transactions are executed in a serial order based on their timestamps.
```

# Notes for Chunk 10
# Exam Notes: Transaction Management

## Transaction Concept

*   A transaction is a unit of program execution that accesses and possibly updates various data items.
    *   Example: Transferring $50 from account A to account B involves reading A, subtracting 50, writing A, reading B, adding 50, and writing B.
*   **ACID Properties:** Essential characteristics ensuring reliable transaction processing.
    *   **Atomicity:** All operations of a transaction are reflected in the database, or none are. It's an "all or nothing" principle.
    *   **Consistency:** A transaction, when executed in isolation, preserves the consistency of the database.  It moves the database from one valid state to another.
    *   **Isolation:** Multiple transactions execute concurrently, but each appears to be executing in isolation from others.  Interleaving should not affect the final outcome as if they were executed serially.
    *   **Durability:** Once a transaction completes successfully (commits), the changes persist even if system failures occur.

## Transaction State

*   **Active:** The initial state when the transaction is executing.
*   **Partially Committed:** Reached after the final statement of the transaction has been executed.
*   **Failed:**  The transaction is in a failed state after discovering that normal execution can no longer proceed.
*   **Aborted:** The transaction has been rolled back, and the database is restored to its state prior to the transaction's start.
*   **Committed:** The transaction has completed successfully.

## Implementation of Atomicity and Durability

*   The recovery-management component ensures atomicity and durability.
*   **Log:** A sequence of log records that maintains a record of all update activities in the database.
    *   `<Ti start>`:  Indicates when transaction Ti starts.
    *   `<Ti, X, V1, V2>`:  Recorded before Ti executes `write(X)`.  X is the data item, V1 is the value of X before the write, and V2 is the value of X after the write.
    *   `<Ti commit>`: Indicates when Ti finishes its execution.
*   **System Crash:** If the system crashes, the log is consulted to determine which transactions need to be undone (rolled back) and which need to be redone.
*   **Checkpointing:**  The current contents of memory are written to disk. This reduces the amount of work that needs to be done during recovery by creating a known consistent state.

## Isolation

*   Transactions should appear to execute in isolation.
*   Naive (uncontrolled) concurrent execution can lead to incorrect states.
*   **Example of Lost Update Problem:**
    *   Two transactions, T1 and T2, both transfer $50 from account A to account B.
    *   If their operations are interleaved in a specific way, such as both reading A, then both deducting $50 and writing A, the final result is incorrect (A is deducted $50 instead of $100).

## Serializability

*   **Basic Assumption:** Each transaction preserves the consistency of the database.
*   Serial execution preserves database consistency.
*   A schedule (possibly concurrent) is **serializable** if it is equivalent to a serial schedule.
*   **Conflicting Operations:** Two transactions, Ti and Tj, conflict if some operation of Ti conflicts with some operation of Tj (e.g., one writes a data item that the other reads or writes).
*   **Conflict Serializable:** A schedule S is conflict serializable if S can be transformed into a serial schedule by swapping non-conflicting operations.
*   **Non-Conflict Serializable Schedule Example:**
    *   Schedule involving T3 and T4 reading and writing to Q where the order of operations prevents swapping to create a serial schedule.

## Transaction Isolation and Access Modes

*   SQL allows transactions to run at different isolation levels, defining the degree to which they are isolated from other transactions.
*   **READ UNCOMMITTED:** Allows reading data modified but not yet committed by other transactions (Dirty Read).
*   **READ COMMITTED:** Only allows reading data that has been committed. Prevents dirty reads, but non-repeatable reads are possible.
*   **REPEATABLE READ:** Guarantees that if a transaction reads a data item, it will read the same value if it reads it again. Non-repeatable reads are prevented, but phantoms are possible.
*   **SERIALIZABLE:** Guarantees transactions will execute in a serializable manner. This is the highest level of isolation and prevents dirty reads, non-repeatable reads, and phantoms.
*   **Isolation Level Problems:**
    *   READ UNCOMMITTED: Dirty read
    *   READ COMMITTED: Nonrepeatable read
    *   REPEATABLE READ: Phantoms

## Concurrency Control

*   Concurrency control manages the concurrent execution of transactions to ensure serializability.
*   **Goal:** To ensure that transactions execute in a serializable manner.
*   **Two Main Approaches:**
    *   Locking
    *   Timestamping

## Locking

*   A lock is a mechanism to control concurrent access to a data item.
*   **Exclusive Lock:** Data item can be read and written. Only one transaction can hold an exclusive lock on a data item at a time.
*   **Shared Lock:** Data item can only be read. Multiple transactions can hold shared locks on the same data item.
*   **Lock Table:** Used to record which transaction holds what lock on which data item.
*   **Simple Locking Protocol:**
    *   A transaction must obtain a shared or exclusive lock on a data item before reading or writing it.
    *   A transaction must release all locks when it is finished.
    *   **Problems:** Deadlock, starvation

## Timestamping

*   Assign a timestamp to each transaction to determine the serializability order.
*   **Two Timestamps per Data Item:**
    *   **Read-timestamp:** Timestamp of the latest transaction that read the data item.
    *   **Write-timestamp:** Timestamp of the latest transaction that wrote the data item.
*   **Basic Timestamp Ordering:**
    *   If transaction Ti issues a `read(X)` operation:
        *   If `TS(Ti) < write-timestamp(X)`, then abort Ti (because Ti is trying to read a value that has already been overwritten by a later transaction).
        *   Else grant Ti `read(X)` and reset `read-timestamp(X) = max(read-timestamp(X), TS(Ti))`.
    *   If transaction Ti issues a `write(X)` operation:
        *   If `TS(Ti) < read-timestamp(X)`, then abort Ti (because Ti is trying to write a value that a later transaction has already read).
        *   If `TS(Ti) < write-timestamp(X)`, then abort Ti (because Ti is trying to write an obsolete value).
        *   Else grant Ti `write(X)` and reset `write-timestamp(X) = TS(Ti)`.

## Serializability and Recoverability

*   **Recoverable Schedule:** If a transaction Tj reads a data item previously written by transaction Ti, the commit operation of Ti appears before the commit operation of Tj. This ensures that if Tj commits, it's based on a committed value of Ti.
*   **Cascading Rollback:** A single transaction failure may lead to a series of transaction rollbacks. If Tj reads from Ti and Ti aborts, then Tj must also abort.
*   **Cascadeless Schedules:** Avoid cascading rollbacks. Every transaction reads only items that were written by committed transactions.
### No Cycles in the Precedence Graph
* This is ensured when timestamp protocols are used.
### Timestamp protocol ensures freedom from deadlock as no transaction ever waits.
*The schedule may not be cascade-free, and may not even be recoverable.
### Recoverability and Cascade Freedom
*Solution 1: A transaction is structured such that its writes are all performed at the end of its processing. All writes of a transaction form an atomic action; no transaction may execute while a transaction is being written. A transaction that aborts is restarted with a new timestamp.
*Solution 2: Limited form of locking: wait for data to be committed before reading it
*Solution 3: Use commit dependencies to ensure recoverability
### Thomas’ Write Rule
* Modified version of the timestamp-ordering protocol in which obsolete write operations may be ignored under certain circumstances.
* When Ti attempts to write data item Q, if TS(Ti) < W-timestamp(Q), then Ti is attempting to write an obsolete value of {Q}.
* Rather than rolling back Ti as the timestamp ordering protocol would have done, this write operation can be ignored.
* Otherwise, this protocol is the same as the timestamp ordering protocol.
* Thomas' Write Rule allows greater potential concurrency.
* Allows some view-serializable schedules that are not conflict-serializable.
### Validation-Based Protocol
* Idea: can we use commit time as serialization order?
    * To do so: Postpone writes to end of transaction; Keep track of data items read/written by transaction.
* Validation performed at commit time, detect any out-of-serialization order reads/writes
* Also called as optimistic concurrency control since transaction executes fully in the hope that all will go well during validation

## Implementation of Isolation

*   Concurrency control schemes (locking and timestamping) are used to ensure isolation.
*   These schemes can be expensive to implement.
*   Many database systems provide weaker forms of isolation for performance reasons.

## Transaction as SQL Statements

*   `BEGIN TRANSACTION`: Explicitly starts a transaction.
*   `COMMIT`: Ends a transaction and makes changes permanent.
*   `ROLLBACK`: Ends a transaction and undoes any changes.
*   Many database systems implicitly start a transaction when the first SQL statement is executed.

# Notes for Chunk 11
# Validation-Based Protocol

## Transaction Execution Phases
A transaction *T<sub>i</sub>* in a validation-based protocol proceeds through three distinct phases:

1.  **Read and Execution Phase:**
    *   Transaction *T<sub>i</sub>* performs reads and computations.
    *   All writes are directed to temporary local variables, not directly to the database.

2.  **Validation Phase:**
    *   Transaction *T<sub>i</sub>* undergoes a "validation test."
    *   This test determines if the changes made to local variables can be applied to the database without violating serializability.

3.  **Write Phase:**
    *   If the validation test is successful, the updates from the local variables are applied to the database.
    *   If the validation test fails, transaction *T<sub>i</sub>* is rolled back, and its changes are discarded.

The execution of these phases can be interleaved among concurrent transactions, but each transaction must proceed through the phases in the specified order. For simplicity, it's assumed that the validation and write phases occur atomically and serially, meaning only one transaction can be in the validation/write phase at any given time.

## Timestamps

Each transaction *T<sub>i</sub>* is associated with three timestamps:

*   **StartTS( *T<sub>i</sub>* ):** The time when transaction *T<sub>i</sub>* began its execution.
*   **ValidationTS( *T<sub>i</sub>* ):** The time when transaction *T<sub>i</sub>* entered its validation phase.
*   **FinishTS( *T<sub>i</sub>* ):** The time when transaction *T<sub>i</sub>* completed its write phase.

The serializability order in this protocol is determined by the validation time. Therefore:

*   TS(*T<sub>i</sub>*) = ValidationTS(*T<sub>i</sub>*)

## Advantages

The validation-based protocol can offer a greater degree of concurrency compared to locking or Timestamp Ordering (TSO) protocols, especially when the probability of conflicts among transactions is low.

## Validation Test for Transaction *T<sub>j</sub>*

For a transaction *T<sub>j</sub>* to successfully validate, the following condition must hold true for all transactions *T<sub>i</sub>* where TS(*T<sub>i</sub>*) < TS(*T<sub>j</sub>*):

Either:

1.  **Non-Concurrent Execution:** finishTS(*T<sub>i</sub>*) < startTS(*T<sub>j</sub>*)
    *   This condition applies when the execution of *T<sub>i</sub>* and *T<sub>j</sub>* is not concurrent.
    *   It ensures that *T<sub>j</sub>*'s writes occur after *T<sub>i</sub>* has completely finished (its reads and writes), thus not affecting *T<sub>i</sub>*'s reads.

Or:

2.  **Concurrent Execution with No Data Conflict:** startTS(*T<sub>j</sub>*) < finishTS(*T<sub>i</sub>*) < validationTS(*T<sub>j</sub>*) and the write set of *T<sub>i</sub>* does not intersect with the read set of *T<sub>j</sub>*.
    *   This condition handles concurrent execution.
    *   It requires that *T<sub>j</sub>* starts after *T<sub>i</sub>* but finishes its execution before *T<sub>j</sub>* enters its validation phase.
    *   Crucially, it also requires that *T<sub>j</sub>* does not read any data items that are written by *T<sub>i</sub>*. This ensures that *T<sub>j</sub>*’s reads are not affected by *T<sub>i</sub>*’s writes.

If neither of these conditions is met, the validation fails, and transaction *T<sub>j</sub>* is aborted.

## Justification

*   The first condition ensures that if transactions do not run concurrently, the writes of *T<sub>j</sub>* will not affect the reads of *T<sub>i</sub>* because they occur after *T<sub>i</sub>* has completed.

*   The second condition handles the case where the transactions are executing concurrently. The key is to ensure that *T<sub>j</sub>* does not read any data written by *T<sub>i</sub>*, maintaining serializability.

## Schedule Produced by Validation

The protocol produces schedules that are serializable based on the validation timestamps.