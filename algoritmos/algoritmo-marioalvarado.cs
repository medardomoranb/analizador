using System;
using System.Collections.Generic;
public class Estudiante
{
    string nombre = "Lucía";
    List<float> notas = new List<float> { 8.5f, 7.0f, 9.2f };

    public void MostrarDatos()
    {
        Console.WriteLine("Nombre: " + nombre);

        int contador = 1;

        foreach (float nota in notas)
        {
            Console.WriteLine("Nota " + contador + ": " + nota);
            contador++;
        }

        float promedio = CalcularPromedio();
        Console.WriteLine("Promedio: " + promedio);


        if (promedio >= 6)
        {
            Console.WriteLine("Ha aprobado el curso.");
        }
        else
        {
            Console.WriteLine("No ha aprobado el curso.");
        }
    }

    private float CalcularPromedio()
    {
        float suma = 0;

        foreach (float nota in notas)
        {
            suma += nota;
        }
        return suma / notas.Count;
    }

    public static void Main(string[] args)
    {
        Estudiante estudiante = new Estudiante();
        estudiante.MostrarDatos();
    }
}
