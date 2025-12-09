export default function Hero() {
  return (
    <section className="pt-40 sm:pt-32 lg:pt-48">
      <div className="mx-auto max-w-7xl px-6 grid gap-6 lg:grid-cols-12">
        <div className="lg:col-span-6">
          <h1
            className="
              font-libre
              text-[#2f3c1f]
              font-medium
              tracking-tight
              leading-[0.95]
              text-5xl sm:text-7xl lg:text-8xl
            "
          >
            <span className="block">Plan. Cook</span>
            <span className="block">Eat. Repeat.</span>
            <span className="block">Smile.</span>
          </h1>
        </div>
      </div>
    </section>
  );
}
