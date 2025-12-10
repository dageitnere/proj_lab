import tako from "../assets/tako.png";

export default function Hero() {
  return (
    <section className="pt-40">
      <div className="mx-auto max-w-7xl px-6 grid grid-cols-12 gap-6">
        <div className="col-span-6 mt-32">
          <h1
            className="
              font-libre
              text-[#31332E]
              font-medium
              tracking-tight
              leading-[0.95]
              text-[5.3rem]
            "
          >
            <span className="block">Plan. Cook.</span>
            <span className="block">Eat. Repeat.</span>
          </h1>
                <p className="mt-8 text-[#31332E] text-xl max-w-xl leading-relaxed">
                    <span className="block">
                      Make meal planning simple and stress-free,
                    </span>
                    <span className="block">
                      so you can eat better, save more, and live healthier.
                    </span>
                </p>
        </div>
          <div className="col-span-6 -mt-8 flex justify-center">
          <img
            src={tako}
            alt="Tasty tacos"
            className="w-[50rem] object-contain drop-shadow-xl ml-20"
          />
        </div>
      </div>
    </section>
  );
}
