using System.Reflection.Emit;
using System.Reflection;
using System.Diagnostics;

public class EmitDemo
{
    delegate double CalcDelegate(double a, double b, double c);

    public static void RunPerformanceTest()
    {
        int iterations = 10_000_000;
        double a = 10, b = 20, c = 2;

        Stopwatch sw = Stopwatch.StartNew();
        for (int i = 0; i < iterations; i++) { 
            var r = (a + b) * c;
        }
        sw.Stop();
        Console.WriteLine($"Native C#: {sw.ElapsedMilliseconds}ms");

        var methodInfo = typeof(EmitDemo).GetMethod(
            nameof(SimpleCalc),
            BindingFlags.Public | BindingFlags.Static
        ) ?? throw new MissingMethodException(nameof(EmitDemo), nameof(SimpleCalc));
        object[] args = { a, b, c };
        sw.Restart();
        for (int i = 0; i < iterations; i++) {
            methodInfo.Invoke(null, args);
            }
        sw.Stop();
        Console.WriteLine($"Reflection Invoke: {sw.ElapsedMilliseconds}ms");

        var dynamicMethod = new DynamicMethod("FastCalc", typeof(double), new[] { typeof(double), typeof(double), typeof(double) });
        var il = dynamicMethod.GetILGenerator();

        il.Emit(OpCodes.Ldarg_0);
        il.Emit(OpCodes.Ldarg_1);
        il.Emit(OpCodes.Add);
        il.Emit(OpCodes.Ldarg_2);
        il.Emit(OpCodes.Mul);
        il.Emit(OpCodes.Ret);

        var fastCalc = (CalcDelegate)dynamicMethod.CreateDelegate(typeof(CalcDelegate));

        sw.Restart();
        for (int i = 0; i < iterations; i++) { fastCalc(a, b, c); }
        sw.Stop();
        Console.WriteLine($"Reflection.Emit: {sw.ElapsedMilliseconds}ms");
    }

    public static double SimpleCalc(double a, double b, double c) => (a + b) * c;
}