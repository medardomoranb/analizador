using System;

public class Producto
{
    string nombre = "Mouse inalámbrico";
    float precio = 19.99f;
    int stock = 12;

    public void MostrarInfo()
    {
        Console.WriteLine("Producto: " + nombre);
        Console.WriteLine("Precio: $" + precio);
        Console.WriteLine("Stock disponible: " + stock);

        if (stock > 0)
        {
            Console.WriteLine("Producto en inventario.");
        }
        else
        {
            Console.WriteLine("Producto agotado.");
        }

        if (precio >= 15)
        {
            Console.WriteLine("Precio válido para la venta.");
        }
        else
        {
            Console.WriteLine("Precio demasiado bajo, revisar margen de ganancia.");
        }
    }

    public bool DisponibleParaVenta()
    {
        if (stock > 0 && precio >= 15)
        {
            return true;
        }
        return false;
    }

    public static void Main(string[] args)
    {
        Producto p = new Producto();
        p.MostrarInfo();

        bool puedeVenderse = p.DisponibleParaVenta();
        Console.WriteLine("¿Disponible para la venta?: " + puedeVenderse);
    }
}
