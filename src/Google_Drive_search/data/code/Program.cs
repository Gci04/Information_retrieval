using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace examles
{
	class Program
	{
		#region ABA example

		struct TestStruct { public long A, B, C, D, E, F, G; }
		private static Dictionary<int, int> stats = new Dictionary<int, int>();
		private static void add(int addr)
		{
			lock (stats)
			{
				if (!stats.ContainsKey(addr)) stats.Add(addr, 1);
				else stats[addr] += 1;
			}
		}

		private static unsafe void RockNRoll()
		{
				TestStruct ts = new TestStruct();
				add((int)(void*)(&ts));
		}

		private static void ABA() 
		{
			Thread[] ths = Enumerable
							.Range(0, 200)
							.Select(a => new Thread(RockNRoll))
							.ToArray();
			Array.ForEach(ths, th => th.Start());
			
			while (ths.Any(th => th.IsAlive)) { }
			
			foreach (var kvp in stats.OrderByDescending(k => k.Value).Take(20))
				Console.WriteLine("{0} times for {1}", kvp.Value, kvp.Key);
			
		}

		#endregion ABA example 

		#region Deadlock example
		class Item { public int Value; public bool isHungry; }
		class Container { public Item Item1; }
		private static Container ct = new Container { Item1 = new Item() };
	
		private static void LockAB()
		{
			while (true)
			{
				//Thread.Sleep(50);
				lock (ct)
				{
					lock (ct.Item1)
					{
						ct.Item1.Value = 3;
						Console.Write(ct.Item1.Value);
					}
				}
			}
		}

		private static void LockBA()
		{
			while (true)
			{
				//Thread.Sleep(50);
				lock (ct.Item1)
				{
					lock (ct)
					{
						ct.Item1.Value = 4;
						Console.Write(ct.Item1.Value);
					}
				}
			}
		}

		private static void DeadLock()
		{
			new Thread(LockAB).Start();
			new Thread(LockBA).Start();
		}

		#endregion Deadlock example

		#region Polite Livelock example

		static Item[] workers = new Item[] { new Item { isHungry = true }, new Item { isHungry = true } };

		private static void DoYourJob(object me)
		{
			int i = (int)me;
			do
			{
				if (workers[1 - i].isHungry)
				{
					Console.WriteLine("Wait when others finish");
					Thread.Sleep(50);
				}
				else break;
			} while (true);
			Console.WriteLine("I can do my job!");
		}

		private static void LiveLock()
		{
			foreach (int i in new[] { 0, 1 })
				new Thread(DoYourJob).Start(i);
		}

		#endregion Polite Lovelock example

		#region Abandoned

		static Mutex mux = new Mutex(false);
		static Random rnd = new Random();

		private static void Dangerous() 
		{
			while (true)
			{
				try
				{
					mux.WaitOne(0);
					
					Thread.Sleep(500);
					if (rnd.Next(1000) % 7 == 0) 
						throw new NotFiniteNumberException();
					else 
						Console.WriteLine("Everything is oookey!");

					mux.ReleaseMutex();
				}
				catch (NotFiniteNumberException ex) { Console.WriteLine("Oops! " + ex.Message); }
			}
		}

		private static void Abandoned()
		{
			foreach (int i in new[] { 0, 1 })
				new Thread(Dangerous).Start();
		}

		#endregion Abandoned

		static void Main(string[] args)
		{
			//ABA();
			//DeadLock();
			//LiveLock();
			Abandoned();
			Console.ReadLine();
		}
	}
}
