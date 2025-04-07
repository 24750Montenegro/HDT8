package uvg.edu;

/**
 * Proyecto: Hoja de Trabajo 8
 * Fecha: 06-04-2025
 * Autor: Juan Montenegro
 */

public interface PriorityQueue<E> {
    boolean add(E value);
    E remove();
    E peek();
    boolean isEmpty();
    int size();
    void clear();
}