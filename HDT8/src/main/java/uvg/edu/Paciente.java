package uvg.edu;

/**
 * Proyecto: Hoja de Trabajo 8
 * Fecha: 06-04-2025
 * Autor: Juan Montenegro
 */

public class Paciente implements Comparable<Paciente> {
    private String nombre;
    private String condicion;
    private char prioridad;

    public Paciente(String nombre, String condicion, char prioridad) {
        this.nombre = nombre;
        this.condicion = condicion;
        this.prioridad = Character.toUpperCase(prioridad);
    }

    @Override
    public int compareTo(Paciente otro) {
        return Character.compare(this.prioridad, otro.prioridad);
    }

    @Override
    public String toString() {
        return "Nombre: " + nombre + ", Síntoma: " + condicion + ", Prioridad: " + prioridad;
    }

    public char getPrioridad() {
        return prioridad;
    }
}