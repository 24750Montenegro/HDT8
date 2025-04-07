package uvg.edu;

/**
 * Proyecto: Hoja de Trabajo 8
 * Fecha: 06-04-2025
 * Autor: Juan Montenegro
 */

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.PriorityQueue;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Seleccione la implementación de la cola de prioridad:");
        System.out.println("1. VectorHeap");
        System.out.println("2. java collection framework PriorityQueue");
        System.out.print("Ingrese su opción: ");
        int seleccion = scanner.nextInt();
        scanner.nextLine();

        PriorityQueue<Paciente> colaPriorityQueue = null;
        VectorHeap<Paciente> colaHeap = null;

        if (seleccion == 1) {
            colaHeap = new VectorHeap<>();
        } else if (seleccion == 2) {
            colaPriorityQueue = new PriorityQueue<>();
        } else {
            System.out.println("Opción no válida. Saliendo...");
            scanner.close();
            return;
        }

        try {
            BufferedReader br = new BufferedReader(new FileReader("src/main/java/uvg/edu/pacientes.txt"));
            String linea;
            while ((linea = br.readLine()) != null) {
                String[] datos = linea.split(",");
                if (datos.length == 3) {
                    String nombre = datos[0].trim();
                    String condicion = datos[1].trim();
                    char prioridad = datos[2].trim().charAt(0);
                    Paciente paciente = new Paciente(nombre, condicion, prioridad);

                    if (colaHeap != null) {
                        colaHeap.add(paciente);
                    } else if (colaPriorityQueue != null) {
                        colaPriorityQueue.add(paciente);
                    }
                }
            }
            br.close();
        } catch (Exception e) {
            System.out.println("Error al leer el archivo: " + e.getMessage());
        }

        int opcion = 0;
        while ((colaHeap != null && !colaHeap.isEmpty() || colaPriorityQueue != null && !colaPriorityQueue.isEmpty()) && opcion != 3) {
            System.out.println();
            int size = (colaHeap != null) ? colaHeap.size() : colaPriorityQueue.size();
            System.out.println("PACIENTES EN COLA: " + size);
            System.out.println("1. Atender paciente en cola");
            System.out.println("2. Ver siguiente paciente");
            System.out.println("3. Salir");
            System.out.print("Seleccione una opción: ");
            opcion = scanner.nextInt();
            scanner.nextLine();
            System.out.println();

            switch (opcion) {
                case 1:
                    Paciente atendido = (colaHeap != null) ? colaHeap.remove() : colaPriorityQueue.poll();
                    if (atendido != null) {
                        System.out.println("Paciente atendido: " + atendido);
                    } else {
                        System.out.println("No hay pacientes en la cola.");
                    }
                    break;
                case 2:
                    Paciente siguientePaciente = (colaHeap != null) ? colaHeap.peek() : colaPriorityQueue.peek();
                    if (siguientePaciente != null) {
                        System.out.println("Siguiente paciente: " + siguientePaciente);
                    } else {
                        System.out.println("No hay pacientes en la cola.");
                    }
                    break;
                case 3:
                    System.out.println("Saliendo :) ...");
                    break;
                default:
                    System.out.println("Error: Opción no válida.");
            }
        }

        if ((colaHeap != null && colaHeap.isEmpty()) || (colaPriorityQueue != null && colaPriorityQueue.isEmpty())) {
            System.out.println();
            System.out.println("No hay más pacientes en la cola.");
        }

        scanner.close();
    }
}