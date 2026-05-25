"use client";

import { useEffect, useState } from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Home() {
  const [markets, setMarkets] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any[]>([]);
  const [strategy, setStrategy] = useState<any[]>([]);

  useEffect(() => {
    fetchMarkets();
    fetchAnalytics();
    fetchStrategy();

    const interval = setInterval(() => {
      fetchMarkets();
      fetchAnalytics();
      fetchStrategy();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const fetchMarkets = async () => {
    const response = await fetch(
      "http://127.0.0.1:8000/markets"
    );

    const data = await response.json();

    setMarkets(Array.isArray(data) ? data : []);
  };

  const fetchAnalytics = async () => {
    const response = await fetch(
      "http://127.0.0.1:8000/analytics"
    );

    const data = await response.json();

    setAnalytics(Array.isArray(data) ? data : []);
  };

  const fetchStrategy = async () => {
    const response = await fetch(
      "http://127.0.0.1:8000/strategy/results"
    );

    const data = await response.json();

    setStrategy(Array.isArray(data) ? data : []);
  };

  const runStrategy = async () => {
    await fetch(
      "http://127.0.0.1:8000/strategy/run",
      {
        method: "POST",
      }
    );

    fetchStrategy();
  };

  return (
    <main className="min-h-screen bg-black text-white p-8">
      <div className="max-w-7xl mx-auto space-y-10">

        <div>
          <h1 className="text-5xl font-bold">
            Crypto Analytics Dashboard
          </h1>

          <p className="text-gray-400 mt-2">
            Real-time crypto analytics and trading signals
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {markets.slice(0, 3).map((coin) => (
            <div
              key={coin.id}
              className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800"
            >
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold uppercase">
                  {coin.symbol}
                </h2>

                <span className="text-green-400">
                  LIVE
                </span>
              </div>

              <p className="text-3xl font-semibold mt-4">
                ${coin.current_price.toLocaleString()}
              </p>

              <p className="text-gray-400 mt-2">
                Volume: {(coin.total_volume / 1_000_000_000).toFixed(2)}B
              </p>
            </div>
          ))}
        </div>

        <section className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-3xl font-bold">
              Market Overview
            </h2>
          </div>

          <table className="w-full">
            <thead>
              <tr className="text-left text-gray-400 border-b border-zinc-700">
                <th className="pb-4">Symbol</th>
                <th className="pb-4">Price</th>
                <th className="pb-4">Volume</th>
              </tr>
            </thead>

            <tbody>
              {markets.map((coin) => (
                <tr
                  key={coin.id}
                  className="border-b border-zinc-800"
                >
                  <td className="py-4 uppercase font-semibold">
                    {coin.symbol}
                  </td>

                  <td>${coin.current_price.toLocaleString()}</td>

                  <td>{(coin.total_volume / 1_000_000_000).toFixed(2)}B</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">

          <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
            <h2 className="text-2xl font-bold mb-6">
              Analytics
            </h2>

            <div className="space-y-4">
              {analytics.map((item) => (
                <div
                  key={item.symbol}
                  className="bg-zinc-800 p-4 rounded-xl"
                >
                  <div className="flex justify-between">
                    <h3 className="uppercase font-bold">
                      {item.symbol}
                    </h3>

                    <span
                      className={
                        item.price_change_percent >= 0
                          ? "text-green-400"
                          : "text-red-400"
                      }
                    >
                      {item.price_change_percent}%
                    </span>
                  </div>

                  <p className="text-gray-400 mt-2">
                    Volume Change:
                    {" "}
                    {item.volume_change_percent}%
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">
                Strategy Signals
              </h2>

              <button
                onClick={runStrategy}
                className="bg-white text-black px-4 py-2 rounded-lg font-semibold"
              >
                Run Strategy
              </button>
            </div>

            <div className="space-y-4">
              {strategy.map((item) => (
                <div
                  key={item.symbol}
                  className="bg-zinc-800 p-4 rounded-xl"
                >
                  <div className="flex justify-between">
                    <h3 className="uppercase font-bold">
                      {item.symbol}
                    </h3>

                    <span
                      className={
                        item.signal === "BUY"
                          ? "text-green-400"
                          : item.signal === "SELL"
                          ? "text-red-400"
                          : "text-yellow-400"
                      }
                    >
                      {item.signal}
                    </span>
                  </div>

                  <p className="text-gray-400 mt-2">
                    Short MA: {item.short_ma}
                  </p>

                  <p className="text-gray-400">
                    Long MA: {item.long_ma}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
          <h2 className="text-3xl font-bold mb-6">
            BTC Price Chart
          </h2>

          <div className="w-full">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={markets}>
                <XAxis dataKey="symbol" />
                <YAxis />
                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="current_price"
                  stroke="#22c55e"
                  strokeWidth={3}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

      </div>
    </main>
  );
}