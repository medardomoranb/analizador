public class Estudiante
{
    string nombre = "Lucía";
    float nota = 8.5;

    public void MostrarDatos()
    {
        Console.WriteLine("Nombre: " + nombre);
        Console.WriteLine("Nota: " + nota);

        if (nota >= 6)
        {
            Console.WriteLine("Ha aprobado el curso.");
        }
        else
        {
            Console.WriteLine("No ha aprobado el curso.");
        }
    }

    public bool EstaAprobado()
    {
        return nota >= 7;
    }

    public static void Main(string[] args)
    {
        Estudiante estudiante = new Estudiante();
        estudiante.MostrarDatos();

        bool aprobado = estudiante.EstaAprobado();
        Console.WriteLine("¿Aprobado?: " + aprobado);
    }
}
