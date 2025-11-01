// src/components/Hero.jsx
export default function Hero() {
  return (
    <section className="pt-40 sm:pt-32 lg:pt-48">
      <div className="mx-auto max-w-7xl px-6 grid gap-6 lg:grid-cols-12">

        <div className="lg:col-span-6">
          <h1 className="text-white font-medium tracking-tight leading-[0.95]
                         text-5xl sm:text-7xl lg:text-8xl">
            <span className="block">Plan. Cook</span>
            <span className="block">Eat. Repeat.</span>
            <span className="block">Smile.</span>
          </h1>
        </div>


        <div className="lg:col-span-6 lg:col-start-10 text-white/90 lg:mt-6">
          <p className="text-base sm:text-lg leading-relaxed max-w-sm">
            NutriMax lets you plan dishes for the whole week, organize ingredients,
            and automatically generate shopping lists. No more stress about what to cook
            or buy – everything is right where you need it. Eat smart, save time, and enjoy every bite.
          </p>

          <div className="mt-6">
            <button
              className="inline-flex items-center justify-center rounded-full px-6 py-3
                         bg-white text-[#2F6235] font-semibold shadow
                         hover:bg-white/90 focus:outline-none focus-visible:ring
                         focus-visible:ring-white/60 transition"
            >
              Try for free
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
