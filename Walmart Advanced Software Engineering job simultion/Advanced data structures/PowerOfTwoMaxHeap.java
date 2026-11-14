import java.util.ArrayList;

public class PowerOfTwoMaxHeap {
    private final int numChildren;
    private final ArrayList<Integer> heap;

    public PowerOfTwoMaxHeap(int branchingPower) {
        if (branchingPower < 0 || branchingPower > 30) {
            throw new IllegalArgumentException("branchingPower must be between 0 and 30.");
        }
        this.numChildren = 1 << branchingPower;
        this.heap = new ArrayList<>();
    }

    public void insert(int value) {
        heap.add(value);
        int currentIndex = heap.size() - 1;

        while (currentIndex > 0) {
            int parentIndex = (currentIndex - 1) / numChildren;
            int currentValue = heap.get(currentIndex);
            int parentValue = heap.get(parentIndex);

            if (currentValue > parentValue) {
                heap.set(currentIndex, parentValue);
                heap.set(parentIndex, currentValue);
                currentIndex = parentIndex;
            } else {
                break;
            }
        }
    }

    public int popMax() {
        if (heap.isEmpty()) {
            throw new IllegalStateException("Heap is empty.");
        }

        int maxValue = heap.get(0);
        int lastValue = heap.remove(heap.size() - 1);

        if (!heap.isEmpty()) {
            heap.set(0, lastValue);
            siftDown(0);
        }

        return maxValue;
    }

    private void siftDown(int currentIndex) {
        int heapSize = heap.size();

        while (true) {
            long firstChildIndexLong = ((long) currentIndex * numChildren) + 1;
            if (firstChildIndexLong >= heapSize) {
                break;
            }
            int firstChildIndex = (int) firstChildIndexLong;

            int largestChildIndex = firstChildIndex;
            int largestChildValue = heap.get(firstChildIndex);

            int endChildIndex = (int) Math.min(firstChildIndexLong + numChildren, heapSize);
            for (int i = firstChildIndex + 1; i < endChildIndex; i++) {
                int candidateValue = heap.get(i);
                if (candidateValue > largestChildValue) {
                    largestChildValue = candidateValue;
                    largestChildIndex = i;
                }
            }

            int currentValue = heap.get(currentIndex);
            if (largestChildValue > currentValue) {
                heap.set(currentIndex, largestChildValue);
                heap.set(largestChildIndex, currentValue);
                currentIndex = largestChildIndex;
            } else {
                break;
            }
        }
    }

    public static void main(String[] args) {
        // Test 1: Very small branchingPower (2^0 = 1 child per parent)
        PowerOfTwoMaxHeap smallHeap = new PowerOfTwoMaxHeap(0);
        smallHeap.insert(10);
        smallHeap.insert(50);
        smallHeap.insert(30);
        System.out.println("Small exponent max (expected 50): " + smallHeap.popMax());
        System.out.println("Next max (expected 30): " + smallHeap.popMax());

        // Test 2: Standard branchingPower (2^2 = 4 children per parent)
        PowerOfTwoMaxHeap mediumHeap = new PowerOfTwoMaxHeap(2);
        int[] sampleValues = {50, 70, 40, 60, 90, 95, 15};
        for (int val : sampleValues) {
            mediumHeap.insert(val);
        }
        System.out.println("Medium exponent max (expected 95): " + mediumHeap.popMax());
        System.out.println("Next max (expected 90): " + mediumHeap.popMax());

        // Test 3: Very large branchingPower (2^20 = 1,048,576 children per parent)
        PowerOfTwoMaxHeap largeHeap = new PowerOfTwoMaxHeap(20);
        largeHeap.insert(100);
        largeHeap.insert(500);
        largeHeap.insert(250);
        System.out.println("Large exponent max (expected 500): " + largeHeap.popMax());
    }
}
