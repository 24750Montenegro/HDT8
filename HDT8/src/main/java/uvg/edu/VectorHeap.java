package uvg.edu;

import java.util.Vector;

/**
 * Proyecto: Hoja de Trabajo 8
 * Fecha: 06-04-2025
 * Autor: Juan Montenegro
 */

public class VectorHeap<E extends Comparable<E>> implements PriorityQueue<E> {
    private Vector<E> heap;

    public VectorHeap() {
        heap = new Vector<>();
    }

    @Override
    public boolean add(E value) {
        heap.add(value);
        siftUp(heap.size() - 1);
        return true;
    }

    @Override
    public E remove() {
        if (heap.isEmpty()) return null;

        E root = heap.get(0);
        E last = heap.remove(heap.size() - 1);

        if (!heap.isEmpty()) {
            heap.set(0, last);
            siftDown(0);
        }
        return root;
    }

    @Override
    public E peek() {
        return heap.isEmpty() ? null : heap.get(0);
    }

    @Override
    public boolean isEmpty() {
        return heap.isEmpty();
    }

    @Override
    public int size() {
        return heap.size();
    }

    @Override
    public void clear() {
        heap.clear();
    }

    private void siftUp(int index) {
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (heap.get(parent).compareTo(heap.get(index)) <= 0) {
                break;
            }
            swap(parent, index);
            index = parent;
        }
    }

    private void siftDown(int index) {
        int minIndex = index;
        int left = 2 * index + 1;
        int right = 2 * index + 2;

        if (left < heap.size() && heap.get(left).compareTo(heap.get(minIndex)) < 0) {
            minIndex = left;
        }
        if (right < heap.size() && heap.get(right).compareTo(heap.get(minIndex)) < 0) {
            minIndex = right;
        }

        if (minIndex != index) {
            swap(index, minIndex);
            siftDown(minIndex);
        }
    }

    private void swap(int i, int j) {
        E temp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, temp);
    }
}
