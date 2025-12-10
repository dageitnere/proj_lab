import { useEffect, useState } from "react";
import NavbarLogo from "../components/NavbarLogo.jsx";
import Footer from "../components/Footer.jsx";

export default function AllProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await fetch("/products/showProducts/json", {
          method: "GET",
          credentials: "include",
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();
        setProducts(data.products || []);
      } catch (err) {
        setError(err.message || "Failed to load products");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <>
      <NavbarLogo />

      <div className="pt-32 pb-32 max-w-7xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-center mb-8 text-brandGreen">
          All Products
        </h1>

        {loading && <p className="text-center">Loading...</p>}
        {error && <p className="text-center text-red-500">{error}</p>}

        {!loading && !error && products.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse bg-white text-black shadow rounded">
              <thead>
                <tr className="bg-gray-200">
                  <th className="p-2 border">ID</th>
                  <th className="p-2 border">Product</th>
                  <th className="p-2 border">Kcal</th>
                  <th className="p-2 border">Fats</th>
                  <th className="p-2 border">Saturated Fats</th>
                  <th className="p-2 border">Carbs</th>
                  <th className="p-2 border">Sugars</th>
                  <th className="p-2 border">Protein</th>
                  <th className="p-2 border">Dairy Protein</th>
                  <th className="p-2 border">Animal Protein</th>
                  <th className="p-2 border">Plant Protein</th>
                  <th className="p-2 border">Salt</th>
                  <th className="p-2 border">Price 1kg</th>
                  <th className="p-2 border">Price 100g</th>
                </tr>
              </thead>
              <tbody>
                {products.map((p) => (
                  <tr key={p.id} className="odd:bg-gray-50 even:bg-gray-100">
                    <td className="p-2 border">{p.id}</td>
                    <td className="p-2 border">{p.productName}</td>
                    <td className="p-2 border">{p.kcal}</td>
                    <td className="p-2 border">{p.fat}</td>
                    <td className="p-2 border">{p.satFat}</td>
                    <td className="p-2 border">{p.carbs}</td>
                    <td className="p-2 border">{p.sugars}</td>
                    <td className="p-2 border">{p.protein}</td>
                    <td className="p-2 border">{p.dairyProt}</td>
                    <td className="p-2 border">{p.animalProt}</td>
                    <td className="p-2 border">{p.plantProt}</td>
                    <td className="p-2 border">{p.salt}</td>
                    <td className="p-2 border">{p.price1kg}</td>
                    <td className="p-2 border">{p.price100g}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {!loading && !error && products.length === 0 && (
          <p className="text-center text-gray-500">No products found.</p>
        )}

        <div className="mt-6 text-center">
          <a href="/new-page">
            <button className="px-4 py-2 bg-brandGreen text-white rounded hover:bg-green-700 transition">
              Main Page
            </button>
          </a>
        </div>
      </div>

      <Footer />
    </>
  );
}