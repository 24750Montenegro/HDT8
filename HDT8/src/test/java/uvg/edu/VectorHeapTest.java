package uvg.edu;

/**
 * Proyecto: Hoja de Trabajo 8
 * Fecha: 06-04-2025
 * Autor: Juan Montenegro
 */

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import uvg.edu.Paciente;
import uvg.edu.VectorHeap;
import uvg.edu.PriorityQueue;


/**
 * Pruebas unitarias  para VectorHeap.
 */
public class VectorHeapTest {

    private VectorHeap<Paciente> heap;

    @Before
    public void setUp() {
        heap = new VectorHeap<>();
    }

    /**
     * Prueba que un paciente se inserte correctamente.
     */
    @Test
    public void testAdd() {
        Paciente paciente = new Paciente("Juan", "fractura", 'C');
        heap.add(paciente);
        assertEquals(1, heap.size());
        assertEquals(paciente, heap.peek());
    }

    /**
     * Prueba que un paciente se retire correctamente.
     */
    @Test
    public void testRemove() {
        Paciente paciente = new Paciente("Juan", "fractura", 'C');
        heap.add(paciente);
        assertEquals(paciente, heap.remove());
        assertEquals(0, heap.size());
    }

    /**
     * Prueba el orden de prioridad al insertar dos pacientes.
     */
    @Test
    public void testPriorityOrder() {
        Paciente p1 = new Paciente("Juan", "fractura", 'C');
        Paciente p2 = new Paciente("Maria", "infarto", 'A');
        heap.add(p1);
        heap.add(p2);
        assertEquals(p2, heap.remove()); // 'A' debe salir primero
    }
}