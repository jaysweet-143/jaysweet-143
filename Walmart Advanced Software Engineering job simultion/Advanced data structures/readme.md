# Power-of-Two Max Heap

![Java](https://img.shields.io/badge/Java-17%2B-orange)
![Data Structure](https://img.shields.io/badge/data%20structure-d--ary%20max%20heap-blue)

An array-backed d-ary Max Heap in Java where every parent node has $2^x$ children. It was built during the Walmart USA Advanced Software Engineering Job Simulation to explore how priority queue performance changes under heavy insertion workloads.

## Table of Contents

- [Overview](#overview)
- [Key Features and Optimizations](#key-features-and-optimizations)
- [Time and Space Complexity](#time-and-space-complexity)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)

## Overview

In high-volume shipping and streaming pipelines, a standard binary heap (2 children per node) can be slowed down by tree depth when insertions are frequent. Raising the branching factor to $2^x$ flattens the tree, which reduces the number of swaps during `insert`. The trade-off is extra comparison work during `popMax`, since more children must be scanned at each level.

The heap avoids node pointer overhead by storing the tree in a contiguous `ArrayList` and using integer arithmetic and bit shifting for all index calculations.

## Key Features and Optimizations

- **Configurable branching factor ($2^x$):** The constructor takes a `branchingPower` parameter and computes the number of children with a single bitwise left shift (`1 << branchingPower`).
- **Flat array-backed storage:** With no node objects or pointers, memory use stays low and cache locality improves. Positions are found with direct index math:
  - **Parent index:** `(childIndex - 1) / numChildren`
  - **First child index:** `(parentIndex * numChildren) + 1`
- **Edge-case and overflow protection:**
  - Constructor input is validated (`0 <= branchingPower <= 30`) to rule out negative branching factors and 32-bit integer overflow.
  - Intermediate child index calculations in `siftDown` are cast to `long`, so large exponents do not overflow.
  - Empty heaps and single-element removals are handled explicitly to avoid off-by-one errors.

## Time and Space Complexity

Let $N$ be the number of elements in the heap and $d = 2^{\text{branchingPower}}$ be the number of children per parent.

| Operation | Time Complexity | Notes |
| :--- | :--- | :--- |
| `insert(int value)` | $O(\log_d N)$ | Faster than a binary heap because the tree is shorter. |
| `popMax()` | $O(d \log_d N)$ | Scans up to $d$ children per level while sifting down. |
| Space | $O(N)$ | Contiguous dynamic array with no node wrapper overhead. |

## Project Structure

```text
walmart-heap/
├── PowerOfTwoMaxHeap.java   # Core heap implementation
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites

- Java Development Kit (JDK) 17 or higher

### Compile and Run

1. Navigate to the project directory:

   ```bash
   cd walmart-heap
   ```

2. Compile the source file:

   ```bash
   javac PowerOfTwoMaxHeap.java
   ```

3. Use the heap in your application or test runner:

   ```java
   // Creates a max heap where each parent has 2^2 = 4 children
   PowerOfTwoMaxHeap shippingQueue = new PowerOfTwoMaxHeap(2);
   shippingQueue.insert(90);
   shippingQueue.insert(95);
   int topPriority = shippingQueue.popMax(); // Returns 95
   ```
